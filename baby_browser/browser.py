from baby_browser.gui import * 
from baby_browser.html_tokenizer import * 
from baby_browser.networking import * 
class BabyBrowser:
    BOOKMARK_FILE = os.path.join("baby_browser", "bookmarks.txt")
    def __init__(self):
        self.html_tokenizer = Html_Tokenizer()
        self.gui = None
        self.networking = Network()
        self.previous_pages = []
        self.forward_pages = []
        self.current_url = None
        bookmarks_file = open(BabyBrowser.BOOKMARK_FILE, 'r+')
        self.bookmarks = list(bookmarks_file)
    def fetch_url(self, url):
        response = self.network_get(url)
        if self.current_url and self.current_url!=url:
            self.previous_pages.append(self.current_url)
        self.current_url = response
        return self.tokenize_html(response)
    def network_get(self, url):
        return self.networking.get(url) 
    def tokenize_html(self, html):
        self.html_tokenizer.tokenize(html)
        return self.html_tokenizer.dom
    def show_gui(self, dom):
        self.gui = Browser_GUI(self) 
    def go_back(self):
        page_url = self.previous_pages.pop()
        self.forward_pages.append(page_url)
        return page_url
    def go_forward(self):
        page_url = self.forward_pages.pop()
        self.previous_pages.append(page_url)
        return page_url
    def add_bookmark(self, url):
        if url not in self.bookmarks:
            self.bookmarks.append(url)
    def remove_bookmark(self, url):
        if url in self.bookmarks:
            self.bookmarks.remove(url)
    

if __name__=="__main__":
    browser = BabyBrowser()
    url = "https://lauryndbrown.github.io/BabyBrowser/baby_browser/Examples/helloWorld2.html"
    html = browser.network_get(url)
    #html  = "<html>\n<head><title>Website Title</title></head>\n<body>\nHi\n</body>\n</html>"
    dom = browser.tokenize_html(html)
    browser.show_gui(dom)
