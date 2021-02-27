import re

class Reporter:
    def __init__(self, reportTemplateFileName):
        with open(reportTemplateFileName) as f:
            self.reportTemplate = f.readlines()

    def saveReport(self, report, filename):
        f = open(filename, 'w')
        f.write(report)
        f.close()

    def produceReport(self, conversationText):
        #remove comments
        lines = []
        for line in self.reportTemplate:
            #remove comments
            parts = line.partition("//")
            #just add head (everything before delimiter)
            lines.append(parts[0])
        return conversationText + "\n=============\n" + "".join(lines)

    def __loadMedicalHistory(self):
        pass