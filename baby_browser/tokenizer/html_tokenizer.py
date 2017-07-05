import re
from baby_browser.tokenizer.html_objects import * 
import logging, sys
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
class HtmlTokenizer:
    """
    Takes a string containing HTML and converts it to a DOM
    """
    def __init__(self):
        self.dom = None
        self.current_state = None
    def tokenize(self, html):
        """Method to be called that creates the DOM.
        :param html: str containing html markup
        :returns: No value is returned. The DOM is stored in the class member variable dom.
        """
        index = 0
        self.dom = DOM()
        self.current_state = BEFORE_HTML 
        print(html)
        while index<len(html):
            index = self.__parse(html, index)
    def __parse(self, html, index):
        """Method called by tokenize. Matches regex tokens in the HTML string.
        :param html: str containing html markup
        :returns: Index of the next position of the str to be parsed
        """
        add_to_index = 0
        opentag =  t_OPENTAG.match(html[index:])
        closetag =  t_CLOSETAG.match(html[index:])
        whitespace = t_WHITESPACE.match(html[index:])
        data = t_DATA.match(html[index:])
        if opentag:
            tag, attrs, tag_len = self.__p_opentag(opentag)
            self.__handle_opentag(tag, attrs)
            add_to_index = tag_len
        elif closetag:
            tag, attrs, tag_len = self.__p_closetag(closetag)
            self.__handle_closetag(tag)
            add_to_index = tag_len+2
        elif whitespace:
            add_to_index = len(whitespace.group(0))
        elif data:
            data_result = self.__p_data(data.group(0))
            self.__handle_data(data_result, data.group(0))
            add_to_index = len(data.group(0))
        else:
            add_to_index = 1
        return add_to_index+index
####Parsing Methods
    def __p_opentag(self, match):
        """Method called by parse when an opentag token is matched.
        :param match: match object
        :returns: Strings representing Tag Name and Tag Attributes 
                  as well as the length of the entire matched string 
        """
        tag = match.group("tag")
        attrs = match.group("attrs")
        self.__set_opentag_state(tag)
        return tag, attrs, len(match.group(0))
    def __p_opentag_attrs(self, tag, attrs):
        """Method called by handle_open_tag. 
        
        Parses HTML tag attributes and adds them to the tag object.
        
        :param tag: Tag object representing the open tag found during parsing
        :param attrs: str representing html tag attributes 
        :returns: None. Modifies the given Tag object.
        """
        for match in re.finditer(t_ATTRIBUTES, attrs):
            attr_name = match.group("attr_name")
            attr_value = match.group("attr_value")
            tag.add_attr(attr_name, attr_value)
    def __p_closetag(self, match):
        """Method called by parse. 
        :param match: match object
        :returns: str of the name of tag, None object, length of the matched str
        """
        tag = match.group(1)
        if tag.lower()==HTML:
            self.current_state = AFTER_AFTER_BODY
        elif tag.lower()==HEAD:
            self.current_state = AFTER_HEAD
        elif tag.lower()==BODY:
            self.current_state = AFTER_BODY
        return tag, None, len(tag)
    def __p_data(self, data):
        """Method called by parse. 
        :param data: str of internal text found within an HTML tag
        :returns: cleaned input string 
        """
        data = self.__remove_excess_whitespace(data)
        return data
####Data Handling
    def __handle_opentag(self, tag_str, attrs):
        """Method called by parse. Creates Tag objects and adds to the DOM.
        :param tag_str: str representing the open tag found during parsing
        :param attrs: str representing html tag attributes 
        :returns: None. Modifies the DOM.
        """
        print("Found start tag:", tag_str, attrs)
        logging.debug("Found start tag:", tag_str, attrs)
        tag = Tag(tag_str)
        tag.parse_state = self.current_state 
        if attrs:
            self.__p_opentag_attrs(tag, attrs)
        self.dom.add_child(tag) 
        if tag.is_self_closing():
            self.__handle_closetag(tag)
    def __handle_closetag(self, tag):
        """Method called by parse. Closes Tag in the DOM.
        :param tag: str representing close html tag
        :returns: None. Modifies the DOM.
        """
        print("Found end tag:", tag)
        logging.debug("Found end tag:", tag)
        self.dom.close_child() 
    def __handle_data(self, display_data, original_data):
        """Method called by parse. Adds inner text to the DOM.
        If parse state is IN_BODY a Text object is created for later display.
        Otherwise the text is added to the content field of the currently open DOM element.
        :param display_data: str representing the cleaned text
        :param original_data: str representing the original text
        :returns: None. Modifies the DOM.
        """
        print("Found data:", display_data)
        logging.debug("Found data:", display_data)
        if self.current_state==IN_BODY:
            data = Text(display_data, original_data)
            data.parse_state = self.current_state 
            self.dom.add_text(data)
        else:
            self.dom.add_content(display_data)
####Additional Helper Methods
    def __set_opentag_state(self, tag):
        """Helper method called by p_open_tag. 
        Sets the parsing state if the tag has special meaning.
        :param tag: str representing HTML tag
        :returns: None. Modifies the parsing state.
        """
        if tag.lower()==HTML:
            self.current_state = BEFORE_HEAD
        elif tag.lower()==HEAD:
            self.current_state = IN_HEAD
        elif tag.lower()==BODY:
            self.current_state = IN_BODY

    def __remove_excess_whitespace(self, data):
        """Helper method that removes all extra whitespace from inner text.
        Resultant str can be later used for displaying.
        :param data: str representing inner text between HTML tags
        :returns: str with extra whitespace removed
        """
        #split the data and remove empty strings
        data = filter(lambda x: x, re.split("\s", data))
        return " ".join(data)

if __name__=="__main__":
    import sys
    import os
    example_path = os.path.join("baby_browser", "Examples", sys.argv[1]) 
    html_file = open(example_path, 'r')
    html_str = "\n".join(list(html_file))
    html_file.close()
    #html_str = "<html>\n<head><title>Website Title</title></head>\n<body>\n<div id=\"bye\"class=\"hello world\">Hi</div>\n<img src=\"html5.gif\" alt=\"HTML5 Icon\" width=\"128\" height=\"128\">\n</body>\n</html>"
    tokenizer = Html_Tokenizer()
    tokenizer.tokenize(html_str) 
    print(tokenizer.dom)
