# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 00:31:23 2021

@author: manoj
"""
import subprocess
from collections import defaultdict
from Validator import Validator
from ParameterFile import ParameterFile
from FileFormatter import FileFormatter
from PublishResults import PublishResults
from ExtractDetails import ExtractDetails
import pathlib

class GetStorage:

    '''
    Initialize GetStorage variables
    path          : specifies the path from where the disk space results will be generated
    osProxy       : specifies the path is a Linux, Windows, MacOs, etc. OS
    scriptName    : specifies the name of the script which will be run in target OS from python
    fileFormat    : specifies what file format the disk space results will be formatted to like json, xml, etc.
    publishType   : specifies how the results will be publised i.e. store in local disk, email, transfer to a shared path, etc.
    '''
    def __init__(self, path, osProxy, scriptName, fileFormat, publishType):
        self.path = path
        self.osProxy = osProxy
        self.scriptName = scriptName
        self.fileFormat = fileFormat
        self.publishType = publishType
        self.initializeClassObjects()
        self.initializeGlobalVariables()

    '''
    Initialize GetStorage -> Object variables
    validator     : Object of class Validator used for all validation
    fileFormatter : Object of class FileFormatter used for all valid file formatting
    publishResults: Object of class PublishResults used for all valid publish results
    extractDetails: Object of class ExtractDetails used for all valid extract details method
    '''
    def initializeClassObjects(self):
        self.validator = Validator()
        self.fileFormatter = FileFormatter()
        self.publishResults = PublishResults()
        self.extractDetails = ExtractDetails()

    '''
    osList         : All valid operating system this product will be utilized in to capture the results
    fileFormatList : All valid file formatting this product will be utilized in to capture the results
    rawFilePath    : Temporary storage path for manipulation, default is current directory 
    resultsFileName: File name where the results will be captured before transmission
    commonFrameworkResults: Common framework results used for intermediate storage  
    '''
    def initializeGlobalVariables(self):
        self.osList = ["Linux", "Windows"]
        self.fileFormatList = ["json", "xml", "txt"]
        self.rawFilePath = ''
        self.resultsFileName = 'diskSpaceInfo'
        self.commonFrameworkResults = defaultdict(list)

    def validateParameters(self):
        '''
        Validate all the parameters set in __init__ class
        '''        
        if not self.validator.validateNull(self.path):
            print('<<< path parameter cannot be null, so setting default to current directory >>>')
            #add to Logger details
        
        if not self.validator.validateNull(self.osProxy):
            print('<<< osProxy parameter cannot be null, setting default to Windows >>>')
            #add to Logger details
            
        if not self.validator.validateGetValue(self.osProxy, self.osList):
            print('<<< osProxy parameter should be one of the value from: ', self.osList, '>>>')
            #add to Logger details
        
        if not self.validator.validateNull(self.scriptName):
            print('<<< scriptName paramtere cannot be null, setting default to Windows scriptName >>>')
            if self.osProxy == 'Windows':
                self.scriptName = 'folderPathFileSizeInfo.bat'
            elif self.osProxy == 'Linux':
                self.scriptName = 'folderPathFileSizeInfo.bash'
            #add error logger
        
        if not self.validator.validateNull(self.fileFormat):
            print('<<< fileFormat parameter cannot be null, so setting default to json format >>>')
            #add to Logger details
            
        if not self.validator.validateGetValue(self.fileFormat, self.fileFormatList):
            print('<<< fileFormat should be one of the value from: ', self.fileFormatList, '>>>')
            #add to Logger details
        
    def getStorageDetails(self):
        '''
        Trigger OS Specific script to extract file disk space in raw format under /TempStorage/rawFileOutput.txt
        '''        
        self.runScript()
            
    def runScript(self):
        '''
        Trigger script to capture disk space
        '''
        currentPath = str(pathlib.Path(__file__).parent.resolve())
        parameter2 = currentPath
        if self.osProxy == 'Linux':
            parameter1 = currentPath + "/TempStorage/rawFileOutput.txt"
            subprocess.run(['/bin/bash', './Scripts/folderPathFileSizeInfo.bash'])
        elif self.osProxy == 'Windows':
            #This is used for asynchronous Process
            parameter1 = currentPath + "\\TempStorage\\rawFileOutput.txt"
            scriptRunPath = currentPath + "\\Scripts\\folderPathFileSizeInfo.bat"
            p = subprocess.Popen([scriptRunPath, parameter1, parameter2], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = p.communicate()
            p.wait() # wait for process to terminate
        self.rawFilePath = parameter1

    def loadStorage(self):
        '''
        Set the search string based on osProxy parameter
        '''
        if self.osProxy == 'Linux':
            currentPath = str(pathlib.Path(__file__).parent.resolve())
            self.commonFrameworkResults = self.extractDetails.extractDetailsLinux(currentPath, self.rawFilePath)
        elif self.osProxy == 'Windows':
            searchString = 'Directory of'
            self.commonFrameworkResults = self.extractDetails.extractDetailsWindows(searchString, self.rawFilePath)
    
    def formatFile(self):
        '''
        Format the common framework file into user specifed file format, if provided none default is .txt
        '''
        currentPath = str(pathlib.Path(__file__).parent.resolve())
        if self.osProxy == 'Windows':
            PublishFilePath = currentPath + "\\PublishResults\\" + self.resultsFileName
        else:
            PublishFilePath = currentPath + "/PublishResults/" + self.resultsFileName
        if self.fileFormat.lower() == "json":
            self.resultsFileName = PublishFilePath + ".json"
            self.transferResults = self.fileFormatter.loadJsonFileFormat(self.commonFrameworkResults)
        elif self.fileFormat.lower() == "xml":
            self.resultsFileName = PublishFilePath + ".xml"
            self.transferResults = self.fileFormatter.loadXMLFileFormat(self.commonFrameworkResults)
        else:
            self.resultsFileName = PublishFilePath + ".txt"
            self.transferResults = self.fileFormatter.loadTextFileFormat(self.commonFrameworkResults)
    
    def resultsPublisher(self):
        if self.publishType.lower() == 'disk':
            self.publishResults.transferFileToDisk(self.resultsFileName, self.commonFrameworkResults)
        elif self.publishType.lower() == 'email':
            self.publishResults.transferFileToEmail(self.resultsFileName, self.commonFrameworkResults)
        elif self.publishType.lower() == 'transfer':
            self.publishResults.transferFileToSharedServer(self.resultsFileName, self.commonFrameworkResults)
        else:
            self.publishResults.transferFileToDisk(self.resultsFileName, self.commonFrameworkResults)

parameterFile = "param.json"
#Initialize ParameterFile Class
parameterFile = ParameterFile(parameterFile)
osProxy, scriptName, fileFormat, publishType, path = parameterFile.readParameterFile()
newPath = r'C:\{}'.format(path)

#Initialize GetStorage Class
getStorage = GetStorage(newPath, osProxy, scriptName, fileFormat, publishType)
#Validate All Parameters
getStorage.validateParameters()

#Get Storage Details
getStorage.getStorageDetails()
#Run Script Which Captures File Disk Space And Generates A Raw File
getStorage.runScript()
#Load & Extract The Script Raw File OutPut Into A Temporary Common Format
getStorage.loadStorage()
#Detect Output File Formatter
getStorage.formatFile()
#Load The Disk Space Storage Details Into Desired Format
getStorage.resultsPublisher()