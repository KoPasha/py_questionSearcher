from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

def main():
    app = QApplication([])
    window = QWidget()
    window.setGeometry(100,100,400,300)
    window.setWindowTitle('Question searcher! (with answers;))')

    layout = QVBoxLayout()

    label = QLabel('Words contained in question:')
    label.setFont(QFont('Arial', 16))
    button_search = QPushButton('Search...')
    button_search.clicked.connect(search_button_clicked)
    search_box = QTextEdit()
    answers_box = QTextBrowser()

    layout.addWidget(label)
    layout.addWidget(button_search)
    layout.addWidget(search_box)
    layout.addWidget(answers_box)
    window.setLayout(layout)

    window.show()
    app.exec_()

def search_button_clicked():
    #print('Hello, I\'am the main algorithm in all this mess')
    message = QMessageBox()
    message.setWindowTitle('Important message')
    message.setText('Hello, I\'am the main algorithm in all of this mess')
    message.exec_()


if __name__ == '__main__':
    main()