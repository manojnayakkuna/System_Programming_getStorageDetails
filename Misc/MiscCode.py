# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 23:08:01 2021

@author: manoj
"""
import pickle
import os
currentPath = ''
parameter1 = ''
parameter2 = ''
scriptRunPath = currentPath + '\Scripts\folderPathFileSizeInfo.bat ' + ' ' + parameter1 + ' ' + parameter2
print('scriptRunPath', scriptRunPath)
os.system(scriptRunPath)

resultsFileName = 'output.pickle'
commonFrameworkResults = {}
pickleOutput = open(resultsFileName, "wb")
pickle.dump(commonFrameworkResults, pickleOutput)
pickleOutput.close()