import maya.cmds as cmds
import os

allabc = cmds.ls(type="AlembicNode")

for q in allabc:
    getPath=cmds.getAttr("%s.abc_File"%q)
    splitPath=getPath.split("/")
    
    #SPECIFY A CERTAIN NAME IF WANT TO REPATH FILES FROM DIFFERENT LOCATION
    if "deck" in splitPath:
        setPath=cmds.setAttr("%s.abc_File"%q,"YOUR_PATH"+splitPath[-1],type="string")
        
    elif "ground" in splitPath:
        setPath=cmds.setAttr("%s.abc_File"%q,"YOUR_PATH"+splitPath[-1],type="string")
        
    else:
        print "something is wrong!!!"
