from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLCDNumber, QMessageBox, QCheckBox, QMainWindow, QPushButton, QSlider, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel
import random, csv, re
from services.aes import * 
from urllib.parse import urlparse


class AddWidget(QMainWindow):
    def __init__(self, main_widget, home_screen, password_hash):
        QMainWindow.__init__(self)
        self.main_widget = main_widget
        self.home_screen = home_screen
        self.password_hash = password_hash

        self.central_widget = QWidget(self)                
        self.setCentralWidget(self.central_widget)   
        self.grid_layout = QVBoxLayout(self)            
        self.central_widget.setLayout(self.grid_layout) 

        #Site enter text settings
        self.siteEditWidget = QWidget()
        self.siteEditLayout = QVBoxLayout(self.siteEditWidget)
        self.lineEditSite = QLineEdit()
        self.lineEditSite.setPlaceholderText('Please enter site')
        self.label_site = QLabel('<font size="4"> Site </font>')
        self.siteEditLayout.addWidget(self.label_site)
        self.siteEditLayout.addWidget(self.lineEditSite)
        
        #Username enter text settings
        self.usernameEditWidget = QWidget()
        self.usernameEditLayout = QVBoxLayout(self.usernameEditWidget)
        self.lineEditUsername = QLineEdit()
        self.lineEditUsername.setPlaceholderText('Please enter username or e-mail')
        self.label_username = QLabel('<font size="4"> Username </font>')
        self.usernameEditLayout.addWidget(self.label_username)
        self.usernameEditLayout.addWidget(self.lineEditUsername)

        #Settings of generete password
        self.passEditWidget = QWidget()
        self.passEditLayout = QVBoxLayout(self.passEditWidget)
        self.buttonsPasswordParametrsWidget = QWidget()
        self.buttonsPasswordParametrsLayout = QHBoxLayout(self.buttonsPasswordParametrsWidget)
        self.label_pass = QLabel('<font size="4"> Password </font>')
        self.checkLetters = QCheckBox('Letters', self)
        self.checkDigits = QCheckBox('Digits', self)
        self.checkSM = QCheckBox('Special symbols', self)
        self.passLenght = QSlider(Qt.Horizontal)
        self.lcd = QLCDNumber()
        self.lineEditPass = QLineEdit()
        self.lineEditPass.setPlaceholderText('Please enter your exist password')
        self.passLenght.setMinimum(4)
        self.passLenght.setMaximum(30)
        self.passLenght.setSingleStep(1)
        self.passLenght.setValue(12)
        self.flagLetters = True
        self.flagDigits = True
        self.flagSM = True
        self.passLenghtValue = 12
        self.checkLetters.toggle()
        self.checkDigits.toggle()
        self.checkSM.toggle()
        self.checkLetters.stateChanged.connect(self.changeFlagLetter)
        self.checkDigits.stateChanged.connect(self.changeFlagDigit)
        self.checkSM.stateChanged.connect(self.changeFlagSM)
        self.passLenght.valueChanged.connect(self.getValue)
        self.lcd.display(self.passLenghtValue)
        self.passEditLayout.addWidget(self.label_pass)
        self.passEditLayout.addWidget(self.lineEditPass)
        self.buttonsPasswordParametrsLayout.addWidget(self.checkLetters)
        self.buttonsPasswordParametrsLayout.addWidget(self.checkDigits)
        self.buttonsPasswordParametrsLayout.addWidget(self.checkSM)
        self.passEditLayout.addWidget(self.buttonsPasswordParametrsWidget)
        self.passEditLayout.addWidget(self.passLenght)
        self.passEditLayout.addWidget(self.lcd)

        self.ButtonsWidget = QWidget()
        self.ButtonsLayout = QHBoxLayout(self.ButtonsWidget)
        self.backButton = QPushButton('Back')
        self.generateButton = QPushButton('Add password')
        self.backButton.clicked.connect(self.back)
        self.generateButton.clicked.connect(self.generate_password)
        self.ButtonsLayout.addWidget(self.backButton)
        self.ButtonsLayout.addWidget(self.generateButton)

        self.grid_layout.addWidget(self.siteEditWidget)
        self.grid_layout.addWidget(self.usernameEditWidget)
        self.grid_layout.addWidget(self.passEditWidget)
        self.grid_layout.addWidget(self.ButtonsWidget)

    def generate_password(self):
        massiveLetters = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        massiveDigits = '1234567890'
        massiveSM = '+-/*!&$#?=@<>'
        resultMassive = ''
        password = ''
        msg = QMessageBox()

        if self.flagDigits:
            resultMassive += massiveDigits
        if self.flagLetters:
            resultMassive += massiveLetters
        if self.flagSM:
            resultMassive += massiveSM
        
        self.addSite = self.lineEditSite.text()

        if resultMassive != '' and self.addSite != '' and self.lineEditUsername.text() != '':

            if "http" not in self.addSite:
                self.addSite = "http://" + self.addSite

            checkSite = re.match(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*', self.addSite)
            
            if checkSite:
                if "https" in self.addSite:
                    self.addSite = "https://" + urlparse(self.addSite).netloc
                elif "http" in self.addSite:
                    self.addSite = "http://" + urlparse(self.addSite).netloc

                if self.lineEditPass.text() != "":
                    password = self.lineEditPass.text()
                else:
                    for _ in range(self.passLenghtValue):
                        password += random.choice(resultMassive)
                key = self.password_hash
                data_file = decrypt_file(FOLDER_PATH + 'data/data.csv', key).strip().split("\n")

                dataFile = open(FOLDER_PATH + 'data/data.csv', 'wb')
                
                reader = csv.reader(data_file)
                for row in reader:
                    if row != []:
                        dataFile.write((row[0] + '\n').encode("utf-8"))

                dataFile.write((self.addSite + ';' + self.lineEditUsername.text() + ';' + password + '\n').encode("utf-8"))
                dataFile.close()
                encrypt_file(FOLDER_PATH + 'data/data.csv', self.password_hash)
                msg.setText('Success')
                msg.exec_()
                self.home_screen.createTable()
                self.main_widget.setCurrentWidget(self.home_screen)
                self.main_widget.removeWidget(self)
            else:
                msg.setText('Incorrect site link')
                msg.exec_()
        else:
             msg.setText('Wrong settings')
             msg.exec_()

    def getValue(self):
        self.passLenghtValue = self.passLenght.value()
        self.lcd.display(self.passLenghtValue)

    def back(self):
        self.main_widget.setCurrentWidget(self.home_screen)
        self.main_widget.removeWidget(self)

    def changeFlagLetter(self):
        if self.flagLetters:
            self.flagLetters = False
        else:
            self.flagLetters = True

    def changeFlagDigit(self):
        if self.flagDigits:
            self.flagDigits = False
        else:
            self.flagDigits = True

    def changeFlagSM(self):
        if self.flagSM:
            self.flagSM = False
        else:
            self.flagSM = True
