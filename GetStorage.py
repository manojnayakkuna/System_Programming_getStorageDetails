# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 00:31:23 2021

@author: manoj
"""
import subprocess
from collections import defaultdict
from Validator import Validator
import pathlib
import json
import sys
#import pickle
#import os

class GetStorage:

    def __init__(self, path, osProxy, scriptName, fileFormat, publishType, validator):
        '''
        Initialize class variable parameters
        path          : specifies the path from where the disk space results will be generated
        osProxy       : specifies the path is a Linux, Windows, MacOs, etc. OS
        scriptName    : specifies the name of the script which will be run in target OS from python
        fileFormat    : specifies what file format the disk space results will be formatted to like json, xml, etc.
        publishType   : specifies how the results will be publised i.e. store in local disk, email, transfer to a shared path, etc.
        validator     : Object of class Validator used for all validation
        osList        : All valid operating system this product will be utilized in to capture the results
        fileFormatList: All valid file formatting this product will be utilized in to capture the results
        rawFilePath   : Temporary storage path for manipulation, default is current directory 
        '''
        self.path = path
        self.osProxy = osProxy
        self.scriptName = scriptName
        self.fileFormat = fileFormat
        self.publishType = publishType
        self.validator = validator
        self.osList = ['Linux', 'Windows']
        self.fileFormatList = ['json', 'xml']
        self.commonFrameworkResults = defaultdict(list)
        self.rawFilePath = ''
        self.resultsFileName = 'diskSpaceInfo'
        
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
        Trigger scriptName.bat or scriptName.bash using python library subprocess to extract file 
        disk space in raw format under /TempStorage/rawFileOutput.txt
        '''        
        self.runScript()
            
    def runScript(self):
        '''
        Trigger script to capture disk space
        '''
        currentPath = str(pathlib.Path(__file__).parent.resolve())
        parameter1 = currentPath + "\\TempStorage\\rawFileOutput.txt"
        parameter2 = currentPath
        if self.osProxy == 'Linux':
            subprocess.run(['/bin/bash', './Scripts/folderPathFileSizeInfo.sh rawFileOutput.txt'])
        elif self.osProxy == 'Windows':
            #This is used for asynchronous Process
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
            searchString = ''
            self.extractDetailsLinux(searchString)
        elif self.osProxy == 'Windows':
            searchString = 'Directory of'
            self.extractDetailsWindows(searchString)
    
    def extractDetailsWindows(self, searchString):
        '''
        Read raw output file 'rawFileOutput.txt' to load into a common temporary variable for Windows
        '''
        results = defaultdict(list)
        with open(self.rawFilePath) as file:
            tempKey = ''
            for line in file:
                if len(line.strip()) > 0:
                    if searchString in line[1:14]:
                        tempKey = line[14:].replace('\n','')
                        results.get(tempKey, [])
                    elif line[0] != ' ':
                        record = [value for value in line.split(' ') if value != '']
                        fileName = record[4].replace('\n','')
                        fileSize = int(record[3].replace(',', ''))
                        results[tempKey].append(dict({fileName: fileSize}))
                        
        self.commonFrameworkResults = results
    
    def extractDetailsLinux(self, rawFileName):
        '''
        Read raw output file 'rawFileOutput.txt' to load into a common temporary variable for Linux
        '''
        pass
    
    def fileFormatter(self):
        '''
        Format the common framework file into user specifed file format, if provided none default is .txt
        '''
        currentPath = str(pathlib.Path(__file__).parent.resolve())
        PublishFilePath = currentPath + "\\PublishResults\\" + self.resultsFileName
        if self.fileFormat.lower() == 'json':
            self.transferResults = self.loadJsonFileFormat()
            self.resultsFileName = PublishFilePath + '.json'
        elif self.fileFormat.lower() == 'xml':
            self.resultsFileName = PublishFilePath + '.xml'
            self.transferResults = self.loadXMLFileFormat()
        else:
            self.resultsFileName = PublishFilePath + '.txt'
            self.transferResults = self.loadTextFileFormat()
    
    def loadJsonFileFormat(self):
        '''
        Format the common framework file into *.json file format
        '''
        return json.dumps(self.commonFrameworkResults)        
        
    def loadXMLFileFormat(self):
        '''
        Format the common framework file into *.xml file format
        '''
        pass
    
    def loadTextFileFormat(self):
        '''
        Format the common framework file into *.txt file format
        '''
        pass
    
    def publishResults(self):
        if self.publishType.lower() == 'disk':
            self.transferFileToDisk()
        elif self.publishType.lower() == 'email':
            self.transferFileToEmail()
        elif self.publishType.lower() == 'transfer':
            self.transferFileToSharedServer()
        else:
            self.transferFileToDisk()
            
    def transferFileToDisk(self):
        '''
        Send/Transfer the results to local disk
        '''
        with open(self.resultsFileName, 'w') as outfile:
            json.dump(self.commonFrameworkResults, outfile)
    
    def transferFileToEmail(self):
        '''
        Send/Transfer the results to specified user email
        '''
        pass
    
    def transferFileToSharedServer(self):
        '''
        Send/Transfer the results to a shared server path
        '''
        pass

osProxy = sys.argv[1]
scriptName = sys.argv[2]
fileFormat = sys.argv[3]
publishType = sys.argv[4]
newPath = r'C:\{}'.format(sys.argv[5])

#Initialize All Class Variables
validator = Validator()
getStorage = GetStorage(newPath, osProxy, scriptName, fileFormat, publishType, validator)

#Validate All Parameters
getStorage.validateParameters()

#Get Storage Details
getStorage.getStorageDetails()

#Run Script Which Captures File Disk Space And Generates A Raw File
getStorage.runScript()

#Load & Extract The Script Raw File OutPut Into A Temporary Common Format
getStorage.loadStorage()

#Detect Output File Formatter
getStorage.fileFormatter()

#Load The Disk Space Storage Details Into Desired Format
getStorage.publishResults()
