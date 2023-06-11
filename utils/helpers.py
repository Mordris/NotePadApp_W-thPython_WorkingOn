from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox, QApplication
from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat, QTextDocument
from PyQt5.QtCore import Qt, QTimer

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
                format_.setBackground(QColor("yellow"))  # Set the background color to yellow

                # Remove the previous yellow background color
                old_format = QTextCharFormat()
                old_format.setBackground(QColor(Qt.white))  # Set the background color to white

                self.text_edit.clearFocus()  # Remove the text edit's focus to prevent highlighting during the search

                # Remove the yellow background color from all occurrences
                cursor.setPosition(0)
                while cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor):
                    cursor.mergeCharFormat(old_format)

                # Find and highlight new occurrences
                cursor = self.text_edit.document().find(text)
                while not cursor.isNull():
                    start = cursor.selectionStart()
                    end = cursor.selectionEnd()

                    # Apply the yellow background color to the current position
                    cursor.mergeCharFormat(format_)
                    cursor = self.text_edit.document().find(text, cursor)

                self.text_edit.setFocus()  # Restore the focus to the text edit after the search
            else:
                self.show_error_message("Text not found.")

    def replace_text(self):
        find_text = self.find_input.text()
        replace_text = self.replace_input.text()
        if find_text and replace_text:
            self.text_edit.moveCursor(QTextCursor.Start)
            while self.text_edit.find(find_text, QTextDocument.FindCaseSensitively):
                self.text_edit.textCursor().insertText(replace_text)
        else:
            self.show_error_message("Please enter both find and replace text.")

    def show_error_message(self, message):
        error_message_box = QMessageBox(self)
        error_message_box.setIcon(QMessageBox.Warning)
        error_message_box.setWindowTitle("Error")
        error_message_box.setText(message)
        error_message_box.setStandardButtons(QMessageBox.Ok)
        error_message_box.setDefaultButton(QMessageBox.Ok)
        error_message_box.setWindowModality(Qt.ApplicationModal)

        # Set a timer to close the error message box after 2 seconds
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(error_message_box.close)
        timer.start(2000)

        error_message_box.exec_()
