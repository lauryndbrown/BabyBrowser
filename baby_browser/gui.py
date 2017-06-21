import sys
from PyQt5 import QtWidgets

#Address bar for inserting a URI
#Back and forward buttons
#Bookmarking options
#Refresh and stop buttons for refreshing or stopping the loading of current documents
#Home button that takes you to your home page
#Among those are the address bar, status bar and tool bar


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    button = QtWidgets.QPushButton("Hello")
    button.setFixedSize(400, 400)
    button.show()
    app.exec_()
