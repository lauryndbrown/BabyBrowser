import sys
from PyQt5.QtWidgets import QDesktopWidget, QWidget, QApplication

#Address bar for inserting a URI
#Back and forward buttons
#Bookmarking options
#Refresh and stop buttons for refreshing or stopping the loading of current documents
#Home button that takes you to your home page
#Among those are the address bar, status bar and tool bar
class Browser_Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Title')
        self.setGeometry(100, 100, 1200, 1200)
        self.show()
    def center(self):
        geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        geometry.moveCenter(center_point)
        self.move(geometry.topLeft())
if __name__=="__main__":
    app = QApplication(sys.argv)
    widget = Browser_Widget()
    widget.center()
    sys.exit(app.exec_())
