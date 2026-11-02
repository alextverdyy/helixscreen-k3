# SPDX-License-Identifier: GPL-3.0-or-later
import hashlib
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
import uuid

from package import refresh


class PackageChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        payload = self.path / "helixscreen"
        (payload / "bin").mkdir(parents=True)
        (payload / "ui_xml/portrait").mkdir(parents=True)
        self.binary = b"unchanged compiled-binary fixture"
        (payload / "bin/helix-screen").write_bytes(self.binary)
        (payload / "ui_xml/portrait/controls_panel.xml").write_text("old runtime fixture")
        self.archive = self.path / "input.tar.gz"
        with tarfile.open(self.archive, "w:gz") as bundle:
            bundle.add(payload, arcname="helixscreen")

    def test_runtime_refresh_preserves_binary_and_records_provenance(self):
        output = refresh(self.archive, self.path / "out.tar.gz", "a" * 40, "b" * 40)
        with tarfile.open(output) as bundle:
            self.assertEqual(bundle.extractfile("helixscreen/bin/helix-screen").read(), self.binary)
            xml = bundle.extractfile("helixscreen/ui_xml/portrait/controls_panel.xml").read()
            self.assertIn(b'k3_scroll_content', xml)
            self.assertIn(b'text="Control"', bundle.extractfile("helixscreen/ui_xml/portrait/navigation_bar.xml").read())
            self.assertIn(b'k3_print_files', bundle.extractfile("helixscreen/ui_xml/portrait/print_status_detailed_idle.xml").read())
            data = json.load(bundle.extractfile("helixscreen/k3-build-provenance.json"))
            self.assertEqual(data["binary_sha256"], hashlib.sha256(self.binary).hexdigest())
            self.assertEqual(data["runtime_source"], "b" * 40)
            self.assertFalse(data["physical_hardware_validated"])
            self.assertIn("helixscreen/k3/configure.py", bundle.getnames())

    def test_bad_provenance_is_rejected_before_writing(self):
        output = self.path / "out.tar.gz"
        with self.assertRaises(ValueError):
            refresh(self.archive, output, "not-a-revision", "b" * 40)
        self.assertFalse(output.exists())

    def test_archive_path_escape_is_rejected(self):
        unique = "k3-escape-test-" + uuid.uuid4().hex
        escaped = Path(tempfile.gettempdir()) / unique
        self.addCleanup(lambda: escaped.unlink(missing_ok=True))
        with tarfile.open(self.archive, "w:gz") as bundle:
            member = tarfile.TarInfo("../" + unique)
            member.size = 4
            bundle.addfile(member, io.BytesIO(b"test"))
        with self.assertRaises(tarfile.TarError):
            refresh(self.archive, self.path / "out.tar.gz", "a" * 40, "b" * 40)
        self.assertFalse(escaped.exists())


if __name__ == "__main__":
    unittest.main()
