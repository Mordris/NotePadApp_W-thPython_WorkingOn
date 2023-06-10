from PyQt5.QtCore import QObject, pyqtSignal


class FindReplaceOptions(QObject):
    def __init__(self):
        super().__init__()
        self.find_text = ""
        self.replace_text = ""
        self.match_case = False
        self.match_word = False
        self.search_backwards = False
        self.replace_all = False
        self.highlight_links = False  # Added flag

    def reset(self):
        self.find_text = ""
        self.replace_text = ""
        self.match_case = False
        self.match_word = False
        self.search_backwards = False
        self.replace_all = False


class FindReplaceModel(QObject):
    find_text_changed = pyqtSignal(str)
    replace_text_changed = pyqtSignal(str)
    match_case_changed = pyqtSignal(bool)
    match_word_changed = pyqtSignal(bool)
    search_backwards_changed = pyqtSignal(bool)
    replace_all_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.options = FindReplaceOptions()

    def set_find_text(self, text):
        self.options.find_text = text
        self.find_text_changed.emit(text)

    def set_replace_text(self, text):
        self.options.replace_text = text
        self.replace_text_changed.emit(text)

    def set_match_case(self, checked):
        self.options.match_case = checked
        self.match_case_changed.emit(checked)

    def set_match_word(self, checked):
        self.options.match_word = checked
        self.match_word_changed.emit(checked)

    def set_search_backwards(self, checked):
        self.options.search_backwards = checked
        self.search_backwards_changed.emit(checked)

    def set_replace_all(self, checked):
        self.options.replace_all = checked
        self.replace_all_changed.emit(checked)

    def get_find_text(self):
        return self.options.find_text

    def get_replace_text(self):
        return self.options.replace_text

    def reset_options(self):
        self.options.reset()
        self.find_text_changed.emit("")
        self.replace_text_changed.emit("")
        self.match_case_changed.emit(False)
        self.match_word_changed.emit(False)
        self.search_backwards_changed.emit(False)
        self.replace_all_changed.emit(False)
