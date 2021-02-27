from utils.corpusManager import CorpusManager
from os import listdir
from os.path import isfile, join
import json

if __name__ == "__main__":
    #get all webscraper files as dicts
    path = "./webscraper_data/"
    webscraperData = [json.load(open(path + f, 'r')) for f in listdir(path) if isfile(join(path, f))]

    print(webscraperData[0])

    #CorpusManager.generateCorpus()
