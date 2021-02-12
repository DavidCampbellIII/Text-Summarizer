import speech_recognition as sr
from punctuator import Punctuator

class Recorder:
    def __init__(self, punctuatorModelFileName):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone(device_index=0)
        self.punctuatorModelFileName = punctuatorModelFileName

    def record(self):
        audio = self.__recordAudio()
        text = self.__transcribeAudio(audio)
        return self.__punctuateText(text, self.punctuatorModelFileName)

    def __recordAudio(self):
        print("Listening...")
        with self.mic as source:
            #r.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source)
        return audio

    def __transcribeAudio(self, audio):
        print("Thinking...")
        try:
            #pocketsphinx sucks right now.  Try using different acoustic model to improve accuracy?
            #result = r.recognize_sphinx(audio)
            
            #google is far better, but requires internet connection
            result = self.recognizer.recognize_google(audio)
            print(result)
            return result
        except sr.UnknownValueError:
            print("Unknown audio detected!")

    def __punctuateText(self, text, modelFileName):
        punc = Punctuator(modelFileName)
        return punc.punctuate(text)