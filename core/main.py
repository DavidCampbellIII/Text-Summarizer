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

#Questions:
#Do numbers ever really matter? (Not "one", but "1" etc.)
#   YES
#How will finally summary be sent to users?  As downloadable document?  Another
#   program on their compute that syncs up?
#   PREFERABLY IN EPIC SOFTWARE DIRECTLY, BUT UNTIL THEN, A FILE IS FINE
#Speaking of the above, how will the device work in general?  All processing done on Raspberry Pi maybe?
#   Or recorded on a normal deivce, and then uploaded to computer?  Mix of both?

import json
import speech_recognition as sr
from punctuator import Punctuator
from core.summarizer import Summarizer
from core.resourceManager import ResourceManager
from core.reporter import Reporter
import utils.webscraper
import utils.corpusLoader

def recordAudio():
    print("Listening...")
    with mic as source:
        #r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    return audio

def transcribeAudio(audio):
    print("Thinking...")
    try:
        #pocketsphinx sucks right now.  Try using different acoustic model to improve accuracy?
        #result = r.recognize_sphinx(audio)
        
        #google is far better, but requires internet connection
        result = r.recognize_google(audio)
        print(result)
        return result
    except sr.UnknownValueError:
        print("Unknown audio detected!")

def punctuateText(text, modelFileName):
    punc = Punctuator(modelFileName)
    return punc.punctuate(text)

if __name__ == "__main__":
    with open("config/config.json") as f:
        config = json.load(f)
    
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=0)

    recording = True
    while recording:
        audio = recordAudio()

        text = transcribeAudio(audio)
        text = punctuateText(text, config["puncuatorModels_PATH"] + config["puncuatorModel"])
        print("Puncuated text:", text)
        if text == "stop recording":
            print("Stopping recording...")
            recording = False
        else:
            print(Summarizer.summarize(text, compressionRate=0.9))