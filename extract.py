import shutil
import glob
import os
import inkml2img
from datetime import datetime

dataPath = 'CROHME_labeled_2016/'
dataMergedPath = 'data_merged/'
targetFolder = 'data_processed/'
logger = open('log.txt', 'w+')
    
def writeLog(message):
    logger.write("[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] " + str(message) + "\n")

def createDirectory(dirPath):
    if not os.path.exists(dirPath): 
        os.mkdir(dirPath)
        writeLog("Create " + dirPath)

if __name__ == "__main__":
    writeLog("Start processing.")
    filesPath = glob.glob(dataPath + '*/*.inkml')
    writeLog("There are " + str(len(filesPath)) + " files in " + dataPath)
    createDirectory(dataMergedPath)

    cnt = 0
    for fileName in filesPath:
        cnt = cnt + 1
        print("Copying %d/%d" % (cnt, len(filesPath)))
        writeLog("Copied " + fileName + " --> " + dataMergedPath + fileName)
        shutil.copy2(fileName, dataMergedPath)

    createDirectory(targetFolder)

    listFiles = glob.glob(dataMergedPath + '*.inkml')
    numberOfFile = len(listFiles)
    writeLog("There are " + str(numberOfFile) + " files in " + dataMergedPath)
    cnt = 0

    for fileInkml in listFiles:
        cnt = cnt + 1
        fileName = fileInkml.split('\\')[1]
        print("Processing %s [%d/%d]" % (fileName, cnt, numberOfFile))
        writeLog("[" + str(cnt) + "/" + str(numberOfFile) + "]" + "Processed " + fileInkml + " --> " + targetFolder + fileName + ".png")
        try:
            inkml2img.inkml2img(fileInkml, targetFolder + fileName.split('.')[0] + '.png')
        except:
            writeLog("Failed!")
            print("An error occured!")

        writeLog("Successful!")

