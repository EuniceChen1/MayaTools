import os
import maya.cmds as cmds
import maya.mel
import maya.OpenMayaUI as apiUI
import Pipeline
import xml.etree.ElementTree as xml
from cStringIO import StringIO
from Pipeline.misc import createXML
from Pipeline.misc import decode
from Pipeline.animation import playblastTool
import Pipeline.LayoutSetupFunc as PL
import Pipeline.FileLoaderFunc as PFile

reload(Pipeline)
reload(createXML)
reload(decode)
reload(playblastTool)
reload(PL)
reload(PFile)

version = int(cmds.about(v=1))


#del PL
if version == 2017:
    import PySide2.QtCore as QtCore
    import PySide2.QtWidgets as QtGui
    import PySide2 as PySide
    import pyside2uic as pysideuic
    import shiboken2 as shiboken
    #import PySide2.QtWidgets as QtGui
    #version =2017
elif version == 2015:
    #from PySide import QtCore,QtGui
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    import PySide
    import pysideuic
    import shiboken

#############################################################################################

def loadUiType(uiFile):
    """
    Pyside lacks the "loadUiType" command, so we have to convert the ui file to py code in-memory first
    and then execute it in a special frame to retrieve the form_class.
    """
    parsed = xml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text
	
    with open(uiFile, 'r') as f:
        o = StringIO()
        frame = {}
			
        pysideuic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame
        #Fetch the base_class and form class based on their type in the xml from designer
        form_class = frame['Ui_%s'%form_class]
        if version > 2015:
            base_class = getattr(PySide.QtWidgets, widget_class)
        elif version == 2015:
            base_class = eval('QtGui.%s'%widget_class)
    return form_class, base_class

if __name__ == "__main__":
    UI_file = os.path.join(r"C:\Users\nagikuan\Documents\maya\scripts_pip\Pipeline", 'ui', 'main_ui_3.ui')
else:
    UI_file = os.path.join(os.path.dirname(__file__), 'ui', 'main_ui_3.ui')
formClass , baseClass = loadUiType(UI_file)

try:
    cmds.deleteUI("pipeDock")
except:
    pass

def getMayaWindow():
    '''
    Get the maya main window as a QMainWindow instance
    '''
    ptr = apiUI.MQtUtil.mainWindow()

    if hasattr(QtGui,"QMainWindow") :
        return shiboken.wrapInstance(long(ptr), QtGui.QMainWindow)
    if hasattr(PySide.QtWidgets,"QMainWindow"):
        return shiboken.wrapInstance(long(ptr), PySide.QtWidgets.QMainWindow)

class pipeWindow(formClass, baseClass):
    '''
    Main Class
    '''
    def __init__(self, parent = getMayaWindow()):
        '''
        Initialize
        '''
        super(pipeWindow,self).__init__(parent)
        self.setupUi(self)
        self.setObjectName('pipe_window')
        self.project = ""
        self.projIndex = self.projCombo.currentIndex()
        
        self.scnRawCode = createXML.deCode(find = "SceneFileName")[self.projIndex]        
        self.scnFileName=decode.dollarDecode(raw=self.scnRawCode)
        
        self.sceneCode = [ q for q in self.scnFileName if "scn" ==q[0]][0][1]
        self.shotsCode = [ q for q in self.scnFileName if "sht" ==q[0]][0][1]
        self.versionCode = [ q for q in self.scnFileName if "ver" ==q[0]][0][1]
        self.oriHud = playblastTool.customPBMask().oriHudStatus()
        #################################################################################
        ##Create connections                                                           ##
        #################################################################################
        
        self.projCombo.clear()
        self.project = createXML.deCode(find="Project")
        self.scnFolder = cmds.workspace(fre="scene")
        
        for combo in self.project:
            self.projCombo.addItem(combo)
        
        self.projCombo.currentIndexChanged.connect(self.func_projCombo)
        #self.projCombo.setCurrentIndex(1)
        
        #Layout Setup Tab(r"%0"+str(6)+"d") % 1
        #self.SceneCombo.addItems([(r"%0"+str(self.sceneCode.split("$F")[-1])+"d") % i for i in range(1,100)]) #For Scene Combo on Layout Setup Tab
        #self.ShotsCombo.addItems([(r"%0"+str(self.shotsCode.split("$F")[-1])+"d") % i for i in range(1,100)])
        
        self.directory = createXML.deCode(find = "Directory")
        #self.projIndex = self.projCombo.currentIndex()

        self.assetTypeCombo.currentIndexChanged.connect(self.func_assetTypeCombo)
        
        #Add file names into list of selected assets column
        self.ModelsRigsCol.itemDoubleClicked.connect(self.func_ModelsRigsCol)
        self.addAssetBt.clicked.connect(self.func_ModelsRigsCol)
        
        #Remove file names from list of selected assets column
        self.SelectedAssetsCol.itemDoubleClicked.connect(self.func_delAssetBt)
        self.delAssetBt.clicked.connect(self.func_delAssetBt)
        
        #Clear all items in the list of selected assets column
        self.resetBt.clicked.connect(self.func_resetBt)
        
        #Duplciate all selected items in the list of selected assets column
        self.dupAssetBt.clicked.connect(self.func_dupAssetBt)
        
        #Reference
        self.referenceBt.clicked.connect(self.func_referenceBt)
        
        #Playblast Mask Function
        self.bt_PBM0.clicked.connect(self.func_bt_PBM0)
        self.bt_PBM2.clicked.connect(self.func_bt_PBM2)
        self.bt_PBM4.clicked.connect(self.func_bt_PBM4)        
        self.bt_PBM5.clicked.connect(self.func_bt_PBM5)
        self.bt_PBM7.clicked.connect(self.func_bt_PBM7)
        self.bt_PBM9.clicked.connect(self.func_bt_PBM9)
        
        self.bt_TogglePBM.clicked.connect(self.func_bt_TogglePBM)
        self.bt_loadPBM.clicked.connect(self.func_bt_loadPBM)
        self.bt_resetPBM.clicked.connect(self.func_bt_resetPBM)
        
        #Overwrite Checkbox
        self.overwriteChbox.setChecked(False)
        
        ###################################################################################
        ##Create Layout and Dock Control                                                 ##
        ###################################################################################
        if cmds.dockControl('pipeDock', q=1, ex=1):
            cmds.deleteUI('pipeDock')#cmds.deleteUI('dockPane')

        self.pane = cmds.paneLayout('dockPane',cn='single')
        cmds.dockControl('pipeDock',con=self.pane , area = 'right',allowedArea = ['right','left'],label = "ANMD_Pipeline",w=365)
        cmds.control( 'pipe_window', e = True, p = self.pane)
        
        self.projCombo.addItem("useless")
        self.projCombo.setCurrentIndex(1)
        self.projCombo.setCurrentIndex(0)
        self.projCombo.removeItem(self.projCombo.count()-1)
    #####################################################################################
    ##FUNCTIONS CONNECT                                                                ##
    #####################################################################################
    def func_projCombo(self):
        self.projIndex = self.projCombo.currentIndex()
        
        self.scnRawCode = createXML.deCode(find = "SceneFileName")[self.projIndex ]        
        self.scnFileName=decode.dollarDecode(raw=self.scnRawCode)
        
        self.sceneCode = [ q for q in self.scnFileName if "scn" ==q[0]][0][1]
        self.shotsCode = [ q for q in self.scnFileName if "sht" ==q[0]][0][1]
        self.versionCode = [ q for q in self.scnFileName if "ver" ==q[0]][0][1]
        
        self.scnFolder = cmds.workspace(fre="scene")
        if ";" in self.scnFolder:
            self.scnFolder = cmds.workspace(fre="scene").split(";")
        PL.layoutSetupClass().projSelection(self)
        PFile.fileLoaderClass().findSceneFolders(self)
        
        self.pbMaskCode = createXML.deCode(find = "maskCode")[self.projIndex ]
        self.pbMaskInfo=decode.dollarDecode(raw=self.pbMaskCode,split=";") 
        playblastTool.customPBMask().initialPBMask(self)             

    def func_assetTypeCombo(self):
        PL.layoutSetupClass().assetTypeSelection(self)

    def func_ModelsRigsCol(self):
        PL.layoutSetupClass().modelsRigsSelection(self)

    def func_delAssetBt(self):
        PL.layoutSetupClass().deSelect(self)

    def func_resetBt(self):
        PL.layoutSetupClass().reset(self)

    def func_dupAssetBt(self):
        PL.layoutSetupClass().dup(self)

    def func_referenceBt(self):
        PL.layoutSetupClass().loadnSave(self)
        
    #File loader section
    def func_scneCombo(self):
        self.animScn = self.scnCombo.currentText()
        
    #PlayBlast Mask section
    def func_bt_PBM0(self):
        playblastTool.customPBMask().pbButton(self,maskInd=0)
    def func_bt_PBM2(self):
        playblastTool.customPBMask().pbButton(self,maskInd=2)
    def func_bt_PBM4(self):
        playblastTool.customPBMask().pbButton(self,maskInd=4)
    def func_bt_PBM5(self):
        playblastTool.customPBMask().pbButton(self,maskInd=5)
    def func_bt_PBM7(self):
        playblastTool.customPBMask().pbButton(self,maskInd=7)
    def func_bt_PBM9(self):
        playblastTool.customPBMask().pbButton(self,maskInd=9)
        
    def func_bt_TogglePBM(self):
        playblastTool.customPBMask().pbSwitch(self)
        
    def func_bt_loadPBM(self):
        playblastTool.customPBMask().PBrefresh(self)
        
    def func_bt_resetPBM(self):
        playblastTool.customPBMask().PBrefresh(self,reset=1)
        
    def closeEvent(self,event):
        for (hud,visi) in self.oriHud:
            cmds.headsUpDisplay(hud,e=1,vis=visi)
        for hud in cmds.headsUpDisplay(lh=1) :
            if "pbMask" in hud:
                cmds.headsUpDisplay(hud,e=1,rem=1)
        super(pipeWindow, self).closeEvent(event)
        #del PL,Pipeline

if __name__ == "__main__":
    pipeWindow()
