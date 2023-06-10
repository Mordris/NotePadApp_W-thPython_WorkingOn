# views.py
import sys
import re

from PyQt5.QtWidgets import QMainWindow, QPlainTextEdit, QAction, QFileDialog, QMessageBox, QUndoStack, QTextEdit, \
    QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QFormLayout
from PyQt5.QtGui import QIcon, QTextCharFormat, QTextCursor, QPalette
from PyQt5.QtCore import Qt, QRegularExpression
from app.models import FindReplaceModel
from utils.helpers import find_replace_dialog, FindReplaceDialog


class HighlightingTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlights = []
        self.setExtraSelections([])

    def highlightText(self, pattern):
        self.highlights = []
        text = self.toPlainText()
        format_ = QTextCharFormat()
        format_.setBackground(Qt.yellow)
        regex = QRegularExpression(pattern)
        matches = regex.globalMatch(text)
        while matches.hasNext():
            match = matches.next()
            start = match.capturedStart()
            length = match.capturedLength()
            self.highlights.append((start, length))

        self.updateExtraSelections()

    def updateExtraSelections(self):
        selections = []
        format_ = QTextCharFormat()
        format_.setBackground(Qt.yellow)

        for start, length in self.highlights:
            start_cursor = QTextCursor(self.document())
            start_cursor.setPosition(start)
            end_cursor = QTextCursor(self.document())
            end_cursor.setPosition(start + length)
            selection = QTextEdit.ExtraSelection()
            selection.format = format_
            selection.cursor = start_cursor
            selection.cursor.setPosition(end_cursor.position(), QTextCursor.KeepAnchor)
            selections.append(selection)

        self.setExtraSelections(selections)


class NotepadApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

        self.find_replace_model = FindReplaceModel()

    def init_ui(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Notepad App")
        self.setWindowIcon(QIcon("icons/icon.png"))

        self.text_edit = HighlightingTextEdit(self)
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
        undo_action.triggered.connect(self.undo)

        redo_action = QAction(QIcon("icons/redo.png"), "Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.redo)

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

        self.text_edit.textChanged.connect(self.highlight_links)

        self.undo_stack = QUndoStack(self)
        undo_action.setEnabled(self.undo_stack.canUndo())
        redo_action.setEnabled(self.undo_stack.canRedo())

    def new_file(self):
        self.text_edit.clear()
        self.undo_stack.clear()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "r") as file:
                self.text_edit.setPlainText(file.read())
            self.undo_stack.clear()

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_edit.toPlainText())
            self.undo_stack.setClean()

    def undo(self):
        self.undo_stack.undo()

    def redo(self):
        self.undo_stack.redo()

    def highlight_links(self):
        url_pattern = r"\b(?:https?://|www\.)\S+\b"
        self.text_edit.highlightText(url_pattern)

    def show_find_replace_dialog(self):
        find_replace_dialog(self.text_edit, self.find_replace_model)