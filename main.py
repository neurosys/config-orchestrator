#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET

# ToDo
# - Options: 
#    * generate only one file
#    * list IDs from config file
#    * backup if exists
#    * do not overwrite

isDebug = False
LVL1_TAG = "configuration"

def dbg(msg):
    global isDebug
    if isDebug == True:
        print(msg)

def showHelp():
    helpText = """
Usage: orchestrator.py [OPTION]... 
Assemble config files from pieces based on a xml file that describes the operation
Example: orchestrator.py --config=sample.xml 

Options:
    --config=PATH          PATH to the xml describing the steps for creating the files
    --debug                Enable debug information
    --help                 Shows this help message
    --only=SECTION         Generate only SECTION and ignore all other files
    --list                 List the files for which we have assemble steps
    --no-overwrite         Don't overwrite the destinations
    --backup-if-exists     If the target exists, it will be backed up as <name>_bkp
    """
    print(helpText)

class Params():
    def __init__(self, args):
        self.pathToConfigFile = None
        self.sectionToGenerate = None
        self.generateAll = True
        self.showHelp = False
        self.showDebug = False
        self.listIds = False
        self.noOverwrite = False
        self.backupIfExists = False
        self._parseParams(args)
        self._validate()

    def _parseParams(self, args):
        global isDebug
        # First parameter is the name of the script and we don't care aout it
        for arg in args[1 : ]:
            dbg("TRACE: Params::_parseParams() arg = " + arg)
            if arg == "--debug":
                self.showDebug = True
                isDebug = True
            elif arg == "--help":
                self.showHelp = True
            elif arg.startswith("--config=") == True:
                self.pathToConfigFile = arg.split("=")[1]
            elif arg.startswith("--only="):
                self.sectionToGenerate = arg.split("=")[1]
                self.generateAll = False
            elif arg == "--list":
                self.listIds = True
            else:
                print("ERROR: Unknown parameter '" + arg + "'")

    def __str__(self):
        textRepresentation = "Params {\n"
        textRepresentation += "\tpathToConfigFile = " + str(self.pathToConfigFile) + "\n"
        textRepresentation += "\tsectionToGenerate = " + str(self.sectionToGenerate) + "\n"
        textRepresentation += "\tgenerateAll = " + str(self.generateAll) + "\n"
        textRepresentation += "\tshowHelp = " + str(self.showHelp) + "\n"
        textRepresentation += "\tshowDebug = " + str(self.showDebug) + "\n"
        textRepresentation += "\tlistIds = " + str(self.listIds) + "\n"
        textRepresentation += "\tnoOverwrite = " + str(self.noOverwrite) + "\n"
        textRepresentation += "\tbackupIfExists = " + str(self.backupIfExists) + "\n"
        textRepresentation += "}\n"
        return textRepresentation

    def _validate(self):
        dbg(str(self))
        if self.showHelp or self.listIds:
            return True
        elif self.pathToConfigFile == None:
            print("ERROR: No config file specified")
            self.showHelp = True

class FilePart():
    def __init__(self):
        self.sourceFile = None
        self.orderIndex = None
        self.oldNeedle = None
        self.newNeedle = None

class ConfigFile():
    def __init__(self):
        self.id = None
        self.destination = None
        self.fileParts = None
        self.inlineValues = None

class XmlParser():
    def __init__(self, pathToXml):
        self.pathToXml = pathToXml
        self.tree = ET.parse(self.pathToXml)
        self.root = self.tree.getroot()

    def parse(self):
        if self.root.tag != LVL1_TAG:
            print("ERROR: Invalid config, can't find " + LVL1_TAG)
            dbg("XmlParser: Parse() instead of " + LVL1_TAG + " found self.root.tag = '" + self.root.tag + "'")
            sys.exit(1)
        for child in self.root:
            self.parseFileStructure(child)

    def parseFileStructure(self, node):
        self.printNode(node)
        for child in node:
            self.printNode(child)


    def test(self):
        self.printNode(self.root)
        for child in self.root:
            self.printNode(child)

    def printNode(self, node):
        textReprOfNode = ""
        textReprOfNode += "<" + node.tag + " " 
        for k in node.attrib:
            textReprOfNode += k + "=\"" + node.attrib[k] + "\" "
        print(textReprOfNode + "/>")

class FileBuilder():
    def __init__(self, pathToConfig):
        self._confFile = pathToConfig



if __name__ == "__main__":
    config = Params(sys.argv)

    if config.showHelp == True:
        showHelp()
        sys.exit(0)

    parser = XmlParser(config.pathToConfigFile)
    #parser.test()
    parser.parse()
