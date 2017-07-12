import pickle
import os

from baby_browser.menu_objects import MenuWebPage 
from baby_browser.gui.gui import * 
from baby_browser.tokenizer.html_tokenizer import * 
from baby_browser.tokenizer.css_tokenizer import * 
from baby_browser.utility.networking import * 


class BabyBrowser:

    BOOKMARK_FILE = os.path.join("baby_browser","utility", "bookmarks.txt")
    DEFAULT_CSS = os.path.join("baby_browser", "assets", "css", "browser.css")

    def __init__(self):
        self.html_tokenizer = HtmlTokenizer()
        self.css_tokenizer = CSSTokenizer()
        self.gui = None
        self.networking = Network()
        self.bookmarks_has_changed = False
        if os.stat(BabyBrowser.BOOKMARK_FILE).st_size!=0:
            with open(BabyBrowser.BOOKMARK_FILE, 'rb') as bookmarks_file:
                self.bookmarks = pickle.load(bookmarks_file)
        else:
            self.bookmarks = []
        with open(BabyBrowser.DEFAULT_CSS, 'r') as default_css:
            self.default_css = "".join(list(default_css))

    def fetch_url(self, url):
        """Method that GETs a url and tokenizes the response
        :param url: str containing the url to GET 
        :returns: resulting DOM Object 
        """
        try:
            response = self.network_get(url)
            return self.tokenize_html(response)
        except:
            return None

    def network_get(self, url):
        """Method that GETs a url and tokenizes the response
        :param url: str containing the url to GET 
        :returns: str containing the request reponse 
        """
        try:
            return self.networking.get(url) 
        except:
            return None

    def tokenize_html(self, html):
        """Method that converts an HTML str and to a DOM object
        :param html: str containing HTML markup 
        :returns: DOM object 
        """
        self.html_tokenizer.tokenize(html)
        dom = self.html_tokenizer.dom
        #Default Browser Styles
        self.css_tokenizer.tokenize(self.default_css, dom) 
        #Style in Head
        style_elements = dom.find_children_by_tag("style")
        for element in style_elements:
            self.css_tokenizer.tokenize(element.content, dom) 
        print(dom)
        return dom

    def show_gui(self):
        """Method that creates and shows the Browser UI
        :returns: None. 
        """
        self.gui = Browser_GUI(self) 

    def has_bookmark(self, url):
        """Method that checks if a url has been bookmarked
        :param url: str containing webpage url 
        :returns: boolean representing if bookmark exists
        """
        for bookmark in self.bookmarks:
            if bookmark.url == url:
                return True
        return False

    def index_of_bookmark(self, url):
        """Method that returns the index of a url that has been bookmarked
        :param url: str containing webpage url 
        :returns: int representing the index of the given url; None if bookmark doesn't exist
        """
        for index in range(len(self.bookmarks)):
            if self.bookmarks[index].url == url:
                return index
        return None

    def add_bookmark(self, url, title=None, icon=None):
        """Method that adds a url to bookmarked list
        :param url: str containing webpage url 
        :param title: str containing webpage title 
        :param icon: QIcon containing webpage icon 
        :returns: None.
        """
        if not self.has_bookmark(url):
            self.bookmarks.append(MenuWebPage(url, title))
            self.bookmarks_has_changed = True

    def remove_bookmark(self, url):
        """Method that removes a url from the bookmarked list
        :param url: str containing webpage url 
        :returns: None.
        """
        if self.has_bookmark(url):
            index = self.index_of_bookmark(url)
            self.bookmarks.pop(index)
            self.bookmarks_has_changed = True

    def on_close(self):
        """Method called prior to program end. Stores changes to bookmark list.
        :returns: None.
        """
        if self.bookmarks_has_changed:
            with open(BabyBrowser.BOOKMARK_FILE, 'wb') as bookmarks_file:
                pickle.dump(self.bookmarks, bookmarks_file, protocol=pickle.HIGHEST_PROTOCOL)
        
def start():
    browser = BabyBrowser()
    browser.show_gui()
if __name__=="__main__":
    start()
