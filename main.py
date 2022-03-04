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
        
        

    def addWidget(self, widget):
        self.central_widget.add

    def next_window(self):
        text_path, audio_path = self.ui.getPaths()
                
        #get new window to set text file path
        downloader_window = self.central_widget.widget(Window.DOWNLOADER.value)

        if pathlib.Path(text_path).is_file():
            #checks if windows is created, if not create it with valid path
            if not self.central_widget.widget(Window.DOWNLOADER.value):
                downloader_window = DownloaderWindow(text_path)
                self.central_widget.addWidget(downloader_window)
            
            self.central_widget.setCurrentIndex(Window.DOWNLOADER.value)
        


class DownloaderWindow(QtWidgets.QWidget):
    def __init__(self, file_text_path ,parent= None):
        super(DownloaderWindow, self).__init__(parent)
        self.ui = Ui_DownloaderWindow(file_text_path)
        self.ui.setupUi(self)
        self.ui.button_back.clicked.connect(self.back_window)
    
    def back_window(self):
        self.parent().setCurrentIndex(Window.MAIN.value)
    def set_path(self):
        self.parent().label_title.setText("DIO PORCO")
        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()