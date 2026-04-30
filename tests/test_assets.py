import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from seewo_editor import assets  # noqa: E402


class AssetTests(unittest.TestCase):
    def test_ensure_assets_materializes_package_resources(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with mock.patch.dict("os.environ", {"APPDATA": temp_dir}):
                builtin = assets.ensure_assets()

            self.assertTrue(builtin.default_image.exists())
            self.assertTrue(builtin.icon.exists())
            self.assertTrue(builtin.sound.exists())
            self.assertTrue(str(builtin.default_image).startswith(temp_dir))


if __name__ == "__main__":
    unittest.main()
