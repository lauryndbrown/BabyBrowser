class RenderObject:
    def __init__(self, boxstyle):
        self.box_style = boxstyle
class CSSUnit:
    PIXEL = "px"
    POINT = "pt"
    PERCENT = "%"
    TYPES = [PIXEL, POINT, PERCENT]
    def __init__(self, name):
        self.name = name
class Text:
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"
    JUSTIFY = "justify"
    ALIGNS = [CENTER, LEFT, RIGHT, JUSTIFY]
    NONE = "none"
    OVERLINE = "overline"
    LINE_THROUGH = "line-through"
    UNDERLINE = "underline"
    DECORATIONS = [NONE, OVERLINE, LINE_THROUGH, UNDERLINE]
    UPPERCASE = "uppercase"
    LOWERCASE = "lowercase"
    CAPITALIZE = "capitalize"
    TRANSFORMS = [UPPERCASE, LOWERCASE, CAPITALIZE] 
    def __init__(self, color=None, align=None, decoration=None, transform=None):
        self.color = color
        self.align = align
        self.decoration = decoration
        self.transform = transform
class Font:
    STYLE_NORMAL = "normal"
    STYLE_ITALIC = "italic"
    STYLES = [STYLE_NORMAL, STYLE_ITALIC]
    WEIGHT_NORMAL = "normal"
    WEIGHT_BOLD = "bold"
    FONT_WEIGHTS = [WEIGHT_NORMAL, WEIGHT_BOLD]
    def __init__(self, family=None, style=None, size=None, weight=None):
        self.family = family
        self.style = style
        self.size = size
        self.weight = weight
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
class BoxStyle:
    BLOCK = "block"
    INLINE = "inline"
    INLINE_BLOCK = "inline-block"
    NONE = "none"
    HIDDEN = "hidden"
    VISIBLE = "visible"
    def __init__(self, display):
        self.properties = {"display":display, "height":None, "width":None, "background-color":None, "color":None, "visibility":BoxStyle.VISIBLE, "min_height":None, "min_width":None, "max_height":None, "max_width":None}
        #self.margin = BoxStyleAttribute()
        #self.padding = BoxStyleAttribute()
        #self.border = Border()

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
