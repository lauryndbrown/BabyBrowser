import unittest
from baby_browser.html_objects import *
from baby_browser.css_objects import *

class TestHtmlObjects(unittest.TestCase):
    def test_default_init(self):
        html = HtmlObject(None, None)
        self.assertEqual(html.children, [])
        self.assertEqual(html.attrs, {CLASS:None, ID:None})
        self.assertIs(html.parse_state, None)
        self.assertIsInstance(html.css, RenderObject)
    def test_get_css_property(self):
        pass

class TestText(unittest.TestCase):
    def test_init(self):
        pass
    def test_str(self):
        pass
class TestTag(unittest.TestCase):
    def setUp(self):
        self.img = Tag('img')
        self.hr = Tag('hr')
        self.br = Tag('br')
        self.prg = Tag('p')
        self.h1 = Tag('h1')
        self.body = Tag('body')
    def test_is_self_closing(self):
        self.assertTrue(self.img.is_self_closing())
        self.assertTrue(self.hr.is_self_closing())
        self.assertTrue(self.br.is_self_closing())
        self.assertFalse(self.h1.is_self_closing())
        self.assertFalse(self.prg.is_self_closing())
        self.assertFalse(self.body.is_self_closing())
    def test_add_attr(self):
        pass
    def test_str(self):
        pass
class TestDOM(unittest.TestCase):
    def test_default_init(self):
        dom = DOM()
        self.assertIsNone(dom.root)
        self.assertIsNone(dom.current_level)
    def test_init(self):
        pass
    def test_add_child(self):
        pass
    def test_close_child(self):
        pass
    def test_add_content(self):
        pass
    def test_add_text(self):
        pass
    def test_find_children_by_class(self):
        pass
    def test_find_child_by_id(self):
        pass
    def test_find_children_by_tag(self):
        pass
    def test_str_traverse(self):
        pass
    def test_str(self):
        pass
    def test_str_css(self):
        pass

    
