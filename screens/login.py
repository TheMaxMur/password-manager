from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox, QInputDialog)
import hashlib
import screens.home
import os
from services.aes import *

class LoginWidget(QWidget):
	def __init__(self, main_widget):
		super().__init__()
		self.setWindowTitle('Login Form')
		self.main_widget = main_widget
		self.password_hashFlag = True
		self.dataFlag = True
		
		try:
			file = open("data/hash", "r")
			file.close()
		except:
			try:
				os.mkdir("data")
			except:
				pass
			self.password_hashFlag = False

		try:
			file = open("data/data.csv", "r")
			file.close()
		except:
			self.dataFlag = False

		self.layout = QGridLayout()
		self.label_password = QLabel('<font size="4"> Password </font>')
		self.lineEdit_password = QLineEdit()
		self.lineEdit_password.setPlaceholderText('Please enter your password')
		self.lineEdit_password.setEchoMode(QLineEdit.Password)
		self.lineEdit_password.returnPressed.connect(self.check_password)
		self.layout.addWidget(self.label_password, 1, 0)
		self.layout.addWidget(self.lineEdit_password, 1, 1)

		self.button_login = QPushButton('Login')
		self.button_login.clicked.connect(self.check_password)
		self.layout.addWidget(self.button_login, 2, 0, 1, 2)
		self.layout.setRowMinimumHeight(2, 75)

		self.setLayout(self.layout)

		if not self.password_hashFlag:
			self.savePassword()

	def check_password(self):
		msg = QMessageBox()
		text = hashlib.sha224(self.lineEdit_password.text().encode('utf-8')).hexdigest()[:32]
		try:
			password_hash = decrypt_file('data/hash', text)
			if text == password_hash:
				home_screen = screens.home.MainWindow(self.main_widget, password_hash)
				self.main_widget.addWidget(home_screen)
				self.main_widget.setCurrentWidget(home_screen)
		except Exception as e:
			msg.setText('Incorrect password')
			msg.exec_()

	def savePassword(self):
		msg = QMessageBox()
		text, ok = QInputDialog.getText(None, "Attention", "Enter main password", 
                                QLineEdit.Password)
		if ok and text and len(text) > 3:
			password = hashlib.sha224(text.encode('utf-8')).hexdigest()
			password_hash = password[:32]
			open('data/hash', 'w').write((password_hash))
			encrypt_file('data/hash', password_hash)
			if not self.dataFlag:
				open('data/data.csv', 'w')
				encrypt_file('./data/data.csv', password_hash)
			msg.setText('Success')
			msg.exec_()
		else:
			msg.setText('Incorrect password')
			msg.exec_()
			self.savePassword()