
import os, sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import FUNCTIONS

class nameproject(QDialog):
    def __init__(self,superparent):
        super().__init__()
        self.resize(300,200)
        self.setWindowTitle("NEW PROJECT")
        self.setBackground()
        self.superparent = superparent
        self.label1 = QLabel()
        self.label1.setText('Name:')
        self.label2 = QLabel()
        self.label2.setText('Project Type:')
        self.textarea = QLineEdit(self)
        self.combobox = QComboBox()
        self.combobox.addItem("DNA-seq")
        self.combobox.addItem("RNA-seq")
        self.combobox.addItem("ChIP-seq")
        self.combobox.addItem("Methyl-Seq")
        self.button1 = QPushButton("Create",self)
        self.button2 = QPushButton("Cancel",self)
        self.button1.clicked.connect(self.create)
        self.button2.clicked.connect(self.cancel)
        self.label1.setStyleSheet('color:white')
        self.label2.setStyleSheet('color:white')
        self.textarea.setStyleSheet('background-color:white')
        self.vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.hbox1.addWidget(self.label1)
        self.hbox1.addWidget(self.textarea)
        self.hbox3.addWidget(self.label2)
        self.hbox3.addWidget(self.combobox)
        self.hbox2.addWidget(self.button1)
        self.hbox2.addWidget(self.button2)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addLayout(self.hbox2)
        self.setLayout(self.vbox)

    def create(self,event):
        invalidchars = [" ","\\","/",",",".","$",":","*","?","\"","<",">","!","@","#","~","-",
                        "`","%","^","&","+","=",";","'",".{","}","[","]","|","0","1","2","3","4","5","6","7","8","9"]
        projectname = str(self.textarea.text())
        projecttype = str(self.combobox.currentText())
        ok = True
        for chars in invalidchars:
            if chars in projectname:
                ok = False
        directory = "./Projects/"+projectname+"/"
        subdir1 = directory+"Genome"
        subdir2 = directory+"Pipeline"
        subdir3 = directory+"Data"
        xmlfile = directory+projectname+".xml"
        datatowrite = "<automan><project><name>"+projectname+"</name><type>"+projecttype+"</type><version>1.0</version></project></automan>"
        if ((not os.path.exists(directory)) and (ok)):
            os.makedirs(directory)
            os.makedirs(subdir1)
            os.makedirs(subdir2)
            os.makedirs(subdir3)
            fopen = open(xmlfile,"w+")
            fopen.write(datatowrite)
            fopen.close()
            self.superparent.currentprojectname = self.textarea.text()
            self.superparent.currentprojecttype = projecttype
            self.superparent.currentprojectdirectory = directory
            self.superparent.setWindowTitle("AutoMan - "+self.superparent.currentprojectname)
            self.superparent.projectarray = []
            self.superparent.tabarray = []
            self.superparent.selectedfilelocation = ""
            self.superparent.selectediconrow = 0
            self.superparent.currenttabname = ""
            self.superparent.currenttabindex = -1
            self.superparent.iconsarray = []
            self.superparent.selectediconindex = 0
            for i in range(0,self.superparent.tabcontrol.count()):
                self.superparent.tabcontrol.removeTab(0)
            self.hide()
        else:
            if ok:
                QMessageBox.information(self,"Info","Similar project already exist")
            else:
                QMessageBox.information(self,"Info","Project name should not contain invalid characters")
        
    def cancel(self,event):
        self.hide()

    def setBackground(self):            # Window Background Color
        self.setAutoFillBackground(True)
        Palette = self.palette()
        Palette.setColor(self.backgroundRole(),QColor(49,51,77))
        self.setPalette(Palette)

class nametab(QDialog):
    def __init__(self,superparent):
        super().__init__()
        self.resize(300,200)
        self.setWindowTitle("NEW TAB")
        self.setBackground()
        self.superparent = superparent
        self.label1 = QLabel()
        self.label1.setText('Name:')
        self.textarea = QLineEdit(self)
        self.button1 = QPushButton("Create",self)
        self.button2 = QPushButton("Cancel",self)
        self.button1.clicked.connect(self.create)
        self.button2.clicked.connect(self.cancel)
        self.label1.setStyleSheet('color:white')
        self.textarea.setStyleSheet('background-color:white')
        self.vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox1.addWidget(self.label1)
        self.hbox1.addWidget(self.textarea)
        self.hbox2.addWidget(self.button1)
        self.hbox2.addWidget(self.button2)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.setLayout(self.vbox)

    def create(self,event):
        invalidchars = ["\\","/",",",".","$",":","*","?","\"","<",">","!","@","#","~",
                        "`","%","^","&","+","=",";","'",".{","}","[","]","|"]
        tabname = str(self.textarea.text())
        ok = True
        for chars in invalidchars:
            if chars in tabname:
                ok = False
        if ok:
            self.superparent.currenttabname = self.textarea.text()
            self.superparent._addnewtab(self.superparent.currenttabname)
            self.hide()
        else:
            QMessageBox.information(self,"Info","Tab name should not contain invalid characters")
        
    def cancel(self,event):
        self.hide()

    def setBackground(self):            # Window Background Color
        self.setAutoFillBackground(True)
        Palette = self.palette()
        Palette.setColor(self.backgroundRole(),QColor(49,51,77))
        self.setPalette(Palette)

class fastxtrim(QDialog):
    def __init__(self,superparent,inputfile,outputdir,row,tabindex):
        super().__init__()
        self.resize(300,200)
        self.setMinimumSize(300,200)
        self.setMaximumSize(300,200)
        self.setWindowTitle("Trim Fastq")
        self.setBackground()
        self.inputfile = inputfile
        self.outputdir = outputdir
        self.row = row
        self.tabindex = tabindex
        self.superparent = superparent
        self.label1 = QLabel()
        self.label1.setText('Phred:')
        self.textarea1 = QComboBox()
        self.textarea1.addItem("33")
        self.textarea1.addItem("64")
        self.label2 = QLabel()
        self.label2.setText('Begin:')
        self.textarea2 = QLineEdit(self)
        self.label3 = QLabel()
        self.label3.setText('End:')
        self.textarea3 = QLineEdit(self)
        self.button1 = QPushButton("Trim",self)
        self.button2 = QPushButton("Cancel",self)
        self.button1.clicked.connect(self.trim)
        self.button2.clicked.connect(self.cancel)
        self.label1.setStyleSheet('color:white')
        self.textarea1.setStyleSheet('background-color:white')
        self.label2.setStyleSheet('color:white')
        self.textarea2.setStyleSheet('background-color:white')
        self.label3.setStyleSheet('color:white')
        self.textarea3.setStyleSheet('background-color:white')
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.vbox1 = QVBoxLayout()
        self.vbox2 = QVBoxLayout()
        self.vbox1.addWidget(self.label1)
        self.vbox1.addWidget(self.label2)
        self.vbox1.addWidget(self.label3)
        self.vbox2.addWidget(self.textarea1)
        self.vbox2.addWidget(self.textarea2)
        self.vbox2.addWidget(self.textarea3)
        self.hbox1.addWidget(self.button1)
        self.hbox1.addWidget(self.button2) 
        self.hbox.addLayout(self.vbox1)
        self.hbox.addLayout(self.vbox2)
        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.hbox1)
        self.setLayout(self.vbox)

    def trim(self,event):
        numarray = ["0","1","2","3","4","5","6","7","8","9"]
        canrun = True
        isint = True
        if (self.textarea2.text() == "") or (self.textarea3.text() == ""):
            QMessageBox.information(self,"Info","Empty parameters not allowed")
            canrun = False
        fulltext = self.textarea2.text()+self.textarea3.text()
        for i in fulltext:
            if not(i in numarray):
                canrun = False
                isint = False
        if canrun:
            trimm = FUNCTIONS.fastxtrim(self,self.superparent,self.inputfile,self.outputdir,self.row,
                              self.tabindex,self.textarea1.currentText(),self.textarea2.text(),self.textarea3.text())
            trimm.run()
        else:
            if not isint:
                QMessageBox.information(self,"Info","Only integer type parameters allowed")
        
    def cancel(self,event):
        self.hide()

    def setBackground(self):            # Window Background Color
        self.setAutoFillBackground(True)
        Palette = self.palette()
        Palette.setColor(self.backgroundRole(),QColor(49,51,77))
        self.setPalette(Palette)

class fastxclip(QDialog):
    def __init__(self,superparent,inputfile,outputdir,row,tabindex):
        super().__init__()
        self.resize(300,200)
        self.setMinimumSize(300,200)
        self.setMaximumSize(300,200)
        self.setWindowTitle("Fastx Clipper")
        self.setBackground()
        self.inputfile = inputfile
        self.outputdir = outputdir
        self.row = row
        self.tabindex = tabindex
        self.superparent = superparent
        self.label1 = QLabel()
        self.label1.setText('Phred Quality:')
        self.textarea1 = QComboBox()
        self.textarea1.addItem("33")
        self.textarea1.addItem("64")
        self.label2 = QLabel()
        self.label2.setText('Discard Sequence below:')
        self.textarea2 = QLineEdit(self)
        self.label3 = QLabel()
        self.label3.setText('Adapter Sequence:')
        self.textarea3 = QLineEdit(self)
        self.button1 = QPushButton("Clip",self)
        self.button2 = QPushButton("Cancel",self)
        self.button1.clicked.connect(self.clip)
        self.button2.clicked.connect(self.cancel)
        self.label1.setStyleSheet('color:white')
        self.textarea1.setStyleSheet('background-color:white')
        self.label2.setStyleSheet('color:white')
        self.textarea2.setStyleSheet('background-color:white')
        self.label3.setStyleSheet('color:white')
        self.textarea3.setStyleSheet('background-color:white')
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.vbox1 = QVBoxLayout()
        self.vbox2 = QVBoxLayout()
        self.vbox1.addWidget(self.label1)
        self.vbox1.addWidget(self.label2)
        self.vbox1.addWidget(self.label3)
        self.vbox2.addWidget(self.textarea1)
        self.vbox2.addWidget(self.textarea2)
        self.vbox2.addWidget(self.textarea3)
        self.hbox1.addWidget(self.button1)
        self.hbox1.addWidget(self.button2) 
        self.hbox.addLayout(self.vbox1)
        self.hbox.addLayout(self.vbox2)
        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.hbox1)
        self.setLayout(self.vbox)

    def clip(self,event):
        canrun = True
        if (self.textarea2.text() == "") or (self.textarea3.text() == ""):
            QMessageBox.information(self,"Info","Empty parameters not allowed")
            canrun = False
        if canrun:
            clip = FUNCTIONS.fastxclip(self,self.superparent,self.inputfile,self.outputdir,self.row,
                              self.tabindex,self.textarea1.currentText(),self.textarea2.text(),self.textarea3.text())
            clip.run()
        
    def cancel(self,event):
        self.hide()

    def setBackground(self):            # Window Background Color
        self.setAutoFillBackground(True)
        Palette = self.palette()
        Palette.setColor(self.backgroundRole(),QColor(49,51,77))
        self.setPalette(Palette)

def fastxwindow2(superparent,inputfile,outputdir,row,tabindex):
    window=fastxclip(superparent,inputfile,outputdir,row,tabindex)
    window.exec_()

def fastxwindow1(superparent,inputfile,outputdir,row,tabindex):
    window=fastxtrim(superparent,inputfile,outputdir,row,tabindex)
    window.exec_()

def asktabname(superparent):
    window=nametab(superparent)
    window.exec_()

def askprojectname(superparent):
    window=nameproject(superparent)
    window.exec_()
        
