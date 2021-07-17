import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHeaderView, QVBoxLayout, QPushButton
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget
from PyQt5.QtCore import QSize

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
        data = {'github.com': {'username': 'password'}, 'google.com': {'testname': 'password2'}}
        headers = ['Domain', 'Username', 'Copy']
        massive_domain_buttons = []
        massive_username_buttons = []
        massive_copy_buttons = []

        self.table.setColumnCount(len(headers))     
        self.table.setRowCount(len(data.keys()))       
        self.table.setHorizontalHeaderLabels(headers)

        for row, domain in enumerate(data.keys()):
            username = list(data[domain].keys())[0]
            massive_domain_buttons.append(QPushButton(domain))
            massive_username_buttons.append(QPushButton(username))
            massive_copy_buttons.append(QPushButton('Copy'))
            self.table.setCellWidget(row, 0, massive_domain_buttons[row])
            self.table.setCellWidget(row, 1, massive_username_buttons[row])
            self.table.setCellWidget(row, 2, massive_copy_buttons[row])
         
        for index in range(len(massive_copy_buttons)):
            massive_copy_buttons[index].clicked.connect(lambda copy, arg=index: self.copyText(arg, data))

        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table.resizeColumnsToContents()
        self.table.setStyleSheet('font-size: 20px;')
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

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
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(data[list(data.keys())[button_index]][list(data[list(data.keys())[button_index]].keys())[0]], mode=cb.Clipboard)