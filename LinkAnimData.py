nsInfo = cmds.namespaceInfo(lon=1,r=1)

namespaceList=[]
for a in nsInfo:
    if a == 'UI' or a == 'shared':
        continue
    else:
        namespaceList.append(a)
        
aniCurveList=[]
animCurveObj=[]

for i in namespaceList:            
    for aniCurve in cmds.ls(type="animCurve"):
        if("animDest" not in cmds.listAttr(aniCurve)):
            continue
        animDestNS = cmds.getAttr("%s.animDest"%aniCurve).split(":")[0]
        if animDestNS == None:
            continue
        if animDestNS == i:
            try:
                cmds.connectAttr(aniCurve+".output",cmds.getAttr("%s.animDest"%aniCurve), f=1)
            except:
                pass
