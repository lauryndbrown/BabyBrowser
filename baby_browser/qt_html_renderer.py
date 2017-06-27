from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QT_HTML_Renderer:
    HEADERS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    def __init__(self):
        pass
    def set_page_title(self, title, page):
        page.setWindowTitle(title)
        page.title = title
