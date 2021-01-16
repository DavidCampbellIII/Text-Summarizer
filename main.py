#===Required installs
#-pip install SpeechRecognition
#-pip install pyaudio
#-pip install pocketsphinx
#If wheel fails to install for pyaudio and/or pocketsphinx, pip install pipwin
#then reinstall using pipwin instead of pip

import speech_recognition as sr
r = sr.Recognizer()
mic = sr.Microphone(device_index=0)

while True:
    print("Listening...")

    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    print("Thinking...")
    print(r.recognize_sphinx(audio))