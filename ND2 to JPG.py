#import javabridge as jv
#jv.start_vm(class_path=BF.JARS, max_heap_size='8G') 
# The above will increase the amount of memory available to Java. 
# This is important for large images, multipoint files, or files
# with a lot of metadata.

from ij import IJ
from fiji.util.gui import GenericDialogPlus
from loci.plugins import BF
from ij.io import FileSaver
import os

def run():
    gd = GenericDialogPlus("ND2 Conversion Tool")
    gd.addMessage("This plugin uses BioFormats to convert ND2 images to various file formats for further processing in ImageJ.")
    gd.addDirectoryOrFileField("Input: ", "Z:\\") #srcDir
    gd.addDirectoryOrFileField("Output: ", "Z:\\") #dstDir
    gd.addStringField("File name contains: ", "") #nameContains
    gd.addCheckbox("Preserve directory structure?", True) #keepDirs
    gd.addCheckbox("Run in headless mode?", False) #anneBoleyn 
    #overwrite existing JPGs?
    gd.showDialog()
    if gd.wasCanceled():
        return
    srcDir = gd.getNextString()
    dstDir = gd.getNextString()
    nameContains = gd.getNextString()
    keepDirectories = gd.getNextBoolean()
    anneBoleyn = gd.getNextBoolean()
    for root, directories, filenames in os.walk(srcDir):
        for filename in filenames:
            # Check for file extension
            if not filename.endswith(".nd2"):
                continue
            # Check for file name pattern
            if nameContains not in filename:
                continue
            process(srcDir, dstDir, nameContains, root, filename, keepDirectories, anneBoleyn)

def process(srcDir, dstDir, nameContains, currentDir, fileName, keepDirectories, anneBoleyn):
    print "Opening", fileName
    saveDir = currentDir.replace(srcDir, dstDir) if keepDirectories else dstDir
    imps = BF.openImagePlus(os.path.join(currentDir, fileName))
    print "Opened", fileName
    for imp in imps:
        if not anneBoleyn:
            print "Now showing image..."
            imp.show()
    fs = FileSaver(imp)
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
    print "Saving to", saveDir
    fs.saveAsJpeg(os.path.join(saveDir, fileName))
    #IJ.selectWindow("Log")
    #IJ.run("Close")
    imp.close()

run()
