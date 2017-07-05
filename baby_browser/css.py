from collections import namedtuple
#Property Names
#  Font Property Names
p_FONT_FAMILY = "font-family"
p_FONT_STYLE = "font-style"
p_FONT_SIZE = "font-size"
p_FONT_WEIGHT = "font-weight"
#  BoxStyle Property Names
p_BACKGROUND_COLOR = "background-color"
p_COLOR = "color"
p_WIDTH = "width"
p_HEIGHT = "height"
p_DISPLAY = "display"
p_VISIBILITY = "visibility"
p_MAX_WIDTH = "max_width"
p_MAX_HEIGHT = "max_height"
p_MIN_WIDTH = "min_width"
p_MIN_HEIGHT = "min_height"
#  Text Property Names
p_COLOR = "color"
p_ALIGN = "text-align"
p_DECORATION = "decoration"
p_TRANSFORM = "text-transform"

#Text Constants
TEXT_ALIGN_CENTER = "center"
TEXT_ALIGN_LEFT = "left"
TEXT_ALIGN_RIGHT = "right"
TEXT_ALIGN_JUSTIFY = "justify"
TEXT_ALIGNS = [TEXT_ALIGN_CENTER, TEXT_ALIGN_LEFT, TEXT_ALIGN_RIGHT, TEXT_ALIGN_JUSTIFY]
TEXT_DECORATION_NONE = "none"
TEXT_DECORATION_OVERLINE = "overline"
TEXT_DECORATION_LINE_THROUGH = "line-through"
TEXT_DECORATION_UNDERLINE = "underline"
TEXT_DECORATIONS = [TEXT_DECORATION_NONE, TEXT_DECORATION_OVERLINE, TEXT_DECORATION_LINE_THROUGH, TEXT_DECORATION_UNDERLINE]
UPPERCASE = "uppercase"
LOWERCASE = "lowercase"
CAPITALIZE = "capitalize"
TEXT_TRANSFORMS = [UPPERCASE, LOWERCASE, CAPITALIZE] 

#Font Constants
FONT_STYLE_NORMAL = "normal"
FONT_STYLE_ITALIC = "italic"
FONT_STYLES = [FONT_STYLE_NORMAL, FONT_STYLE_ITALIC]
FONT_WEIGHT_NORMAL = "normal"
FONT_WEIGHT_BOLD = "bold"
FONT_WEIGHTS = [FONT_WEIGHT_NORMAL, FONT_WEIGHT_BOLD]

#Display Constants
DISPLAY_BLOCK = "block"
DISPLAY_INLINE = "inline"
DISPLAY_INLINE_BLOCK = "inline-block"
DISPLAY_NONE = "none"
HIDDEN = "hidden"
VISIBLE = "visible"

#Unit Constants
PIXEL = "px"
POINT = "pt"
PERCENT = "%"
UNITS = [PIXEL, POINT, PERCENT]

class RenderObject:
    def __init__(self):
        self.properties = {
        p_FONT_FAMILY:None,p_FONT_STYLE:None,p_FONT_SIZE:None,p_FONT_WEIGHT:None,
        p_DISPLAY:DISPLAY_BLOCK,p_HEIGHT:None,p_WIDTH:None,  
        p_BACKGROUND_COLOR:None,p_COLOR:None,p_VISIBILITY:VISIBLE,  
        p_MIN_HEIGHT:None,p_MIN_WIDTH:None,p_MAX_HEIGHT:None,p_MAX_WIDTH:None,
        p_COLOR:None,p_ALIGN:None,p_DECORATION:None,p_TRANSFORM:None
                        }
    def get_set_properties(self):
        return {key:value for (key,value) in self.properties.items() if value}
    def cascade_properties(self, render_object):
        new_props = render_object.get_set_properties()
        for key in new_props:
            self.properties[key] = new_props[key]
    def __str__(self):
        return str(self.get_set_properties())
    def __repr__(self):
        return str(self)
class CSSUnit:
    def __init__(self, value, unit):
        self.unit = unit
        self.value = int(value)
    def __str__(self):
        return "{}{}".format(self.value, self.unit)
    def __repr__(self):
        return str(self)
class BoxStyleAttribute:
    def __init__(self, top=None, right=None, bottom=None, left=None):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left
class Border:
    def __init__(self, top_border=None, right_border=None, bottom_border=None, left_border=None):
        self.style_top = top_border
        self.style_right = right_border
        self.style_bottom = bottom_border
        self.style_left = left_border
class BorderStyle(BoxStyleAttribute):
    def __init__(self, top=None, right=None, bottom=None, left=None, style=None, color=None):
        super().__init__(top, right, bottom, left)
        self.style = style
        self.color = color
class Position:
    STATIC = "static"
    RELATIVE = "relative"
    FIXED = "fixed"
    ABSOLUTE = "absolute"
    TYPES = [STATIC, RELATIVE, FIXED, ABSOLUTE]
    def __init__(self, position, top=None, right=None, left=None, bottom=None):
        if position in Position.TYPES:
            self.position = position
        else:
            self.position = None
        self.top = top
        self.right = right
        self.left = left
        self.bottom = bottom
