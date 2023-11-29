from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic, QtGui
import questionSearchedCommands as qsc

class SearcherGUI(QMainWindow):

    search_index = {}
    dataset = []
    results = []

    def __init__(self):
        super(SearcherGUI, self).__init__()
        uic.loadUi('searcherMainWindow.ui', self)
        self.show()
        self.searchAgainButton.clicked.connect(self.search_button_clicked)
        self.listView.clicked.connect(self.list_clicked)
        
        self.dataset = qsc.read_dataset()
        qsc.optimize_dataset(self.dataset)
        self.search_index = qsc.build_search_index(self.dataset)

    def list_clicked(self,index_clicked):
        items = self.listView.selectedIndexes()
        for item in items:
            result_to_view = self.results[item.row()]
            self.textEdit.setText(result_to_view.united_question_text_for_print)

    def list_changed(self,index_clicked):
        items = self.listView.selectedIndexes()
        for item in items:
            result_to_view = self.results[item.row()]
            self.textEdit.setText(result_to_view.united_question_text_for_print)

    def search_button_clicked(self):
        self.textEdit.setText('')#no need for old result
        search_string = self.lineEdit.text()
        self.results = qsc.search(search_string, self.dataset, self.search_index)
        #operate result data to put it in the form fields of ListView object
        model = QtGui.QStandardItemModel()
        self.listView.setModel(model)
        self.listView.selectionModel().selectionChanged.connect(self.list_changed)
        for result in self.results:
            item = QtGui.QStandardItem(result.united_question_text_for_search)
            model.appendRow(item)
            print(f'question: {result} \n')
            if self.results.index(result) == 0:
                index_for_qt = model.index(0,0)
                self.listView.selectionModel().setCurrentIndex(index_for_qt,QtCore.QItemSelectionModel().SelectCurrent)
        
        

def main():
    app = QApplication([])
    window =  SearcherGUI()
    app.exec_()
    # window.search_data_set = get_data_for_search()

if __name__ == '__main__':
    main()