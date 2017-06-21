import re
#Tokens
t_OPENTAG = re.compile("<(\w+)>")
t_CLOSETAG = re.compile("</(\w+)>")
t_DATA = re.compile("[^<>]+")
t_WHITESPACE = re.compile("\s+")
class Html_Tokenizer:
    def handle_opentag(self, tag, attrs):
        print("Found start tag:", tag)
    def handle_closetag(self, tag):
        print("Found end tag:", tag)
    def handle_data(self, data):
        print("Found data:", data)

    def p_opentag(self, match):
        tag = match.group(0)
        return tag, None, len(tag)
    def p_closetag(self, match):
        tag = match.group(0)
        return tag, None, len(tag)
    def tokenize(self, html):
        index = 0
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
            add_to_index = tag_len+1
        elif closetag:
            tag, attrs, tag_len = self.p_closetag(closetag)
            self.handle_closetag(tag)
            add_to_index = tag_len+1
        elif whitespace:
            add_to_index = len(whitespace.group(0))
        elif data:
            self.handle_data(data.group(0))
            add_to_index = len(data.group(0))
        else:
            add_to_index = 1
        return add_to_index+index
if __name__=="__main__":
    html_str = "<html>\n<body>\nHi\n</body>\n</html>"
    tokenizer = Html_Tokenizer()
    tokenizer.tokenize(html_str) 
