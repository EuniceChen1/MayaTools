validMat=[]
#SET ATTRIBUTE
assetName = cmds.file(query=1,sceneName=1).split("_")[-2]    

for q in cmds.ls(sl=1,type = "shadingEngine"):
    allString = ""
    #print cmds.listConnections(q,type="mesh")
    if "MatID" not in cmds.listAttr(q) and "AssetID" not in cmds.listAttr(q):
        
        cmds.addAttr(q,longName = "MatID",dataType="string", keyable=0)
        cmds.addAttr(q,longName = "AssetID",dataType="string", keyable=0)
    
            
    listConn = cmds.listConnections(q,type="mesh")
    if listConn != None:
        validMat.append(q)
        for conn in listConn:
            allString += (conn+";")

    cmds.setAttr("%s.MatID"%q,lock=0)
    cmds.setAttr("%s.AssetID"%q,lock=0)   
    
    cmds.setAttr("%s.MatID"%q,allString,type="string")
    cmds.setAttr("%s.AssetID"%q,assetName,type="string")
    
    cmds.setAttr("%s.MatID"%q,lock=1)
    cmds.setAttr("%s.AssetID"%q,lock=1)    


cmds.select(validMat,ne=1)
if len(validMat) <1:
    cmds.warning("No valid selections.")
