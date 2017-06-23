import sys
import os
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from baby_browser.html_tokenizer import *
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

        self.title = None
        #self.layout = QVBoxLayout(self)
        #self.setLayout(self.layout)

    def center(self):
        geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        geometry.moveCenter(center_point)
        self.move(geometry.topLeft())

class Browser_Main_Widget(QMainWindow):
    def __init__(self, browser=None):
        super().__init__()
        self.initUI()
        self.browser = browser
    def initUI(self):
        #exitAction = QAction('Exit', '&Exit', self)
        #exitAction.setShortcut('Ctrl+Q')
        #exitAction.setStatusTip('Exit Application')
        #exitAction.triggered.connect(qApp.quit)
        icon_path =  os.path.join("baby_browser", "images", "favicon-tint.ico")
        self.setWindowIcon(QIcon(icon_path))


        #Tabs
        self.tabBar = QTabWidget()
        self.tabBar.tabCloseRequested.connect(self.removeTab)
        self.tabBar.setTabsClosable(True)
        self.tabBar.setMovable(True)
        self.setCentralWidget(self.tabBar)

        self.new_tab_button = QPushButton()
        tab_icon_path =  os.path.join("baby_browser", "images", "new folder black.png")
        self.new_tab_button.setIcon(QIcon(tab_icon_path))
        button_font = self.new_tab_button.font()
        button_font.setBold(True)
       # self.new_tab_button.setFixedSize(50,40)
        self.new_tab_button.setIconSize(QSize(50, 50))
        self.tabBar.setCornerWidget(self.new_tab_button)
        self.new_tab_button.clicked.connect(self.addDefaultTab)


        #toolbar
        toolbar = self.addToolBar("Tool Bar")
        toolbar.setMovable(False)
        #Url Bar
        self.urlBar = QLineEdit()
        url_submit = QPushButton("Submit")
        url_submit.clicked.connect(self.fetch_url)
        toolbar.addWidget(self.urlBar)
        toolbar.addSeparator()
        toolbar.addWidget(url_submit)
        #toolbar.addWidget(urlBar)
        #menubar = self.menuBar()
        #fileMenu = menubar.addMenu('File')
        #fileMenu.addAction(exitAction)


        #Add html widget
        #layout = QVBoxLayout() 
        #layout.addWidget(self.htmlWidget)
        #tab1.setLayout(layout)
        #self.setCentralWidget(self.htmlWidget)
        self.setGeometry(100, 100, 1200, 1200)
        self.setWindowTitle('BabyBrowser')
    def removeTab(self, index, no_add=False):
        if self.tabBar.count()==1 and not no_add:
            self.addDefaultTab()
        widget = self.tabBar.widget(index)
        widget.deleteLater()
        self.tabBar.removeTab(index)
    def addDefaultTab(self):
        self.addTab("New Tab", Browser_Widget())
    def addTab(self, tabName, widget):
        self.tabBar.addTab(widget, tabName)
        self.tabBar.setCurrentWidget(widget)
    def fetch_url(self):
        url = self.urlBar.text()
        print(url)
        if self.browser:
            dom = self.browser.fetch_url(url)
            index = self.tabBar.currentIndex()
            self.removeTab(index, True)

            widget = Browser_Widget()
            Browser_GUI.render_dom(dom, widget)
            self.addTab(widget.title, widget)
            print("DONE------------------------")
            print("has title:", widget.title)
            print(dom)
class Browser_GUI:
    def __init__(self, dom, browser=None):
        self.app = QApplication(sys.argv)
        self.browser = browser
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
        self.widget = Browser_Main_Widget(browser)
        htmlWidget = Browser_Widget()
        Browser_GUI.render_dom(self.dom, htmlWidget)
        if htmlWidget.title:
            self.widget.addTab(htmlWidget.title, htmlWidget)
        else:
            self.widget.addTab("         ", htmlWidget)
        self.widget.show()
        sys.exit(self.app.exec_())
    def render_dom(dom, htmlWidget):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        htmlWidget.setLayout(layout)
        Browser_GUI.traverse_dom(dom.root, htmlWidget, layout)
    def traverse_dom(root, htmlWidget, layout):
        for child in root.children:
            Browser_GUI.traverse_dom(child, htmlWidget, layout)
        if root.tag.lower()=="title":
            title = root.content.rstrip()
            htmlWidget.setWindowTitle(title)
            htmlWidget.title = title
        if root.parse_state==IN_BODY:
            tag = root.tag.lower()
            content = root.content
            if tag=="h1":
                text = QLabel(content)
                font = QFont("Raleway")
                font.setPointSize(36)
                font.setBold(True)
                text.setFont(font)
                layout.addWidget(text)
            elif content:
                text = QLabel(root.content)
                layout.addWidget(text)
            

        
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
