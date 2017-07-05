import os
import re
from baby_browser.css import *
#Tokens
t_CSS = re.compile("\s*(?P<selectors>[#\.\w\-\s,_]+)\s*\{\s*(?P<declarations>[^}]+)\}") #Groups the identifier and the css rules
t_DECLARATIONS = re.compile("(?P<property>[\w-]+):\s*(?P<value>[\w-]+);")
t_NUM_UNIT = re.compile("(?P<value>\d+)(?P<unit>pt|px)")
t_SELECTOR_GROUPS = re.compile("\s*(?P<selector>[#\.\w\-\s_]+)\s*")
t_SELECTOR = re.compile("\s*(?P<symbol>\.|#)?(?P<name>[\w-]+)\s*")
                
CLASS_SELECTOR = "."
ID_SELECTOR = "#"
TAG_SELECTOR = None
class CSSTokenizer:
    def __init__(self):
        pass
    def tokenize(self, css_str, dom):
        """Method that finds CSS code in given str and passes it to parse. 
        :param css_str: str containing css 
        :param dom: DOM object 
        :returns: None. Modifies the DOM. 
        """
        for css in re.finditer(t_CSS, css_str):
            selectors = css.group('selectors')
            declarations = css.group('declarations')

            render_object = self.__parse_css(declarations)
            self.__add_css(selectors, render_object, dom)

    def __parse_css(self, declarations):
        """Method that parses CSS and creates a RenderObject. 
        :param declarations:  str specifying css properties 
        :returns: RenderObject 
        """
        render_object = RenderObject()
        for match in re.finditer(t_DECLARATIONS, declarations):
            css_property =  match.group("property")
            css_value =  match.group("value")
            render_object.properties[css_property] = self.__parse_unit(css_value)
        return render_object
    def __add_css(self, selectors, render_object, dom):
        """Method that parses CSS selectors and adds CSS to dom elements.
        :param selectors: str representing the CSS selectors
        :param render_object: RenderObject representing css to add  
        :returns: None. Modifies RenderObjects in the DOM.
        """
        for match in re.finditer(t_SELECTOR_GROUPS, selectors):
            selected_html = self.__get_dom_elements(match.group("selector"), dom)
            for html_element in selected_html:
                html_element.css.cascade_properties(render_object)
    def __get_dom_elements(self, selector, dom):
        """Method that parses CSS Selectors and returns selected HTMLObjects. 
        :param selector: str representing css selectors for a style
        :param dom: DOM object 
        :returns: List of HTMLObjects
        """
        root = dom.root
        elements = None
        for match in re.finditer(t_SELECTOR, selector):
            symbol = match.group("symbol")
            name = match.group("name")
            if symbol==TAG_SELECTOR:
                elements = dom.find_children_by_tag(name, root)
            elif symbol==CLASS_SELECTOR:
                elements = dom.find_children_by_class(name, root)
            elif symbol==ID_SELECTOR:
                elements = dom.find_child_by_id(name, root)
            if not root:
                return None
        return elements

    def __parse_unit(self, css_value):
        """Method that parses CSS Units. 
        :param css_value: str representing a css property value 
        :returns: None. 
        """
        num_unit = re.match(t_NUM_UNIT, css_value)
        if num_unit:
            return CSSUnit(num_unit.group("value"), num_unit.group("unit")) 
        return css_value
                    
if __name__=="__main__":
    from baby_browser.html_tokenizer import *
   # html_str = "<html>\n<head><title>Website Title</title></head>\n<body>\n<h1 class=\"hello\">Hi</h1>\n<h2 class=\"hello goodbye\">Yah!</h2>\n</body>\n</html>"
    html_str = "<html>\n<head><title>Website Title</title></head>\n<body>\n<div id=\"bye\"class=\"hello world\">Hi</div>\n<img src=\"html5.gif\" alt=\"HTML5 Icon\" width=\"128\" height=\"128\">\n</body>\n</html>"
    #html_str = "".join(list(open(os.path.join("baby_browser", "Examples", "headers2.html"))))
    html_tokenizer = HtmlTokenizer()
    html_tokenizer.tokenize(html_str)
    print(html_tokenizer.dom)
    #css_str = "body{background-color:red;color:white;}\nh1{background-color:white;}\n.hello{color:yellow;}\n.goodbye{padding:4px;}"
    css_str = "".join(list(open(os.path.join("baby_browser", "browser.css"))))
    css_tokenizer = CSSTokenizer()
    css_tokenizer.tokenize(css_str, html_tokenizer.dom)
    print(html_tokenizer.dom.str_css())
