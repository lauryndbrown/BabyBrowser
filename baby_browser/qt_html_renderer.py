from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QT_HTML_Renderer:
    def __init__(self):
        pass
    def set_page_title(self, title, page):
        page.setWindowTitle(title)
        page.title = title
