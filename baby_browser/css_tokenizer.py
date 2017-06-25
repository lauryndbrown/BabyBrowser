import re
from baby_browser.css_objects import *
#Tokens
#t_CSS_WHOLE = re.compile("\s*(?P<selector>[#\.\w\-_]+)\s*\{\s*(?P<declarations>(?P<property>[\w-]+):\s*(?P<value>[\w-]+);\s*)+\}\s*")
t_RULE = re.compile("\s*(?P<selector>[#\.\w\-_]+)\s*\{\s*(?P<declarations>[^}]+)\}") #Groups the identifier and the css rules
t_DECLARATIONS = re.compile("(?P<property>[\w-]+):\s*(?P<value>[\w-]+);")
#([\w-]+):\s*(\w+);
#Whole CSS expression
#\s*(\w+)\s*\{\s*(([\w-]+):\s*(\w+);)+\s*\}
class CSS_Tokenizer:
    def __init__(self):
        pass
    def tokenize(self, css_str, dom):
        index = 0
        while index<len(css_str):
            index = self.parse(css_str, dom, index) 
    def parse(self, css_str, dom, index):
        add_to_index = 0
        css = t_RULE.match(css_str[index:])
        print(css)
        if css:
            selector = css.group('selector')
            declarations = css.group('declarations')
            dom_element = dom.find_child_by_tag(selector)
            print(css.group("selector"))
            print(css.group("declarations"))
            if dom_element:
                render_obect = RenderObject(BoxStyle(BoxStyle.BLOCK))
                for match in re.finditer(t_DECLARATIONS, declarations):
                    css_property =  match.group("property")
                    css_value =  match.group("value")
                    print(css_property,css_value)
                    self.create_style(render_object, css_property, css_value)
    def create_style(self, render_object, css_property, css_value):
       if 
                    
        
    
        
if __name__=="__main__":
    from baby_browser.html_tokenizer import *
    html_str = "<html>\n<head><title>Website Title</title></head>\n<body>\nHi\n</body>\n</html>"
    html_tokenizer = Html_Tokenizer()
    html_tokenizer.tokenize(html_str)
    print(html_tokenizer.dom)
    print("Found: ", html_tokenizer.dom.find_child_by_tag("body"))
    css_str = "body{background-color:red;color:white;}"
    css_tokenizer = CSS_Tokenizer()
    css_tokenizer.tokenize(css_str, html_tokenizer.dom)
    print(css_tokenizer.render_tree)
