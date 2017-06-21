from baby_browser.gui import * 
from baby_browser.html_tokenizer import * 
from baby_browser.networking import * 
class BabyBrowser:
    def __init__(self):
        self.html_tokenizer = Html_Tokenizer()
        self.gui = None
        self.networking = None
    def network(self):
        return "<html>\n<head><title>Website Title</title></head>\n<body>\nHi\n</body>\n</html>"
    def tokenize_html(self, html):
        self.html_tokenizer.tokenize(html)
        return self.html_tokenizer.dom
    def show_gui(self, dom):
        self.gui = Browser_GUI(dom) 
if __name__=="__main__":
    browser = BabyBrowser()
    html = browser.network()
    dom = browser.tokenize_html(html)
    browser.show_gui(dom)
