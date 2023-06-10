from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QFormLayout
from PyQt5.QtCore import Qt


class FindReplaceDialog(QDialog):
    def __init__(self, text_edit, find_replace_model, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find and Replace")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout(self)

        find_label = QLabel("Find:")
        self.find_input = QLineEdit()
        self.find_input.textChanged.connect(find_replace_model.set_find_text)

        replace_label = QLabel("Replace:")
        self.replace_input = QLineEdit()
        self.replace_input.textChanged.connect(find_replace_model.set_replace_text)

        match_case_checkbox = QCheckBox("Match Case")
        match_case_checkbox.stateChanged.connect(find_replace_model.set_match_case)

        match_word_checkbox = QCheckBox("Match Whole Word")
        match_word_checkbox.stateChanged.connect(find_replace_model.set_match_word)

        search_backwards_checkbox = QCheckBox("Search Backwards")
        search_backwards_checkbox.setChecked(find_replace_model.options.search_backwards)
        search_backwards_checkbox.stateChanged.connect(
            lambda state: find_replace_model.set_search_backwards(state == Qt.Checked))

        find_button = QPushButton("Find")
        find_button.clicked.connect(lambda: text_edit.find(find_replace_model.get_find_text()))

        replace_button = QPushButton("Replace")
        replace_button.clicked.connect(lambda: text_edit.replace(find_replace_model.get_find_text(), find_replace_model.get_replace_text()))

        replace_all_button = QPushButton("Replace All")
        replace_all_button.clicked.connect(lambda: text_edit.replace_all(find_replace_model.get_find_text(), find_replace_model.get_replace_text()))

        form_layout = QFormLayout()
        form_layout.addRow(find_label, self.find_input)
        form_layout.addRow(replace_label, self.replace_input)
        form_layout.addRow(match_case_checkbox)
        form_layout.addRow(match_word_checkbox)
        form_layout.addRow(search_backwards_checkbox)
        form_layout.addRow(find_button)
        form_layout.addRow(replace_button)
        form_layout.addRow(replace_all_button)

        layout.addLayout(form_layout)

        self.setLayout(layout)


def find_replace_dialog(text_edit, find_replace_model):
    dialog = FindReplaceDialog(text_edit, find_replace_model)
    dialog.exec_()
