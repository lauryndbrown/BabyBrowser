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

        self.title = None
        #self.layout = QVBoxLayout(self)
        #self.setLayout(self.layout)

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
    def move_new_tab_button(self):
        size = sum([self.tabBar.tabRect(i).width() for i in range(self.tabBar.count())])
        height = self.tabBar.geometry().top()
        width = self.width()
        print("Size:", size)
        if size > width:
            self.new_tab_button.move(width-54, height)
        else:
            self.new_tab_button.move(size, height)
    def removeTab(self, index):
        if self.tabBar.count()==1:
            self.addDefaultTab()
        widget = self.tabBar.widget(index)
        widget.deleteLater()
        self.tabBar.removeTab(index)
    def addDefaultTab(self):
        self.addTab("New Tab", Browser_Widget())
    def addTab(self, tabName, widget):
        self.tabBar.addTab(widget, tabName)
    def fetch_url(self):
        print(self.urlBar.text())

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
        htmlWidget = Browser_Widget()
        self.render_dom(self.dom, htmlWidget)
        if htmlWidget.title:
            self.widget.addTab(htmlWidget.title, htmlWidget)
        else:
            self.widget.addTab("         ", htmlWidget)
        self.widget.show()
        sys.exit(self.app.exec_())
    def render_dom(self, dom, htmlWidget):
        print(dom)
        inside_body = False
        layout = QGridLayout()
        self.traverse_dom(dom.root, htmlWidget, layout, inside_body)
    def traverse_dom(self, root, htmlWidget, layout, inside_body):
        for child in root.children:
            self.traverse_dom(child, htmlWidget, layout, inside_body)
        if root.tag.lower()=="title":
            htmlWidget.setWindowTitle(root.content)
            htmlWidget.title = root.content
        if root.tag.lower()=="body": 
            inside_body = True
        if root.content and inside_body:
            text = QLabel(root.content, htmlWidget)
            
            #text.setText(root.content)
            #layout.addWidget(text, 0, 0, -1, 1)

            

        
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
