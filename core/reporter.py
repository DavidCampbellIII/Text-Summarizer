class Reporter:
    def __init__(self, reportTemplateFileName):
        with open(reportTemplateFileName) as f:
            self.reportTemplate = f.readlines()

    def saveReport(self, mainText):
        pass

    def produceReport(self, mainText):
        pass