import unittest
import tempfile
from pathlib import Path
import pandas as pd

from io_utils import (
    load_file,
    save_file,
    file_exists,
    folder_exists,
    move_file,
    copy_file,
    create_folderpath,
)


class TestIOUtils(unittest.TestCase):

    def setUp(self):
        # Temporäres Arbeitsverzeichnis für jeden Test
        self.tmpdir = tempfile.TemporaryDirectory()
        self.base = Path(self.tmpdir.name)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_ensure_folder_and_exists(self):
        folder = self.base / "subdir"
        self.assertFalse(folder_exists(folder))
        create_folderpath(folder)
        self.assertTrue(folder_exists(folder))

    def test_save_and_load_csv(self):
        df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
        path = save_file(df, self.base, "testdata", "csv")

        self.assertTrue(file_exists(path))

        loaded = load_file(path)
        self.assertTrue(isinstance(loaded, pd.DataFrame))
        self.assertEqual(list(loaded.columns), ["a", "b"])
        self.assertEqual(len(loaded), 3)

    def test_save_and_load_txt(self):
        text = "Hello World"
        path = save_file(text, self.base, "mytext", "txt")

        self.assertTrue(file_exists(path))

        loaded = load_file(path)
        self.assertIn("Hello World", loaded)

    def test_load_file_unknown_extension(self):
        file = self.base / "notes.md"
        content = "# Überschrift\nEtwas Inhalt"
        file.write_text(content, encoding="utf-8")

        loaded = load_file(file)
        self.assertIsInstance(loaded, str)
        self.assertIn("Überschrift", loaded)
        self.assertIn("Etwas Inhalt", loaded)

    def test_move_file(self):
        src_file = self.base / "src.txt"
        dst_file = self.base / "moved" / "dst.txt"

        src_file.write_text("content")

        moved_path = move_file(src_file, dst_file)
        self.assertFalse(src_file.exists())
        self.assertTrue(dst_file.exists())
        self.assertEqual(moved_path, dst_file)

    def test_copy_file(self):
        src_file = self.base / "src.txt"
        dst_file = self.base / "copied" / "dst.txt"

        src_file.write_text("content")

        copied_path = copy_file(src_file, dst_file)
        self.assertTrue(src_file.exists())   # Quelle bleibt erhalten
        self.assertTrue(dst_file.exists())   # Ziel existiert
        self.assertEqual(copied_path, dst_file)

    def test_overwrite_behavior(self):
        src_file = self.base / "src.txt"
        dst_file = self.base / "dst.txt"

        src_file.write_text("old")
        dst_file.write_text("new")

        # ohne overwrite=False -> Exception
        with self.assertRaises(FileExistsError):
            copy_file(src_file, dst_file, overwrite=False)

        # mit overwrite=True -> klappt
        copy_file(src_file, dst_file, overwrite=True)
        self.assertEqual(dst_file.read_text(), "old")


if __name__ == "__main__":
    unittest.main()
