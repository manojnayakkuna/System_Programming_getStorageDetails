# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 00:58:40 2021

@author: manoj
"""
from Validator import Validator

def test_validateNull_returnFalseWhenNull():
    validator = Validator()
    stringValue = ''
    result = validator.validateNull(stringValue)
    assert result == False
    
def test_validateNull_returnTrueWhenNotNull():
    validator = Validator()
    stringValue = 'abc'
    result = validator.validateNull(stringValue)
    assert result == True
    
def test_validateEmpty_returnFalseWhenNull():
    validator = Validator()
    list_sample = [] 
    result = validator.validateEmpty(list_sample)
    assert result == False
    
def test_validateEmpty_returnTrueWhenNotNull():
    validator = Validator()
    list_sample = [1,2,3,4,5]
    result = validator.validateEmpty(list_sample)
    assert result == True
    
def test_validateGetValue_returnFalseWhenNotFound():
    validator = Validator()
    value = 10
    dataObject = [1,2,3,4,5]
    result = validator.validateGetValue(value, dataObject)
    assert result == False
    
def test_validateGetValue_returnTrueWhenFound():
    validator = Validator()
    value = 1
    dataObject = [1,2,3,4,5]
    result = validator.validateGetValue(value, dataObject)
    assert result == True