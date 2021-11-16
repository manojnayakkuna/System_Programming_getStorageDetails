# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 00:51:03 2021

@author: manoj
"""

class Validator:

    def __init__(self):
        pass
        
    def validateNull(self, stringValue):
        if stringValue is None or stringValue == '' or len(stringValue.strip()) == 0:
            print('inside null check:', stringValue)
            return False
        return True
        
    def validateEmpty(self, dataObject):
        if len(dataObject) == 0:
            return False
        return True
        
    def validateGetValue(self, value, dataObject):
        print('value:', value)
        print('dataObject:', dataObject)
        return value in dataObject