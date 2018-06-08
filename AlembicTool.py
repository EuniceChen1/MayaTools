import os
import glob
import maya.cmds as cmds

full_dir = cmds.workspace(fileRuleEntry="abcOut").replace("/","\\")
sqList = glob.glob(full_dir+'\\'+'sq'+'*')
scnList = glob.glob(full_dir+'\\'+'sc'+'*')

def seqMenu(*n):
    if len(sqList) != 0 :
        cmds.optionMenu("seqMenu",e=1,dai=1)
        for sequence in sqList:
            sqCode = sequence.split("\\")[-1].split("q")[-1]
            cmds.menuItem(label = sqCode, parent = 'seqMenu')
        
def sceneMenu(*n):
    if len(scnList) == 0: #New directory convention
        cmds.optionMenu("sceneMenu",e=1,dai=1)
        if cmds.optionMenu("seqMenu",q=1,en=1):
            querySeqMenu = cmds.optionMenu("seqMenu", q=1, v=1)
            fullSeqList = full_dir+'\\'+'sq'+querySeqMenu
            fullSeqList = os.listdir(fullSeqList)
            
        else:
            cmds.optionMenu("sceneMenu",q=1,en=0)
            
        for scenes in fullSeqList:
            scnCode = scenes.split("\\")[-1].split("c")[-1]
            cmds.menuItem(label = scnCode, parent = 'sceneMenu')
            
    else: #Old directory convention
        cmds.optionMenu("sceneMenu",e=1,dai=1)
        for scenes in scnList:
            scnCode =  scenes.split("\\")[-1].split("c")[-1]
            cmds.menuItem(label = scnCode, parent = 'sceneMenu')
            
def shotMenu(*n):
    cmds.optionMenu("shotsMenu",e=1,dai=1)
    
    if cmds.optionMenu("seqMenu",q=1,en=1): #New directory ocnvention (sequence is enabled)
        querySeqMenu = cmds.optionMenu("seqMenu", q=1, v=1)
        queryScnMenu = cmds.optionMenu("sceneMenu", q=1, v=1) 
        fullSceneList = full_dir+'\\'+'sq'+querySeqMenu+'\\'+'sc'+queryScnMenu
        fullSceneList = os.listdir(fullSceneList)
        
    else:
        queryScnMenu = cmds.optionMenu("sceneMenu", q=1, v=1)
        fullSceneList = full_dir+'\\'+'sc'+queryScnMenu
        fullSceneList = os.listdir(fullSceneList)
    
    for files in fullSceneList:
        shtCode = files.split("\\")[-1].split("h")[-1]
        cmds.menuItem(label=shtCode,parent="shotsMenu")

def selectShader (*n):## define renderable mesh objType to 'geometry'     
    validMat=[]
    #SET ATTRIBUTE
    #assetFileName = cmds.file(query=1,sceneName=1).split("/")[-1] DOESN'T WORK ON SOME COMPUTER
    assetFileName = cmds.file(query=1,l=1)[0].split("/")[-1] 
    assetName = assetFileName.split(".")[0]   
    shdSavePath = cmds.workspace(fileRuleEntry = 'shdOut')
    
    #cmds.optionMenu("hairTypeMenu", q=1, e=1, dai=1)
    queryhairType = cmds.optionMenu("hairTypeMenu", q=1, v=1)
    
    if queryhairType == 'maya_hair':
        hairPlugin = 'pfxHair'
    elif queryhairType == 'xgen':
        hairPlugin = 'xgmDescription'
    elif queryhairType == 'yeti':
        hairPlugin = 'pgYetiMaya'
    else:
        hairPlugin = 'None'
        print 'Maya hair and xgen were not used!! '
        
    shadingEngine = [q for q in cmds.ls(type = "shadingEngine") if (q != "initialShadingGroup" and q != "initialParticleSE") ]
    
    for q in shadingEngine:        
        
        allString = ""
        if "ShapeID" not in cmds.listAttr(q) and "AssetID" not in cmds.listAttr(q):# and q != "initialShadingGroup" and q != "initialParticleSE":
            
            cmds.addAttr(q,longName = "ShapeID",dataType="string", keyable=0)
            cmds.addAttr(q,longName = "AssetID",dataType="string", keyable=0)
 
        hairConn = cmds.listConnections(q,type="%s"%hairPlugin)
        listConn = cmds.listConnections(q,type="mesh")
    
        if hairConn != None: 
            for hconn in hairConn:
                if "objType" in cmds.listAttr(hconn):
                    if cmds.getAttr("%s.objType"%hconn) == "hair/fur":
                        #This currently doesn't do anything since nothing is assigned as "hair/fur"
                        allString += ((hconn.split("|")[-1])+";")
                        validMat.append(q)
        
        else:
            if listConn != None: 
                for conn in listConn:
                    if "objType" in cmds.listAttr(conn):
                        if cmds.getAttr("%s.objType"%conn) == "geometry" or cmds.getAttr("%s.objType"%conn) == "sets":
                            allString += ((conn.split("|")[-1])+";")
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
    
    for export in cmds.ls():
        if "objType" in cmds.listAttr(export):
            if cmds.getAttr("%s.objType"%export) == "export_with_shd":
                cmds.select(export,add=1)         
                
def exportShader(*n):#Auto Export selection
    assetFileName = cmds.file(query=1,l=1)[0].split("/")[-1]   
    shdSavePath = cmds.workspace(fileRuleEntry = 'shdOut')
    
    if len(cmds.ls(sl=1)) < 1:
        print validMat,cmds.ls(sl=1)
        cmds.warning("No valid selections.")
    
    else:
        if cmds.file(q=1,l=1)[0].split(".")[-1] == 'mb':
            cmds.file(shdSavePath+"/"+(assetFileName.replace("rig","shd").replace("mdl","shd")),f=1,op="v=0;",typ = "mayaBinary",pr=1,es=1)
        elif cmds.file(q=1,l=1)[0].split(".")[-1] == 'ma':
            cmds.file(shdSavePath+"/"+(assetFileName.replace("rig","shd").replace("mdl","shd")),f=1,op="v=0;",typ = "mayaASCII",pr=1,es=1)
        else:
            print 'THIS IS NOT A MAYA FILE'

def linkAllShader(*n): #no selection needed

    meshList = cmds.ls("*:*",type = "mesh")
    transList = []
    for mesh in meshList :
        relatives = cmds.listRelatives(mesh,type = "transform",p=1)
        if len(relatives) > 0 :
            transList.append(relatives[0])
                    
    for abc in transList:#abc = cmds.ls(sl=1)[0]

        getNamespace = "_".join(abc.split(":")[0].split("_")[:3])
        #getNamespace = abc.split(":")[0]
   
        shape = abc.split(":")[-1]
        rig_grp = getNamespace+"_grp"
  
        if not cmds.objExists(rig_grp) and "_cam_" not in getNamespace: #and "_shd" not in getNamespace and "_cfx" not in getNamespace:
            cmds.group(name = rig_grp,w=1,em=1)
 
        #looping shading engine and find matches with the attribute. And assign the material to it.
        for shd in cmds.ls(type = "shadingEngine"):
            if ("ShapeID" not in cmds.listAttr(shd) and "AssetID" not in cmds.listAttr(shd)) or shd == "initialShadingGroup" or shd == "initialParticleSE":
                continue
            if cmds.getAttr("%s.AssetID"%shd) == None:
                continue    
            if (getNamespace in cmds.getAttr("%s.AssetID"%shd)): 
                for mat in cmds.getAttr("%s.ShapeID"%shd).split(";"):
                    if shape == mat:                
                        #print  "%s assigned to %s"%(abc,shd)
                        cmds.sets(abc,e=1,forceElement=shd)
                    try:
                        cmds.parent(abc,rig_grp)
                    except:
                        pass
                    
def autoBlendShape(*n):
    queryhairType = cmds.optionMenu("hairTypeMenu", q=1, v=1)
    nsInfo = cmds.namespaceInfo(lon=1,r=1)
    namespaceList=[]
    
    for a in nsInfo: #get namespace list
        if a == 'UI' or a == 'shared':
            continue
        else:
            namespaceList.append(a)
    
    if queryhairType == 'maya_hair':
        
        cfxList = []
        shdList = []
        grpList = []
        for k in namespaceList: #select deformed mesh, then select original mesh and do blend shape
            for grp in cmds.ls("%s:*_grp"%k,type="transform",l=1):
                if "hair" in grp.split(":")[0]:
                    cfxList.append(grp.split("|")[1]) 
                
                elif "shd" in grp.split(":")[0]:
                    shdList.append(grp.split("|")[-1])

                if "grp" in grp:
                    grpList.append(grp.split("|")[1].split(":")[0])  

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
        for ns in namespaceList: #set attribute for blendshape to go to 1
            if ns in set(grpList):   
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
                                    
        #set attribute for curve attraction
        mayaHairList = []
        for ns in namespaceList:
            for blended in cmds.listRelatives("%s:*"%ns,type="transform",f=1,c=1):
                if "MayaHairSystem" in blended:
                    mayaHairList.append(blended.split("|")[-1])
                                          
        for mayaHair in mayaHairList:
            cmds.setAttr("%s.attractionScale[1].attractionScale_Position"%mayaHair,1)
            cmds.setAttr("%s.attractionScale[1].attractionScale_FloatValue"%mayaHair,1)
            cmds.setAttr("%s.startCurveAttract"%mayaHair,1)
            
    elif queryhairType == 'xgen':
        print "BlendShape for xgen hair workflow is still under development"
        pass
    else:
        print 'Maya hair and xgen were not used!! '
        


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
    queryShtMenu = cmds.optionMenu("shotsMenu", q=1, v=1)
    if cmds.optionMenu("seqMenu", q=1, en=1):
        querySeqMenu = cmds.optionMenu("seqMenu", q=1, v=1)
        queryScnMenu = cmds.optionMenu("sceneMenu", q=1, v=1)
        fullSeqList = full_dir+'\\'+'sq'+querySeqMenu
        fullSceneList = fullSeqList+'\\'+'sc'+queryScnMenu
        fullShotList = fullSceneList+'\\'+'sh'+queryShtMenu

    else:
        queryScnMenu = cmds.optionMenu("sceneMenu", q=1, v=1)
        fullSceneList = full_dir+'\\'+'sc'+queryScnMenu
        fullShotList = fullSceneList+'\\'+'sh'+queryShtMenu
        
    loc=fullShotList
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
            if splitList[-1]==".abc" or splitList[-1]=='.fbx' and (searchText.lower() in splitList[0].lower()) :
                cmds.textScrollList("assetTextScroll",e=1,append = q)
        return
    cmds.textScrollList("assetTextScroll",e=1,removeAll = 1)
    cmds.textScrollList("assetTextScroll",e=1,ann = "")
    allFiles = os.listdir(loc)
    for q in allFiles:
        if os.path.splitext(q)[-1]==".abc" or os.path.splitext(q)[-1]==".ma" or os.path.splitext(q)[-1]==".mb":

            cmds.textScrollList("assetTextScroll",e=1,append = q)
    cmds.textScrollList("assetTextScroll",e=1,ann = loc)

def batchAsset(*n):
    selectedItem = cmds.textScrollList("assetTextScroll",q=1,si = 1)
    location = cmds.textScrollList("assetTextScroll",q=1,ann = 1)
    mode = cmds.radioButtonGrp("imRefradio",q=1,sl=1)
    shdSavePath = cmds.workspace(fileRuleEntry = 'shdOut')
    listShd = [i for i in os.listdir(shdSavePath) if i != ".mayaSwatches"]
    rigPath = cmds.workspace(fn=1)+"\\"+cmds.workspace(fileRuleEntry="templates")+"\\rig"
    listRig = [j for j in os.listdir(rigPath)]
    shaders=[]
    
    camera = [cam for cam in selectedItem if "_cam_" in cam]
          
    if mode == 1 :
        for item in selectedItem:
            splitSelectedItem = item.split(".")[0].split("_rig")[0]
            nspcRig = splitSelectedItem+"_rig"
            shaders.append(splitSelectedItem)
            extension = item.split(".")[-1]
            assetType = splitSelectedItem.split("_")[1]
            
            if extension == "mb" or extension == "ma":
                if assetType == "c":
                    assetPath = rigPath +"\\"+listRig[0]+"\\"+splitSelectedItem
                    if extension == "ma":
                        cmds.file(assetPath+"\\"+nspcRig+".ma",reference=1,namespace=nspcRig)
                    elif extension == "mb":
                        cmds.file(assetPath+"\\"+nspcRig+".mb",reference=1,namespace=nspcRig)
                        
                elif assetType == "p":
                    assetPath = rigPath +"\\"+listRig[1]+"\\"+splitSelectedItem
                    if extension == "ma":
                        cmds.file(assetPath+"\\"+nspcRig+".ma",reference=1,namespace=nspcRig)
                    elif extension == "mb":
                        cmds.file(assetPath+"\\"+nspcRig+".mb",reference=1,namespace=nspcRig)
                else:
                    print "naming is wrong, asset not found!"
            cmds.file(location+"/"+item,reference=1,namespace = os.path.splitext(item)[0])

        #Link Animation Data and Rig File
        nsInfo = cmds.namespaceInfo(lon=1,r=1)
        namespaceList=[]
        for a in nsInfo:
            if a == 'UI' or a == 'shared':
                continue
            else:
                namespaceList.append(a)

        animationCurve = cmds.ls(type="animCurve")
        animDestList=[]
        if len(animationCurve) != 0:
            for k in namespaceList:            
                for aniCurve in animationCurve:
                    if("animDest" not in cmds.listAttr(aniCurve)):
                        continue
                    animDestNS = cmds.getAttr("%s.animDest"%aniCurve).split(":")[0]           
                    if animDestNS == None:
                        print "animDestNS None"
                        continue
                    if animDestNS == k:
                        try:
                            cmds.connectAttr(aniCurve+".output",cmds.getAttr("%s.animDest"%aniCurve), f=1)
                            print "Connected %s to %s"%(aniCurve+".output",aniCurve)
                        except:
                            print "Something Is Not Connected"
                            pass
                    else:
                        print animDestNS,k
                        print "namespace doesn't match"
                    cmds.select(aniCurve)
                startFrame = cmds.keyframe(q=1)[0]
                endFrame = cmds.keyframe(q=1)[-1]
            cmds.playbackOptions(min=startFrame,max=endFrame)

        referenceList=[]
        for ref in cmds.file(q=1,r=1):
            filename = ref.split("/")[-1].split(".")[0]
            if "_shd" in filename:
                referenceList.append(filename)
         
        for shd in listShd:
            for shader in shaders:
                if shd.split(".")[0].split("_shd")[0] in shader and not cmds.namespace(q=1,ex=1):
                    if shd.split(".")[0] not in referenceList:
                        cmds.file(shdSavePath+"/"+shd,reference=1,namespace = os.path.splitext(shd)[0])
                        print "referencing %s"%shd
                        break

    else:
        for item in selectedItem:
            cmds.file(location+"/"+item,i=1)
            cmds.file(shdSavePath+"/"+listShd,i=1)

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
        
def run():    
    try:
        cmds.deleteUI("createFxWind")
    except:
        pass

    cmds.window('createFxWind',vis=1,wh=[300,110],sizeable=0,title = "Fx Tools Window")
    cmds.columnLayout("fxMainLay",w=300)
    cmds.frameLayout("tagFrame",label = "Tag Creation",cll=1,w=299,parent ='fxMainLay' ,cl=True,cc=readjustWindow,ec=readjustWindow,bgc=(.5,0,0))
    cmds.rowColumnLayout('tagColLay',p='tagFrame',co=[(1,"both",5),(2,"both",5)],cw=[(1,300),(2,300)],rowOffset=[(1,"top",5),(4,"top",5)])
    cmds.optionMenu('tagOpMenu',parent = 'tagColLay',label = "Object Type:",w=100,ann = "Assign tag to selected objects.\ngeometry: objects will be render.\neyedart: object just to visible in viewport not render.\npolyHair: hair object for LOD purpose.\ncacheMesh: object to apply cache on it. Mostly for fx dept.\nprop_geometry: just for prop or object to be combine after cacheMesh is created.")#print "\"cmds.optionMenu('tagOpMenu',q=1,v=1)\""
    menuItemList = ["geometry","sets",'camera',"eyedart","export_with_shd","hair/fur","cacheMesh","prop_geometry","cacheCurve","ctrl"]
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
    cmds.button("fxSelAsgnBt",en=1,parent = 'fxFrame',label = "Assign Selection Order",c = assignOrder)
    cmds.button("fxSelOrderBt",en=1,parent = 'fxFrame',label = "Selection Reorder",c = selReorder)
    
    cmds.separator('fxWindSperatorE',h=5,p='fxFrame')
    
    cmds.rowColumnLayout("fxMeshLayD",co=[(1,"both",5),(2,"both",5)],cw=[(1,300),(2,300)],rowOffset=[(1,"top",5),(4,"top",5)],parent = 'fxFrame')
    #cmds.rowLayout("fxMeshLayC",nc = 3, co3 = [4,1,4],cw3=(93,93,95),ct3=('left','both','right'),parent = 'fxFrame')
    cmds.rowLayout("fxMeshLayC",nc = 3, cw2=(140,140),cl2=('left','right'),parent = 'fxFrame')
    cmds.rowLayout("fxMeshLayE",nc = 3, cw2=(140,140),cl2=('left','right'),parent = 'fxFrame')
    
    cmds.optionMenu('hairTypeMenu',parent='fxMeshLayD',label = "Hair/Fur Type :", w=100, ann = "Choose which plug-in was used to groom the hair/fur. xgm for xgen, pfxHair for Maya Hair.")
    hairItemList = ["none","maya_hair","xgen","yeti"]
    for hair in hairItemList:
        cmds.menuItem(label = hair, parent = 'hairTypeMenu')
        
    cmds.button("selectShdBt",h=36, w=149, parent = 'fxMeshLayC', label = "Select Shader", ann = 'Select shading engines that has connections.', c=selectShader)      
    cmds.button("autoExportBt",h=36, w=145, parent='fxMeshLayC', label = 'Auto Export \nShader', ann = 'Export selected shading groups with anything else that has tag "export_with_shd".', c=exportShader)
    cmds.button("linkShdBt", w=149, parent = 'fxMeshLayE', label = "Link Shading \nGroups To Mesh",ann = 'Link Shading Groups to Renderable Mesh.', c=linkAllShader)
    cmds.button("autoBlendShapeBt", h=36, w=145, parent = "fxMeshLayE", label = "Auto BlendShape", ann = 'Automatically performs blendshape action onto matching object names.', c=autoBlendShape)

    cmds.separator('fxWindSperatorB',h=10,p='fxMainLay')

    cmds.frameLayout("rmanFrame",label = "RenderMan Attribute",cll=1,w=299,parent ='fxMainLay' ,cl=True,cc=readjustWindow,ec=readjustWindow,bgc=(0,0,.5))#cmds.frameLayout("rmanFrame",q=1,h=1)
    cmds.button("rmanAddBt",parent = 'rmanFrame',label = "Add Subdiv Scheme",c = "rmanAttr(mode = 1)")
    cmds.button("rmanDelBt",parent = 'rmanFrame',label = "Remove Subdiv Scheme",c = "rmanAttr(mode = 0)")

    cmds.separator('fxWindSperatorC',h=10,p='fxMainLay')

    cmds.frameLayout("importRefFrame",label = "Batch Import/Reference Asset",cll=1,w=299,parent ='fxMainLay' ,cl=True,cc=readjustWindow,ec=readjustWindow,bgc=(0,.5,.5))#cmds.frameLayout("rmanFrame",q=1,h=1)
    cmds.textFieldGrp("importSearchBar",parent = 'importRefFrame',label = "Search: ",ad2=1,cc='searchAsset(prompt=0,search=1)')
    
    cmds.optionMenu("seqMenu", parent='importRefFrame',label='Sequence: ', cc = sceneMenu)
    cmds.optionMenu("sceneMenu", parent='importRefFrame' ,label='Scene: ',cc = shotMenu)
    cmds.optionMenu("shotsMenu",parent='importRefFrame',label='Shots: ',cc = searchAsset)

    cmds.textScrollList("assetTextScroll",parent = 'importRefFrame',ams=1,h=300)
    #cmds.button("imRefBt",parent = 'importRefFrame',label = "General Location",c = searchAsset)
    cmds.button("speciLocBt", en=0,parent = 'importRefFrame',label = "Specific Location",c = 'searchAsset(prompt=1)')
    cmds.radioButtonGrp("imRefradio",en2=0,parent = 'importRefFrame',label = "Action Type:",nrb=2,la2=["Reference","Import"],cw3=[80,100,100],sl=1)
    cmds.button("bringBt",parent = 'importRefFrame',label = "Bring Them In!",c = batchAsset)

    cmds.separator('fxWindSperatorD',h=10,p='fxMainLay')

    if len(sqList) == 0 :
        cmds.optionMenu("seqMenu",e=1,en=0)
    else:
        seqMenu(1)
    
    sceneMenu(1)
    shotMenu(1)
    searchAsset()

if __name__ == "__main__":
    run()
    
