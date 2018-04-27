import os
import maya.cmds as cmds


for abc in cmds.ls(type = "AlembicNode"):#abc = cmds.ls(sl=1)[0]
    #list meshes created by abc file
    meshList = cmds.listConnections(abc,type="mesh")
    
    for mesh in meshList:
        #cmds.setAttr("%s.visibility"%mesh,1)
        if mesh.split("|")[-1] == "MESH NAME":
            cmds.setAttr("%s.visibility"%mesh,0)
