import os
import sys
import maya.cmds as cmds
from PySide2 import QtCore
from PySide2 import QtWidgets

class AutoPlayblast(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        hbox = QtWidgets.QFormLayout()
        
        self.setGeometry(250, 150, 250, 100)
        self.setMaximumSize(QtCore.QSize(250, 250))
        self.setWindowTitle('Auto Playblast')
        
        #Path Label
        self.geoLabel = QtWidgets.QLabel('Enter Body Part Name: ', self)
        hbox.addWidget(self.geoLabel)

        #Line Edit
        self.geoLine = QtWidgets.QLineEdit()
        self.geoLine.setMaxLength(50)
        hbox.addWidget(self.geoLine)
        
        self.versionLabel = QtWidgets.QLabel('Enter File Version: ', self)
        hbox.addWidget(self.versionLabel)

        #Line Edit
        self.versionLine = QtWidgets.QLineEdit()
        self.versionLine.setMaxLength(2)
        hbox.addWidget(self.versionLine)
        
        #OK Button
        self.OKBt = QtWidgets.QPushButton('OK')
        hbox.addWidget(self.OKBt)
        self.setLayout(hbox)
        
        #CONNECTIONS
        self.OKBt.clicked.connect(self.playblastFunc)
        self.versionLine.returnPressed.connect(self.playblastFunc)
        
    def playblastFunc(self):
            
        self.extension = cmds.file(q=1,l=1)[0].split(".")[-1]
        bodypart = (self.geoLine.text()).lower()
        version = self.versionLine.text()
        
        if version.isalpha() == True:
            versionBox = QtWidgets.QMessageBox()
            versionBox.setIcon(QtWidgets.QMessageBox.Information)
            versionBox.setWindowTitle("Information")
            versionBox.setText("Version must be a number")
            versionBox.exec_()
            return
            
        if "v" in version:
            versionBox = QtWidgets.QMessageBox()
            versionBox.setIcon(QtWidgets.QMessageBox.Information)
            versionBox.setWindowTitle("Information")
            versionBox.setText("Version must be number only")
            versionBox.exec_()
            return
            
        if len(bodypart) == 0:
            self.filename = r"C:/mnt/animation/JUEJI/submission/dailies"+"_".join(cmds.file(q=1,l=1)[0].split("work")[-1].split(".")[0].split("_")[:-1])+"_"+"v"+"%02d"%int(version)+".mov"
            
        else:
            if bodypart.isalpha() == True:
                self.filename = r"C:/mnt/animation/JUEJI/submission/dailies"+"_".join(cmds.file(q=1,l=1)[0].split("work")[-1].split(".")[0].split("_")[:-1])+"_"+"%s"%bodypart+"_"+"v"+"%02d"%int(version)+".mov"
            else:
                bodypartBox = QtWidgets.QMessageBox()
                bodypartBox.setIcon(QtWidgets.QMessageBox.Information)
                bodypartBox.setWindowTitle("Information")
                bodypartBox.setText("Body Part Input is incorrect. Should have letters only")
                bodypartBox.exec_()
        
        versionBox = QtWidgets.QMessageBox()
        versionBox.setIcon(QtWidgets.QMessageBox.Information)
        versionBox.setWindowTitle("Information")
        versionBox.setText("Confirm playblast?")
        versionBox.setInformativeText(self.filename)
        versionBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        versionBox.setDefaultButton(QtWidgets.QMessageBox.Yes)
        response = versionBox.exec_()
        
        if response == QtWidgets.QMessageBox.Yes:
            print "playblasting ",self.filename
            if os.path.exists(self.filename):
                overwriteBox = QtWidgets.QMessageBox()
                overwriteBox.setIcon(QtWidgets.QMessageBox.Information)
                overwriteBox.setWindowTitle("Information")
                overwriteBox.setText("File exists")
                overwriteBox.setInformativeText("Overwrite file?")
                overwriteBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                overwriteBox.setDefaultButton(QtWidgets.QMessageBox.Yes)
                overwrite = overwriteBox.exec_()
                if overwrite == QtWidgets.QMessageBox.Yes:
                    cmds.playblast(f=self.filename, format="qt", sqt=0, cc=1, v=1, orn=1, fp=4, p=100, c='H.264', qlt=100, wh = [1920, 1080], fo=1)
            else:
                cmds.playblast(f=self.filename, format="qt", sqt=0, cc=1, v=1, orn=1, fp=4, p=100, c='H.264', qlt=100, wh = [1920, 1080])
        else:
            return


dialog = AutoPlayblast()        
dialog.show()
