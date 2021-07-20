from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox, QInputDialog)
import hashlib
import screens.home
import os

class LoginWidget(QWidget):
	def __init__(self, main_widget):
		super().__init__()
		self.setWindowTitle('Login Form')
		self.main_widget = main_widget
		
		try:
			self.password_hash = open("data/hash", "r").read()
		except:
			try:
				os.mkdir("data")
			except:
				pass
			open('data/hash', 'w')
			self.password_hash = open("data/hash", "r").read()
	
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
		if not self.password_hash:
			msg = QMessageBox()
			text, ok = QInputDialog.getText(None, "Attention", "Password?", 
                                    QLineEdit.Password)
			if ok and text:
				self.password_hash = hashlib.sha224(text.encode('utf-8')).hexdigest()
				open('data/hash', 'w').write(self.password_hash)
				msg.setText('Success')
				msg.exec_()

	def check_password(self):
		msg = QMessageBox()

		if hashlib.sha224(self.lineEdit_password.text().encode('utf-8')).hexdigest() == self.password_hash:
			home_screen = screens.home.MainWindow(self.main_widget)
			self.main_widget.addWidget(home_screen)
			self.main_widget.setCurrentWidget(home_screen)
		else:
			msg.setText('Incorrect Password')
			msg.exec_()
		