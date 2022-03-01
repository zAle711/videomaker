import pathlib
from tkinter.tix import MAIN
from PyQt5 import QtCore, QtGui, QtWidgets
from downloaderUI import Ui_DownloaderWindow
from mainwindowUi import Ui_mainWindow
import enum

class Window(enum.Enum):
    MAIN = 0
    DOWNLOADER = 1

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.resize(800,600)

        self.central_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.central_widget)

        main_window = QtWidgets.QWidget()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(main_window)
        self.ui.button_new_window.clicked.connect(self.next_window)
        self.central_widget.addWidget(main_window)
        self.setWindowTitle(self.central_widget.currentWidget().windowTitle())
        
        downloader_window = DownloaderWindow()
        self.central_widget.addWidget(downloader_window)

    def next_window(self):
        print("DIO PORCO")
        text_path, audio_path = self.ui.getPaths()
        print(text_path +" " + audio_path)
        if pathlib.Path(text_path).is_file() and pathlib.Path(audio_path).is_file():
            self.central_widget.setCurrentIndex(Window.DOWNLOADER.value)
        


class DownloaderWindow(QtWidgets.QWidget):
    def __init__(self, parent= None):
        super(DownloaderWindow, self).__init__(parent)
        ui = Ui_DownloaderWindow()
        ui.setupUi(self)
        ui.button_back.clicked.connect(self.back_window)
    
    def back_window(self):
        self.parent().setCurrentIndex(Window.MAIN.value)
        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()