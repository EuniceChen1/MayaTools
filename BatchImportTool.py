import os
import os
import maya.cmds as cmds

def exportShader (*n):## define renderable mesh objType to 'geometry' 
    validMat=[]
    #SET ATTRIBUTE
    assetFileName = cmds.file(query=1,sceneName=1).split("/")[-1] 
    assetName = assetFileName.split(".")[0]   
    
    shdSavePath = cmds.workspace(fileRuleEntry = 'shdOut')
    
    for q in cmds.ls(type = "shadingEngine"):
        allString = ""
        #print cmds.listConnections(q,type="mesh")
        if "ShapeID" not in cmds.listAttr(q) and "AssetID" not in cmds.listAttr(q):
            
            cmds.addAttr(q,longName = "ShapeID",dataType="string", keyable=0)
            cmds.addAttr(q,longName = "AssetID",dataType="string", keyable=0)
        
                
        listConn = cmds.listConnections(q,type="mesh")
        
        
        if listConn == None:
            continue
            
        for conn in listConn:
            if "objType" in cmds.listAttr(conn):
                if cmds.getAttr("%s.objType"%conn) == "geometry" or cmds.getAttr("%s.objType"%conn) == "sets":
                    allString += (conn+";")
                    validMat.append(q)
    
        cmds.setAttr("%s.ShapeID"%q,lock=0)
        cmds.setAttr("%s.AssetID"%q,lock=0)   
        
        cmds.setAttr("%s.ShapeID"%q,allString,type="string")
        cmds.setAttr("%s.AssetID"%q,assetName,type="string")
        
        cmds.setAttr("%s.ShapeID"%q,lock=1)
        cmds.setAttr("%s.AssetID"%q,lock=1)    
    
    validMat = list(set(validMat))
    cmds.select(validMat,ne=1)
    ##Export redshift AOV
    if len(cmds.ls(type = "RedshiftOptions"))>0:
        cmds.select(cmds.ls(type= "RedshiftAOV"),add=1)
        
    if len(validMat) <1:
        #print validMat,cmds.ls(sl=1)
        cmds.warning("No valid selections.")
    
    else:
        cmds.file(shdSavePath+"/"+assetFileName.replace("rig","shd"),f=1,op="v=0;",typ = "mayaAscii",pr=1,es=1)    

def linkAllShader(*n): #no selection needed
    for abc in cmds.ls(type = "mesh"):#abc = cmds.ls(sl=1)[0]
    
        namespc=cmds.ls("*:*",type = "transform")
        
        for nspc in namespc:
            getNamespace = nspc.split(":")[0]
            shape = nspc.split(":")[-1]

            #looping shading engine and find matches with the attribute. And assign the material to it.
            for shd in cmds.ls(type = "shadingEngine"):#shd = "Clear_Glass_SG"
                if ("ShapeID" not in cmds.listAttr(shd) and "AssetID" not in cmds.listAttr(shd))or shd == "initialShadingGroup" or shd == "initialParticleSE":
                    continue   
                #print shd    
                if (getNamespace in cmds.getAttr("%s.AssetID"%shd)): 
                    for mat in cmds.getAttr("%s.ShapeID"%shd).split(";"):
                        if shape == mat:                     
                            #print  "%s assigned to %s"%(abc,shd)
                            cmds.sets(abc,e=1,forceElement=shd)

def assignOrder(*n):
    for ind, q in enumerate(cmds.ls(sl=1)):
        if "selOrder" not in cmds.listAttr(q):
            cmds.addAttr(q,longName = "selOrder",attributeType = "long" , keyable =0)
        cmds.setAttr("%s.selOrder"%q,channelBox=0)
        cmds.setAttr("%s.selOrder"%q,lock=0)
        cmds.setAttr("%s.selOrder"%q,ind)
        cmds.setAttr("%s.selOrder"%q,lock=1)

def selReorder(*n):
    itemList = cmds.ls(sl=1)
    newList = range(len(itemList))
    listLen = 0
    for item in itemList:
        if "selOrder" in cmds.listAttr(item):
            ind = cmds.getAttr("%s.selOrder"%item)
            newList[ind] = item
            listLen+=1
    cmds.select(newList[:listLen])
    
def searchAsset(prompt = 0,search=0):# 0 = Reference , 1 = Import batchAsset()
    loc="c:/animation/RuiLiTheBull_2/Scene/_AnimLoop/Anim/bake"
    if prompt ==1 :
        res = cmds.promptDialog(m="Insert Custom Location",db="Confirm",ds="Confirm")
        if res == "Confirm":
            loc =cmds.promptDialog(q=1,tx=1)
    if search==1:
        cmds.textScrollList("assetTextScroll",e=1,removeAll = 1)
        loc = cmds.textScrollList("assetTextScroll",q=1,ann = 1)
        allFiles = os.listdir(loc)
        searchText = cmds.textFieldGrp("importSearchBar",q=1,tx=1)
        for q in allFiles:
            splitList = os.path.splitext(q)
            if splitList[-1]==".mb" and (searchText.lower() in splitList[0].lower()) :
                cmds.textScrollList("assetTextScroll",e=1,append = q)
        return
    cmds.textScrollList("assetTextScroll",e=1,removeAll = 1)
    cmds.textScrollList("assetTextScroll",e=1,ann = "")
    allFiles = os.listdir(loc)
    for q in allFiles:
        if os.path.splitext(q)[-1]==".mb":
            cmds.textScrollList("assetTextScroll",e=1,append = q)
    cmds.textScrollList("assetTextScroll",e=1,ann = loc)

def batchAsset(*n):
    selectedItem = cmds.textScrollList("assetTextScroll",q=1,si = 1)
    location = cmds.textScrollList("assetTextScroll",q=1,ann = 1).replace("c:/animation/RuiLiTheBull_2/","")
    mode = cmds.radioButtonGrp("imRefradio",q=1,sl=1)
    #print location    
    if mode == 1 :
        for item in selectedItem:
            cmds.file(location+"/"+item,reference=1,namespace = os.path.splitext(item)[0])
    else:
        for item in selectedItem:
            cmds.file(location+"/"+item,i=1)

def rmanAttr(mode = 1):      
    rmanAddAttrScript = '$allItem = `ls -sl`;for ($i=0;$i<`size $allItem`;$i++){$mesh = `listRelatives -type "mesh" $allItem[$i]`;rmanAddAttr $mesh[0] `rmanGetAttrName subdivScheme` "";rmanAddAttr $mesh[0] `rmanGetAttrName subdivFacevaryingInterp` "";}'
    if mode == 1 :
        mel.eval(rmanAddAttrScript)
    else:
        for q in cmds.ls(sl=1):
            selectedShape = cmds.listRelatives(q,children=1,type="shape")[0]
            cmds.deleteAttr("%s.rman__torattr___subdivScheme"%selectedShape)
            cmds.deleteAttr("%s.rman__torattr___subdivFacevaryingInterp"%selectedShape)


def readjustWindow(*n):
    tagFrame = cmds.frameLayout("tagFrame",q=1,h=1)
    fxFrame = cmds.frameLayout("fxFrame",q=1,h=1)
    rmanFrame = cmds.frameLayout("rmanFrame",q=1,h=1)
    importRefFrame = cmds.frameLayout("importRefFrame",q=1,h=1)
    cmds.window('createFxWind',e=1,h=(tagFrame+fxFrame+rmanFrame+importRefFrame)+40)

def deleteTag(*n):
    for q in cmds.ls(sl=1,long=1):
        if "objType" in cmds.listAttr(q):
            print q
            cmds.setAttr("%s.objType"%q,lock=0)
            cmds.deleteAttr(q, attribute = 'objType')
            
def assignTag(tagName = ""):
    for q in cmds.ls(sl=1):
        if "objType" not in cmds.listAttr(q):
            cmds.addAttr(q,longName="objType",dataType="string",keyable=1)
        else:
            cmds.setAttr("%s.objType"%q,lock=0)
        cmds.setAttr("%s.objType"%q,tagName,type="string")
        cmds.setAttr("%s.objType"%q,lock=1)
        if tagName == "eyedart":
            if not cmds.objExists('eyeDart_SHDSG'):
                createSurfShad(name = 'eyeDart_SHD')
            cmds.setAttr("%s.castsShadows"%q,0,lock=1)
            cmds.setAttr("%s.receiveShadows"%q,0,lock=1)
            cmds.setAttr("%s.visibleInReflections"%q,0,lock=1)
            cmds.setAttr("%s.visibleInRefractions"%q,0,lock=1)
            cmds.setAttr("%s.primaryVisibility"%q,0,lock=1)
            cmds.setAttr("%s.doubleSided"%q,1,lock=1)
            cmds.sets(q,e=1,forceElement='eyeDart_SHDSG')
            
    print "Assigned %s to %s" %(tagName , cmds.ls(sl=1))    

def createSurfShad(name = '',color = (0,0,0),opacity = (1,1,1)):#createSurfShad(name = "eyeDart_SHD")
    shadeNode = cmds.shadingNode("surfaceShader",asShader = 1,n=name)
    shadeSets = cmds.sets(renderable = True , noSurfaceShader = True ,empty = True, name = "%sSG"%name)
    cmds.connectAttr("%s.outColor"%shadeNode ,"%s.surfaceShader"%shadeSets, force=1)
    cmds.setAttr("%s.outColor"%shadeNode , color[0],color[1],color[2],type = "double3")
    cmds.setAttr("%s.outMatteOpacity"%shadeNode , opacity[0],opacity[1],opacity[2],type = "double3")

def createCacheMesh(*n):
    meshList=[] #len(dulMeshList)   
    for q in cmds.ls(transforms=1):
        if "objType" in cmds.listAttr(q):
            if cmds.getAttr("%s.objType"%q) in ["geometry","eyedart","polyHair","gloss"]:
                meshList.append(q)
                
    newMesh = cmds.polyUnite(meshList)[0]
    bsMesh = cmds.duplicate(newMesh,n="DUPL_"+newMesh)[0]    
    cmds.addAttr(bsMesh,longName="objType",dataType="string",keyable=1)
    cmds.setAttr("%s.objType"%bsMesh,"cacheMesh",type="string")
    
    currentFilePath = "/".join(cmds.file(query=1,sceneName=1).split("/")[:-1])
    currentFileName = cmds.file(query=1,sceneName=1).split("/")[-1]
    if "/old" not in currentFilePath:
        currentFilePath+="/old"
    
    if cmds.checkBox("fxMeshBt",q=1,value=1):
        for q in cmds.file(q=1,r=1):
            cmds.file(q,ir=1)
        
    if cmds.checkBox("fxSaveCB",q=1,value=1):
        cmds.select(bsMesh)
        cmds.file((currentFilePath+"/"+currentFileName.replace("rig","fx_model")),force=1,options="v=0;",type="mayaBinary",preserveReferences=1,exportSelected=1)
    
    bsNode = cmds.blendShape(newMesh,bsMesh,n="%s_BS"%bsMesh)[0]
    cmds.setAttr("%s.%s"%(bsNode,newMesh),1)
    cmds.setAttr("%s.visibility"%(newMesh),0)
    cmds.parent(newMesh,bsMesh,"Geometry")
    if cmds.checkBox("fxSaveCB",q=1,value=1):
        cmds.file(rn=(currentFilePath+"/"+currentFileName.replace("rig","fx_rig")))
        cmds.file(save=1,force=1,options="v=0;",type="mayaBinary",preserveReferences=1)
    
try:
    cmds.deleteUI("createFxWind")
except:
    pass

cmds.window('createFxWind',vis=1,wh=[300,110],sizeable=0,title = "Fx Tools Window")
cmds.columnLayout("fxMainLay",w=300)
cmds.frameLayout("tagFrame",label = "Tag Creation",cll=1,w=299,parent ='fxMainLay' ,cl=True,cc=readjustWindow,ec=readjustWindow,bgc=(.5,0,0))
cmds.rowColumnLayout('tagColLay',p='tagFrame',co=[(1,"both",5),(2,"both",5)],cw=[(1,300),(2,300)],rowOffset=[(1,"top",5),(4,"top",5)])
cmds.optionMenu('tagOpMenu',parent = 'tagColLay',label = "Object Type:",w=100,ann = "Assign tag to selected objects.\ngeometry: objects will be render.\neyedart: object just to visible in viewport not render.\npolyHair: hair object for LOD purpose.\ncacheMesh: object to apply cache on it. Mostly for fx dept.\nprop_geometry: just for prop or object to be combine after cacheMesh is created.")#print "\"cmds.optionMenu('tagOpMenu',q=1,v=1)\""
menuItemList = ["geometry","sets","eyedart","polyHair","cacheMesh","prop_geometry","cacheCurve"]
for item in menuItemList:
    cmds.menuItem(label = item,parent = 'tagOpMenu')
cmds.separator("tagSepA",parent = 'tagColLay',h=10)
cmds.button("tagBt",parent = 'tagColLay',label = "Assign Tag to Selected Objects",c = "assignTag(tagName = cmds.optionMenu('tagOpMenu',q=1,v=1))")
cmds.button("tagRemoveBt",parent = 'tagColLay',label = "Remove Tag on Selected Objects",c = deleteTag)

cmds.separator('fxWindSperatorA',h=10,p='fxMainLay')

cmds.frameLayout("fxFrame",label = "FX Mesh",cll=1,w=299,parent ='fxMainLay' ,cl=True,cc=readjustWindow,ec=readjustWindow,bgc=(0,.5,0))
cmds.rowLayout("fxMeshLay",en=0,nc = 3, cw3=(70,125,100),cl2=('left','right'),parent = 'fxFrame')
cmds.checkBox("fxSaveCB",parent = 'fxMeshLay',label = "Auto Save",ann = 'Export fx_model and save a new file as fx_rig.')
cmds.checkBox("fxImCB",parent = 'fxMeshLay',label = "Import All Reference",ann = 'Import all references in this file.')
cmds.button("fxMeshBt",parent = 'fxMeshLay',label = "Create Fx Mesh",c = createCacheMesh)
cmds.button("fxSelAsgnBt",en=0,parent = 'fxFrame',label = "Assign Selection Order",c = assignOrder)
cmds.button("fxSelOrderBt",en=0,parent = 'fxFrame',label = "Selection Reorder",c = selReorder)
cmds.separator('fxWindSperatorE',h=10,p='fxFrame')
cmds.rowLayout("fxMeshLayC",nc = 3, cw2=(140,140),cl2=('left','right'),parent = 'fxFrame')
cmds.button("exportShdBt",h=36, w = 145 ,parent = 'fxMeshLayC',label = "Export Shader",ann = 'Assign \"geometry\" tag to renderable mesh before export the shading network.',c=exportShader)
cmds.button("linkShdBt", w = 145 ,parent = 'fxMeshLayC',label = "Link Shading Groups \nTo Mesh",ann = 'Import Shading Group first before use this function.',c= linkAllShader)
#cmds.button("linkShdBt",q=1,h=1)

cmds.separator('fxWindSperatorB',h=10,p='fxMainLay')

cmds.frameLayout("rmanFrame",label = "RenderMan Attribute",cll=1,w=299,parent ='fxMainLay' ,cl=True,cc=readjustWindow,ec=readjustWindow,bgc=(0,0,.5))#cmds.frameLayout("rmanFrame",q=1,h=1)
cmds.button("rmanAddBt",parent = 'rmanFrame',label = "Add Subdiv Scheme",c = "rmanAttr(mode = 1)")
cmds.button("rmanDelBt",parent = 'rmanFrame',label = "Remove Subdiv Scheme",c = "rmanAttr(mode = 0)")

cmds.separator('fxWindSperatorC',h=10,p='fxMainLay')

cmds.frameLayout("importRefFrame",label = "Batch Import/Reference Asset",cll=1,w=299,parent ='fxMainLay' ,cl=True,cc=readjustWindow,ec=readjustWindow,bgc=(0,.5,.5))#cmds.frameLayout("rmanFrame",q=1,h=1)
cmds.textFieldGrp("importSearchBar",parent = 'importRefFrame',label = "Search: ",ad2=1,cc='searchAsset(prompt=0,search=1)')
cmds.textScrollList("assetTextScroll",parent = 'importRefFrame',ams=1,h=300)
cmds.button("imRefBt",parent = 'importRefFrame',label = "General Location",c = searchAsset)
cmds.button("speciLocBt",parent = 'importRefFrame',label = "Specific Location",c = 'searchAsset(prompt=1)')
cmds.radioButtonGrp("imRefradio",parent = 'importRefFrame',label = "Action Type:",nrb=2,la2=["Reference","Import"],cw3=[80,100,100],sl=1)
cmds.button("bringBt",parent = 'importRefFrame',label = "Bring Them IN!",c = batchAsset)

cmds.separator('fxWindSperatorD',h=10,p='fxMainLay')
