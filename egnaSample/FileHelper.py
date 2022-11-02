class FileHelper() :
   
    fileName = ''
    results = ''

    def __init__(self) :
        """
        """

    def set_fileName(self,fileName):
        self.fileName = fileName

    def set_results(self,results):
        self.results   = results

    def createFile(self):
        f = open(self.fileName, 'wb')
        f.write(self.results)
        f.close

    def readFile(self):
        f = open(self.fileName, 'rb')
        self.results = f.read()
        f.close