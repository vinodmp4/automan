# 1. About
#------------------------------------------#

"""
    Created on 01/04/2018
    Created by Vinod M P
    Created for MASSIVE DATA ANALYTICS

"""
# 2. Variables
#------------------------------------------#

"""
    **--------------------------------------------------
    
    **********
     > ONLY GLOBAL VARIABLES EXPLAINED <
     > LOCAL VARIABLES NOT EXPLAINED <
     
    **********
    
    INTEGER

    1)  currenttabindex : Index of current tab
    2)  selectediconindex : Index of current icon
    3)  selectediconrow : Row of selected icon

    STRING
    
    4)  currenttabname : Name of current tab
    5)  currentprojectdirectory : Current working directory
    6)  currentprojectname : Name of current project
    7)  currentprojecttype : Type of current project
    8)  selectedfilelocation : filelocation of selected icon

    PYQT

    9)  Color : Window color
    10) mainMenu : Menu bar
    11) programbar : dynamic toolbar
    12) statusbar : Status bar
    13) tabcontrol : Main work area
    14) toolbar : toolbar
    

    ARRAYS
    
    11) iconsarray : array of all icons (only used when updating tabs)
    12) programicons : array hold toolbar icons (used for updating toolbar)
    13) projectarray : Array form of saved data
    14) selectedfilelocation : filelocation of selected icon
    15) tabarray : Tabs data (subset of project array)

    **--------------------------------------------------

"""

# 2. Methods
#------------------------------------------#

"""
    **--------------------------------------------------

    DIRECT METHODS
    
    1)  mainwindow         : QMainWindow class
    2)  __init__           : initializing method
    3)  initialize         : initialize main GUI
    4)  properties         : initialize variables
    5)  container          : initialize GUI Frame
    6)  settoolbar         : default toolbar initializing
    7)  menuevents         : menu bar initializing
    8)  setBackground      : background color setting
    9)  onloading          : launch splash window
    10) reportmessage      : single window medium for message reporting
    11) distributearray    : on loading data values in project array is assigned to other variables
    12) convergearray      : on saving data values in other variables are repacked into project array
    13) refreshtabpage     : refresh tab on file adding
    14) _registeraction    : single window medium for log registering
    15) changeprogramtools : dynamically changes program toolbar
    16) catchselection     : catch and process type of selected file icon
    17) loadprogramicons   : program toolbar icon initializing
    18) closeEvent         : ask for confirmation before closing (saved data?)

    MENUBAR / TOOLBAR METHODS

    19) _addnewdata        : Handle actions on load and download data
    20) _appendnewdata     : used to append new file
    21) _addnewtab         : handle actions while adding a new tab
    22) _removetab         : handle actions while removing a tab
    23) _saveproject       : handle actions while saving data
    24) _loadproject       : handle actions while loading a saved project
    25) _downloadsra       : used to download new sra file
    26) downloadsra        : check whether tab present before downloading sra
    27) addnewtab          : add a new tab
    28) showlogs           : view activity log of current tab
    29) autoinfo           : Info about AutoMan
    30) browsefile         : check whether tab present before loading data
    31) _browsefile        : used to load new data
    32) _newproject        : handle actions to create new project
    33) _openproject       : handle actions to open existing project
    34) _closeproject      : handle actions to close current project
    35) _convertsra        : pointer method to initiate sra convertion
    36) _analysefastq      : pointer method to analyse fatsq file
    37) _viewhtml          : pointer method to view html file
    38) _trimfastq         : pointer method to trim fastq file
    39) _clipfastq         : pointer method to clip fastq file

    40) mainloop           : holds required actions to run the application
    

    **--------------------------------------------------

"""

# 4. Source Code
#------------------------------------------#

"""
A. IMPORTING MODULES

    A. 1. IN-BUILT MODULES
    
"""

import os,sys,ntpath,datetime,threading
import urllib.request

""" A. 2. THIRD-PARTY MODULES """

from PyQt4.QtGui import *
from PyQt4.QtCore import *

""" A. 3. CUSTOM-MADE MODULES """
import TABCONTROL,ICONS,DIALOG,WEB,SPLASH,XML,FUNCTIONS,HTML,LOG
"""
B. MAIN CLASS

"""

class mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize()
        self.showMaximized()

    def initialize(self):
        self.centralWidget = QWidget(self)
        self.toolbar = self.addToolBar("Basic Tools")
        self.programbar = self.addToolBar("Programs")
        self.statusbar = self.statusBar()
        self.settoolbar()
        self.properties()
        self.container()
        self.setBackground()
        self.onloading()
        self.menuevents()

    def properties(self):
        self.setWindowTitle("AutoMan")
        self.resize(650,400)
        self.color = QColor(49,51,77)
        self.tabcontrol = TABCONTROL.tabcontrol(self)
        self.currentprojectname = ""
        self.currentprojecttype = ""
        self.projectarray = []
        self.tabarray = []
        self.selectedfilelocation = ""
        self.selectediconrow = 0
        self.currenttabname = ""
        self.currenttabindex = -1
        self.iconsarray = []
        self.selectediconindex = 0
        self.currentprojectdirectory = "./"
        self.programicons = []
        self.loadprogramicons()

    def container(self):
        self.vbox = QVBoxLayout()
        self.vbox.setSpacing(0)
        self.vbox.setMargin(0)
        self.vbox.addWidget(self.tabcontrol)
        self.centralWidget.setLayout(self.vbox)
        self.setCentralWidget(self.centralWidget)

    def settoolbar(self):
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolbar.setStyleSheet("background-color: rgb(255, 255, 255);")
        browsefile = QAction(QIcon("./images/browse.png"),"Browse File",self)
        downloadfile = QAction(QIcon("./images/download.png"),"Download SRA",self)
        newtabz = QAction(QIcon("./images/newtab.png"),"New Tab",self) 
        infomenu = QAction(QIcon("./images/log.png"),"Log Data",self)
        self.toolbar.addAction(browsefile)
        self.toolbar.addSeparator()
        self.toolbar.addAction(downloadfile)
        self.toolbar.addSeparator()
        self.toolbar.addAction(newtabz)
        self.toolbar.addSeparator()
        self.toolbar.addAction(infomenu)
        browsefile.triggered.connect(self.browsefile)
        downloadfile.triggered.connect(self.downloadsra)
        newtabz.triggered.connect(self.addnewtab)
        infomenu.triggered.connect(self.showlogs)

    def menuevents(self):
        newproj = QAction("New Project",self)
        openproj = QAction("Open Project",self)
        closeproj = QAction("Close Project",self)
        browsefile = QAction("Add New",self)
        downloadfile = QAction("Download SRA",self)
        appclose = QAction("&Quit",self)
        addtab = QAction("Add Tab",self)
        removetab = QAction("Remove Tab",self)
        tablog = QAction("Tab Log",self)
        aboutautoman = QAction("AutoMan",self)
        newproj.triggered.connect(self._newproject)
        openproj.triggered.connect(self._openproject)
        closeproj.triggered.connect(self._closeproject)
        browsefile.triggered.connect(self.browsefile)
        downloadfile.triggered.connect(self.downloadsra)
        appclose.setShortcut("Ctrl+Q")
        appclose.triggered.connect(sys.exit)
        addtab.triggered.connect(self.addnewtab)
        removetab.triggered.connect(self._removetab)
        tablog.triggered.connect(self.showlogs)
        aboutautoman.triggered.connect(self.autoinfo)

        mainMenu = self.menuBar()
        filemenu = mainMenu.addMenu("&File")
        editmenu = mainMenu.addMenu("&Edit")
        viewmenu = mainMenu.addMenu("&View")
        aboutmenu = mainMenu.addMenu("&About")
        filemenu.addAction(newproj)
        filemenu.addAction(openproj)
        filemenu.addAction(closeproj)
        filemenu.addAction(browsefile)
        filemenu.addAction(downloadfile)
        filemenu.addAction(appclose)
        editmenu.addAction(addtab)
        editmenu.addAction(removetab)
        viewmenu.addAction(tablog)
        aboutmenu.addAction(aboutautoman)

    def setBackground(self):
        self.setAutoFillBackground(True)
        Palette = self.palette()
        Palette.setColor(self.backgroundRole(),self.color)
        self.setPalette(Palette)

        #-----------------------------------------------

    def onloading(self):
        if self.currentprojectname=="":
            SPLASH.splashwindow(self)

    def reportmessage(self,message):
        QMessageBox.information(self,"Info",message)

    def distributearray(self):
        arraysize = len(self.projectarray)
        if arraysize > 0:
            self.currentprojectname = self.projectarray[0][0]
            self.currentprojecttype = self.projectarray[0][1]
            if arraysize > 1:
                for i in range(1,arraysize):
                    self.tabarray.append(self.projectarray[i])

    def convergearray(self):
        mainarray = []
        projectproperties = []
        projectproperties.append(self.currentprojectname)
        projectproperties.append(self.currentprojecttype)
        projectproperties.append("1.0")
        mainarray.append(projectproperties)
        for i in range(0,len(self.tabarray)):
            mainarray.append(self.tabarray[i])
        self.projectarray = mainarray
        

    def refreshtabpage(self):
        if self.currenttabindex >= 0:
            tabindex = self.currenttabindex
            tabname = self.tabarray[tabindex][0][0]
            iconarray = ICONS.iconmanager(self,self.tabarray[tabindex][1])
            tabpage = TABCONTROL.tabpage(self,iconarray.ICON_ARRAY)
            self.tabcontrol.removetab()
            self.tabcontrol.insertTab(tabindex,tabpage,tabname)
            self.tabcontrol.setCurrentIndex(tabindex)

    def _addnewdata(self,filelocation): #common for both browse-n-load and download
        filearray = []
        filearray.append(filelocation)
        self.tabarray[self.currenttabindex][1].append(filearray)
        self.refreshtabpage()
        self._saveproject()

    def _appendnewdata(self,filelocation,row,tabindex): #used to append new file
        self.tabcontrol.setCurrentIndex(tabindex)
        if filelocation in self.tabarray[tabindex][1][row]:
            pass
        else:
            self.tabarray[tabindex][1][row].append(filelocation)
            self.refreshtabpage()
            self._saveproject()

    def _addnewtab(self,name):
        timestamp = datetime.datetime.now()
        virtualtab = []
        virtualtabproperties = []
        virtualtabproperties.append(name)
        tablog = []
        tablog.append(("Tab with alias "+name+" was added successfully at "+str(timestamp)))
        virtualtabproperties.append(tablog)
        virtualtab.append(virtualtabproperties)
        virtualtab.append([]) # an empty array representing section array (2D ARRAY)
        self.tabarray.append(virtualtab)
        iconarray = ICONS.iconmanager(self,[])
        tabpage = TABCONTROL.tabpage(self,iconarray.ICON_ARRAY)
        self.tabcontrol.addtab(tabpage,name)
        self._saveproject()

    def _removetab(self):
        choice = QMessageBox.question(self,"Confirm","This action can't be undone.\nAre you sure?",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            del self.tabarray[self.currenttabindex]
            self.tabcontrol.removeTab(self.currenttabindex)
            self._saveproject()
        else:
            pass

        
    def _registeraction(self,logtext):
        timestamp = datetime.datetime.now()
        self.tabarray[self.currenttabindex][0][1].append(str(logtext)+" at "+str(timestamp))
        self._saveproject()
        

    def _saveproject(self):
        self.convergearray()
        XML.writeproject(self.projectarray,self.currentprojectdirectory)

    def _loadproject(self): # called only once when loading a saved project
        for tabs in self.tabarray:
            iconarray = ICONS.iconmanager(self,tabs[1])
            tabpage = TABCONTROL.tabpage(self,iconarray.ICON_ARRAY)
            self.tabcontrol.addtab(tabpage,tabs[0][0])

    def _downloadsra(self):
        WEB.showdownloader(self,os.path.dirname(self.currentprojectdirectory))

    def downloadsra(self):
        if len(self.tabarray)>0:
            self._downloadsra()
        else:
            self.addnewtab()
            self._downloadsra()
    
    def addnewtab(self):
        DIALOG.asktabname(self)

    def showlogs(self):
        timestamp = datetime.datetime.now()
        if (len(self.tabarray)>0):
            text = ""
            num = 1
            for log in self.tabarray[self.currenttabindex][0][1]:
                text = text+"\n"+str(num)+"\t"+str(log)
                num = num + 1
            LOG.showlog(text)
        else:
            QMessageBox.information(self,"Info","Nothing to show at "+str(timestamp))

    def autoinfo(self):
        QMessageBox.information(self,"AutoMan version 0.010","AutoMan Project\nVersion 0.010 pre-alpha release\nData format version 1.0\nOwned by Massive Data Analytics 2018")

    def browsefile(self):
        if len(self.tabarray)>0:
            self._browsefile()
        else:
            self.addnewtab()
            self._browsefile()
            
    def _browsefile(self):
        dialog1 = QFileDialog()
        dialog1.setFileMode(QFileDialog.AnyFile)
        dialog1.setFilter("Fastq files (*.fastq);;SRA files (*.sra);;All Files (*.sra *.fastq)")
        if dialog1.exec_():
            filenames = dialog1.selectedFiles()
            for files in filenames:
                self._addnewdata(files)
                self._registeraction(files+" was loaded into the project")

    def _newproject(self):
        DIALOG.askprojectname(self)

    def _openproject(self):
        prev_file = self.currentprojectdirectory
        dialog1 = QFileDialog()
        dialog1.setFileMode(QFileDialog.ExistingFile)
        dialog1.setFilter("AutoMan Project (*.xml)")
        if dialog1.exec_():
            filename = dialog1.selectedFiles()[0]
            XML.loadproject(self,filename)
            if not(self.projectarray[0][0]=="") and (type("text")==type(self.projectarray[0][0])):
                self.currentprojectname = self.projectarray[0][0]
                self.currentprojectdirectory = filename
                self.setWindowTitle("AutoMan - "+self.currentprojectname)
                for i in range(0,self.tabcontrol.count()):
                    self.tabcontrol.removeTab(0)
                self.tabarray=[]
                self.distributearray()
                self._loadproject()
            else:
                QMessageBox.information(self,"Info","Invalid or Broken File")
                XML.loadproject(self,prev_file)
                self.currentprojectname = self.projectarray[0][0]
                self.currentprojectdirectory = filename
                self.setWindowTitle("AutoMan - "+self.currentprojectname)
                for i in range(0,self.tabcontrol.count()):
                    self.tabcontrol.removeTab(0)
                self.tabarray=[]
                self.distributearray()
                self._loadproject()
                
    def _closeproject(self):
        self.currentprojectname = ""
        self.currentprojecttype = ""
        self.projectarray = []
        self.tabarray = []
        self.selectedfilelocation = ""
        self.selectediconrow = 0
        self.currenttabname = ""
        self.currenttabindex = -1
        self.iconsarray = []
        self.selectediconindex = 0
        self.currentprojectdirectory = "./"
        for i in range(0,self.tabcontrol.count()):
            self.tabcontrol.removeTab(0)
        self.onloading()
            

    def changeprogramtools(self,index):
        self.programbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.programbar.setStyleSheet("background-color: rgb(255, 255, 255);")
        for i in range(0,len(self.programicons)):
            for j in range(0,len(self.programicons[i])):
                self.programbar.removeAction(self.programicons[i][j])
        for tools in range(0,len(self.programicons[index])):
            self.programbar.addAction(self.programicons[index][tools])

    def catchselection(self,filetype):
        if filetype == "sra":
            self.changeprogramtools(0)
        elif filetype == "fastq":
            self.changeprogramtools(1)
        elif filetype == "html":
            self.changeprogramtools(2)
        else:
            pass

    def loadprogramicons(self):
        sraprogram1 = QAction(QIcon("./images/convert.png"),"Convert SRA",self)
        fastqprogram1 = QAction(QIcon("./images/fastqc.png"),"Check Quality",self)
        fastqprogram2 = QAction(QIcon("./images/trim.png"),"Trim",self)
        fastqprogram3 = QAction(QIcon("./images/clip.png"),"Clip",self)
        htmlprogram1 = QAction(QIcon("./images/viewhtml.png"),"View Report",self)
        sraprogram1.triggered.connect(self._convertsra)
        fastqprogram1.triggered.connect(self._analysefastq)
        fastqprogram2.triggered.connect(self._trimfastq)
        fastqprogram3.triggered.connect(self._clipfastq)
        htmlprogram1.triggered.connect(self._viewhtml)
        forsra = []
        forfastq = []
        forhtml = []
        forsra.append(sraprogram1)
        forfastq.append(fastqprogram1)
        forfastq.append(fastqprogram2)
        forfastq.append(fastqprogram3)
        forhtml.append(htmlprogram1)
        self.programicons.append(forsra)
        self.programicons.append(forfastq)
        self.programicons.append(forhtml)

    def _convertsra(self):
        datadir = os.path.dirname(self.currentprojectdirectory)+"/Data"
        sramanager = FUNCTIONS.sraconvertor(self,self.selectedfilelocation,datadir,self.selectediconrow,self.currenttabindex)
        sramanager.startconvertion()
    def _analysefastq(self):
        datadir = os.path.dirname(self.currentprojectdirectory)+"/Data"
        fastqmanager = FUNCTIONS.fastqc(self,self.selectedfilelocation,datadir,self.selectediconrow,self.currenttabindex)
        fastqmanager.run()
    def _viewhtml(self):
        HTML.showhtml(self.selectedfilelocation)
    def _trimfastq(self):
        datadir = os.path.dirname(self.currentprojectdirectory)+"/Data"
        DIALOG.fastxwindow1(self,self.selectedfilelocation,datadir,self.selectediconrow,self.currenttabindex)
    def _clipfastq(self):
        datadir = os.path.dirname(self.currentprojectdirectory)+"/Data"
        DIALOG.fastxwindow2(self,self.selectedfilelocation,datadir,self.selectediconrow,self.currenttabindex)

        #-----------------------------------------------

    def closeEvent(self,event):
        choice = QMessageBox.question(self,"Confirm","Are you sure to quit the app?",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def mainloop():
    application=QApplication(sys.argv)
    window = mainwindow()
    window.show()
    sys.exit(application.exec_())

if __name__ == "__main__":
    mainloop()
