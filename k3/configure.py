#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Apply a K3 appearance profile without replacing printer configuration.

Python 3.9+, standard library only. Stop HelixScreen before applying a profile.
All changed files are backed up; exports contain appearance only, never printer keys.
"""
import argparse
from copy import deepcopy
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import re
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PROFILES = json.loads((ROOT / "k3/profiles.json").read_text())
THEME = ROOT / "assets/config/themes/defaults/k3-violet.json"
ENV_KEYS = ("HELIX_SCREEN_SIZE", "HELIX_DISPLAY_ROTATION", "HELIX_DISPLAY_BACKEND", "HELIX_DISABLE_AUTO_UPDATES")


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def atomic_write(path, data):
    # The official installer links individual config files into printer_data.
    # Replace the target atomically while preserving the installer's symlink.
    if path.is_symlink():
        path = path.resolve(strict=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".k3-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@contextmanager
def stopped_config(directory):
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / ".helix-screen.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError("HelixScreen is running. Stop its service before changing settings.") from None
        yield


def validate_options(options):
    allowed = {"profile", "size", "rotation", "backend", "accent", "mode", "brightness", "touch_device"}
    if not isinstance(options, dict) or set(options) - allowed:
        raise ValueError("Appearance file contains unsupported fields.")
    result = dict(profile="auto", size=None, rotation=0, backend="auto", accent=None,
                  mode="dark", brightness=80, touch_device=None)
    result.update(options)
    if result["profile"] not in PROFILES:
        raise ValueError("Unknown display profile.")
    if result["rotation"] not in (0, 90, 180, 270) or type(result["rotation"]) is not int:
        raise ValueError("Rotation must be 0, 90, 180 or 270.")
    if result["backend"] not in ("auto", "drm", "fbdev"):
        raise ValueError("Backend must be auto, drm or fbdev.")
    if result["mode"] not in ("dark", "light"):
        raise ValueError("Mode must be dark or light.")
    if type(result["brightness"]) is not int or not 1 <= result["brightness"] <= 100:
        raise ValueError("Brightness must be an integer from 1 to 100.")
    accent = result["accent"]
    if accent is not None and (not isinstance(accent, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", accent)):
        raise ValueError("Accent must use #RRGGBB.")
    size = result["size"]
    if size is not None:
        if not isinstance(size, str) or not re.fullmatch(r"[0-9]{3,4}x[0-9]{3,4}", size):
            raise ValueError("Size must use WIDTHxHEIGHT, for example 480x800.")
        if any(not 272 <= int(n) <= 4096 for n in size.split("x")):
            raise ValueError("Each screen dimension must be between 272 and 4096 pixels.")
    touch = result["touch_device"]
    if touch is not None and (not isinstance(touch, str) or not re.fullmatch(r"/dev/input/(event[0-9]+|by-id/[A-Za-z0-9_.:+-]+)", touch)):
        raise ValueError("Touch device must be /dev/input/eventN or a /dev/input/by-id/ path.")
    return result


def update_env(text, options):
    # These keys are owned by the profile. Preserve every other setting/comment.
    lines = [line for line in text.splitlines()
             if not any(re.match(r"^\s*(?:export\s+)?" + key + r"\s*=", line) for key in ENV_KEYS)]
    size = options["size"] or PROFILES[options["profile"]]["size"]
    if size:
        lines.append("HELIX_SCREEN_SIZE=" + size)
    lines.append("HELIX_DISPLAY_ROTATION=" + str(options["rotation"]))
    if options["backend"] != "auto":
        lines.append("HELIX_DISPLAY_BACKEND=" + options["backend"])
    # An upstream update would replace this fork's XML. Update the fork deliberately.
    lines.append("HELIX_DISABLE_AUTO_UPDATES=1")
    return "\n".join(lines).strip() + "\n"


def dashboard_defaults(existing=None):
    """Extend only the measured 400x1280 default; preserve every other grid."""
    layout = deepcopy(existing) if existing is not None else json.loads((ROOT / "assets/config/default_layout.json").read_text())
    if not isinstance(layout, dict) or not isinstance(layout.get("anchors"), list):
        raise ValueError("Existing default_layout.json must contain an anchors array.")
    custom = json.loads((ROOT / "k3/home-layout.json").read_text())
    variants = layout.setdefault("variants", {})
    if not isinstance(variants, dict):
        raise ValueError("Existing default_layout.json has invalid variants.")
    portrait = variants.get("portrait")
    if portrait is None:
        portrait = {"anchors": deepcopy(layout["anchors"]),
                    "disabled": deepcopy(layout.get("disabled", {})),
                    "gaps": deepcopy(layout.get("gaps", {}))}
        variants["portrait"] = portrait
    elif isinstance(portrait, list):
        portrait = {"anchors": portrait}
        variants["portrait"] = portrait
    if not isinstance(portrait, dict) or not isinstance(portrait.get("anchors"), list):
        raise ValueError("Existing portrait defaults must contain an anchors array.")
    if any(not isinstance(a, dict) or not isinstance(a.get("placements", {}), dict) for a in portrait["anchors"]):
        raise ValueError("Existing portrait anchors have invalid placements.")
    if any(not isinstance(portrait.get(k, {}), dict) for k in ("disabled", "gaps")):
        raise ValueError("Existing portrait default metadata is invalid.")
    key = custom["grid"]
    for kind, field in (("placements", "id"), ("slots", "slot")):
        for name, rect in custom[kind].items():
            anchor = next((a for a in portrait["anchors"] if a.get(field) == name), None)
            if anchor is None:
                anchor = {field: name, "placements": {}}
                portrait["anchors"].append(anchor)
            anchor["placements"][key] = dict(zip(("col", "row", "colspan", "rowspan"), rect))
    portrait.setdefault("disabled", {})[key] = custom["disabled"]
    portrait.setdefault("gaps", {})[key] = custom["gaps"]
    return layout


def apply(directory, options):
    options = validate_options(options)
    directory = Path(directory).resolve()
    with stopped_config(directory):
        settings_path = directory / "settings.json"
        if settings_path.exists():
            settings = json.loads(settings_path.read_text())
            if not isinstance(settings, dict) or not settings.get("config_version"):
                raise ValueError("Existing settings have no config_version; run HelixScreen setup first.")
        else:
            settings = json.loads((ROOT / "config/settings.json.template").read_text())
            settings.setdefault("appearance", {})["show_widget_labels"] = True
            settings["printers"]["default"]["printer_image"] = "shipped:annex-k3"
        settings["dark_mode"] = options["mode"] == "dark"
        settings["brightness"] = options["brightness"]
        settings.setdefault("display", {}).update(theme="k3-violet", rotate=options["rotation"])
        if options["touch_device"] is not None:
            settings.setdefault("input", {})["touch_device"] = options["touch_device"]
        theme = json.loads(THEME.read_text())
        if options["accent"]:
            for palette in ("dark", "light"):
                theme[palette]["primary"] = options["accent"]
                theme[palette]["focus"] = options["accent"]
        env_path = directory / "helixscreen.env"
        env = env_path.read_text() if env_path.exists() else ""
        layout_path = directory / "default_layout.json"
        existing_layout = json.loads(layout_path.read_text()) if layout_path.exists() else None
        changes = {
            "themes/k3-violet.json": json_bytes(theme),
            "default_layout.json": json_bytes(dashboard_defaults(existing_layout)),
            "helixscreen.env": update_env(env, options).encode(),
            "k3-appearance.json": json_bytes(options),
            "settings.json": json_bytes(settings),
        }
        previous = {}
        for name in changes:
            path = directory / name
            validate_destination(path)
            previous[name] = path.read_bytes() if path.exists() else None
        if all(previous[name] == data for name, data in changes.items()):
            return None
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        backup = directory / "k3-backups" / stamp
        backup.mkdir(parents=True, mode=0o700)
        atomic_write(backup / "manifest.json", json_bytes({name: data is not None for name, data in previous.items()}))
        for name, data in previous.items():
            if data is not None:
                atomic_write(backup / name, data)
        try:
            for name, data in changes.items():
                atomic_write(directory / name, data)
        except OSError:
            for name, data in previous.items():
                if data is None:
                    (directory / name).unlink(missing_ok=True)
                else:
                    atomic_write(directory / name, data)
            raise
        return backup


def restore(directory, stamp):
    directory = Path(directory).resolve()
    if not re.fullmatch(r"[0-9]{8}T[0-9]{6}\.[0-9]{6}Z", stamp):
        raise ValueError("Use a backup folder name, not a path.")
    backup = directory / "k3-backups" / stamp
    manifest = json.loads((backup / "manifest.json").read_text())
    names = {"settings.json", "helixscreen.env", "themes/k3-violet.json", "k3-appearance.json", "default_layout.json"}
    if set(manifest) != names or any(type(v) is not bool for v in manifest.values()):
        raise ValueError("Invalid backup manifest.")
    names = set(manifest)
    # Read and validate everything before replacing any live file.
    data = {name: (backup / name).read_bytes() if exists else None for name, exists in manifest.items()}
    for name, content in data.items():
        if content is not None and name.endswith(".json"):
            json.loads(content)
    with stopped_config(directory):
        for name in names:
            validate_destination(directory / name)
        for name, content in data.items():
            if content is None:
                (directory / name).unlink(missing_ok=True)
            else:
                atomic_write(directory / name, content)


def doctor(directory):
    # Local read-only inventory. Never reads API keys or sends a printer command.
    report = {"config_directory": str(directory), "settings_exist": (directory / "settings.json").exists()}
    report["drm_modes"] = {str(p): p.read_text().splitlines() for p in Path("/sys/class/drm").glob("card*-*/modes")}
    report["framebuffers"] = [str(p) for p in Path("/dev").glob("fb[0-9]*")]
    report["touch_devices"] = [str(p) for p in Path("/dev/input/by-id").glob("*event*")]
    report["backlights"] = [p.name for p in Path("/sys/class/backlight").glob("*")]
    print(json.dumps(report, indent=2))


def validate_destination(path):
    if path.is_symlink() and (not path.is_file() or path.resolve().stat().st_uid != os.geteuid()):
        raise ValueError("Refusing a dangling or foreign-owned symlink: " + path.name)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-dir", type=Path, default=Path.home() / "helixscreen/config")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("profiles")
    commands.add_parser("doctor")
    export = commands.add_parser("export", help="Export appearance only; no connection details or keys")
    export.add_argument("file", type=Path)
    restore_cmd = commands.add_parser("restore")
    restore_cmd.add_argument("backup", help="Folder name under config/k3-backups")
    apply_cmd = commands.add_parser("apply")
    apply_cmd.add_argument("--from-file", type=Path)
    apply_cmd.add_argument("--profile", choices=PROFILES)
    apply_cmd.add_argument("--size")
    apply_cmd.add_argument("--rotation", type=int, choices=(0, 90, 180, 270))
    apply_cmd.add_argument("--backend", choices=("auto", "drm", "fbdev"))
    apply_cmd.add_argument("--accent")
    apply_cmd.add_argument("--mode", choices=("dark", "light"))
    apply_cmd.add_argument("--brightness", type=int)
    apply_cmd.add_argument("--touch-device")
    args = parser.parse_args(argv)
    directory = args.config_dir.expanduser().resolve()
    try:
        if args.command == "profiles":
            for name, profile in PROFILES.items():
                print(name + ": " + profile["description"])
        elif args.command == "doctor":
            doctor(directory)
        elif args.command == "export":
            source = directory / "k3-appearance.json"
            if not source.exists():
                raise ValueError("Apply a K3 profile before exporting its appearance.")
            if args.file.resolve() == source.resolve():
                raise ValueError("Choose an export path outside the active appearance file.")
            data = json_bytes(validate_options(json.loads(source.read_text())))
            # An export must never overwrite settings, a theme, or an existing file.
            with args.file.open("xb") as stream:
                os.chmod(args.file, 0o600)
                stream.write(data)
            print("Exported K3 profile options. In-screen Theme Editor changes are saved separately.")
        elif args.command == "restore":
            restore(directory, args.backup)
            print("Restored backup. Start HelixScreen to use it.")
        else:
            source = args.from_file or directory / "k3-appearance.json"
            options = json.loads(source.read_text()) if source.exists() else {}
            if args.from_file and not source.exists():
                raise ValueError("Appearance file does not exist.")
            for key in ("profile", "size", "rotation", "backend", "accent", "mode", "brightness", "touch_device"):
                value = getattr(args, key)
                if value is not None:
                    options[key] = value
            if args.profile is not None and args.size is None:
                options["size"] = None
            backup = apply(directory, options)
            print("Already configured." if backup is None else "Applied K3 profile. Backup: " + str(backup))
            print("Start HelixScreen to use these settings; finish its setup wizard for your printer.")
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.exit(1, "K3 configuration failed: " + str(error) + "\n")


if __name__ == "__main__":
    main()
