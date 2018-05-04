extension = cmds.file(q=1,l=1)[0].split("/")[-1].split(".")[-1]
abcOutPath = cmds.workspace(fileRuleEntry="abcOut")     
nsInfo = cmds.namespaceInfo(lon=1,r=1)


namespaceList=[]
for a in nsInfo:
    if a == 'UI' or a == 'shared':
        continue
    else:
        namespaceList.append(a)

animCurveList = []
animCurveObj=[]
for i in namespaceList:
    curveList=[]
    for j in cmds.ls("%s:*"%i,type="nurbsCurve"):
    	transform = cmds.listRelatives(j,type="transform",p=1,f=1)[0]
    	if "objType" in cmds.listAttr(transform):
    		if cmds.getAttr("%s.objType"%transform) == "ctrl":
    		    conn = cmds.listConnections(transform,type="animCurve",d=0,p=1,c=1)
    		    #print conn
    		    if conn != None:
    		        objList = conn[1::2]
    		        connList = conn[::2]
    		       
                    for obj in objList:
                        animCurveObj.append(obj.split(".")[0])
                        
                    for m in connList:
                        animCurveList.append(m)

                    for ind,q in enumerate(animCurveObj):
                        
                        if "animDest" not in cmds.listAttr(q):
                            cmds.addAttr(q,longName="animDest",dataType="string",keyable=1)
                        
                        cmds.setAttr("%s.animDest"%q,lock=0)
                        cmds.setAttr("%s.animDest"%q,"%s"%animCurveList[ind],type="string")
                        cmds.setAttr("%s.animDest"%q,lock=1)
                        
    cmds.select(animCurveObj)
    if extension == "ma":
        cmds.file((abcOutPath+"/"+i+"Anim"),f=1,op="precision=8;intValue=17;nodeNames=1;verboseUnits=0;whichRange=1;range=0:10;options=keys;hierarchy=none;controlPoints=0;shapes=0;helpPictures=0;useChannelBox=0;copyKeyCmd=-animation objects -option keys -hierarchy none -controlPoints 0 -shape 0 ",typ = "mayaAscii",pr=1,es=1) #Export Animation Curve Data

    elif extension == "mb":
        cmds.file((abcOutPath+"/"+i+"Anim"),f=1,op="precision=8;intValue=17;nodeNames=1;verboseUnits=0;whichRange=1;range=0:10;options=keys;hierarchy=none;controlPoints=0;shapes=0;helpPictures=0;useChannelBox=0;copyKeyCmd=-animation objects -option keys -hierarchy none -controlPoints 0 -shape 0 ",typ = "mayaBinary",pr=1,es=1) #Export Animation Curve Data
    
    else:
        print "file type unknown, can't be exported"
        continue

                        
