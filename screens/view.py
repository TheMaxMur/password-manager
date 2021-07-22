from PyQt5.QtWidgets import QApplication, QInputDialog, QMessageBox, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel
import hashlib
from services.aes import *

class viewWidget(QMainWindow):
    def __init__(self, main_widget, home_screen, domain, username, password):
        QMainWindow.__init__(self)
        self.main_widget = main_widget
        self.home_screen = home_screen
        self.password = password

        self.central_widget = QWidget(self)                
        self.setCentralWidget(self.central_widget)   
        self.grid_layout = QVBoxLayout(self)            
        self.central_widget.setLayout(self.grid_layout) 

        #Site enter text settings
        self.siteEditWidget = QWidget()
        self.siteEditLayout = QVBoxLayout(self.siteEditWidget)
        self.label_site = QLabel('<font size="20"> Site </font>')
        self.data_site = QLabel('<font size="10">' + domain + ' </font>')
        self.siteEditLayout.addWidget(self.label_site)
        self.siteEditLayout.addWidget(self.data_site)
        
        #Username enter text settings
        self.usernameEditWidget = QWidget()
        self.usernameEditLayout = QVBoxLayout(self.usernameEditWidget)
        self.label_username = QLabel('<font size="20"> Username </font>')
        self.data_username = QLabel('<font size="10">' + username + ' </font>')
        self.usernameEditLayout.addWidget(self.label_username)
        self.usernameEditLayout.addWidget(self.data_username)

        #Settings of generete password
        self.passEditWidget = QWidget()
        self.passEditLayout = QVBoxLayout(self.passEditWidget)
        self.label_pass = QLabel('<font size="20"> Password </font>')
        self.copyPass = QPushButton('Copy password')
        self.copyPass.clicked.connect(self.copyText)
        self.passEditLayout.addWidget(self.label_pass)
        self.passEditLayout.addWidget(self.copyPass)


        self.ButtonsWidget = QWidget()
        self.ButtonsLayout = QHBoxLayout(self.ButtonsWidget)
        self.backButton = QPushButton('Back')
        self.backButton.clicked.connect(self.back)
        self.ButtonsLayout.addWidget(self.backButton)

        self.grid_layout.addWidget(self.siteEditWidget)
        self.grid_layout.addWidget(self.usernameEditWidget)
        self.grid_layout.addWidget(self.passEditWidget)
        self.grid_layout.addWidget(self.ButtonsWidget)
        
    def back(self):
        self.main_widget.setCurrentWidget(self.home_screen)
        self.main_widget.removeWidget(self)


    def copyText(self):
        msg = QMessageBox()
        text, ok = QInputDialog.getText(None, "Attention", "Password?", 
                                    QLineEdit.Password)
        key = hashlib.sha224(text.encode('utf-8')).hexdigest()[:32]
        try:
            passhash = decrypt_file('./data/hash', key)
        except:
            passhash = ''
            
        if ok and text and key == passhash:
            cb = QApplication.clipboard()
            cb.clear(mode=cb.Clipboard)
            cb.setText(self.password, mode=cb.Clipboard)
        else:
            if text == "":
                pass
            else:
                msg.setText('Incorrect Password')
                msg.exec_()
