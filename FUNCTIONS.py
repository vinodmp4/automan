"""
    Created at 12/04/2018
    Created by Vinod M P
    Created for KERALA UNIVERSITY
    Created under MASSIVE DATA ANALYTICS
"""

import os,threading

class sraconvertor:
        def __init__(self,superparent,inputurl,outputdirectory,row,tabindex):
                super().__init__()
                self.superparent = superparent
                self.inputurl = inputurl
                self.outputurl = outputdirectory
                self.outputfilelocation = ""
                self.row = row
                self.flag = False
                self.tabindex = tabindex

        def _convertsra(self):
                inputfilelocation = os.path.abspath(self.inputurl)
                inputfile = self.inputurl.split("/")[-1]
                outputfile = inputfile[:-3]+"fastq"
                outputfilelocation = self.outputurl+"/"+outputfile
                self.outputfilelocation = outputfilelocation
                command = "./Plugins/NCBI/fastq-dump -O "+self.outputurl+" "+inputfilelocation
                report = os.system(command)
                if report == 0:
                    self.flag = True
                else:
                    pass
                
        def startconvertion(self):
                NewThread = threading.Thread(target = self._convertsra)
                NewThread.start()
                msg = "Started Converting "+self.inputurl.split("/")[-1]
                self.superparent.reportmessage(msg)
                NewThread.join()
                msg = "Finished Converting "+self.inputurl.split("/")[-1]
                if self.flag:
                    self.superparent._appendnewdata(self.outputfilelocation,self.row,self.tabindex)
                    self.superparent._registeraction("Converted "+self.inputurl+" into fastq")
                self.superparent.reportmessage(msg)
                
                

class fastqc:
        def __init__(self,superparent,inputurl,outputdirectory,row,tabindex):
                super().__init__()
                self.superparent = superparent
                self.inputurl = inputurl
                self.outputurl = outputdirectory
                self.row = row
                self.outputfilelocation = ""
                self.flag = False
                self.tabindex = tabindex

        def _fastqcrun(self):
                inputfilelocation = os.path.abspath(self.inputurl)
                inputfile = self.inputurl.split("/")[-1]
                outputfilename = inputfile.split(".")[0]
                outputfile = outputfilename+"_fastqc.html"
                outputfilelocation = self.outputurl+"/"+outputfile
                self.outputfilelocation = outputfilelocation
                command = "./Plugins/FastQC/fastqc "+inputfilelocation+" --extract --outdir "+self.outputurl
                report = os.system(command)
                if report == 0:
                    self.flag = True
                else:
                    pass
        
        def run(self):
                NewThread = threading.Thread(target = self._fastqcrun)
                NewThread.start()
                msg = "Started Analysing "+self.inputurl.split("/")[-1]
                self.superparent.reportmessage(msg)
                NewThread.join()
                msg = "Finished Analysing "+self.inputurl.split("/")[-1]
                self.superparent.reportmessage(msg)
                if self.flag:
                    self.superparent._appendnewdata(self.outputfilelocation,self.row,self.tabindex)
                    self.superparent._registeraction("Analysed "+self.inputurl+" using fastqc")

class fastxtrim:
        def __init__(self,parent,superparent,inputurl,outputdirectory,row,tabindex,phread,first,last):
                super().__init__()
                self.parent = parent
                self.superparent = superparent
                self.inputurl = inputurl
                self.outputurl = outputdirectory
                self.row = row
                self.phread= phread
                self.first = first
                self.last = last
                self.outputfilelocation = ""
                self.flag = False
                self.tabindex = tabindex

        def _fastxrun(self):
                inputfilelocation = os.path.abspath(self.inputurl)
                inputfile = self.inputurl.split("/")[-1]
                outputfilename = inputfile.split(".")[0]
                outputfile = outputfilename+"_trim.fastq"
                outputfilelocation = self.outputurl+"/"+outputfile
                self.outputfilelocation = outputfilelocation
                command = "./Plugins/FastX/fastx_trimmer -Q "+self.phread+" -f "+self.first+" -l "+self.last+" -i "+inputfilelocation+" -o "+self.outputfilelocation
                report = os.system(command)
                if report == 0:
                    self.flag = True
                else:
                    pass
        
        def run(self):
                NewThread = threading.Thread(target = self._fastxrun)
                NewThread.start()
                msg = "Started trimming "+self.inputurl.split("/")[-1]
                self.superparent.reportmessage(msg)
                NewThread.join()
                msg = "Finished trimming "+self.inputurl.split("/")[-1]
                self.superparent.reportmessage(msg)
                if self.flag:
                    self.superparent._appendnewdata(self.outputfilelocation,self.row,self.tabindex)
                    self.superparent._registeraction("Trimmed "+self.inputurl+" using fastx_trimmer (-f "+self.first+" -l "+self.last+" )")
                    self.parent.hide()

class fastxclip:
        def __init__(self,parent,superparent,inputurl,outputdirectory,row,tabindex,phread,discard,adapter):
                super().__init__()
                self.parent = parent
                self.superparent = superparent
                self.inputurl = inputurl
                self.outputurl = outputdirectory
                self.row = row
                self.phread= phread
                self.discard = discard
                self.adapter = adapter
                self.outputfilelocation = ""
                self.flag = False
                self.tabindex = tabindex

        def _fastxrun(self):
                inputfilelocation = os.path.abspath(self.inputurl)
                inputfile = self.inputurl.split("/")[-1]
                outputfilename = inputfile.split(".")[0]
                outputfile = outputfilename+"_clip.fastq"
                outputfilelocation = self.outputurl+"/"+outputfile
                self.outputfilelocation = outputfilelocation
                command = "./Plugins/FastX/fastx_clipper -v -Q "+self.phread+" -l "+self.discard+" -a "+self.adapter+" -i "+inputfilelocation+" -o "+self.outputfilelocation
                report = os.system(command)
                if report == 0:
                    self.flag = True
                else:
                    pass
        
        def run(self):
                NewThread = threading.Thread(target = self._fastxrun)
                NewThread.start()
                msg = "Started clipping "+self.inputurl.split("/")[-1]
                self.superparent.reportmessage(msg)
                NewThread.join()
                msg = "Finished clipping "+self.inputurl.split("/")[-1]
                self.superparent.reportmessage(msg)
                if self.flag:
                    self.superparent._appendnewdata(self.outputfilelocation,self.row,self.tabindex)
                    self.superparent._registeraction("Clipped "+self.inputurl+" using fastx_clipper (-discard below "+self.discard+" -adapter "+self.adapter+" )")
                    self.parent.hide()

                
                
