import maya.cmds as cmds
import os

nsInfo = cmds.namespaceInfo(lon=1,r=1)
namespaceList=[]
for a in nsInfo:
    if a == 'UI' or a == 'shared':
        continue
    else:
        namespaceList.append(a)
        
cfxList = []
shdList = []
for k in namespaceList:
    for grp in cmds.ls("%s:*_grp"%k,type="transform",l=1):
        if "hair" in grp.split(":")[0]:
            cfxList.append(grp.split("|")[1]) 
             
        elif "shd" in  grp.split(":")[0]:
            shdList.append(grp.split("|")[-1]) 

for deformed in set(cfxList):
    cmds.setAttr("%s.visibility"%deformed,0)
    for ori in set(shdList):
        if deformed.split(":")[-1] == ori.split(":")[-1]:
            cmds.select(deformed,r=1)
            cmds.select(ori,add=1)
            cmds.blendShape()
            cmds.select(clear=1)  
        else:
            continue

topLevelGrp = []
for ns in namespaceList:
    for blended in cmds.listRelatives("%s:*_grp"%ns,type="transform",f=1,c=1):
        if "hair" in blended.split(":")[0]:
            topLevelGrp.append(blended.split("|")[1])
            if "grp" not in blended.split(":")[-1]:
                if cmds.ls(type="blendShape") != None:
                    for bs in cmds.ls(type="blendShape"):
                        cmds.select(blended.split("|")[-1],r=1)
                        cmds.select("%s"%bs,af=1)
                        for tp in list(set(topLevelGrp)):
                            try:
                                cmds.setAttr("%s.%s"%(bs,tp.split(":")[-1]),1)
                            except:
                                pass

#get maya hair system and set attribute for curve attraction
mayaHairList = []
for ns in namespaceList:
    for blended in cmds.listRelatives("%s:*"%ns,type="transform",f=1,c=1):
        if "MayaHairSystem" in blended:
            mayaHairList.append(blended.split("|")[-1])
                                  
for mayaHair in mayaHairList:
    cmds.setAttr("%s.attractionScale[1].attractionScale_Position"%mayaHair,1)
    cmds.setAttr("%s.attractionScale[1].attractionScale_FloatValue"%mayaHair,1)
    cmds.setAttr("%s.startCurveAttract"%mayaHair,1)
        

