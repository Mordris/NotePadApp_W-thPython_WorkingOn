from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox
from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat, QTextDocument


class FindReplaceDialog(QDialog):
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit
        self.setWindowTitle("Find and Replace")
        self.setWindowModality(True)

        layout = QVBoxLayout()

        self.find_label = QLabel("Find:")
        self.find_input = QLineEdit()
        self.find_button = QPushButton("Find")
        self.find_button.clicked.connect(self.find_text)

        self.replace_label = QLabel("Replace:")
        self.replace_input = QLineEdit()
        self.replace_button = QPushButton("Replace")
        self.replace_button.clicked.connect(self.replace_text)

        form_layout = QFormLayout()
        form_layout.addRow(self.find_label, self.find_input)
        form_layout.addRow(self.find_button, None)
        form_layout.addRow(self.replace_label, self.replace_input)
        form_layout.addRow(self.replace_button, None)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def find_text(self):
        text = self.find_input.text()
        if text:
            cursor = self.text_edit.document().find(text)

            if not cursor.isNull():
                format_ = QTextCharFormat()
                format_.setBackground(QColor("yellow"))  # Set the background color to red

                while not cursor.isNull():
                    cursor.mergeCharFormat(format_)
                    cursor = self.text_edit.document().find(text, cursor)

    def replace_text(self):
        find_text = self.find_input.text()
        replace_text = self.replace_input.text()
        if find_text and replace_text:
            self.text_edit.moveCursor(QTextCursor.Start)
            while self.text_edit.find(find_text, QTextDocument.FindCaseSensitively):
                self.text_edit.textCursor().insertText(replace_text)
        else:
            QMessageBox.warning(self, "Replace", "Please enter both find and replace text.")
