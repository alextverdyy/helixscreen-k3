# SPDX-License-Identifier: GPL-3.0-or-later
"""Integration tests for configuration preservation and recovery; no printer needed."""
import fcntl
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import configure


class ConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)

    def seed(self):
        data = json.loads((configure.ROOT / "config/settings.json.template").read_text())
        data["printers"]["default"].update(name="My printer", moonraker_host="printer.local", moonraker_api_key="test-key-never-export")
        data["future_option"] = {"must_survive": True}
        self.original = configure.json_bytes(data)
        (self.path / "settings.json").write_bytes(self.original)
        return data

    def read(self):
        return json.loads((self.path / "settings.json").read_text())

    def test_apply_preserves_all_printer_data_and_unknown_fields(self):
        before = self.seed()
        configure.apply(self.path, {"profile": "portrait-480x800", "rotation": 90})
        after = self.read()
        self.assertEqual(before["printers"], after["printers"])
        self.assertEqual(before["future_option"], after["future_option"])
        self.assertEqual(after["display"]["rotate"], 90)
        self.assertIn("HELIX_SCREEN_SIZE=480x800", (self.path / "helixscreen.env").read_text())

    def test_new_install_keeps_setup_wizard(self):
        configure.apply(self.path, {})
        self.assertFalse(self.read()["wizard_completed"])
        self.assertGreater(self.read()["config_version"], 0)

    def test_bad_existing_config_is_never_replaced(self):
        for content in (b'{"config_version":0}', b'{broken', b'[]'):
            (self.path / "settings.json").write_bytes(content)
            with self.assertRaises(ValueError):
                configure.apply(self.path, {})
            self.assertEqual((self.path / "settings.json").read_bytes(), content)

    def test_idempotent_apply_does_not_create_more_backups(self):
        configure.apply(self.path, {})
        self.assertIsNone(configure.apply(self.path, {}))
        self.assertEqual(len(list((self.path / "k3-backups").iterdir())), 1)

    def test_restore_recovers_exact_original_bytes(self):
        self.seed()
        backup = configure.apply(self.path, {"mode": "light"})
        self.assertEqual(backup.stat().st_mode & 0o777, 0o700)
        configure.restore(self.path, backup.name)
        self.assertEqual((self.path / "settings.json").read_bytes(), self.original)
        self.assertFalse((self.path / "k3-appearance.json").exists())
        self.assertFalse((self.path / "themes/k3-violet.json").exists())

    def test_running_app_lock_blocks_apply(self):
        self.seed()
        with (self.path / ".helix-screen.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaisesRegex(ValueError, "running"):
                configure.apply(self.path, {})
        self.assertEqual((self.path / "settings.json").read_bytes(), self.original)

    def test_auto_profile_removes_only_owned_env_overrides(self):
        (self.path / "helixscreen.env").write_text("# Keep me\nHELIX_DPI=160\nexport HELIX_SCREEN_SIZE=480x800\nHELIX_DISPLAY_BACKEND=fbdev\nHELIX_SCREEN_SIZE=320x1480\n")
        configure.apply(self.path, {})
        text = (self.path / "helixscreen.env").read_text()
        self.assertIn("# Keep me\nHELIX_DPI=160", text)
        self.assertNotIn("HELIX_SCREEN_SIZE=", text)
        self.assertNotIn("HELIX_DISPLAY_BACKEND=", text)

    def test_invalid_import_cannot_write_shell_or_escape(self):
        for options in ({"size": "480x800\nBAD=1"}, {"rotation": True}, {"brightness": True},
                        {"touch_device": "/etc/passwd"}, {"accent": "$(id)"},
                        {"profile": "../../x"}, {"backend": "$(id)"}, {"printers": {}}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                configure.apply(self.path, options)
        self.assertFalse((self.path / "settings.json").exists())

    def test_dangling_symlink_destination_is_refused(self):
        target = self.path / "missing"
        (self.path / "helixscreen.env").symlink_to(target)
        with self.assertRaisesRegex(ValueError, "symlink"):
            configure.apply(self.path, {})
        self.assertFalse(target.exists())

    def test_installer_settings_symlink_survives_apply_and_restore(self):
        self.seed()
        target = self.path / "printer-data-settings.json"
        (self.path / "settings.json").rename(target)
        (self.path / "settings.json").symlink_to(target)
        backup = configure.apply(self.path, {})
        self.assertTrue((self.path / "settings.json").is_symlink())
        self.assertEqual(json.loads(target.read_text())["display"]["theme"], "k3-violet")
        configure.restore(self.path, backup.name)
        self.assertTrue((self.path / "settings.json").is_symlink())
        self.assertEqual(target.read_bytes(), self.original)

    def test_export_cannot_overwrite_active_settings(self):
        self.seed()
        configure.apply(self.path, {})
        before = (self.path / "settings.json").read_bytes()
        with self.assertRaises(SystemExit):
            configure.main(["--config-dir", str(self.path), "export", str(self.path / "settings.json")])
        self.assertEqual((self.path / "settings.json").read_bytes(), before)

    def test_failed_write_rolls_back_changed_files(self):
        self.seed()
        original_write = configure.atomic_write
        failed = False

        def fail_once(path, data):
            nonlocal failed
            if path == self.path / "settings.json" and not failed:
                failed = True
                raise OSError("simulated disk failure")
            original_write(path, data)

        with patch.object(configure, "atomic_write", fail_once), self.assertRaises(OSError):
            configure.apply(self.path, {})
        self.assertEqual((self.path / "settings.json").read_bytes(), self.original)
        self.assertFalse((self.path / "themes/k3-violet.json").exists())

    def test_export_never_contains_printer_credentials(self):
        self.seed()
        configure.apply(self.path, {"accent": "#7946E8"})
        output = self.path / "share.json"
        configure.main(["--config-dir", str(self.path), "export", str(output)])
        text = output.read_text()
        self.assertNotIn("test-key-never-export", text)
        self.assertNotIn("printer.local", text)
        self.assertEqual(json.loads(text)["accent"], "#7946E8")

    def test_cli_rejects_missing_import_before_writes(self):
        result = subprocess.run([sys.executable, str(configure.ROOT / "k3/configure.py"),
                                 "--config-dir", str(self.path), "apply", "--from-file", str(self.path / "missing")],
                                capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.path / "settings.json").exists())

    def test_restore_rejects_path_traversal(self):
        with self.assertRaises(ValueError):
            configure.restore(self.path, "../../elsewhere")


if __name__ == "__main__":
    unittest.main()
