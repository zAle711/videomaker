import asyncio
import pathlib
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal 
from PyQt5.QtGui import QPixmap
from downloader import ImageDownloader
from qasync import QEventLoop, asyncSlot
import enum

class Window(enum.Enum):
    MAIN = 0
    DOWNLOADER = 1

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent = None):
        super(MainWindow, self).__init__(parent)
        #self.loop = asyncio.get_event_loop()
        self.resize(800,600)

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        #creating window
        main_window = QtWidgets.QWidget()
        uic.loadUi('mainwindowUI.ui', main_window)
        #linking function to buttons
        main_window.button_new_window.clicked.connect(self.next_window)
        main_window.button_path_text.clicked.connect(self.setTextPath)
        main_window.button_path_audio.clicked.connect(self.setAudioPath)
        
        self.stacked_widget.addWidget(main_window)
        self.setWindowTitle(self.stacked_widget.currentWidget().windowTitle())
    
    def getPaths(self):
        window = self.stacked_widget.widget(Window.MAIN.value)
        return [window.text_path.text(), window.audio_path.text()]

    def setTextPath(self):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName( caption="Choose a text file", filter="Text file (*.txt)")
        window = self.stacked_widget.currentWidget()
        window.text_path.setText(fname)
    
    def setAudioPath(self):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName( caption="Choose an audio file", filter="Text file (*.wav)")
        window = self.stacked_widget.currentWidget()
        window.audio_path.setText(fname)


    def next_window(self):
        text_path, audio_path = self.getPaths()
                
        #get new window to set text file path
        downloader_window = self.stacked_widget.widget(Window.DOWNLOADER.value)

        if pathlib.Path(text_path).is_file():
            #checks if windows is created, if not create it with valid path
            if not downloader_window:
                downloader_window = DownloaderWindow(text_path)
                self.stacked_widget.addWidget(downloader_window)
            
            self.stacked_widget.setCurrentIndex(Window.DOWNLOADER.value)           
        


class DownloaderWindow(QtWidgets.QWidget):
    url_signal = pyqtSignal()
    current_index = 0
    urls_loaded = False
    def __init__(self, file_text_path, parent= None):
        super(DownloaderWindow, self).__init__(parent)
        self.file_text_path = file_text_path
        #self.loop = asyncio.get_event_loop()

        uic.loadUi('downloaderUI.ui', self)
        self.image_downloader = ImageDownloader(file_text_path)
        self.button_back.clicked.connect(self.previousWindow)
        self.url_signal.connect(self.showImage)
        self.current_urls = self.getUrls() 

    def previousImage(self):
        pass
    def nextImage(self):
        pass
    @asyncSlot()
    async def getUrls(self):
        self.urls = await self.image_downloader.getAllUrls()
        self.url_signal.emit()

    @asyncSlot()
    async def showImage(self):
        images = await self.image_downloader.fetchAll(self.urls)
        self.images = [img for img in images]
        pixelmap = QPixmap()
        pixelmap.loadFromData(self.images[0])
        
        self.label_image.setPixmap(pixelmap.scaled(600,430))
    
    def previousWindow(self):
        self.parent().setCurrentIndex(Window.MAIN.value)

    def set_path(self):
        self.parent().label_title.setText("DIO PORCO")
        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow()
    window.show()
    with loop:
        loop.run_forever()