import unittest
from baby_browser.css import *

class TestRenderObject(unittest.TestCase):
    def test_init(self):
        render_object = RenderObject()
        self.assertIsNotNone(render_object.properties)
    def test_get_set_properties(self):
        css = RenderObject()
        css.properties = {1:None, 2:"Data", 3:None, 4:None, 5:"Data"}

        prop = css.get_set_properties()
        self.assertNotEqual(css.properties, prop)
        self.assertEqual({2:"Data", 5:"Data"}, prop)
    def test_cascade_properties(self):
        css1 = RenderObject()
        css1.properties = {1:None, 2:"Data", 3:None, 4:None, 5:"Data"}
        css2 = RenderObject()
        css2.properties = {1:"Data2", 2:None, 3:None, 4:None, 5:"Data2"}

        css1.cascade_properties(css2)
        self.assertEqual(css1.properties, {1:"Data2", 2:"Data", 3:None, 4:None, 5:"Data2"})

    def test_str(self):
        pass

class TestCSSUnit(unittest.TestCase):
    def setUp(self):
        self.pixel = CSSUnit(10, PIXEL)
        self.point = CSSUnit(22, POINT)
        self.percent = CSSUnit(50, PERCENT)
    def test_init(self):
        value = 33
        pixel = CSSUnit(value, PIXEL)
        self.assertEqual(pixel.unit, PIXEL)
        self.assertEqual(pixel.value, value)
    def test_str(self):
        pixel_str = "{}{}".format(self.pixel.value, self.pixel.unit)
        point_str = "{}{}".format(self.point.value, self.point.unit)
        percent_str = "{}{}".format(self.percent.value, self.percent.unit)
        self.assertEqual(str(self.pixel), pixel_str)
        self.assertEqual(str(self.point), point_str)
        self.assertEqual(str(self.percent), percent_str)
