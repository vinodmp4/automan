"""
    Created at 01/04/2018
    Created by Vinod M P
    Created for KERALA UNIVERSITY
    Created under MASSIVE DATA ANALYTICS
"""

# AUTOMAN CUSTOM WIDGETS
import sys
import DIALOG,XML
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# 1. LIST BOX

class listitem(QWidget):
    def __init__(self,name,flag,superparent,parent):
        super(listitem,self).__init__()
        self.resize(100,75)
        self.superparent=superparent
        self.parent=parent
        self.setMouseTracking(True)
        self.ismouseover=False
        self.color=QColor(99,101,127)
        self.type = flag
        self.projectname = QLabel()
        self.projectname.setText(str(name))
        self.projectname.setStyleSheet('color:white')
        self.bolder= QFont("Times",12,QFont.Bold)
        self.lighter =QFont("Times",9)
        self.projectname.setFont(self.bolder)
        self.projectname.setAlignment(Qt.AlignCenter)
        self.hbox = QHBoxLayout()
        self.vbox2 = QVBoxLayout()
        self.vbox2.addWidget(self.projectname)
        self.hbox.addLayout(self.vbox2)
        self.setLayout(self.hbox)
        self.setbackground()
        
    def mouseMoveEvent(self,event):
        if self.ismouseover==False:
            self.ismouseover=True
            self.color=QColor(0,180,200)
            self.setbackground()
            
    def leaveEvent(self,event):
        if self.ismouseover==True:
            self.ismouseover=False
            self.color=QColor(99,101,127)
            self.setbackground()
    def mousePressEvent(self,event):
        if self.type=="new":
            DIALOG.askprojectname(self.superparent)
            self.parent.hide()
        elif self.type=="open":
            dialog1 = QFileDialog()
            dialog1.setFileMode(QFileDialog.ExistingFile)
            dialog1.setFilter("AutoMan Project (*.xml)")
            if dialog1.exec_():
                filename = dialog1.selectedFiles()[0]
                XML.loadproject(self.superparent,filename)
                if not(self.superparent.projectarray[0][0]=="") and (type("text")==type(self.superparent.projectarray[0][0])):
                    self.superparent.currentprojectname = self.superparent.projectarray[0][0]
                    self.superparent.currentprojectdirectory = filename
                    self.superparent.setWindowTitle("AutoMan - "+self.superparent.currentprojectname)
                    self.superparent._loadproject()
                    self.parent.hide()
                else:
                    QMessageBox.information(self,"Info","Invalid or Broken File")
                
        else:
            sys.exit()
            
    def setbackground(self):
        self.setAutoFillBackground(True)
        Palette = self.palette()
        Palette.setColor(self.backgroundRole(),self.color)
        self.setPalette(Palette)
        
class listbox(QWidget):
    def __init__(self,superparent,parent):
        super(listbox,self).__init__()
        self.resize(400,75)
        self.setMinimumSize(400,75)
        self.setMaximumSize(400,75)
        self.setMouseTracking(True)
        self.new = listitem("NEW","new",superparent,parent)
        self.open = listitem("OPEN", "open",superparent,parent)
        self.quit = listitem("QUIT", "quit",superparent,parent)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.new)
        self.hbox.addWidget(self.open)
        self.hbox.addWidget(self.quit)
        self.setLayout(self.hbox)
        
class newproject(QDialog):
    def __init__(self,parent):
        super().__init__()
        self.resize(500,300)
        self.setMinimumSize(500,250)
        self.setMaximumSize(500,250)
        self.setWindowTitle("AutoMan")
        self.setBackground()
        self.list = listbox(parent,self)
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("./images/automanlogo.png"))
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.vbox.addWidget(self.logo)
        self.vbox.addWidget(self.list)
        self.hbox.addLayout(self.vbox)
        self.setLayout(self.hbox)

    def setBackground(self):            # Window Background Color
        self.setAutoFillBackground(True)
        Palette = self.palette()
        Palette.setColor(self.backgroundRole(),QColor(49,51,77))
        self.setPalette(Palette)
        
    def closeEvent(self,event):
        sys.exit()
        
def splashwindow(superparent):
    window=newproject(superparent)
    window.exec_()
