import json

class ResourceManager:
    def __init__(self, configFileName):
        self.configFileName = configFileName
        with open(configFileName) as f:
            self.config = json.load(f)
        self.__generatePaths(self.config)

    def __generatePaths(self, config):
        self.puncuatorPath = config["puncuatorModels_PATH"] + config["puncuatorModel"]
        self.corpusPath = config["corpuses_PATH"] + config["corpus"]
        self.testTextPath = config["testTexts_PATH"] + config["testText"]
        self.reportTemplatePath = config["reportTemplates_PATH"] + config["reportTemplate"]

    def __gatherResources(self, templateFileName, medicalInfoFileName):
        pass