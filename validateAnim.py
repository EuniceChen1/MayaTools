import os
import maya.cmds as cmds
from PySide2 import QtWidgets

allNS= cmds.namespaceInfo(lon=1,r=1)
defaultNS = ["UI","shared"]
others = [ns for ns in allNS if ns not in defaultNS]

allCam = cmds.ls(type = "camera",l=1)
defaultCam = ['backShape','bottomShape','leftShape','frontShape', 'perspShape','sideShape', 'topShape']
allCam = [cam for cam in allCam if cam.split("|")[-1] not in defaultCam]

#--------------------------VALIDATION--------------------------------------
informationRig = ""
informationCam = ""
informationText = ""
for q in allNS:
    if "rig" in q:
        i=q.split(":")
        if len(i) >= 2 and "_rig" not in i[0]:
            informationRig += (q+";"+"\n" )
            
if len(allCam) > 1:
    for finalCam in allCam:
        cleanUpCam = finalCam.split("|")[-1]   
        informationCam += (cleanUpCam+";"+"\n" )
        
numOfCam = len(allCam)

if informationRig != "" or informationCam != "":
    if informationRig != "" and informationCam == "":
        informationText += ("Please clean up namespace"+"\n"+informationRig)
        
    elif informationCam != "" and informationRig == "":
        informationText += ("%s Cameras in the Scene"%numOfCam+"\n"+"Please clean up camera"+"\n"+informationCam)
    
    elif informationRig != "" and informationCam != "" :
        informationText += ("Please clean up namespace"+"\n\n"+informationRig+"\n"+"Please clean up camera. ( %s cameras in the scene )"%numOfCam+"\n\n"+informationCam)
    
    msgBox = QtWidgets.QMessageBox()
    msgBox.setIcon(QtWidgets.QMessageBox.Warning)
    msgBox.setWindowTitle("Alert!")
    msgBox.setText("Validation Error!")
    msgBox.setInformativeText("Publish unsuccessful."+"\n\n"+informationText)
    msgBox.exec_()
