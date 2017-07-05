import unittest
from baby_browser.css_objects import *

class TestRenderObject(unittest.TestCase):
    def test_init(self):
        render_object = RenderObject()
        self.assertIsNotNone(render_object.box_style)
        self.assertIsNotNone(render_object.font)
        self.assertIsNotNone(render_object.properties)
        self.assertEqual(render_object.properties[RenderObject.BOX_STYLE], render_object.box_style)
        self.assertEqual(render_object.properties[RenderObject.FONT], render_object.font)
    def test_str(self):
        pass

class TestCSSUnit(unittest.TestCase):
    def setUp(self):
        self.pixel = CSSUnit(10, CSSUnit.PIXEL)
        self.point = CSSUnit(22, CSSUnit.POINT)
        self.percent = CSSUnit(50, CSSUnit.PERCENT)
    def test_init(self):
        value = 33
        pixel = CSSUnit(value, CSSUnit.PIXEL)
        self.assertEqual(pixel.unit, CSSUnit.PIXEL)
        self.assertEqual(pixel.value, value)
    def test_str(self):
        pixel_str = "{}{}".format(self.pixel.value, self.pixel.unit)
        point_str = "{}{}".format(self.point.value, self.point.unit)
        percent_str = "{}{}".format(self.percent.value, self.percent.unit)
        self.assertEqual(str(self.pixel), pixel_str)
        self.assertEqual(str(self.point), point_str)
        self.assertEqual(str(self.percent), percent_str)

class TestCSS_Style(unittest.TestCase):
    def test_init(self):
        css = CSS_Style()
        self.assertIsNone(css.properties)
    def test_get_set_properties(self):
        css = CSS_Style()
        css.properties = {1:None, 2:"Data", 3:None, 4:None, 5:"Data"}

        prop = css.get_set_properties()
        self.assertNotEqual(css.properties, prop)
        self.assertEqual({2:"Data", 5:"Data"}, prop)
    def test_str(self):
        css = CSS_Style()
        css.properties = {1:None, 2:"Data", 3:None, 4:None, 5:"Data"}

        prop = css.get_set_properties()
        self.assertEqual(str(css), str(prop))
class TestFont(unittest.TestCase):
    def test_init(self):
        font = Font()
        self.assertNotNone(font.properties)
        self.assertIn(Font.p_FONT_FAMILY)
        self.assertIn(Font.p_FONT_STYLE)
        self.assertIn(Font.p_FONT_SIZE)
        self.assertIn(Font.p_FONT_WEIGHT)
        
class TestFont(unittest.TestCase):
    def test_init(self):
        boxstyle = BoxStyle(BoxStyle.BLOCK)
        self.assertIsNotNone(boxstyle.properties)
        self.assertEqual(boxstyle.properties[BoxStyle.p_DISPLAY], BoxStyle.BLOCK)
        self.assertIn(boxstyle.p_HEIGHT, boxstyle.properties)
        self.assertIn(boxstyle.p_WIDTH, boxstyle.properties)
        self.assertIn(boxstyle.p_BACKGROUND_COLOR, boxstyle.properties)
        self.assertIn(boxstyle.p_COLOR, boxstyle.properties)
        self.assertIn(boxstyle.p_VISIBILITY, boxstyle.properties)
        self.assertIn(boxstyle.p_MIN_HEIGHT, boxstyle.properties)
        self.assertIn(boxstyle.p_MIN_WIDTH, boxstyle.properties)
        self.assertIn(boxstyle.p_MAX_HEIGHT, boxstyle.properties)
        self.assertIn(boxstyle.p_MAX_WIDTH, boxstyle.properties)
        
