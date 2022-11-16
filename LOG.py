from PyQt4.QtGui import *
from PyQt4.QtCore import *

class logwindow(QDialog):
    def __init__(self,text):
        super().__init__()
        self.resize(900,600)
        self.setWindowTitle("LOG Window")
        self.setBackground()
        self.text = text
        self.editor = QTextEdit()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.editor)
        self.setLayout(self.vbox)
        self.loadtext()

    def loadtext(self):
        self.editor.setText(self.text)

    def setBackground(self):            # Window Background Color
        self.setAutoFillBackground(True)
        Palette = self.palette()
        Palette.setColor(self.backgroundRole(),QColor(255,255,255))
        self.setPalette(Palette)
    
def showlog(text):
    window=logwindow(text)
    window.exec_()
