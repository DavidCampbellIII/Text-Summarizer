#===REQUIRED INSTALLS===
#-pip install nltk
#-pip install spacy
#-python -m spacy download en_core_web_sm
#-pip install punctuator
#-pip install --upgrade pymc3 #Only do this if theano gives error, and after "pip uninstall theano"
#-pip install SpeechRecognition
#-pip install pyaudio
#-pip install pocketsphinx
#If wheel fails to install for pyaudio and/or pocketsphinx, pip install pipwin
#then reinstall using pipwin instead of pip

#TODO:
#[] Record individual setences before transcribing and summarizing
#[] Investigate about creating a custom acoustic model for pocket-sphinx
#[] Create special corpus for certain subjects with associated word weights
#[] Apply special corpus weights to final word summarization
#[] Experiment with abstraction summarization vs extraction summarization
#[] Use lemmatization for more accurate extraction summarization
#[] Investigate why Punctator will not start up correctly (may be due to corrupt dependency library)
#[x] Email OpenAI about GPT-3
#[] Experiment with QIE Engine for Epic software data importing
#[] Research BERT and see how it can be implemented in this project (clinical BERT specifically)

#Questions:
#Do numbers ever really matter? (Not "one", but "1" etc.)
#   YES
#How will finally summary be sent to users?  As downloadable document?  Another
#   program on their compute that syncs up?
#   PREFERABLY IN EPIC SOFTWARE DIRECTLY, BUT UNTIL THEN, A FILE IS FINE
#Speaking of the above, how will the device work in general?  All processing done on Raspberry Pi maybe?
#   Or recorded on a normal deivce, and then uploaded to computer?  Mix of both?

#from core.recorder import Recorder
from core.summarizer import Summarizer
from core.resourceManager import ResourceManager
from core.reporter import Reporter
from utils.corpusManager import CorpusManager

if __name__ == "__main__":
    configFileName = "config/config.json"
    resourceManager = ResourceManager(configFileName)
    #recorder = Recorder(resourceManager.puncuatorPath)
    #text = recorder.record()
    #summarizedText = Summarizer.summarize(text, compressionRate=0.9)

    #print(summarizedText)

    corpusFilePath = resourceManager.corpusPath
    corpus = CorpusManager.loadCorpus(corpusFilePath)

    #test report saving
    reporter = Reporter(resourceManager.reportTemplatePath)
    report = reporter.produceReport("Test conversational text right here")
    reportFileName = resourceManager.generateReportExportFileName()
    #reporter.saveReport(report, reportFileName)