'''
To break connections
'''

for abc in cmds.ls(type = "mesh"):#abc = cmds.ls(sl=1)[0]
    #list meshes created by abc file
    meshList = cmds.listConnections(abc,type="shadingEngine",p=1,c=1)
    input = meshList[::2]
    output = meshList[1::2]

    
    for ind,out in enumerate(output):
        shd = out.split(".")[0]
        if shd == "initialShadingGroup":
            cmds.disconnectAttr(input[ind],out)
