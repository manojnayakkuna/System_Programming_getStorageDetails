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
        print('self.parameterFileName:', self.parameterFileName)
        with open(self.parameterFileName) as json_data:
            data_dict = json.load(json_data)
            
        osProxy = data_dict["osProxy"]
        scriptName = data_dict["scriptName"]
        fileFormat = data_dict["fileFormat"]
        publishType = data_dict["publishType"]
        path = data_dict["path"]

        return osProxy, scriptName, fileFormat, publishType, path