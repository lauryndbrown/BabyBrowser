import sys
import functools
import os
import posixpath

from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from baby_browser.tokenizer.html_tokenizer import *
from baby_browser.gui.qt_html_renderer import *

IMG_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
FONT_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts")
class Browser_Widget(QWidget):

    def __init__(self):
        super().__init__()
        self.__initUI()
        self.previous_pages = []
        self.forward_pages = []
        self.current_url = None
        self.title = None

    def __initUI(self):
        """Method that builds WebPage Tab UI. 
        :returns: None. 
        """
        self.widget = QWidget()

        #Scoll Area Properites
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        widget_layout = QVBoxLayout(self)
        widget_layout.setAlignment(Qt.AlignTop)
        self.widget.setLayout(widget_layout)
        scrollArea.setWidget(self.widget)

        #Scroll Area Layout
        scroll_layout = QVBoxLayout(self)
        scroll_layout.addWidget(scrollArea)
        self.setLayout(scroll_layout)
        scroll_layout.setSizeConstraint(QLayout.SetMinimumSize)
        scroll_layout.setAlignment(Qt.AlignTop)

    def go_back(self):
        """Method that manages data for back button.
        :returns: str representing previous URL visited. 
        """
        if not self.previous_pages:
            return None
        page_url = self.previous_pages.pop()
        self.forward_pages.append(self.current_url)
        return page_url

    def go_forward(self):
        """Method that manages data for forward button.
        :returns: str representing forward URL. 
        """
        if not self.forward_pages:
            return None
        page_url = self.forward_pages.pop()
        self.previous_pages.append(self.current_url)
        return page_url

class Browser_Main_Widget(QMainWindow):
    NEW_TAB_TITLE = "New Tab"
    def __init__(self, browser=None):
        super().__init__()
        self.browser = browser
        self.__initUI()
    
    def __initUI(self):
        """Method that builds browser user interface. 
        :returns: None. 
        """
        def createTabBar():
            """Method that creates TabBar 
            :returns: None. 
            """
            self.tabBar = QTabWidget()
            self.tabBar.tabCloseRequested.connect(self.removeTab)
            self.tabBar.currentChanged.connect(self.onTabChange)
            close_icon_path = os.path.join(IMG_PATH,"close.png")
            close_icon_path = reverse_slashes(close_icon_path)
            print(close_icon_path)
            self.setStyleSheet("QTabBar::close-button { image: url("+close_icon_path+"); }")
            self.tabBar.setTabsClosable(True)
            self.tabBar.setMovable(True)
            self.setCentralWidget(self.tabBar)
        def reverse_slashes(input_str):
            return "/".join(input_str.split("\\"))

        def createNewTabButton():
            """Method that creates New Tab Button on the TabBar 
            :returns: None. 
            """
            new_tab_button = QPushButton()
            tab_icon_path =  os.path.join(IMG_PATH, "new folder black.png")
            new_tab_button.setToolTip(self.NEW_TAB_TITLE)
            new_tab_button.setIcon(QIcon(tab_icon_path))
            button_font = new_tab_button.font()
            button_font.setBold(True)
            new_tab_button.setIconSize(QSize(50, 50))
            self.tabBar.setCornerWidget(new_tab_button)
            new_tab_button.clicked.connect(self.addDefaultTab)
            icon_path =  os.path.join(IMG_PATH, "crib_background.png")
            self.setWindowIcon(QIcon(icon_path))
            self.page_icon = QIcon(os.path.join(IMG_PATH,  "page.png"))
        
        def createURLBar():
            """Method that creates URL bar and submit button 
            :returns: QPushButton for URL bar submit button 
            """
            self.urlBar = QLineEdit()
            self.urlBar.returnPressed.connect(self.fetch_url)
            submit_button = QPushButton()
            submit_button.setIcon(QIcon(os.path.join(IMG_PATH, "search.png")))
            submit_button.clicked.connect(self.fetch_url)
            submit_button.setToolTip('Sumbit Url')
            return submit_button
       
        def createBackButton():
            """Method that creates back button for browser UI 
            :returns: QPushButton for back button
            """
            back_button = QPushButton()
            back_button.setIcon(QIcon(os.path.join(IMG_PATH, "back.png")))
            back_button.setToolTip('Back')
            back_button.clicked.connect(self.go_back)
            return back_button

        def createForwardButton():
            """Method that creates forward button for browser UI 
            :returns: QPushButton for forward button
            """
            forward_button = QPushButton()
            forward_button.setIcon(QIcon(os.path.join(IMG_PATH, "forward.png")))
            forward_button.setToolTip('Forward')
            forward_button.clicked.connect(self.go_forward)
            return forward_button

        def createFavButton():
            """Method that creates bookmark button for browser UI 
            :returns: None
            """
            self.favorite_button = QPushButton()
            self.fav_border_icon = QIcon(os.path.join(IMG_PATH, "fav-border.png"))
            self.fav_full_icon = QIcon(os.path.join(IMG_PATH,"fav-full.png"))
            self.favorite_button.setIcon(self.fav_border_icon)
            self.favorite_button.setToolTip('Bookmark')
            self.favorite_button.clicked.connect(self.toggle_bookmark)

        def createMenuBar():
            """Method that creates menu bar with bookmarks
            :returns: None
            """
            mainMenu = self.menuBar()
            self.favMenu = mainMenu.addMenu('Bookmarks')
            self.favMenu.setStyleSheet("QMenu { menu-scrollable: 1; }")
            for bookmark in self.browser.bookmarks:
                action = self.create_bookmark(bookmark.url, bookmark.title)
                action.triggered.connect(functools.partial(self.fetch_url, bookmark.url))
                self.favMenu.addAction(action)

        #Tabs
        createTabBar()
        createNewTabButton() 

        #status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        #toolbar
        toolbar = self.addToolBar("Tool Bar")
        toolbar.setMovable(False)

        #toolbar widgets
        submit_button = createURLBar()
        back_button = createBackButton()
        forward_button = createForwardButton()
        createFavButton()
        
        #Add Widgets to Toolbar
        toolbar.addWidget(back_button)
        toolbar.addWidget(forward_button)
        toolbar.addSeparator()
        toolbar.addWidget(self.favorite_button)
        toolbar.addWidget(self.urlBar)
        toolbar.addSeparator()
        toolbar.addWidget(submit_button)
        
        #MenuBar
        createMenuBar()

        #Set Addtional Defaults
        self.addDefaultTab()
        self.setGeometry(100, 100, 1200, 1200)
        self.setWindowTitle('BabyBrowser')
       
    def onTabChange(self, index):
        url = self.getCurrentTab().current_url
        self.updateBookmark(url)
        self.urlBar.setText(url)
        
    def removeTab(self, index):
        """Method removes tab at index. Adds Default Tab if last tab is removed. 
        :param index: int representing tab to be removed 
        :returns: None. 
        """
        if self.tabBar.count()==1:
            self.addDefaultTab()
        widget = self.tabBar.widget(index)
        widget.deleteLater()
        self.tabBar.removeTab(index)
    
    def addDefaultTab(self):
        """Method adds empty tab. 
        :returns: None. 
        """
        self.addTab(self.NEW_TAB_TITLE, Browser_Widget())
    
    def addTab(self, tabName, widget):
        """Method adds tab to browser. 
        :param tabName: str representing title of webpage 
        :param widget: QWidget representing the webpage 
        :returns: None. 
        """
        self.tabBar.addTab(widget, tabName)
        self.tabBar.setCurrentWidget(widget)
        index = self.tabBar.currentIndex()
        self.tabBar.setTabIcon(index, self.page_icon)
    
    def getCurrentTab(self):
        """Method gets current active tab. 
        :returns: Browser_Widget in the current Tab. 
        """
        index = self.tabBar.currentIndex()
        return self.tabBar.widget(index)
        
    def fetch_url(self, url=None, backwards=None):
        """Method gets webpage and adds it to current tab 
        :param url: str representing url of webpage 
        :param backwards: boolean representing if the method has been called by the go_back 
        :returns: None. 
        """
        if not url:
            url = self.urlBar.text()
        else:
            print("URL:", url)
            self.urlBar.setText(url)

        self.updateBookmark(url)
        self.statusBar.showMessage("Fetching Url")

        tabWidget = self.getCurrentTab()
        
        dom = self.browser.fetch_url(url)

        if not dom:
            self.statusBar.showMessage("")
            return

        if not backwards and tabWidget.current_url and tabWidget.current_url!=url:
            tabWidget.previous_pages.append(tabWidget.current_url)

        tabWidget.current_url = url
        self.statusBar.showMessage("Rendering Webpage")
        self.clear_tab(tabWidget.widget)
        Browser_GUI.render_dom(dom, tabWidget)
        self.setCurrentTitle(tabWidget.title)
        self.statusBar.showMessage("")

    def updateBookmark(self, url): 
        if self.browser.has_bookmark(url):
            self.favorite_button.setIcon(self.fav_full_icon)
        else:
            self.favorite_button.setIcon(self.fav_border_icon)
    def setCurrentTitle(self, title):
        """Method sets title of the current tab 
        :param title: str representing title of webpage 
        :returns: None. 
        """
        tab_index = self.tabBar.currentIndex()
        self.tabBar.setTabText(tab_index, title)
        
    def clear_tab(self, tab):
        """Method clears widgets in the current tab 
        :param tab: Browser_Widget representing webpage 
        :returns: None. 
        """
        layout = tab.layout()
        for i in range(layout.count()): 
            layout.itemAt(i).widget().close()

    def go_back(self):
        """Method called when back button is pressed. Fetches URL. 
        :returns: None. 
        """
        widget = self.getCurrentTab()
        url = widget.go_back()
        if url:
            self.fetch_url(url, True)
    
    def go_forward(self):
        """Method called when forward button is pressed. Fetches URL. 
        :returns: None. 
        """
        widget = self.getCurrentTab()
        url = widget.go_forward()
        if url:
            self.fetch_url(url)
    
    def toggle_bookmark(self):
        """Method called when bookmark button is pressed. Adds/Removes bookmarks of url. 
        :returns: None. 
        """
        widget = self.getCurrentTab()
        if not self.browser.has_bookmark(widget.current_url):
            self.add_bookmark()
        else:
            self.remove_bookmark()
    
    def add_bookmark(self):
        """Method called by toggle_bookmark. Add bookmark of url. 
        :returns: None. 
        """
        tab_index = self.tabBar.currentIndex()
        tab = self.tabBar.widget(tab_index)
        url = tab.current_url

        title = self.tabBar.tabText(tab_index)
        self.browser.add_bookmark(url, title)
        self.favorite_button.setIcon(self.fav_full_icon)
        action = self.create_bookmark(url, title)
        action.triggered.connect(lambda: self.fetch_url(url))
        self.favMenu.addAction(action)
    
    def create_bookmark(self, url, title=None, icon=None):
        """Method called by add_bookmark. Add bookmark of url. 
        :param url: str representing webpage URL 
        :param title: str representing webpage title 
        :param icon: QIcon representing webpage favicon 
        :returns: QAction for bookmark menu
        """
        if title:
            action = QAction(title, self)
            action.setStatusTip(title+"\n"+url)
        else:
            action = QAction(url, self)
            action.setStatusTip(url)
        if icon:
            action.setIcon(icon)
        else:
            action.setIcon(self.page_icon)
        return action

    def remove_bookmark(self):
        """Method called by toggle_bookmark. Removes bookmark of url. 
        :returns: None
        """
        tab_index = self.tabBar.currentIndex()
        tab = self.tabBar.widget(tab_index)

        url = tab.current_url
        title = self.tabBar.tabText(tab_index)

        self.browser.remove_bookmark(url)
        self.favorite_button.setIcon(self.fav_border_icon)

        for action in self.favMenu.actions():
            if action.text()==url or action.text()==title:
                self.favMenu.removeAction(action)
                break

    def closeEvent(self, event):
        """Method called on program exit.
        :param event: event representing program close 
        :returns: None
        """
        self.browser.on_close()

            
class Browser_GUI:
    
    HTML_RENDER = QT_HTML_Renderer()
    
    def __init__(self, browser=None):
        self.app = QApplication(sys.argv)
        self.browser = browser
        # Load the default fonts 
        #ttf_font.setItalic(True)
        #ttf_font.setBold(True)

        self.__initUI()

        self.widget = Browser_Main_Widget(browser)
        self.widget.show()
        sys.exit(self.app.exec_())

    def __initUI(self):
        self.font_db = QFontDatabase()
        
        self.add_font(os.path.join("raleway", "Raleway-Regular.ttf"))
        self.add_font(os.path.join("raleway", "Raleway-Bold.ttf"))
        self.add_font(os.path.join("raleway", "Raleway-Italic.ttf"))

        self.app.setFont(QFont("Raleway"))

    def add_font(self, font_path):
        """Method that adds font to application
        :param font_path: str representing relative path to font  
        :returns: None
        """
        font_path =  os.path.join(FONT_PATH, font_path)
        self.font_db.addApplicationFont(font_path)

    def render_dom(dom, htmlWidget):
        """Method that renders DOM object in the given widget.
        :param htmlWidget: Browser_Widget representing webpage 
        :returns: None
        """
        Browser_GUI.HTML_RENDER.render_dom(dom.root, htmlWidget, htmlWidget.widget.layout())
