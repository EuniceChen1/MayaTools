import xml.etree.ElementTree as xml
import xml.dom.minidom as md
import os

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = xml.tostring(elem, encoding = 'utf-8')
    reparsed = md.parseString(rough_string)
    return reparsed.toprettyxml(indent="   ")

def dataCreate(*arg): 
    dataList = list(arg)
    print dataList
    ptype = xml.SubElement(root, "base",Project = dataList[0])
    proj = xml.SubElement(ptype, "type",Type = dataList[1])
    astype = xml.SubElement(ptype, "type",assetType = dataList[2])
    fps = xml.SubElement(ptype, "type",FPS = dataList[3])
    wid = xml.SubElement(ptype, "type",Width = dataList[4])
    hei = xml.SubElement(ptype, "type",Height = dataList[5])
    unit = xml.SubElement(ptype, "type",Unit = dataList[6])
    pdir = xml.SubElement(ptype, "type", Directory = dataList[18])
    scnFileFormat = xml.SubElement(ptype, "type", SceneFileName = dataList[19])
    #pb = xml.SubElement(ptype, "Playblast")
    pbCode = xml.SubElement(ptype, "Playblast",maskCode = dataList[20])
    vw = xml.SubElement(ptype, "Playblast",view = dataList[7])
    so = xml.SubElement(ptype, "Playblast",showOrnaments = dataList[8])
    os = xml.SubElement(ptype, "Playblast",offScreen = dataList[9])
    form = xml.SubElement(ptype, "Playblast",pformat = dataList[10])
    comp = xml.SubElement(ptype, "Playblast",compression = dataList[11])
    cc = xml.SubElement(ptype, "Playblast",clearCache = dataList[12])    
    qlt = xml.SubElement(ptype, "Playblast",quality = dataList[13])
    perc = xml.SubElement(ptype, "Playblast",percent = dataList[14])
    fp = xml.SubElement(ptype, "Playblast",framePadding = dataList[15])
    fo = xml.SubElement(ptype, "Playblast",forceOverwrite = dataList[16])
    uts = xml.SubElement(ptype, "Playblast",useTraxSounds = dataList[17])
    

def deCode(find = ""):
    xmlFile = os.path.join(r'C:\mnt\animation\Pipeline\xml', 'project.xml')
    read = xml.parse(xmlFile)
    
    findBase = read.findall('base')    
    storeList = []
    for child in findBase:
        findType = child.iter('type')
        store = child.attrib
        if find == "Project":
            storeList.append(store["Project"])
        else:
            for types in findType:
                if find == "":
                    store[types.attrib.keys()[0]] = types.attrib.values()[0]
                    storeList.append(store)
                elif find == types.attrib.keys()[0]:
                    store = types.attrib.values()[0]
                    storeList.append(store)
    if len(storeList)==0:
        for child in findBase:
            findPB = child.iter('Playblast')
            store = child.attrib
            for pb in findPB:
                #print pb.attrib
                if find == pb.attrib.keys()[0]:
                    store = pb.attrib.values()[0]
                    storeList.append(store)
    return storeList

#xml.SubElement(doc, "field1", name="blah").text = "some value1"
#xml.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"
### Character, Props, Environments ,Sets ###
if __name__ == "__main__":
    root = xml.Element("root")
##    dataCreate("TEST","Animation","Rigs\\Characters,Rigs\\Props,Models\\Scenes,Models\\Scenes",
##               "24","2048","1152","cm","1","1","1","qt","H.264","1","85","50","4","1","1",
##               "D:\localTest",
##               "TST$proj_TE$scn$F4_ST$sht$F5_V$ver$F6_$user",
##               "$cam;*;*;*;Anim:$user;TST$proj;*;Lens: $lens/FPS: $fps;*;Frame Range: $frame$F4")
    
    dataCreate("xxxx","Animation","Rigs\\Characters,Rigs\\Props,Models\\Scenes,Models\\Scenes",
               "24","2048","1152","cm","1","1","1","qt","H.264","1","85","50","4","1","1",
               r"PATH TO PROJECT",
               "SMR$proj_ERA$scn$F3_SC$sht$F3_V$ver$F3_$user",
               "$cam;*;*;*;$user;SMR$proj;*;Lens: $lens;*;Frame Range: $frame$F6")
    
    dataCreate("yyyy","Animation","",
               "30","1920","1080","m","1","1","1","qt","H.264","1","100","50","4","1","1",
               r"PATH TO PROJECT",
               "OnePiece$proj_OP$scn$F4_ST$sht$F5_V$ver$F6_$user",
               r"$cam;*;FPS: $fps/Unit: $unit;*;*;One Piece$proj;*;*;*;Frame Range: $frame$F4")

    dataCreate("zzzz","Animation","rig\\chr,rig\\prp,model\\set,model\\env",
               "24","1920","1080","m","1","1","1","qt","H.264","1","85","50","4","1","1",
               r"PATH TO PROJECT",
               "AY$proj_Sc$scn$F3_Sh$sht$F3_V$ver$F3_$user",
               r"$cam;*;*;*;$user;AY$proj;*;Lens: $lens;*;Frame Range: $frame$F6")
               
    #dataCreate("GamesProject1","Games","props,char,env,sets","30","1920","1080","cm","1","1","1","qt","H.264","1","100","50","4","1","1","D:\Eunice\GamesProject")
    deCode = deCode()
    tree = xml.ElementTree(xml.fromstring(prettify(root)))
    
    #xmlFile = os.path.join(os.path.dirname(__file__).replace("misc","xml"), 'project.xml')
    xmlFile = os.path.join(r'XML PATH', 'name.xml')
    tree.write(xmlFile)

