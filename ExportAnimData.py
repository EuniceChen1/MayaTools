allNS= cmds.namespaceInfo(lon=1,r=1)
defaultNS = ["UI","shared"]
others = [ns for ns in allNS if ns not in defaultNS]

#both are the same, some Maya doesn't work with cmds.file(q=1, sceneName=1)
#currentFileNameList = cmds.file(q=1,sceneName =1 ).split("/")[-1].split(".")[0]
currentFileNameList = cmds.file(q=1,l=1)[0].split("/")[-1].split(".")[0]
extension = cmds.file(q=1,l=1)[0].split("/")[-1].split(".")[-1]
abcOutPath = cmds.workspace(fileRuleEntry="abcOut")     
nsInfo = cmds.namespaceInfo(lon=1,r=1)

for q in currentFileNameList.split("_"):
    if "sc" in q:
        abcOutPath += "/%s" %q
        continue
        
    if "sh" in q:
        abcOutPath += "/%s" %q
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
for nc in cmds.ls(type="nurbsCurve"):
    nctrans = cmds.listRelatives(nc, type="transform",p=1,f=1)[0]
    if "objType" in cmds.listAttr(nctrans):
        if cmds.getAttr("%s.objType"%nctrans) == "ctrl":
            transformList.append(nctrans)
            
    if len(transformList) == 0:
        continue
cmds.bakeResults(transformList,sm=1,t=(int(cmds.playbackOptions(q=1,min=1)),int(cmds.playbackOptions(q=1,max=1))),sb=1,osr=1,rba=0,dic=1,pok=1,sac=0,ral=0,bol=0,mr=1,cp=0,s=0)

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
        dest = cmds.listConnections(q,d=1,c=0,p=1)[0]
        
        if "animDest" not in cmds.listAttr(curveObj): #Create Extra Attribute
            cmds.addAttr(curveObj,longName="animDest",dataType="string",keyable=1)

        cmds.setAttr("%s.animDest"%curveObj,lock=0)
        cmds.setAttr("%s.animDest"%curveObj,dest,type="string")
        cmds.setAttr("%s.animDest"%curveObj,lock=1)
                        
    cmds.select(animCurveObj)
            
    if extension == "ma":
        
        cmds.file((abcOutPath+"/"+i+"Anim"),f=1,op="v=0",typ = "mayaAscii",pr=1,es=1) #Export Animation Curve Data
        end = time.time()
        print "Animation data exported in ",(end-start),"seconds"
        start = time.time()
        
    elif extension == "mb":
        
        cmds.file((abcOutPath+"/"+i+"Anim"),f=1,op="v=0",typ = "mayaBinary",pr=1,es=1) #Export Animation Curve Data
        end = time.time()
        print "Animation data exported in ",(end-start),"seconds"
        start = time.time()
        
    else:
        print "file type unknown, can't be exported"
        continue
