#===REQUIRED INSTALLS===
#-pip install nltk
#-pip install SpeechRecognition
#-pip install pyaudio
#-pip install pocketsphinx
#If wheel fails to install for pyaudio and/or pocketsphinx, pip install pipwin
#then reinstall using pipwin instead of pip

#TODO:
#[] Record individual setences before transcribing and summarizing
#[] Create special corpus for certain subjects with associated word weights
#[] Apply special corpus weights to final word summarization
#[] Experiment with abstraction summarization vs extraction summarization

import speech_recognition as sr
from summarizer import Summarizer

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
        #print(r.recognize_sphinx(audio))
        #google is far better, but requires internet connection
        result = r.recognize_google(audio)
        print(result)
        return result
    except sr.UnknownValueError:
        print("Unknown audio detected!")

if __name__ == "__main__":
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=0)

    recording = True
    while recording:
        audio = recordAudio()

        text = transcribeAudio(audio)
        if text == "stop recording":
            print("Stopping recording...")
            recording = False
        else:
            print(Summarizer.summarize(text, compressionRate=0.9))