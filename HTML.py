from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import QWebView

class htmlwindow(QDialog):
    def __init__(self,url):
        super().__init__()
        self.resize(900,600)
        self.setWindowTitle("FastQC output")
        self.setBackground()
        self.url = url
        self.browser = QWebView()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.browser)
        self.setLayout(self.vbox)
        self.loadurl()

    def loadurl(self):
        self.browser.load(QUrl(self.url))

    def setBackground(self):            # Window Background Color
        self.setAutoFillBackground(True)
        Palette = self.palette()
        Palette.setColor(self.backgroundRole(),QColor(255,255,255))
        self.setPalette(Palette)
    
def showhtml(url):
    window=htmlwindow(url)
    window.exec_()
