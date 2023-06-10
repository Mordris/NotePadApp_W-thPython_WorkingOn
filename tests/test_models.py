import unittest

from app.models import FindReplaceModel


class FindReplaceModelTests(unittest.TestCase):
    def setUp(self):
        self.model = FindReplaceModel()

    def test_set_find_text(self):
        text = "Find Text"
        self.model.set_find_text(text)
        self.assertEqual(self.model.get_find_text(), text)

    def test_set_replace_text(self):
        text = "Replace Text"
        self.model.set_replace_text(text)
        self.assertEqual(self.model.get_replace_text(), text)

    def test_set_match_case(self):
        checked = True
        self.model.set_match_case(checked)
        self.assertEqual(self.model.options.match_case, checked)

    def test_set_match_word(self):
        checked = True
        self.model.set_match_word(checked)
        self.assertEqual(self.model.options.match_word, checked)

    def test_set_search_backwards(self):
        checked = True
        self.model.set_search_backwards(checked)
        self.assertEqual(self.model.options.search_backwards, checked)

    def test_set_replace_all(self):
        checked = True
        self.model.set_replace_all(checked)
        self.assertEqual(self.model.options.replace_all, checked)

    def test_reset_options(self):
        self.model.reset_options()
        options = self.model.options
        self.assertEqual(options.find_text, "")
        self.assertEqual(options.replace_text, "")
        self.assertEqual(options.match_case, False)
        self.assertEqual(options.match_word, False)
        self.assertEqual(options.search_backwards, False)
        self.assertEqual(options.replace_all, False)

if __name__ == '__main__':
    unittest.main()
