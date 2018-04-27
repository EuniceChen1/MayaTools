import os
from subprocess import call
import csv

projName = raw_input("Enter Project Name: ")
numOfScn = int(raw_input("Enter Number of Scenes: "))

scnName = []
for q in xrange(numOfScn): #number of scenes
    q = q+1
    scnName.append(os.path.join("sc"+'%03d'%q))

outputFileA = os.path.join("D:\\"+"proxy"+".csv")

keyInList = []
regScnList = []
header = ["Scene","Shot"]

with open(outputFileA,'wb') as g:
    fieldnames = ["Scene","Shot"]
    wr = csv.DictWriter(g,fieldnames=fieldnames)
    wr.writeheader()
    
    keep_running = True
    while (keep_running):
        for i in scnName:
            scnInfo = raw_input("Enter Scene Number, No of Shots in this Scene: ").split(",")
            keyInScn = scnInfo[0].split("c")[-1]
            regScnNum = scnName[-1].split("c")[-1]
            
            regScnElem = i.split("c")[-1]
            
            keyInList.append(int(keyInScn))
            regScnList.append(int(regScnElem))

            assert ( keyInScn <= regScnNum ), "This scene number is not registered in the database"
            if scnInfo[0] in scnName:
                for k in xrange(int(scnInfo[1])):
                    k=k+1
                    wr.writerow({
                                fieldnames[0]:scnInfo[0],
                                fieldnames[1]:(os.path.join("sh"+'%03d'%k))
                                })
            else:
                print "This scene number does not exist!"
                continue

        if sum(keyInList) == sum(regScnList):
            keep_running = False
            break
        

scnList=[]
outputFileB = os.path.join("D:\\"+projName+"_"+"tacticData"+".csv") #YOUR OWN PATH

with open(outputFileA,'r') as inf:
    with open(outputFileB,'wb') as outf:
        reader = inf.readlines()
        for ind, j in enumerate(reader):
            if ind == 0:
                reader[ind] = "Scn,"+j
            else:
                if ind-1 >= len(scnName):
                    reader[ind] = ","+j
                else:
                    reader[ind] = scnName[ind-1]+","+j
                    
            outf.write(reader[ind])

os.remove(outputFileA)
    
    
        

