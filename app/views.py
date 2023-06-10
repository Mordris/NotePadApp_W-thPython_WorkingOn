import sys
from PyQt5.QtWidgets import QMainWindow, QPlainTextEdit, QAction, QFileDialog, QApplication
from PyQt5.QtGui import QIcon, QTextCursor, QColor
from PyQt5.QtCore import Qt
from utils.helpers import FindReplaceDialog


class NotepadApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Notepad App")
        self.setWindowIcon(QIcon("icons/icon.png"))

        self.text_edit = QPlainTextEdit(self)
        self.setCentralWidget(self.text_edit)

        new_action = QAction(QIcon("icons/new.png"), "New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)

        open_action = QAction(QIcon("icons/open.png"), "Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)

        save_action = QAction(QIcon("icons/save.png"), "Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)

        undo_action = QAction(QIcon("icons/undo.png"), "Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.text_edit.undo)

        redo_action = QAction(QIcon("icons/redo.png"), "Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.text_edit.redo)

        copy_action = QAction(QIcon("icons/copy.png"), "Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.text_edit.copy)

        paste_action = QAction(QIcon("icons/paste.png"), "Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.text_edit.paste)

        find_replace_action = QAction(QIcon("icons/find_replace.png"), "Find and Replace", self)
        find_replace_action.setShortcut("Ctrl+F")
        find_replace_action.triggered.connect(self.show_find_replace_dialog)

        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)

        edit_menu = self.menuBar().addMenu("Edit")
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addAction(find_replace_action)

    def new_file(self):
        self.text_edit.clear()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "r") as file:
                self.text_edit.setPlainText(file.read())

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_edit.toPlainText())

    def show_find_replace_dialog(self):
        dialog = FindReplaceDialog(self.text_edit)
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    notepad = NotepadApp()
    notepad.show()
    sys.exit(app.exec_())
