import sys
import os
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *

#Address bar for inserting a URI
#Back and forward buttons
#Bookmarking options
#Refresh and stop buttons for refreshing or stopping the loading of current documents
#Home button that takes you to your home page
#Among those are the address bar, status bar and tool bar
class Browser_Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        #color background white
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(palette)

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

    def center(self):
        geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        geometry.moveCenter(center_point)
        self.move(geometry.topLeft())

class Browser_Main_Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        #exitAction = QAction('Exit', '&Exit', self)
        #exitAction.setShortcut('Ctrl+Q')
        #exitAction.setStatusTip('Exit Application')
        #exitAction.triggered.connect(qApp.quit)
        icon_path =  os.path.join("baby_browser", "images", "favicon-tint.ico")
        self.setWindowIcon(QIcon(icon_path))

        #Tabs
        self.tabs = QTabWidget(self)
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()
        
        self.tabs.addTab(tab1, "Tab 1")
        self.tabs.addTab(tab2, "Tab 2")
        self.tabs.addTab(tab3, "Tab 3")

        self.setCentralWidget(self.tabs)

        #menubar = self.menuBar()
        #fileMenu = menubar.addMenu('File')
        #fileMenu.addAction(exitAction)


        #Add html widget
        self.htmlWidget = Browser_Widget()
        layout = QVBoxLayout() 
        layout.addWidget(self.htmlWidget)
        tab1.setLayout(layout)
        #self.setCentralWidget(self.htmlWidget)
        
        self.setGeometry(100, 100, 1200, 1200)
        self.setWindowTitle('Untitiled')
        self.show()
class Browser_GUI:
    def __init__(self, dom):
        self.app = QApplication(sys.argv)


        # Load the default fonts 
        font_path_regular =  os.path.join("baby_browser", "fonts", "raleway", "Raleway-Regular.ttf")
        font_path_bold =  os.path.join("baby_browser", "fonts", "raleway", "Raleway-Bold.ttf")
        font_path_italic =  os.path.join("baby_browser", "fonts", "raleway", "Raleway-Italic.ttf")
        font_db = QFontDatabase()
        font_db.addApplicationFont(font_path_regular)
        font_db.addApplicationFont(font_path_bold)
        font_db.addApplicationFont(font_path_italic)
        ttf_font = QFont("Raleway")
        #ttf_font.setItalic(True)
        #ttf_font.setBold(True)
        self.app.setFont(ttf_font)

        #self.widget = Browser_Widget()
        #self.widget.center()
        self.inside_body = False
        self.dom = dom
        self.widget = Browser_Main_Widget()
        self.render_dom()
        sys.exit(self.app.exec_())
    def render_dom(self):
       print(self.dom)
       self.inside_body = False
       self.traverse_dom(self.dom.root)
    def traverse_dom(self, root):
        for child in root.children:
            self.traverse_dom(child)
        if root.tag.lower()=="title":
            self.widget.setWindowTitle(root.content)
        if root.tag.lower()=="body": 
            self.inside_body = True
        if root.content and self.inside_body:
            text = QLabel()
            text.setText(root.content)
            htmlWidget = self.widget.htmlWidget.layout
            htmlWidget.addWidget(text)
            htmlWidget.addStretch()
            

        
if __name__=="__main__":
    from baby_browser.html_objects import *
    def create_dom():
        html = Tag("html", None)
        head = Tag("head", None)
        title = Tag("title", None)
        title.content = "My Title!"
        body = Tag("body", None)
        body.content = "Hello World"
        dom = DOM()
        dom.add_child(html)
        dom.add_child(head)
        dom.add_child(title)
        dom.close_child()#title
        dom.close_child()#head
        dom.add_child(body)
        dom.close_child()#body
        dom.close_child()#html
        return dom
    dom = create_dom()
    gui = Browser_GUI(dom)
