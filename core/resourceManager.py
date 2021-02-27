import json
from datetime import datetime

class ResourceManager:
    def __init__(self, configFileName):
        self.configFileName = configFileName
        with open(configFileName) as f:
            self.config = json.load(f)
        self.__generatePaths(self.config)

    def generateReportExportFileName(self):
        processedName = self.__processStringCodes(self.config["reportExportName"])
        return self.reportExportsPath + processedName

    def __generatePaths(self, config):
        self.puncuatorPath = config["puncuatorModels_PATH"] + config["puncuatorModel"]
        self.corpusPath = config["corpuses_PATH"] + config["corpus"]
        self.testTextPath = config["testTexts_PATH"] + config["testText"]
        self.reportTemplatePath = config["reportTemplates_PATH"] + config["reportTemplate"]
        self.reportExportsPath = config["reportExports_PATH"];

    def __gatherResources(self, templateFileName, medicalInfoFileName):
        pass

    def __processStringCodes(self, text):
        text = text.lower()
        if "$date" in text:
            now = datetime.now()
            nowFormatted = now.strftime("%b_%d_%Y_%H-%M-%S")
            return text.replace("$date", nowFormatted)
