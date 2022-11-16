"""
    Created at 06/04/2018
    Created by Vinod M P
    Created for KERALA UNIVERSITY
    Created under MASSIVE DATA ANALYTICS

"""
# Read Me
"""
When user changes tabs, Parent send a 2D ARRAY to Icon Manager.
Icon Manager accept that 2D ARRAY send by parent.
2D ARRAY is an array of filenames array.
for each filenames array, it filter the filenames in it.
filtering is based on the file extension like .sra, .fastq, .html.
based on extension, different icons are generated.
Generated icons are added to a new ICON ARRAY.
in such a fashion, ICON ARRAY for each filenames array is created.
just like 2D ARRAY, a 2D ICON ARRAY of ICON ARRAY's is generated.
finally the 2D ICON ARRAY is returned back to parent.

"""

# AUTOMAN DATA REPRESENTING WIDGETS

import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# 1. ICON MANAGER

class iconmanager():
    def __init__(self,parent,arrayfromparent):
        super(iconmanager,self).__init__()
        self.twoDarray = arrayfromparent
        self.parent = parent
        self.ICON_ARRAY = []
        self.row = 0
        self.generateIcons()

    def generateIcons(self):
        for filenames_array in self.twoDarray:
            self.ICON_ARRAY.append(self.filterFilenames(filenames_array,self.row))
            self.row += 1

    def filterFilenames(self,filenames_array,currentrow):
        iconarray = []
        for files in filenames_array:
            filename = files.split("/")[-1]
            extension = filename.split(".")[-1]
            if extension == "sra":
                newnode = SRAnode((filename.split(".")[0]),self.parent,files,currentrow)
                iconarray.append(newnode)
            elif extension == "fastq":
                newnode = FASTQnode((filename.split(".")[0]),self.parent,files,currentrow)
                iconarray.append(newnode)
            elif extension == "html":
                newnode = HTMLnode((filename.split(".")[0]),self.parent,files,currentrow)
                iconarray.append(newnode)
            else:
                newnode = UNKNOWNnode((filename.split(".")[0]),self.parent,files,currentrow)
                iconarray.append(newnode)
        return iconarray



class UNKNOWNnode(QWidget):
    def __init__(self,text,superparent,filelocation,rowcount):
        super(UNKNOWNnode,self).__init__()
        self.calculatedwidth = 100
        if (int(len(str(text))*8))>100:
            self.calculatedwidth = int(len(str(text))*7)
        self.resize(self.calculatedwidth,80)
        self.row=rowcount
        self.setMaximumSize(self.calculatedwidth,40)
        self.superparent=superparent
        self.filelocation = filelocation
        self.setMouseTracking(True)
        self.ismouseover=False
        self.highlight = QColor(69,71,97)
        self.type = filelocation.split(".")[-1]
        self.NodeLabel = QLabel()
        self.NodeLabel.setText(str(text).upper())
        self.NodeLabel.setStyleSheet('color:black')
        self.bolder= QFont("Times",9,QFont.Bold)
        self.NodeLabel.setFont(self.bolder)
        self.vbox = QVBoxLayout()
        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.NodeLabel)
        self.vbox.addLayout(self.vbox1)
        self.setLayout(self.vbox)
        self.repaint()

    def paintEvent(self,e):
        canvas = QPainter()
        canvas.begin(self)
        self.draw(canvas)
        canvas.setRenderHint(QPainter.Antialiasing)
        canvas.end()
        
    def draw(self,canvas):
        size = self.size()
        width = size.width()
        height = size.height()
        canvas.setBrush(QBrush(QColor(10,20,30)))
        canvas.drawRect(-1,-1,width+1,height+1)
        grad=QLinearGradient(QPointF(int(width/2),0),QPointF(int(width/2),height))
        grad.setColorAt(0,QColor(100,100,100))
        grad.setColorAt(1, QColor(50,50,50))
        canvas.setBrush(QBrush(grad))
        canvas.drawRect(5,5,width-10,height-10)
            
    def mousePressEvent(self,event):
        self.superparent.selectedfilelocation = self.filelocation
        self.superparent.selectediconrow  = self.row
        self.superparent.catchselection(self.type)

class SRAnode(QWidget):
    def __init__(self,text,superparent,filelocation,rowcount):
        super(SRAnode,self).__init__()
        self.calculatedwidth = 100
        if (int(len(str(text))*8))>100:
            self.calculatedwidth = int(len(str(text))*8)
        self.resize(self.calculatedwidth,80)
        self.row=rowcount
        self.setMaximumSize(self.calculatedwidth,40)
        self.superparent=superparent
        self.filelocation = filelocation
        self.setMouseTracking(True)
        self.ismouseover=False
        self.highlight = QColor(69,71,97)
        self.type = filelocation.split(".")[-1]
        self.NodeLabel = QLabel()
        self.NodeLabel.setText(str(text).upper())
        self.NodeLabel.setStyleSheet('color:black')
        self.bolder= QFont("Times",8,QFont.Bold)
        self.NodeLabel.setFont(self.bolder)
        self.vbox = QVBoxLayout()
        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.NodeLabel)
        self.vbox.addLayout(self.vbox1)
        self.setLayout(self.vbox)
        self.repaint()
        
    def mouseMoveEvent(self,event):
        self.highlight = QColor(0,180,200)
        self.repaint()
        
    def leaveEvent(self,event):
        self.highlight = QColor(69,71,97)
        self.repaint()

    def paintEvent(self,e):
        canvas = QPainter()
        canvas.begin(self)
        self.draw(canvas)
        canvas.setRenderHint(QPainter.Antialiasing)
        canvas.end()
        
    def draw(self,canvas):
        size = self.size()
        width = size.width()
        height = size.height()
        canvas.setBrush(QBrush(self.highlight))
        canvas.drawRect(-1,-1,width+1,height+1)
        grad=QLinearGradient(QPointF(int(width/2),0),QPointF(int(width/2),height))
        grad.setColorAt(0,QColor(102,205,170))
        grad.setColorAt(1, QColor(0,128,128))
        canvas.setBrush(QBrush(grad))
        canvas.drawRect(5,5,width-10,height-10)
            
    def mousePressEvent(self,event):
        self.superparent.selectedfilelocation = self.filelocation
        self.superparent.selectediconrow  = self.row
        self.superparent.catchselection(self.type)

        
class FASTQnode(QWidget):
    def __init__(self,text,superparent,filelocation,rowcount):
        super(FASTQnode,self).__init__()
        self.calculatedwidth = 100
        if (int(len(str(text))*8))>100:
            self.calculatedwidth = int(len(str(text))*8)
        self.resize(self.calculatedwidth,80)
        self.row=rowcount
        self.setMaximumSize(self.calculatedwidth,40)
        self.superparent=superparent
        self.filelocation = filelocation
        self.setMouseTracking(True)
        self.ismouseover=False
        self.highlight = QColor(69,71,97)
        self.color=QColor(255,255,255)
        self.type = filelocation.split(".")[-1]
        self.NodeLabel = QLabel()
        self.NodeLabel.setText(str(text).upper())
        self.NodeLabel.setStyleSheet('color:black')
        self.bolder= QFont("Times",8,QFont.Bold)
        self.NodeLabel.setFont(self.bolder)
        self.vbox = QVBoxLayout()
        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.NodeLabel)
        self.vbox.addLayout(self.vbox1)
        self.setLayout(self.vbox)
        self.repaint()

    def mouseMoveEvent(self,event):
        self.highlight = QColor(0,180,200)
        self.repaint()
        
    def leaveEvent(self,event):
        self.highlight = QColor(69,71,97)
        self.repaint()

    def paintEvent(self,e):
        canvas = QPainter()
        canvas.begin(self)
        self.draw(canvas)
        canvas.setRenderHint(QPainter.Antialiasing)
        canvas.end()
        
    def draw(self,canvas):
        size = self.size()
        width = size.width()
        height = size.height()
        canvas.setBrush(QBrush(self.highlight))        
        canvas.drawRect(-1,-1,width+1,height+1)
        grad=QLinearGradient(QPointF(int(width/2),0),QPointF(int(width/2),height))
        grad.setColorAt(0,QColor(0,255,127))
        grad.setColorAt(1, QColor(50,205,50))
        canvas.setBrush(QBrush(grad))
        canvas.drawRect(5,5,width-10,height-10)
            
    def mousePressEvent(self,event):
        self.superparent.selectedfilelocation = self.filelocation
        self.superparent.selectediconrow  = self.row
        self.superparent.catchselection(self.type)

class HTMLnode(QWidget):
    def __init__(self,text,superparent,filelocation,rowcount):
        super(HTMLnode,self).__init__()
        self.calculatedwidth = 180
        self.resize(self.calculatedwidth,100)
        self.row=rowcount
        self.setMaximumSize(self.calculatedwidth,100)
        self.setMinimumSize(self.calculatedwidth,100)
        self.superparent=superparent
        self.filelocation = filelocation
        self.setMouseTracking(True)
        self.ismouseover=False
        self.highlight = QColor(69,71,97)
        self.color=QColor(255,255,255)
        self.type = filelocation.split(".")[-1]
        self.NodeLabel = QLabel()
        self.detail1 = QLabel()
        self.NodeLabel.setText(str(text).upper())
        self.NodeLabel.setStyleSheet('color:black')
        self.detail1.setStyleSheet('color:black')
        self.bolder= QFont("Times",8,QFont.Bold)
        self.light= QFont("Times",9)
        self.NodeLabel.setFont(self.bolder)
        self.detail1.setFont(self.light)
        self.vbox = QVBoxLayout()
        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.NodeLabel)
        self.vbox1.addWidget(self.detail1)
        self.vbox.addLayout(self.vbox1)
        self.setLayout(self.vbox)
        self.repaint()
        self.configurehtmlnode()

    def configurehtmlnode(self):
        htmlfile = self.filelocation.split("/")[-1]
        croppedname = htmlfile.split(".")[0]
        htmldirectory = os.path.dirname(self.filelocation)
        textfile = htmldirectory+"/"+croppedname+"/fastqc_data.txt"
        if os.path.exists(self.filelocation):
            if os.path.exists(textfile):
                with open(textfile) as file:
                    basicstat = [next(file) for x in range(11)]
                    self.detail1.setText(basicstat[6]+basicstat[8]+basicstat[9])
                        
            else:
                self.detail1.setText("Data File Not Found")
        else:
            self.detail1.setText("HTML File Not Found")
        
    def mouseMoveEvent(self,event):
        self.highlight = QColor(0,180,200)
        self.repaint()
        
    def leaveEvent(self,event):
        self.highlight = QColor(69,71,97)
        self.repaint()

    def paintEvent(self,e):
        canvas = QPainter()
        canvas.begin(self)
        self.draw(canvas)
        canvas.setRenderHint(QPainter.Antialiasing)
        canvas.end()
        
    def draw(self,canvas):
        size = self.size()
        width = size.width()
        height = size.height()
        canvas.setBrush(QBrush(self.highlight))        
        canvas.drawRect(-1,-1,width+1,height+1)
        grad=QLinearGradient(QPointF(int(width/2),0),QPointF(int(width/2),height))
        grad.setColorAt(0,QColor(255,0,127))
        grad.setColorAt(1, QColor(205,50,50))
        canvas.setBrush(QBrush(grad))
        canvas.drawRect(5,5,width-10,height-10)
            
    def mousePressEvent(self,event):
        self.superparent.selectedfilelocation = self.filelocation
        self.superparent.selectediconrow  = self.row
        self.superparent.catchselection(self.type)



    
        
