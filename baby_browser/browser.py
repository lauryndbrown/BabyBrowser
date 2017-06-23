from baby_browser.gui import * 
from baby_browser.html_tokenizer import * 
from baby_browser.networking import * 
class BabyBrowser:
    def __init__(self):
        self.html_tokenizer = Html_Tokenizer()
        self.gui = None
        self.networking = Network()
    def fetch_url(self, url):
        response = self.network_get(url)
        return self.tokenize_html(response)
    def network_get(self, url):
        return self.networking.get(url) 
    def tokenize_html(self, html):
        self.html_tokenizer.tokenize(html)
        return self.html_tokenizer.dom
    def show_gui(self, dom):
        self.gui = Browser_GUI(dom, self) 
if __name__=="__main__":
    browser = BabyBrowser()
    url = "https://lauryndbrown.github.io/BabyBrowser/baby_browser/Examples/helloWorld2.html"
    html = browser.network_get(url)
    #html  = "<html>\n<head><title>Website Title</title></head>\n<body>\nHi\n</body>\n</html>"
    dom = browser.tokenize_html(html)
    browser.show_gui(dom)
