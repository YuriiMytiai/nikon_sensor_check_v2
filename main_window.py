import sys
from PyQt5 import QtWidgets, uic
from events_processor import EventsProcessor

app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi("form.ui")

events_processor = EventsProcessor(window)

window.show()
app.exec()