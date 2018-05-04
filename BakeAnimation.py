transformList=[]
for nc in cmds.ls(type="nurbsCurve"):
    nctrans = cmds.listRelatives(nc, type="transform",p=1,f=1)[0]
    if "objType" in cmds.listAttr(nctrans):
        if cmds.getAttr("%s.objType"%nctrans) == "ctrl":
            transformList.append(nctrans)

if len(transformList) == 0:
    pass
cmds.bakeResults(transformList,sm=1,t=(int(cmds.playbackOptions(q=1,min=1)),int(cmds.playbackOptions(q=1,max=1))),sb=1,osr=1,rba=0,dic=1,pok=1,sac=0,ral=0,bol=0,mr=1,cp=0,s=0)
