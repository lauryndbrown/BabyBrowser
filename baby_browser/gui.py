import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from baby_browser.html_objects import *
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
        
        #Add Test Button
        self.layout = QVBoxLayout(self)
        #self.button = QPushButton("Button")
        #self.layout.addWidget(self.button)
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

        self.statusBar()
        #menubar = self.menuBar()
        #fileMenu = menubar.addMenu('File')
        #fileMenu.addAction(exitAction)


        #Add html widget
        self.htmlWidget = Browser_Widget()
        self.setCentralWidget(self.htmlWidget)

        self.setGeometry(100, 100, 1200, 1200)
        self.setWindowTitle('Menubar')
        self.show()
class Browser_GUI:
    def __init__(self, dom):
        self.app = QApplication(sys.argv)
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
if __name__=="__main__":
    dom = create_dom()
    gui = Browser_GUI(dom)
