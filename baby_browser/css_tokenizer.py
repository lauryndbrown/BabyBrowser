import re
from baby_browser.css_objects import *
#Tokens
t_RULE = re.compile("\s*(?P<selector>[#\.\w\-_]+)\s*\{\s*(?P<declarations>[^}]+)\}") #Groups the identifier and the css rules
t_DECLARATIONS = re.compile("(?P<property>[\w-]+):\s*(?P<value>[\w-]+);")
class CSS_Tokenizer:
    def __init__(self):
        pass
    def tokenize(self, css_str, dom):
        for css in re.finditer(t_RULE, css_str):
            self.parse(css, dom) 
    def parse(self, css, dom):
        print(css)
        if css:
            selector = css.group('selector')
            declarations = css.group('declarations')
            dom_element = dom.find_child_by_tag(selector)
            #print(css.group("selector"), css.group("declarations"), dom_element)

            if dom_element:
                render_object = RenderObject(BoxStyle(BoxStyle.BLOCK))
                print(dom_element.tag)
                for match in re.finditer(t_DECLARATIONS, declarations):
                    css_property =  match.group("property")
                    css_value =  match.group("value")
                    self.create_style(render_object, css_property, css_value)
                dom_element.css = render_object
    def create_style(self, render_object, css_property, css_value):
        if css_property in render_object.box_style.properties:
            print("   Adding:",css_property,css_value) 
            render_object.box_style.properties[css_property] = css_value
                    
        
    
        
if __name__=="__main__":
    from baby_browser.html_tokenizer import *
    html_str = "<html>\n<head><title>Website Title</title></head>\n<body>\n<h1>Hi</h1>\n</body>\n</html>"
    html_tokenizer = Html_Tokenizer()
    html_tokenizer.tokenize(html_str)
    print(html_tokenizer.dom)
    css_str = "body{background-color:red;color:white;}\nh1{background-color:white;}"
    css_tokenizer = CSS_Tokenizer()
    css_tokenizer.tokenize(css_str, html_tokenizer.dom)
