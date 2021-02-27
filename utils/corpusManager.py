import json

class CorpusManager:
    def generateCorpus(text):
        pass

    def saveCorpus(corpus, corpusFilePath):
        f = open(corpusFilePath, 'w')
        json.dump(corpus, f, sort_keys=True, indent=4)

    def loadCorpus(corpusFilePath):
        f = open(corpusFilePath, 'r')
        return json.load(f)