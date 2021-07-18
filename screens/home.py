import hashlib
import csv
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHeaderView, QVBoxLayout, QPushButton, QMainWindow, QTableWidget, QInputDialog, QMessageBox, QAbstractItemView
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
 
        self.setMinimumSize(QSize(480, 80))           
        self.setWindowTitle("Main")  
        self.search = QLineEdit(self)
        self.search.setStyleSheet('font-size: 35px; height: 40px;')
        central_widget = QWidget(self)                
        self.setCentralWidget(central_widget)           
 
        grid_layout = QVBoxLayout()            
        central_widget.setLayout(grid_layout)   
 
        self.table = QTableWidget(self)
        data = {}
        with open("./data/data.csv", "r") as data_file:
                reader = csv.reader(data_file, delimiter = ';')
                for row in reader:
                    data[row[0]] = {row[1]: row[2]}

        headers = ['Site', 'Username', 'Copy password']
        massive_domain_buttons = []
        massive_username_buttons = []
        massive_copy_buttons = []

        self.table.setColumnCount(len(headers))     
        self.table.setRowCount(len(data.keys()))       
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)

        for row, domain in enumerate(data.keys()):
            username = list(data[domain].keys())[0]
            massive_domain_buttons.append(QPushButton(domain))
            massive_username_buttons.append(QPushButton(username))
            massive_copy_buttons.append(QPushButton('Copy'))
            #massive_copy_buttons[row].setIcon(QIcon('./assets/copy.png'))
            #massive_copy_buttons[row].setIconSize(QSize(1, 1))
            self.table.setCellWidget(row, 0, massive_domain_buttons[row])
            self.table.setCellWidget(row, 1, massive_username_buttons[row])
            self.table.setCellWidget(row, 2, massive_copy_buttons[row])
         
        for index in range(len(massive_copy_buttons)):
            massive_copy_buttons[index].clicked.connect(lambda copy, arg=index: self.copyText(arg, data))

        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table.resizeColumnsToContents()
        self.table.setStyleSheet('font-size: 20px;')
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(50)

        self.search.textChanged.connect(self.findName)

        grid_layout.addWidget(self.search)
        grid_layout.addWidget(self.table)

    def findName(self):
        name = self.search.text().lower()
        for row in range(self.table.rowCount()):
            domain = self.table.cellWidget(row, 0)
            username = self.table.cellWidget(row, 1)
            result = (name not in domain.text().lower()) and (name not in username.text().lower())
            self.table.setRowHidden(row, result)

    def copyText(self, button_index, data):
        msg = QMessageBox()
        with open("data/hash", "r") as hash:
            text, ok = QInputDialog.getText(None, "Attention", "Password?", 
                                        QLineEdit.Password)
            if ok and text and hashlib.sha224(text.encode('utf-8')).hexdigest() == hash.read().strip():
                cb = QApplication.clipboard()
                cb.clear(mode=cb.Clipboard)
                cb.setText(data[list(data.keys())[button_index]][list(data[list(data.keys())[button_index]].keys())[0]], mode=cb.Clipboard)
            else:
                msg.setText('Incorrect Password')
                msg.exec_()
    