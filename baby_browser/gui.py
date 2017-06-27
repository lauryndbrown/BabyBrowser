import sys
import os
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from baby_browser.html_tokenizer import *
from baby_browser.qt_html_renderer import *
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
        icon_path =  os.path.join("baby_browser", "images", "favicon-tint.ico")
        self.setWindowIcon(QIcon(icon_path))


        #Tabs
        self.tabBar = QTabWidget()
        self.tabBar.tabCloseRequested.connect(self.removeTab)
        self.tabBar.setTabsClosable(True)
        self.tabBar.setMovable(True)
        self.setCentralWidget(self.tabBar)

        new_tab_button = QPushButton()
        tab_icon_path =  os.path.join("baby_browser", "images", "new folder black.png")
        new_tab_button.setToolTip('New Tab')
        new_tab_button.setIcon(QIcon(tab_icon_path))
        button_font = new_tab_button.font()
        button_font.setBold(True)
        new_tab_button.setIconSize(QSize(50, 50))
        self.tabBar.setCornerWidget(new_tab_button)
        new_tab_button.clicked.connect(self.addDefaultTab)


        #toolbar
        toolbar = self.addToolBar("Tool Bar")
        toolbar.setMovable(False)
        #Url Bar
        self.urlBar = QLineEdit()
        submit_button = QPushButton()
        submit_button.setIcon(QIcon(os.path.join("baby_browser", "images", "search.png")))
        submit_button.clicked.connect(self.fetch_url)
        submit_button.setToolTip('Sumbit Url')
        #Back/Forward Buttons
        back_button = QPushButton()
        back_button.setIcon(QIcon(os.path.join("baby_browser", "images", "back.png")))
        back_button.setToolTip('Back')
        back_button.clicked.connect(self.go_back)
        forward_button = QPushButton()
        forward_button.setIcon(QIcon(os.path.join("baby_browser", "images", "forward.png")))
        forward_button.setToolTip('Forward')
        forward_button.clicked.connect(self.go_forward)
        #Favorites Button
        self.favorite_button = QPushButton()
        self.fav_border_icon = QIcon(os.path.join("baby_browser", "images", "fav-border.png"))
        self.fav_full_icon = QIcon(os.path.join("baby_browser", "images", "fav-full.png"))
        
        self.favorite_button.setIcon(self.fav_border_icon)
        self.favorite_button.setToolTip('Bookmark')
        self.favorite_button.clicked.connect(self.toggle_bookmark)
        
        toolbar.addWidget(back_button)
        toolbar.addWidget(forward_button)
        toolbar.addSeparator()
        toolbar.addWidget(self.favorite_button)
        toolbar.addWidget(self.urlBar)
        toolbar.addSeparator()
        toolbar.addWidget(submit_button)

        self.addDefaultTab()
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
    def fetch_url(self, url=None):
        if not url:
            url = self.urlBar.text()
        print(url)
        if self.browser:
            if url in self.browser.bookmarks:
                self.favorite_button.setIcon(self.fav_fill_icon)
            else:
                self.favorite_button.setIcon(self.fav_border_icon)

            dom = self.browser.fetch_url(url)
            index = self.tabBar.currentIndex()
            self.removeTab(index, True)

            widget = Browser_Widget()
            Browser_GUI.render_dom(dom, widget)
            self.addTab(widget.title, widget)
            print("DONE------------------------")
            print("has title:", widget.title)
            print(dom)
    def go_back(self):
        if self.browser:
            url = self.browser.go_back()
            self.fetch_url(url)
    def go_forward(self):
        if self.browser:
            url = self.browser.go_forward()
            self.fetch_url(url)
    def toggle_bookmark(self):
        if self.browser.current_url in self.browser.bookmarks:
            self.add_bookmark()
        else:
            self.remove_bookmark()
    def add_bookmark(self):
        self.browser.add_bookmark(self.browser.current_url)
        self.favorite_button.setIcon(self.fav_fill_icon)
    def remove_bookmark(self):
        self.browser.remove_bookmark(self.browser.current_url)
        self.favorite_button.setIcon(self.fav_border_icon)
            
class Browser_GUI:
    HTML_RENDER = QT_HTML_Renderer()
    def __init__(self, browser=None):
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
        self.widget = Browser_Main_Widget(browser)
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
            Browser_GUI.HTML_RENDER.set_page_title(title, htmlWidget)
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
    gui = Browser_GUI()
