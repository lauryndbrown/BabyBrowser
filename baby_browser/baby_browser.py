import pickle
import os

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

    def fetch_url(self, url, direction=None):
        response = self.network_get(url)
        return self.tokenize_html(response)

    def network_get(self, url):
        return self.networking.get(url) 

    def tokenize_html(self, html):
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
        self.gui = Browser_GUI(self) 

    def has_bookmark(self, url):
        for bookmark in self.bookmarks:
            if bookmark.url == url:
                return True
        return False

    def index_of_bookmark(self, url):
        for index in range(len(self.bookmarks)):
            if self.bookmarks[index].url == url:
                return index
        return None

    def add_bookmark(self, url, title=None, icon=None):
        if not self.has_bookmark(url):
            self.bookmarks.append(MenuWebPage(url, title))
            self.bookmarks_has_changed = True

    def remove_bookmark(self, url):
        if self.has_bookmark(url):
            index = self.index_of_bookmark(url)
            self.bookmarks.pop(index)
            self.bookmarks_has_changed = True

    def on_close(self):
        if self.bookmarks_has_changed:
            with open(BabyBrowser.BOOKMARK_FILE, 'wb') as bookmarks_file:
                pickle.dump(self.bookmarks, bookmarks_file, protocol=pickle.HIGHEST_PROTOCOL)

class MenuWebPage:

    def __init__(self, url, title=None, icon=None):
        self.url = url
        self.icon = icon
        self.title = title

    def __str__(self):
        return "Title:{} Url:{}".format(self.title, self.url)

    def __repr__(self):
        return str(self)


if __name__=="__main__":
    browser = BabyBrowser()
    #url = "https://lauryndbrown.github.io/BabyBrowser/baby_browser/Examples/helloWorld2.html"
    #html = browser.network_get(url)
    #html  = "<html>\n<head><title>Website Title</title></head>\n<body>\nHi\n</body>\n</html>"
    #dom = browser.tokenize_html(html)
    browser.show_gui()
