# 1. ABOUT
#---------------------------------------#
"""
    Created at 04/04/2018
    Created by Vinod M P
    Created for MASSIVE DATA ANALYTICS

    NCBI Link will look like
    ftp://ftp-trace.ncbi.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR304/SRR304976/SRR304976.sra

    Common part in this link for all files is
    "ftp://ftp-trace.ncbi.nih.gov/sra/sra-instant/reads/ByRun/sra"

    After the common part [SRR/ERR/DRR] based on first three letters of RUN ACCESSION CODE
    next part contain first six letters of RUN ACCESSION CODE
    followed by another part contain the RUN ACCESSION CODE as full
    final part contain the [RUN ACCESSION CODE].sra

"""

# 2. SOURCE CODE
#---------------------------------------#

import os, sys, time, threading
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ftplib import FTP


class sradownloader(QDialog):
    def __init__(self,superparent,output):
        super().__init__()
        self.resize(400,150)
        self.setMinimumSize(400,150)
        self.setMaximumSize(400,150)
        self.superparent = superparent
        self.outputdir = output
        self.output=''
        self.accession =""
        self.progress = 0
        self.filesize = 0
        self.downdata = 0
        self.progressloop = True
        self.downloadok = False
        self.setWindowTitle("SRA Downloader")
        self.titlelabel = QLabel(self)
        self.titlelabel.setText("Enter SRA run accession to continue:")
        self.statuslabel = QLabel(self)
        self.statuslabel.setText("Status: Ready")
        self.progressbar = QProgressBar(self)
        self.downloadbutton = QPushButton("Download",self)
        self.downloadbutton.clicked.connect(self.verify)
        self.textbox = QLineEdit(self)
        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.hbox.addWidget(self.textbox)
        self.hbox.addWidget(self.downloadbutton)
        self.vbox.addWidget(self.titlelabel)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.progressbar)
        self.vbox.addWidget(self.statuslabel)
        self.setLayout(self.vbox)
        self.setBackground()
        
    def setBackground(self):            # Window Background Color
        self.setAutoFillBackground(True)
        Palette = self.palette()
        Palette.setColor(self.backgroundRole(),QColor(49,51,77))
        self.setPalette(Palette)
        self.titlelabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.statuslabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.textbox.setStyleSheet("background-color: rgb(255, 255, 255);")

    def generateoutput(self,accession):
        self.output = self.outputdir+"/Data/"+accession+".sra"

    def connect(self,accession):
        directory = '/sra/sra-instant/reads/ByRun/sra/'+accession[:3]+'/'+accession[:6]+'/'+accession+'/'
        ftp = FTP('ftp-trace.ncbi.nih.gov')
        ftp.login()
        ftp.cwd(directory)
        ftp.sendcmd("TYPE i")
        return ftp
    
    def run(self):
        attempts = 5
        filename = self.accession+".sra"
        ftp = self.connect(self.accession)
        file = open(self.output, 'wb')
        size = ftp.size(filename)
        self.filesize = size
        while True:
            try:
                ftp.retrbinary('RETR '+filename, file.write)
                break
            except:
                if attempts != 0:
                    ftp = self.connect(self.accession)
                    attempts -= 1
                else:
                    break
        file.close()
        ftp.close()
        self.progressloop = False
                
    def progressupdate(self):
        while self.progressloop:
            if self.filesize>0:
                self.progress = int((os.path.getsize(self.output)/self.filesize)*100)
                if self.progress<100:
                    self.progressbar.setValue(self.progress)
                    time.sleep(1)
            time.sleep(1)
            
    def outputprogress(self):
        if (self.filesize != 0) and ((os.path.getsize(self.output)) != self.filesize):
            self.statuslabel.setText("Status: Downloading Failed")
            self.superparent._registeraction("Connection lost result in an error downloading "+str(self.url))
                
        else:
            self.progressbar.setValue(100)
            self.statuslabel.setText("Status: Download successfully completed")
            self.downloadok = True
    
    def verify(self):
        self.accession = self.textbox.text().upper()
        self.generateoutput(self.accession)
        self.statuslabel.setText("Status: Download started")
        self.superparent._registeraction("Initiated downloading "+self.accession)
        self.downloadbutton.setEnabled(False)
        try:
            thr1 = threading.Thread(target=self.run)
            thr1.start()
            thr2 = threading.Thread(target=self.progressupdate)
            thr2.start()
            thr1.join()
            thr2.join()
            self.outputprogress()
            
        except:
            self.statuslabel.setText("Status: An error occured while downloading.")
        self.downloadbutton.setEnabled(True)
        try:
            if self.downloadok:
                self.superparent._addnewdata(self.output)
                self.superparent._registeraction("Downloaded "+self.accession+" successfully")
                self.hide()
        except:
            self.statuslabel.setText("Status: Download completed but can't append file.")


def showdownloader(superparent,outputdirectory):
    window = sradownloader(superparent,outputdirectory)
    window.exec_()

            
