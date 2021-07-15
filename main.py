import sys
from PySide6 import QtCore, QtWidgets, QtGui
from screens.login import *


if __name__ == "__main__":
	app = QtWidgets.QApplication([])

	main_widget = QtWidgets.QStackedWidget()
	widget = LoginWidget(main_widget)
	main_widget.addWidget(widget)
	main_widget.resize(800, 600)
	main_widget.show()

	sys.exit(app.exec_())