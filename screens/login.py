from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox, QInputDialog)
import hashlib
import screens.home
import os
from services.aes import *
import sys

if sys.platform == 'linux':
	FOLDER_PATH = os.environ['HOME'] + '/' + '.passwordmanager' + '/'

if sys.platform == 'win32':
	FOLDER_PATH = 'C:\\' + os.environ['HOMEPATH'] + '\\' + '.passwordmanager\\'


class LoginWidget(QWidget):
	def __init__(self, main_widget):
		super().__init__()
		self.setWindowTitle('Login Form')
		self.main_widget = main_widget
		self.password_hashFlag = True
		self.dataFlag = True
		
		try:
			file = open(FOLDER_PATH + "data/hash", "r")
			file.close()
		except:
			try:
				os.mkdir(FOLDER_PATH)
				os.mkdir(FOLDER_PATH + "data")
			except:
				pass
			self.password_hashFlag = False

		try:
			file = open(FOLDER_PATH + "data/data.csv", "r")
			file.close()
		except:
			self.dataFlag = False

		self.layout = QGridLayout()
		self.label_password = QLabel('<font size="4"> Password </font>')
		self.lineEdit_password = QLineEdit()
		self.button_login = QPushButton('Login')
		self.lineEdit_password.setPlaceholderText('Please enter your password')
		self.lineEdit_password.setEchoMode(QLineEdit.Password)
		if self.password_hashFlag:
			self.lineEdit_password.returnPressed.connect(self.check_password)
			self.button_login.clicked.connect(self.check_password)
		else:
			self.label_passwordNotFound = QLabel('<font size="4"> Main password not found. Enter new. </font>')
			self.lineEdit_password.returnPressed.connect(self.savePassword)
			self.button_login.clicked.connect(self.savePassword)
			self.layout.addWidget(self.label_passwordNotFound, 0, 0)
		self.layout.addWidget(self.label_password, 1, 0)
		self.layout.addWidget(self.lineEdit_password, 1, 1)

		self.layout.addWidget(self.button_login, 2, 0, 1, 2)
		self.layout.setRowMinimumHeight(2, 75)

		self.setLayout(self.layout)

	def check_password(self):
		msg = QMessageBox()
		text = hashlib.sha224(self.lineEdit_password.text().encode('utf-8')).hexdigest()[:32]
		try:
			password_hash = decrypt_file(FOLDER_PATH + 'data/hash', text)
			if text == password_hash:
				home_screen = screens.home.MainWindow(self.main_widget, password_hash)
				self.main_widget.addWidget(home_screen)
				self.main_widget.setCurrentWidget(home_screen)
		except Exception as e:
			msg.setText('Incorrect password')
			msg.exec_()

	def savePassword(self):
		msg = QMessageBox()

		if len(self.lineEdit_password.text()) > 3 and len(self.lineEdit_password.text()) < 31:
			password = hashlib.sha224(self.lineEdit_password.text().encode('utf-8')).hexdigest()
			password_hash = password[:32]
			open(FOLDER_PATH + 'data/hash', 'w').write((password_hash))
			encrypt_file(FOLDER_PATH + 'data/hash', password_hash)
			if not self.dataFlag:
				open(FOLDER_PATH + 'data/data.csv', 'w')
				encrypt_file(FOLDER_PATH + 'data/data.csv', password_hash)
			msg.setText('Success')
			msg.exec_()
			home_screen = screens.home.MainWindow(self.main_widget, password_hash)
			self.main_widget.addWidget(home_screen)
			self.main_widget.setCurrentWidget(home_screen)
		else:
			msg.setText('Incorrect password')
			msg.exec_()
			self.savePassword()