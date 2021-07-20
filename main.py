import sys
from PyQt5 import QtWidgets
from screens.login import *


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)

	main_widget = QtWidgets.QStackedWidget()
	loginWidget = LoginWidget(main_widget)
	main_widget.addWidget(loginWidget)
	main_widget.resize(1000, 800)
	main_widget.setWindowTitle('Passwords')
	main_widget.show()

	sys.exit(app.exec_())