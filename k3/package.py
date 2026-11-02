#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Refresh a trusted fork build with reviewed runtime files; Python 3.12+."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def refresh(archive, output, binary_source, data_source):
    for revision in (binary_source, data_source):
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise ValueError("Build provenance must use full git revisions.")
    if Path(archive).resolve() == Path(output).resolve():
        raise ValueError("Choose a separate output archive.")
    with tempfile.TemporaryDirectory(prefix="k3-package-") as temp:
        stage = Path(temp)
        with tarfile.open(archive) as bundle:
            bundle.extractall(stage, filter="data")
        payload = stage / "helixscreen"
        binary = payload / "bin/helix-screen"
        if not binary.is_file() or not (payload / "ui_xml").is_dir():
            raise ValueError("Expected a complete HelixScreen installer archive.")
        binary_digest = hashlib.sha256(binary.read_bytes()).hexdigest()
        for name in ("ui_xml/components/panel_widget_k3_dashboard.xml", "ui_xml/portrait/app_layout.xml", "ui_xml/portrait/settings_panel.xml", 'ui_xml/portrait/k3_action_row.xml', 'ui_xml/portrait/panel_widget_motion.xml', 'ui_xml/portrait/panel_widget_macros.xml', 'ui_xml/portrait/panel_widget_gcode_console.xml', 'ui_xml/portrait/panel_widget_print_stats.xml', 'ui_xml/portrait/panel_widget_preheat.xml', "ui_xml/portrait/controls_panel.xml", "ui_xml/portrait/navigation_bar.xml", "ui_xml/portrait/navbar_estop.xml",
                     "ui_xml/portrait/navbar_drying.xml",
                     "ui_xml/components/print_status_detailed_idle.xml", "ui_xml/portrait/print_status_detailed_idle.xml",
                     "ui_xml/portrait/panel_widget_printer_image.xml", "assets/images/printers/annex-k3.png", "assets/config/themes/defaults/k3-violet.json",
                     "K3_README.md", "PRODUCT.md", "DESIGN.md", "LICENSE", "COPYRIGHT"):
            destination = payload / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, destination)
        shutil.copytree(ROOT / "ui_xml/portrait", payload / "ui_xml/portrait", dirs_exist_ok=True)
        for source in (ROOT / "k3").iterdir():
            if source.is_file() and source.suffix in (".py", ".json", ".md"):
                (payload / "k3").mkdir(exist_ok=True)
                shutil.copyfile(source, payload / "k3" / source.name)
        shutil.copytree(ROOT / "docs/images/k3", payload / "docs/images/k3", dirs_exist_ok=True)
        metadata = {"binary_source": binary_source, "runtime_source": data_source,
                    "binary_sha256": binary_digest, "physical_hardware_validated": False}
        (payload / "k3-build-provenance.json").write_text(json.dumps(metadata, indent=2) + "\n")
        if hashlib.sha256(binary.read_bytes()).hexdigest() != binary_digest:
            raise ValueError("The compiled binary changed during runtime packaging.")
        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        with tarfile.open(output, "w:gz") as bundle:
            bundle.add(payload, arcname="helixscreen")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--binary-source", required=True)
    parser.add_argument("--runtime-source", required=True)
    args = parser.parse_args()
    try:
        print(refresh(args.archive, args.output, args.binary_source, args.runtime_source))
    except (OSError, ValueError, tarfile.TarError) as error:
        parser.exit(1, "K3 packaging failed: " + str(error) + "\n")


if __name__ == "__main__":
    main()
