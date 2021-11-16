import json

class PublishResults:

    def __init__(self):
        pass

    def transferFileToDisk(self, resultsFileName, commonFrameworkResults):
        #  Send/Transfer the results to local disk
        with open(resultsFileName, 'w') as outfile:
            json.dump(commonFrameworkResults, outfile)

    def transferFileToEmail(self, resultsFileName, commonFrameworkResults):
        # Send/Transfer the results to specified user email
        pass

    def transferFileToSharedServer(self, resultsFileName, commonFrameworkResults):
        # Send/Transfer the results to a shared server path
        pass