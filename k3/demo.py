#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Run the native K3 UI against HelixScreen's mock printer, in an isolated config."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

from configure import ROOT, apply


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", default="400x1280")
    parser.add_argument("--binary", type=Path, default=ROOT / "build/bin/helix-screen",
                        help="Native developer binary built from this source revision")
    parser.add_argument("--capture", type=Path, help="Capture home, controls, motion and settings, then exit")
    args = parser.parse_args()
    binary = args.binary.expanduser().resolve()
    if not binary.exists():
        parser.exit(1, "Build the native simulator first: make\n")
    with tempfile.TemporaryDirectory(prefix="helix-k3-") as temp:
        directory = Path(temp)
        apply(directory, {"size": args.size})
        path = directory / "settings.json"
        settings = json.loads(path.read_text())
        settings["wizard_completed"] = True
        settings["printers"]["default"]["wizard_completed"] = True
        settings["printers"]["default"]["printer_name"] = "K3 Demo (mock)"
        settings["printers"]["default"]["type"] = "Voron 2.4"
        settings["display"].update(sleep_sec=0, dim_sec=0, screensaver_type="off")
        settings["sounds_enabled"] = False
        settings["tour"] = {"completed": True, "last_seen_version": 1}
        # --test deliberately reads settings-test.json, not the production filename.
        (directory / "settings-test.json").write_text(json.dumps(settings))
        socket = str(directory / "control.sock")
        env = dict(os.environ, HELIX_CONFIG_DIR=temp, HELIX_DATA_DIR=str(ROOT))
        if args.capture:
            env["SDL_VIDEODRIVER"] = "dummy"
            env["SDL_RENDER_DRIVER"] = "software"
        # --test is unconditional. This tool never accepts real-printer overrides.
        command = [str(binary), "--test", "-vv", "-s", args.size,
                   "--dark", "--skip-splash", "--remote-socket", socket]
        with (directory / "demo.log").open("w") as log:
            process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
            try:
                if not args.capture:
                    print("Mock printer only. Close the simulator window to exit.")
                    raise SystemExit(process.wait())
                output = args.capture.resolve()
                output.mkdir(parents=True, exist_ok=True)

                def ctl(*arguments, check=True):
                    return subprocess.run([str(binary), "ctl", "-s", socket, *arguments],
                                          env=env, cwd=ROOT, capture_output=True, text=True,
                                          check=check, timeout=30)

                deadline = time.monotonic() + 90
                while time.monotonic() < deadline:
                    if process.poll() is not None:
                        raise RuntimeError("Simulator exited during startup")
                    if Path(socket).exists() and ctl("ping", check=False).returncode == 0:
                        break
                    time.sleep(0.25)
                else:
                    raise RuntimeError("Simulator did not become ready in 90 seconds")
                # Let startup discovery/toasts settle before taking review evidence.
                time.sleep(8)
                for screen in ("home", "controls", "motion", "settings"):
                    if screen == "motion":
                        ctl("navigate", "controls")
                        ctl("click", "btn_motion")
                    else:
                        ctl("navigate", screen)
                    time.sleep(1)
                    ctl("screenshot", str(output / (screen + ".png")))
                    if screen == "controls" and int(args.size.split("x")[0]) < int(args.size.split("x")[1]):
                        ctl("scroll", "btn_bed_mesh")
                        time.sleep(0.5)
                        ctl("screenshot", str(output / "controls-scrolled.png"))
                        # Open and cancel the existing confirmation; never press STOP.
                        ctl("click", "k3_emergency_stop")
                        time.sleep(0.5)
                        ctl("screenshot", str(output / "emergency-confirmation.png"))
                        ctl("click", "btn_secondary")
                        ctl("scroll", "card_position")
                print("Native mock screenshots: " + str(output))
            except (RuntimeError, subprocess.SubprocessError):
                print((directory / "demo.log").read_text()[-8000:])
                raise
            finally:
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
                if args.capture:
                    log.flush()
                    shutil.copyfile(directory / "demo.log", output / "native.log")


if __name__ == "__main__":
    main()
