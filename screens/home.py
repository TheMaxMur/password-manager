import hashlib, csv, screens.add, screens.view, shutil, zipfile
from services.aes import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication, QHBoxLayout, QWidget, QLineEdit, QHeaderView, QVBoxLayout, QPushButton, QMainWindow, QTableWidget, QInputDialog, QMessageBox, QAbstractItemView

class MainWindow(QMainWindow):
    def __init__(self, main_widget, password_hash):
        QMainWindow.__init__(self)
        self.main_widget = main_widget
        self.password_hash = password_hash

        self.central_widget = QWidget(self)                
        self.setCentralWidget(self.central_widget)           
 
        self.grid_layout = QVBoxLayout(self)            
        self.central_widget.setLayout(self.grid_layout)

        self.data = {}
        self.data_id = 0
        self.headers = ['Site', 'Username', 'Copy password', 'Delete password']

        #Search bar settings
        self.search = QLineEdit(self)
        self.search.setStyleSheet('font-size: 35px; height: 40px;')
        self.search.setPlaceholderText('Search...')
        self.search.textChanged.connect(self.findName)

        #Table settings
        self.table = QTableWidget(self)
        self.table.setColumnCount(len(self.headers))     
        self.table.setRowCount(len(self.data.keys()))       
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table.resizeColumnsToContents()
        self.table.setStyleSheet('font-size: 20px;')
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(50)

        #Header settings
        self.headerWidget = QWidget()
        self.buttonsWidget = QHBoxLayout(self.headerWidget)
        self.headerAdd = QPushButton('+')
        self.headerImport = QPushButton('Import')
        self.headerExport = QPushButton('Export')
        self.headerAdd.setToolTip('Add a new password')
        self.headerImport.clicked.connect(self.importFile)
        self.headerExport.clicked.connect(self.exportFile)
        self.headerAdd.clicked.connect(self.changeScreenToAdd)
        self.buttonsWidget.addWidget(self.headerAdd)
        self.buttonsWidget.addWidget(self.headerImport)
        self.buttonsWidget.addWidget(self.headerExport)

        self.createTable()
        
        self.grid_layout.addWidget(self.headerWidget)
        self.grid_layout.addWidget(self.search)
        self.grid_layout.addWidget(self.table)
            
    def importFile(self):
        path_to_backup = QFileDialog.getOpenFileName(self, 'Select backup file')
        if path_to_backup != "":
            try:
                with zipfile.ZipFile(path_to_backup[0], 'r') as zip_ref:
                    zip_ref.extractall(FOLDER_PATH + 'data/')
            except Exception as e:
                print(e)
        self.createTable()

    def exportFile(self):
        path_to_backup = QFileDialog.getExistingDirectory(self, 'Select directory for backup')
        if path_to_backup != '':
            try:
                shutil.make_archive(path_to_backup + '/backup', 'zip', FOLDER_PATH + 'data')
            except Exception as e:
                print(e)

    def findName(self):
        name = self.search.text().lower()
        for row in range(self.table.rowCount()):
            domain = self.table.cellWidget(row, 0)
            username = self.table.cellWidget(row, 1)
            result = (name not in domain.text().lower()) and (name not in username.text().lower())
            self.table.setRowHidden(row, result)

    def copyText(self, button_index, data):
        msg = QMessageBox()
        text, ok = QInputDialog.getText(None, "Attention", "Password?", 
                                    QLineEdit.Password)
        key = hashlib.sha224(text.encode('utf-8')).hexdigest()[:32]
        try:
            passhash = decrypt_file(FOLDER_PATH + 'data/hash', key)
        except:
            passhash = ''

        if ok and text and key == passhash:
            cb = QApplication.clipboard()
            cb.clear(mode=cb.Clipboard)
            data = data[button_index]
            cb.setText(list(data[list(data.keys())[0]].values())[0], mode=cb.Clipboard)
        else:
            if text == "":
                pass
            else:
                msg.setText('Incorrect Password')
                msg.exec_()

    def changeScreenToAdd(self):
        add_screen = screens.add.AddWidget(self.main_widget, self, self.password_hash)
        self.main_widget.addWidget(add_screen)
        self.main_widget.setCurrentWidget(add_screen)

    def deletePassword(self, button_index):
        msg = QMessageBox()
        text, ok = QInputDialog.getText(None, "Attention", "Password?", 
                                    QLineEdit.Password)

        key = hashlib.sha224(text.encode('utf-8')).hexdigest()[:32]
        try:
            passhash = decrypt_file(FOLDER_PATH + 'data/hash', key)
        except:
            passhash = ''

        if ok and text and key == passhash:
            data = self.data[button_index]
            result_massive = []
            result = list(data.keys())[0] + ';' + list(data[list(data.keys())[0]].keys())[0] + ';' + list(data[list(data.keys())[0]].values())[0]
            for index in range(len(self.data)):
                data = self.data[index]
                for elID in range(len(data)):
                    datastr = list(data.keys())[elID] + ';' + list(data[list(data.keys())[elID]].keys())[elID] + ';' + list(data[list(data.keys())[elID]].values())[elID]
                    if result != datastr:
                        result_massive.append(datastr)

            decrypt_file(FOLDER_PATH + 'data/data.csv', self.password_hash)
            with open(FOLDER_PATH + 'data/data.csv', 'w') as data_file:
                for index in range(len(result_massive)):
                    data_file.write(result_massive[index] + '\n')
            encrypt_file(FOLDER_PATH + 'data/data.csv', self.password_hash)
            self.createTable()
        else:
            if text == "":
                pass
            else:
                msg.setText('Incorrect Password')
                msg.exec_()

    def createTable(self):
        self.loadData()

        for row in range(len(self.data.keys())):
            self.table.removeCellWidget(row, 0)
            self.table.removeCellWidget(row, 1)
            self.table.removeCellWidget(row, 2)
            self.table.removeCellWidget(row, 3)

        self.table.setRowCount(0)
        
        self.table.setColumnCount(len(self.headers))     
        self.table.setRowCount(len(self.data.keys()))  
            
        self.massive_domain_buttons = []
        self.massive_username_buttons = []
        self.massive_copy_buttons = []
        self.massive_delete_buttons = []

        for row, res_data in enumerate(list(self.data.values())):
            domain = list(res_data.keys())[0]
            username = list(res_data[domain].keys())[0]
            domain = domain.split('.')[-2]
            domain = domain.split("/")[-1]
            self.massive_domain_buttons.append(QPushButton(domain))
            self.massive_username_buttons.append(QPushButton(username))
            self.massive_copy_buttons.append(QPushButton('Copy'))
            self.massive_delete_buttons.append(QPushButton('Delete'))
            self.table.setCellWidget(row, 0, self.massive_domain_buttons[row])
            self.table.setCellWidget(row, 1, self.massive_username_buttons[row])
            self.table.setCellWidget(row, 2, self.massive_copy_buttons[row])
            self.table.setCellWidget(row, 3, self.massive_delete_buttons[row])
    
        for index in range(len(self.massive_copy_buttons)):
            self.massive_copy_buttons[index].clicked.connect(lambda copy, arg=index: self.copyText(arg, self.data))

        for index in range(len(self.massive_delete_buttons)):
            self.massive_delete_buttons[index].clicked.connect(lambda delete, arg=index: self.deletePassword(arg))

        for index in range(len(self.massive_delete_buttons)):
            self.massive_domain_buttons[index].clicked.connect(lambda view, arg=index: self.viewScreen(arg))
            self.massive_username_buttons[index].clicked.connect(lambda view, arg=index: self.viewScreen(arg))

    def viewScreen(self, button_index):
        data = self.data[button_index]
        domains = list(data.keys())[0]
        usernames = list(data[domains])[0]
        password = list(data[list(data.keys())[0]].values())[0]
        view_screen = screens.view.viewWidget(self.main_widget, self, domains, usernames, password)
        self.main_widget.addWidget(view_screen)
        self.main_widget.setCurrentWidget(view_screen)

    def loadData(self):
        self.data = {}
        data_file = decrypt_file(FOLDER_PATH + 'data/data.csv', self.password_hash).strip().split("\n")
        reader = csv.reader(data_file, delimiter = ';')
        try:
            for row in reader:
                self.data[self.data_id] = {row[0]: {row[1]: row[2]}}
                self.data_id += 1     
            self.data_id = 0
        except:
            pass