# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 00:51:03 2021

@author: manoj
"""
import json

class ParameterFile:

    def __init__(self, parameterFileName):
        self.parameterFileName = parameterFileName

    def readParameterFile(self):
        with open(self.parameterFileName) as json_file:
            data = json.load(json_file)
        osProxy = data['osProxy']
        scriptName = data['scriptName']
        fileFormat = data['fileFormat']
        publishType = data['publishType']
        path = data['path']

        return osProxy, scriptName, fileFormat, publishType, path