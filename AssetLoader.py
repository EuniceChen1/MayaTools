import os
import maya.cmds as cmds
import maya.mel as mel
from Pipeline.misc import createXML
from Pipeline.misc import decode
class layoutSetupClass(object):
    ###################################################################################################
    ##FOR PROJECT SELECTION MENU                                                                     ##
    ###################################################################################################
       
    def projSelection(self, object):
        '''
        Selecting the relevant project index number and set project
        '''
        
        #object.projIndex = object.projCombo.currentIndex()        
        mel.eval(r'setProject "%s"' %createXML.deCode(find = "Directory")[object.projIndex].replace("\\","/"))
        object.SceneTypeLabel.setText(object.SceneTypeLabel.text().split(":")[0]+": %s"%object.sceneCode.split("$")[0])
        object.ShotsTypeLabel.setText(object.ShotsTypeLabel.text().split(":")[0]+": %s"%object.shotsCode.split("$")[0])
        object.SceneCombo.clear()
        object.ShotsCombo.clear()
        object.SceneCombo.addItems([(r"%0"+str(object.sceneCode.split("$F")[-1])+"d") % i for i in range(1,100)]) #For Scene Combo on Layout Setup Tab
        object.ShotsCombo.addItems([(r"%0"+str(object.shotsCode.split("$F")[-1])+"d") % i for i in range(1,100)])    
        object.assetTypeCombo.setCurrentIndex(1)
        object.assetTypeCombo.setCurrentIndex(0)
        
    ####################################################################################################
    ##FOR LAYOUT SETUP TAB                                                                            ##
    ####################################################################################################

    def assetTypeSelection(self, object):
        '''
        Every time an asset type is chosen, the directories related to that project and 
        asset folder will be shown on the Models Rigs Column
        '''
        self.assetIndex = object.assetTypeCombo.currentIndex()
        object.dir = createXML.deCode(find = "Directory")[object.projIndex]+"\\%s\\"%cmds.workspace(fileRuleEntry = 'templates')+createXML.deCode(find = "assetType")[object.projIndex].split(",")[self.assetIndex]
        print object.dir
        object.ModelsRigsCol.clear()
        
        for root, dirs, files in os.walk(object.dir):     
            for file_name in files:
                if file_name.endswith('.ma') or file_name.endswith('.mb'):    
                    filePath = os.path.join(root, file_name)
                    object.ModelsRigsCol.addItem(file_name+"\t--\t" +filePath) 
        
    def modelsRigsSelection(self, object):
        '''
        Every time an item is clicked in the Models/Rigs column, it will
        show in the List of Selected Assets column
        '''
        #selected items from the models/rigs column
        object.items = object.ModelsRigsCol.selectedItems() 
        #print self.items[self.projIndex]
        
        for i in object.items:
            object.itemsName = i.text().split(".") #redifining to split the name and the extension
            #object.fullPath = object.dir+"\\"+object.itemsName[0]+"\\"+i.text()
            object.SelectedAssetsCol.addItem(i.text())#object.SelectedAssetsCol.addItem(i.text()+ "\t--\t" + object.dir + "\\" + object.itemsName[0] + "\\")
            object.SelectedAssetsCol.clearSelection()

    def deSelect(self, object):
        '''
        Deselect by double clicking or clicking the delete button
        '''
        object.deselect = object.SelectedAssetsCol.selectedItems()
        
        for j in object.deselect:
            object.SelectedAssetsCol.takeItem(object.SelectedAssetsCol.row(j))
            
    def dup(self, object):
        '''
        Duplicate all selected items inside list of selected assets column
        '''
        object.dup = object.SelectedAssetsCol.selectedItems()
        
        for k in object.dup:
            object.SelectedAssetsCol.addItem(k.text())
            
    def reset(self, object):
        '''
        Reset List of Selected Assets Column
        '''
        object.SelectedAssetsCol.clear()   
        
    def loadnSave(self, object):
        '''
        Create reference file and save them in the designated directory with a fix format of file names
        '''
        object.saveitems = []
        for index in xrange(object.SelectedAssetsCol.count()):
            object.saveitems.append(object.SelectedAssetsCol.item(index))
        
        object.path = createXML.deCode(find = "Directory")
        
        object.ScenePath = object.path[object.projIndex]+"\\%s\\" %object.scnFolderList[0]
        #create Scene Path
        if not os.path.exists(object.ScenePath):
            os.makedirs(object.ScenePath)
        
        object.SceneFolder = object.ScenePath+object.sceneCode.split("$")[0]+object.SceneCombo.currentText()

        #create Scene Folder
        if not os.path.exists(object.SceneFolder):
            os.makedirs(object.SceneFolder)
          
        object.ShotPath = object.SceneFolder+"\\"
        object.ShotFolder = object.ShotPath+object.shotsCode.split("$")[0]+object.ShotsCombo.currentText()
        
        #create Shots Path  
        if not os.path.exists(object.ShotFolder):
            os.makedirs(object.ShotFolder)
        
        #version = '{:03d}'.format(1)
        fullname = object.scnFileName
        nameList = []
        
        for ind,(key,val) in enumerate(fullname):
            if "$F" in val:
                if "scn" in key:
                    scns = val.split("$F")
                    nameList.append(scns[0]+object.SceneCombo.currentText())
                    scnLoc = ind
                if "sht" in key:
                    shts = val.split("$F")
                    nameList.append(shts[0]+object.ShotsCombo.currentText())
                    shtLoc = ind
                if "ver" in key:
                    vers = val.split("$F")
                    nameList.append(vers[0]+('{:0%sd}'%vers[1]).format(1))
                    versionLoc = ind
            if "user" in key:
                nameList.append(val)
            if "ext" in key:
                extension = "."+val 
                nameList.append(extension)
                if val == 'ma':
                    extension = "mayaAscii"
                if val == 'mb':
                    extension = "mayaBinary"
                    
            if "proj" in key:
                nameList.append(val)
                
        fullname = "_".join(nameList[:-1])+nameList[-1]
        #fullname = object.projCombo.currentText().split("--")[-1] +"_Sc"+object.SceneCombo.currentText()+"_Sh"+object.ShotsCombo.currentText()+"_V"+version+".ma"
        
        renameFile = object.ShotFolder+"\\"+ fullname 
        
        for ref in object.saveitems: 
            splitref = ref.text().split("\t")
            cmds.file(splitref[-1], reference = True, namespace = splitref[0].split(".")[0])
        
        fileNameList = renameFile.split("\\")
        #vers = fileNameList[-1].split("_V")
        #extension = fullname.split(".")[-1]
        
        #goes through the list of filenames
        var = os.listdir(object.ShotFolder)
        #print "var :", var
        
        ######################################################################################
        ## If file exists in the path above, loop with the following conditions:            ##
        ##    1) filename ends with .ma or .mb                                              ##
        ##    2) filename has the word 'Sc00x'                                              ##
        ##    3) filename has the word 'Sh00x'                                              ##
        ## Append the filenames into the list, add the len of the list by 1 for every loop  ##
        ## Save the file                                                                    ##
        ######################################################################################
        
        #print "File exists :",os.path.exists(renameFile),renameFile
        
        if os.path.exists(renameFile) == True:
            saveFileList = []
            for filenames in var:                
                if ((filenames.endswith('.ma')) or (filenames.endswith('.mb'))) and (filenames.split("_")[scnLoc] in fullname.split("_")[scnLoc]) and (filenames.split("_")[shtLoc] in fullname.split("_")[shtLoc]):
                    saveFileList.append(filenames) 
                    #print "saveFileList :", saveFileList
                
            vchg = int(len(saveFileList)) + int(1)            
            nameList[versionLoc] = vers[0]+('{:0%sd}'%vers[1]).format(vchg)
            saveName = "\\".join(fileNameList[:-1])+"\\"+"_".join(nameList[:-1])+nameList[-1]
                                
            if object.overwriteChbox.isChecked():     
                cmds.file(rename="\\".join(fileNameList[:-1])+"\\"+var[-1])
                print 'Overwriting %s.' % var[-1]
                cmds.file(force=True, type=extension, save=True) 
            else:
                cmds.file(rename=saveName)
                print 'Creating new version %s.' % saveName
                cmds.file(force=True, type=extension, save=True)
                    
        else:
            #save for the first time
            print "Creating new folder and file for %s." % renameFile
            cmds.file(rename=renameFile)
            cmds.file(force=True, type=extension, save=True)

        #cmds.progressBar("MainProgressBar",edit=True, step=1) 

