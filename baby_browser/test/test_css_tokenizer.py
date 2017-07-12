import unittest
from .html_tokenizer import *
from .css_tokenizer import *

class TestCSSTokenizer(unittest.TestCase):
    def setUp(self):
        self.html_str1 = "<html>\n<head><title>Website Title</title></head>\n<body>\n<h1 class=\"hello\">Hi</h1>\n<h2 class=\"hello goodbye\">Yah!</h2>\n</body>\n</html>"
        self.html_str2 = "<html>\n<head><title>Website Title</title></head>\n<body>\n<div id=\"bye\"class=\"hello world\">Hi</div>\n<img src=\"html5.gif\" alt=\"HTML5 Icon\" width=\"128\" height=\"128\">\n</body>\n</html>"
        html_tokenizer = HtmlTokenizer()
        html_tokenizer.tokenize(html_str1)
        self.html_dom1 = html_tokenizer.dom
        html_tokenizer.tokenize(html_str2)
        self.html_dom2 = html_tokenizer.dom 
        self.css_str = "body{background-color:red;color:white;}\nh1{background-color:white;}\n.hello{color:yellow;}\n.goodbye{padding:4px;}"
    css_tokenizer = CSSTokenizer()
    css_tokenizer.tokenize(css_str, html_tokenizer.dom)
    def test_tokenize(self):
        pass
    def test_parse(self):
        pass
    def test_get_dom_elements(self):
        pass
    def test_create_style(self):
        pass
