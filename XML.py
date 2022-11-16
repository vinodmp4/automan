
import os, random
import xml.etree.ElementTree as ET
from PyQt4.QtGui import *

def loadconfiguration(sender,filelocation):
    try:
        xmlfile = filelocation
        xmldata = ET.parse(xmlfile)
        root = xmldata.getroot()
        color = root[0]
        red = color[0].text
        green = color[1].text
        blue = color[2].text
    except:
        red = 255
        green = 255
        blue = 255

    parent.color=QColor(int(red),int(green),int(blue))

def loadproject(parent,filelocation):
    try:
        invalidfiles = []
        xmldata = ET.parse(filelocation)
        root = xmldata.getroot()
        projectdata = root[0]
        projectname = projectdata[0].text
        projecttype = projectdata[1].text
        version = projectdata[2].text
        mainarray = []
        projectinfo = []
        projectinfo.append(projectname)
        projectinfo.append(projecttype)
        projectinfo.append(version)
        mainarray.append(projectinfo)
        tabcount = len(root)-1
        if tabcount>0:
            for tab in range(1,len(root)):
                tabdata = []
                currenttab = root[tab]
                tabproperties = currenttab[0]
                tabname = tabproperties[0].text
                tablog=[]
                if len(tabproperties)>1:
                    if len(tabproperties[1])>0:
                        for logs in range(0,len(tabproperties[1])):
                            tablog.append(tabproperties[1][logs].text)
                tabdata.append([tabname,tablog])
                sectioncount = len(currenttab)-1
                if sectioncount>0:
                    sectioncollection = []
                    for section in range(0,len(currenttab[1])):
                        filecount = len(currenttab[1][section])
                        if filecount>0:
                            filecollection = []
                            for file in range(0,filecount):
                                if os.path.exists(currenttab[1][section][file].text):
                                    filecollection.append(currenttab[1][section][file].text)
                                else:
                                    invalidfiles.append(currenttab[1][section][file].text)
                                    filecollection.append(currenttab[1][section][file].text)
                        sectioncollection.append(filecollection)
                tabdata.append(sectioncollection)
                mainarray.append(tabdata)
            if len(invalidfiles)>0:
                text = "Files not Found"
                for files in invalidfiles:
                    text = text +"\n"+files
                parent.reportmessage(text)
            else:
                pass
    except:
        proj = []
        proj.append("")
        proj.append("")
        proj.append("1.0")
        mainarray=[]
        mainarray.append(proj)
    parent.projectarray = mainarray
    parent.distributearray()

def writeproject(projectarray,filelocation):
    try:
        root = ET.Element("automan")
        projectinfo = projectarray[0]
        projectname = projectinfo[0]
        projecttype = projectinfo[1]
        version = projectinfo[2]
        _projectinfo = ET.SubElement(root,"project")
        _projectname = ET.SubElement(_projectinfo,"name")
        _projecttype = ET.SubElement(_projectinfo,"type")
        _version = ET.SubElement(_projectinfo,"version")
        _projectname.text = projectname
        _projecttype.text = projecttype
        _version.text = version
        if len(projectarray)>1:
            for tab in range(1,len(projectarray)):
                currenttab = projectarray[tab]
                tabproperties = currenttab[0]
                tabname = tabproperties[0]
                _currenttab = ET.SubElement(root,"tab")
                _tabproperties = ET.SubElement(_currenttab,"properties")
                _tabname = ET.SubElement(_tabproperties,"name")
                _tabname.text = tabname
                tablogs = tabproperties[1]
                _tablogs = ET.SubElement(_tabproperties,"log")
                if len(tablogs)>0:
                    for log in range(0,len(tablogs)):
                        logtext = tablogs[log]
                        _log = ET.SubElement(_tablogs,"entry")
                        _log.text = logtext
                if len(currenttab)>1:
                    sectioncollection = currenttab[1]
                    _sectioncollection = ET.SubElement(_currenttab,"sections")
                    if len(sectioncollection)>0:
                        for section in range(0,len(sectioncollection)):
                            filecollection = sectioncollection[section]
                            _filecollection = ET.SubElement(_sectioncollection,"files")
                            if len(filecollection)>0:
                                for file in range(0,len(filecollection)):
                                    _file = ET.SubElement(_filecollection,"file")
                                    _file.text =filecollection[file]
        fileopen = open(filelocation,"w+")
        fileopen.write(ET.tostring(root).decode("UTF-8"))
        fileopen.close()
        result=1
    except:
        result=0
    return result

def loadtips(parent):
    try:
        xmlfile = './tips.xml'
        xmldata = ET.parse(xmlfile)
        root = xmldata.getroot()
        count=root[0].text
        randnum = random.randint(0,(int(count)-1))
        tips = root[1][randnum].text
    except:
        tips = "No tips Found"

    parent.tips = str(tips)

#------------------------------------------------
#------------------------------------------------
