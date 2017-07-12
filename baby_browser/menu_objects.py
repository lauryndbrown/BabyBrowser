class MenuWebPage:

    def __init__(self, url, title=None, icon=None):
        self.url = url
        self.icon = icon
        self.title = title

    def __str__(self):
        return "Title:{} Url:{}".format(self.title, self.url)

    def __repr__(self):
        return str(self)

