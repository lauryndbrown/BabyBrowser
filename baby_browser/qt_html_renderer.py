from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from baby_browser.css_objects import *
from baby_browser.networking import *

class QT_HTML_Renderer:
    HEADERS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    IMG = "img"
    HR = 'hr'
    def __init__(self):
        pass
    def set_page_title(self, title, page):
        page.setWindowTitle(title)
        page.title = title
    def render_body(self, element, htmlWidget):
        widget = htmlWidget.widget
        self.render_box_styles(element, widget)
    def render_in_body_content(self, element, layout):
        widget = self.render_tag(element)
        layout.addWidget(widget)
    def render_tag(self, element):
        tag = element.tag.lower()
        widget = None
        if tag in QT_HTML_Renderer.HEADERS:
            widget = self.render_text(tag, element)
        if tag==QT_HTML_Renderer.IMG:
            widget = self.render_img(element)
        if tag==QT_HTML_Renderer.HR:
            widget = self.render_hr(element)
        else:
            widget =  self.render_text(tag, element)
        self.render_box_styles(element, widget)
        return widget
    def render_hr(self, element):
        hr = QFrame()
        hr.setFrameStyle(QFrame.HLine)
        return hr
    def render_img(self, element):
        element.content = Network.get_image(element.attrs["src"])
        image = QImage()
        image.loadFromData(element.content)
        label = QLabel()
        label.setPixmap(QPixmap(image))
        return label 

    def render_box_styles(self, element, widget):
        css = element.css
        box_style = []
        if css:
            prop_dict = css.box_style.get_set_properties()
            for key in prop_dict:
                if key==BoxStyle.p_BACKGROUND_COLOR:
                    color = prop_dict[key]
                    box_style.append(self.setBackgroundColor(widget, color))
                if key==BoxStyle.p_COLOR:
                    color = prop_dict[key]
                    box_style.append(self.setColor(widget, color))
            if box_style:
                widget.setStyleSheet("".join(box_style))
    def setBackgroundColor(self, widget, color):
        return "background-color:"+color+";"
    def setColor(self, widget, color):
        return "color:"+color+";"
    def render_text(self, tag, element):
        text = QLabel(element.content)
        text.setWordWrap(True)
        text.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum);
        css = element.css
        if css:
            prop_dict = css.get_set_properties()
            font = QFont()
            for key in prop_dict:
                if key == Font.p_FONT_WEIGHT:
                    weight = prop_dict[key]
                    self.set_font_weight(font, weight)
                if key == Font.p_FONT_SIZE:
                    size = prop_dict[key]
                    self.set_font_point_size(font, size)
            text.setFont(font)
        return text

    def set_font_weight(self, font, weight):
        if weight==Font.FONT_WEIGHT_BOLD:
            font.setBold(True)
        elif weight==Font.FONT_WEIGHT_NORMAL:
            fold.setBold(False)
    def set_font_point_size(self, font, size):
        font.setPointSize(size.value)

        

            


       # font = QFont("Raleway")
