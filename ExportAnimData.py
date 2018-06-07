import os
import maya.mel as mel
import maya.cmds as cmds
import time
from PySide2 import QtWidgets

cmds.loadPlugin("AbcExport.mll",qt=1)

def publishAnim():    
    allNS= cmds.namespaceInfo(lon=1,r=1)
    defaultNS = ["UI","shared"]
    others = [ns for ns in allNS if ns not in defaultNS]
    maxTime = str(int(cmds.playbackOptions(q=1,max=1)))
    minTime = str(int(cmds.playbackOptions(q=1,min=1)))
    frameRate = cmds.currentUnit(q=1,t=1)
    
    #both are the same, some Maya doesn't work with cmds.file(q=1, sceneName=1)
    #currentFileNameList = cmds.file(q=1,sceneName =1 ).split("/")[-1].split(".")[0]
    currentFileNameList = cmds.file(q=1,l=1)[0].split("/")[-1].split(".")[0]
    extension = cmds.file(q=1,l=1)[0].split("/")[-1].split(".")[-1]
    abcOutPath = cmds.workspace(fileRuleEntry="abcOut")     
    nsInfo = cmds.namespaceInfo(lon=1,r=1)  
    splitFileName = currentFileNameList.split("_")

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
        return
    
        #----------------------------------------------------------------------

    list = ["sq","sc"]
    for ind, q in enumerate(splitFileName):
        if q.isalpha() == False: #check if there are any words (words like trailer, teaser or rnd)
            if ind == 1: #take the 1st and 2nd index (for sequence and scene)
                abcOutPath += "/%s"%list[0] + splitFileName[ind]
            if ind == 2:
                abcOutPath += "/%s"%list[1] + splitFileName[ind]

    for i in currentFileNameList.split("_"):
        if "sh" in i:
            abcOutPath += "/%s" %i
            continue
            
    if not os.path.exists(abcOutPath):
        os.makedirs(abcOutPath)
        
    namespaceList=[]
    for a in nsInfo:
        if a == 'UI' or a == 'shared':
            continue
        else:
            namespaceList.append(a)

    transformList=[]
    pConstraint=[]
    for nc in cmds.ls(type="nurbsCurve"):
        nctrans = cmds.listRelatives(nc, type="transform",p=1,f=1)[0]
        if "objType" in cmds.listAttr(nctrans):
            if cmds.getAttr("%s.objType"%nctrans) == "ctrl":              
                transformList.append(nctrans)
                if "blendParent1" in cmds.listAttr(nctrans):
                    for const in cmds.listConnections(nctrans,type="constraint",d=1,s=0):
                        if ":" not in const:
                            pConstraint.append(const)
                
        if len(transformList) == 0:
            continue

    cmds.bakeResults(transformList,sm=1,t=(int(cmds.playbackOptions(q=1,min=1)),int(cmds.playbackOptions(q=1,max=1))),sb=1,osr=1,rba=0,dic=1,pok=1,sac=0,ral=0,bol=0,mr=1,cp=0,s=0)
    cmds.delete(pConstraint)

    start = time.time() 
    for i in namespaceList:
        animCurveObj=[]  
        for j in cmds.ls("%s:*"%i,type="nurbsCurve"):
            transform = cmds.listRelatives(j,type="transform",p=1,f=1)[0]
            if "objType" in cmds.listAttr(transform):
                if cmds.getAttr("%s.objType"%transform) == "ctrl":
                    animNode = cmds.listConnections(transform,type="animCurve",d=0)
                    if animNode != None:
                        for obj in animNode:
                            animCurveObj.append(obj)

        for ind,curveObj in enumerate(animCurveObj):
            dest = cmds.listConnections(curveObj,d=1,c=0,p=1)[0]
            
            if "animDest" not in cmds.listAttr(curveObj):
                cmds.addAttr(curveObj,longName="animDest",dataType="string",keyable=1)

            cmds.setAttr("%s.animDest"%curveObj,lock=0)
            cmds.setAttr("%s.animDest"%curveObj,dest,type="string")
            cmds.setAttr("%s.animDest"%curveObj,lock=1)
            
            if "preInfinity" in cmds.listAttr(curveObj):
            
                cmds.setAttr("%s.preInfinity"%curveObj,lock=0)
                cmds.setAttr("%s.preInfinity"%curveObj,4)
                cmds.setAttr("%s.preInfinity"%curveObj,lock=1)
                
        if len(animCurveObj)>0:
            cmds.select(animCurveObj)
            if extension == "ma":
                if ":" in i:
                    cmds.file((abcOutPath+"/"+i.split(":")[-1]+"Anim"),f=1,op="v=0",typ = "mayaAscii",pr=1,es=1) #Export Animation Curve Data
                    end = time.time()
                    print "Animation data exported in ",(end-start),"seconds"
                    start = time.time()
                else:
                    cmds.file((abcOutPath+"/"+i+"Anim"),f=1,op="v=0",typ = "mayaAscii",pr=1,es=1) #Export Animation Curve Data
                    end = time.time()
                    print "Animation data exported in ",(end-start),"seconds"
                    start = time.time()
                    
            elif extension == "mb":
                if ":" in i:
                    cmds.file((abcOutPath+"/"+i.split(":")[-1]+"Anim"),f=1,op="v=0",typ = "mayaBinary",pr=1,es=1) #Export Animation Curve Data
                    end = time.time()
                    print "Animation data exported in ",(end-start),"seconds"
                    start = time.time()
                else:
                    cmds.file((abcOutPath+"/"+i+"Anim"),f=1,op="v=0",typ = "mayaBinary",pr=1,es=1) #Export Animation Curve Data
                    end = time.time()
                    print "Animation data exported in ",(end-start),"seconds"
                    start = time.time()
                
            else:
                print "file type unknown, can't be exported"
                continue
        else:
            pass
                            
    for ns in others:
        objString = ''
        if cmds.namespaceInfo(ns,lod=1,dp=1) == None:
            continue
        for obj in cmds.namespaceInfo(ns,lod=1,dp=1):        
            if "objType" in cmds.listAttr(obj) and cmds.objectType(obj,i="transform"):
                if cmds.getAttr("%s.objType"%obj) == "geometry" or cmds.getAttr("%s.objType"%obj) == "sets": 
                    objString+= (" -root " + obj)
        if objString == '':
            continue        
        finalString = "AbcExport -j \"-frameRange %s %s -attr objType -attrPrefix rs -stripNamespaces -dataFormat ogawa -uvWrite -attrPrefix xgen -writeVisibility -worldSpace%s -file %s\"" %(minTime,maxTime,objString,abcOutPath+"/"+ns.split(":")[-1]+".abc")
        mel.eval(finalString)

    objString = ''
    for cam in allCam:
        objString = ''
        transformNode = cmds.listRelatives(cam,parent =1,type = "transform" )[0]
        if "objType" in cmds.listAttr(transformNode):
            if cmds.getAttr("%s.objType"%transformNode) == "camera": 
                objString+= (" -root " + transformNode)
        if objString == '':
            continue
        finalString = "AbcExport -j \"-frameRange %s %s -attr objType -attrPrefix rs -attrPrefix rman -stripNamespaces -dataFormat ogawa -uvWrite -attrPrefix xgen -worldSpace%s -file %s\"" %(minTime,maxTime,objString,abcOutPath+"/"+transformNode.split(":")[-1]+"_cam.abc")
        mel.eval(finalString)
        
    publishBox = QtWidgets.QMessageBox()
    publishBox.setIcon(QtWidgets.QMessageBox.Information)
    publishBox.setWindowTitle("Information")
    publishBox.setText("Your files have been published successfully!")
    publishBox.setInformativeText("Please check them at their designated location.")
    publishBox.exec_()
    return
        
publishAnim()
