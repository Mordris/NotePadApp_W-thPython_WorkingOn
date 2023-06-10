import unittest
import os
import shutil
import tempfile
from PyQt5.QtWidgets import QApplication

from app.views import NotepadApp
from utils.helpers import FindReplaceDialog

app = QApplication([])  # Create a QApplication instance for running the tests

class NotepadAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = tempfile.mkdtemp()

    def setUp(self):
        self.notepad = NotepadApp()

    def tearDown(self):
        self.notepad.close()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_dir)

    def test_open_file(self):
        file_path = os.path.join(self.test_dir, "test_file.txt")
        with open(file_path, "w") as file:
            file.write("Sample text")

        self.notepad.open_file()  # No argument needed
        text = self.notepad.text_edit.toPlainText()

        self.assertEqual(text, "Sample text")

    def test_save_file(self):
        file_path = os.path.join(self.test_dir, "test_file.txt")
        self.notepad.text_edit.setPlainText("Sample text")

        self.notepad.save_file()  # No argument needed
        with open(file_path, "r") as file:
            saved_text = file.read()

        self.assertEqual(saved_text, "Sample text")

if __name__ == "__main__":
    unittest.main()
