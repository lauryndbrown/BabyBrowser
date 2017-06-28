import re
from baby_browser.html_objects import * 
#Tokens
t_OPENTAG = re.compile("\s*<(?P<tag>\w+)\s*(?P<attrs>[^>]+)?>")
t_ATTRIBUTES = re.compile("(?P<attr_name>\w+)=\"(?P<attr_value>[^\"]+)\s*")
t_CLOSETAG = re.compile("</(\w+)>")
t_DATA = re.compile("[^<>]+")
t_WHITESPACE = re.compile("\s+")
#States
BEFORE_HTML = "before html"
BEFORE_HEAD = "before head"
IN_HEAD = "in head"
AFTER_HEAD = "after head"
IN_BODY = "in body"
AFTER_BODY = "after body"
AFTER_AFTER_BODY = "after after body"
#Special HTML Tags
BODY = "body"
HTML = "html"
HEAD = "head"
STYLE = "style"
class Html_Tokenizer:
    def handle_opentag(self, tag_str, attrs):
        #print("Found start tag:", tag, attrs)
        tag = Tag(tag_str)
        tag.parse_state = self.current_state 
        if attrs:
            self.p_opentag_attrs(tag, attrs)
        self.dom.add_child(tag) 
        if tag.is_self_closing:
            self.handle_closetag(tag)
    def handle_closetag(self, tag):
        #print("Found end tag:", tag)
        self.dom.close_child() 
    def handle_data(self, data):
        #print("Found data:", data)
        self.dom.add_content(data)
    def p_opentag(self, match):
        tag = match.group("tag")
        attrs = match.group("attrs")
        self.set_opentag_state(tag)
        return tag, attrs, len(match.group(0))
    def p_opentag_attrs(self, tag, attrs):
        for match in re.finditer(t_ATTRIBUTES, attrs):
            attr_name = match.group("attr_name")
            attr_value = match.group("attr_value")
            tag.add_attr(attr_name, attr_value)
    def set_opentag_state(self, tag):
        if tag.lower()==HTML:
            self.current_state = BEFORE_HEAD
        elif tag.lower()==HEAD:
            self.current_state = IN_HEAD
        elif tag.lower()==BODY:
            self.current_state = IN_BODY
    def p_closetag(self, match):
        tag = match.group(1)
        if tag.lower()==HTML:
            self.current_state = AFTER_AFTER_BODY
        elif tag.lower()==HEAD:
            self.current_state = AFTER_HEAD
        elif tag.lower()==BODY:
            self.current_state = AFTER_BODY
        return tag, None, len(tag)
    def tokenize(self, html):
        index = 0
        self.dom = DOM()
        self.current_state = BEFORE_HTML 
        while index<len(html):
            index = self.parse(html, index)
    def parse(self, html, index):
        add_to_index = 0
        opentag =  t_OPENTAG.match(html[index:])
        closetag =  t_CLOSETAG.match(html[index:])
        whitespace = t_WHITESPACE.match(html[index:])
        data = t_DATA.match(html[index:])
        if opentag:
            tag, attrs, tag_len = self.p_opentag(opentag)
            self.handle_opentag(tag, attrs)
            add_to_index = tag_len
        elif closetag:
            tag, attrs, tag_len = self.p_closetag(closetag)
            self.handle_closetag(tag)
            add_to_index = tag_len+2
        elif whitespace:
            add_to_index = len(whitespace.group(0))
        elif data:
            data_result = self.p_data(data.group(0))
            self.handle_data(data_result)
            add_to_index = len(data.group(0))
        else:
            add_to_index = 1
        return add_to_index+index
    def p_data(self, data):
        data = self.remove_excess_whitespace(data)
        return data
    def remove_excess_whitespace(self, data):
        #split the data and remove empty strings
        data = filter(lambda x: x, re.split("\s", data))
        return " ".join(data)

if __name__=="__main__":
    html_str = "<html>\n<head><title>Website Title</title></head>\n<body>\n<div id=\"bye\"class=\"hello world\">Hi</div>\n<img src=\"html5.gif\" alt=\"HTML5 Icon\" width=\"128\" height=\"128\">\n</body>\n</html>"
    tokenizer = Html_Tokenizer()
    tokenizer.tokenize(html_str) 
    print(tokenizer.dom)
