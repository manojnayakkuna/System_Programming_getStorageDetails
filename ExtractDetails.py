from collections import defaultdict

class ExtractDetails:

    def __init__(self):
        pass

    def extractDetailsWindows(self, searchString, rawFilePath):
        # Read raw output file 'rawFileOutput.txt' to load into a common temporary variable for Windows
        results = defaultdict(list)
        with open(rawFilePath) as file:
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
        return results

    def extractDetailsLinux(self, searchString, rawFilePath):
        # Read raw output file 'rawFileOutput.txt' to load into a common temporary variable for Linux
        pass