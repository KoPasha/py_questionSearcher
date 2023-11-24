from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic

class SearcherGUI(QMainWindow):

    def __init__(self):
        super(SearcherGUI, self).__init__()
        uic.loadUi('searcherMainWindow.ui', self)
        self.show()
        self.searchAgainButton.clicked.connect(self.search_button_clicked)

    def search_button_clicked(self):
        pass

def main():
    app = QApplication([])
    window =  SearcherGUI()
    app.exec_()

if __name__ == '__main__':
    main()