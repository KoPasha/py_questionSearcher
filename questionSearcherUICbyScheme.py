from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
import questionSearchedCommands as qsc

class SearcherGUI(QMainWindow):

    search_index = {}
    dataset = []

    def __init__(self):
        super(SearcherGUI, self).__init__()
        uic.loadUi('searcherMainWindow.ui', self)
        self.show()
        self.searchAgainButton.clicked.connect(self.search_button_clicked)
        self.dataset = qsc.read_dataset()
        qsc.optimize_dataset(self.dataset)
        self.search_index = qsc.build_search_index(self.dataset)

    def search_button_clicked(self):
        search_string = self.QLineEdit.text
        results = qsc.search(search_string, self.search_data_set, self.search_index)
        #operate result data to put it in the form fields
        return results

def main():
    app = QApplication([])
    window =  SearcherGUI()
    app.exec_()
    # window.search_data_set = get_data_for_search()

if __name__ == '__main__':
    main()