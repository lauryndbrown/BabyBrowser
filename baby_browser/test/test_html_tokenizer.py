import unittest
from .html_tokenizer import *

class TestHtmlTokenizer(unittest.TestCase):
    def test_init(self):
        tokenizer = HtmlTokenizer()
        self.assertIsNone(tokenizer.dom)
        self.assertIsNone(tokenizer.current_state)
    def test_tokenize(self):
        pass
    def test_parse(self):
        pass
    def test_handle_opentag(self):
        pass
    def test_handle_closetag(self):
        pass
    def test_handle_data(self):
        pass
    def test_p_opentag(self):
        pass
    def test_p_opentag_attrs(self):
        pass
    def test_set_opentag_state(self):
        pass
    def test_p_closetag(self):
        pass
    def test_p_data(self):
        pass
    def test_remove_excess_whitespace(self):
        pass



