import json

class FileFormatter:

    def __init__(self):
        pass
        
    def loadJsonFileFormat(self, commonFrameworkResults):
        # Format the common framework file into *.json file format
        return json.dumps(commonFrameworkResults)

    def loadXMLFileFormat(self, commonFrameworkResults):
        # Format the common framework file into *.xml file format
        pass

    def loadTextFileFormat(self, commonFrameworkResults):
        # Format the common framework file into *.txt file format
        pass