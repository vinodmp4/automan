"""
    Created at 01/04/2018
    Created by Vinod M P
    Created for KERALA UNIVERSITY
    Created under MASSIVE DATA ANALYTICS
"""

# AUTOMAN CUSTOM WIDGETS
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import ARROW, DIALOG

# 1. TAB CONTROL

class tabcontrol(QTabWidget): 
    def __init__(self,superparent):
        super(tabcontrol,self).__init__()
        self.superparent = superparent
        self.setMouseTracking(True)
        self.setMinimumSize(650,360)
        self.setBackground()
        self.repaint()
        self.currentChanged.connect(self.setindex)

    def addtab(self,widget,name):
        self.addTab(widget,name)

    def removetab(self):
        self.removeTab(self.currentIndex())

    def setindex(self,event):
        self.superparent.currenttabindex = self.currentIndex()

    def renametab(self,newname):
        if not (self.count()<=0):
            self.setTabText(self.currentIndex(),newname)
        
    def setBackground(self):            # Background Color
        self.setAutoFillBackground(True)
        Palette = self.palette()
        Palette.setColor(self.backgroundRole(),QColor(49,51,77))
        self.setPalette(Palette)
        
    def paintEvent(self,event):
        canvas = QPainter()
        canvas.begin(self)
        self.draw(canvas)
        canvas.setRenderHint(QPainter.Antialiasing)
        canvas.end()
        
    def draw(self,canvas):
        font = QFont('Serif',20,QFont.Bold)
        canvas.setFont(font)
        size = self.size()
        width = size.width()
        height = size.height()
        canvas.setPen(QColor(39,41,67))
        canvas.setBrush(QColor(39,41,67))
        canvas.drawText(0,0,width,height,Qt.AlignCenter,"AUTOMAN")

class tabpage(QWidget):
    def __init__(self,superparent,iconarrays):
        super(tabpage,self).__init__()
        self.setMouseTracking(True)
        self.superparent = superparent
        self.iconarrays = iconarrays
        self.resize(600,400)
        self.iconarraycount = len(self.iconarrays)
        self.layouts = [] # QHBoxLayout collection in an array
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.arrangeicons()

    def arrangeicons(self):
        for arraynumber in range(0,self.iconarraycount):
            currenticonarray = self.iconarrays[arraynumber]
            currentrow = 0
            for icon in currenticonarray:
                if currenticonarray.index(icon) == 0:
                    self.layouts.append(QHBoxLayout())
                    self.layouts[(len(self.layouts)-1)].addWidget(icon)
                    self.grid.addLayout(self.layouts[(len(self.layouts)-1)],arraynumber,currentrow)
                    currentrow += 1
                else:
                    arrow = ARROW.arrow("right")
                    self.layouts.append(QHBoxLayout())
                    self.layouts[(len(self.layouts)-1)].addWidget(arrow)
                    self.grid.addLayout(self.layouts[(len(self.layouts)-1)],arraynumber,currentrow)
                    currentrow += 1
                    self.layouts.append(QHBoxLayout())
                    self.layouts[(len(self.layouts)-1)].addWidget(icon)
                    self.grid.addLayout(self.layouts[(len(self.layouts)-1)],arraynumber,currentrow)
                    currentrow += 1
























