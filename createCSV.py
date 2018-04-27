import os
from subprocess import call
import csv

projName = raw_input("Enter Project Name: ")
numOfScn = int(raw_input("Enter Number of Scenes: "))

scnName = []
for q in xrange(numOfScn): #number of scenes
    q = q+1
    scnName.append(os.path.join("sc"+'%03d'%q))

outputFile = os.path.join("D:\\"+projName+"_"+"tacticData"+".csv")

keyInList = []
regScnList = []

with open(outputFile,'wb') as g:
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

        #print "key in sum:",sum(keyInList)
        #print "registered sum :",sum(regScnList)
        if sum(keyInList) == sum(regScnList):
            keep_running = False
            break
        



##with open(outputFile,'r') as inf:
##    reader = inf.read()
##    for j in scnName:
##        
##        inf.write(output)
        
##    for lines in inf:
##        print lines
##    reader = csv.DictReader(inf)

##        for ind, row in enumerate(reader):
##            if ind == 0:
##                pass
##            elif ind == 1:
##                pass
##            else:
##                row = row + ['Scn']
##                print row
##            print row
            
##            writefile.writerow({
##                header[2]:k[ind]
##                })

        
