class Html_Object:
    def __init__(self, parent, children, attrs, css=None):
        self.parent = parent
        if children==None:
            self.children = []
        else:
            self.children = children
        self.attrs = attrs
        self.parse_state = None
        self.css = css
class Tag(Html_Object):
    def __init__(self, tag, attrs, content=None, parent=None, children=None):
        super().__init__(parent, children, attrs)
        self.tag = tag
        self.content = content
    def __str__(self):
        return self.tag
    def __repr__(self):
        return self.__str__()
class DOM:
    def __init__(self, root=None):
        self.root = root
        self.current_level = None
    def add_child(self, html_object):
        if self.root:
           self.current_level.children.append(html_object)
           html_object.parent = self.current_level
           self.current_level = html_object
        else:
            self.root = html_object
            self.current_level = self.root
    def close_child(self):
        self.current_level = self.current_level.parent
    def add_content(self, content):
        self.current_level.content = content 
    def find_child_by_tag(self, child_name):
       return self.find_child_by_tag_helper(self.root, child_name.lower())
    def find_child_by_tag_helper(self, root, child_name):
        if root:
            if root.tag==child_name:
                return root
            for child in root.children:
                result = self.find_child_by_tag_helper(child, child_name)
                if result:
                    return result

    def __str__(self):
        return self.str_traverse(self.root, 0)
    def str_traverse(self, root, level):
        lst_root = "  "*level+str(root)
        if root.content:
            lst_root += "\n"+("  "*(level+1))+str(root.content)
        for child in root.children:
            lst_root+= "\n"+self.str_traverse(child, level+1)
        #lst_root+= "\n"+"  "*level+str(root)
        return lst_root
    def __repr__(self):
        return self.__str__()
if __name__=="__main__":
    html = Tag("html", None)
    head = Tag("head", None)
    title = Tag("title", None)
    body = Tag("body", None)
    dom = DOM()
    dom.add_child(html)
    dom.add_child(head)
    dom.add_child(title)
    dom.close_child()#title
    dom.close_child()#head
    dom.add_child(body)
    dom.close_child()#body
    dom.close_child()#html
    print(dom)

