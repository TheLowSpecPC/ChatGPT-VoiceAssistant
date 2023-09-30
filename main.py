from pynput import keyboard
import whisper
import time
import threading
import pyaudio
import wave
import os
from playsound import playsound
from bardapi import Bard
import pyttsx3

Secure1PSID = "bgh7Dg0XKR0e1sfzzdEqK6lVn9wEBJNdlHIMORXXjjNtZ3Mc2BFdBkQ71oQzh5DBjywWoA."
bard = Bard(token = Secure1PSID)
engine = pyttsx3.init()
#load model
#model selection -> (tiny base small medium large)
print("loading model...")
model_name = "small"
model = whisper.load_model(model_name)
playsound("sounds/model_loaded.wav")
print(f"{model_name} model loaded")

file_ready_counter=0
stop_recording=False
is_recording=False
pykeyboard= keyboard.Controller()

def transcribe_speech():
    global file_ready_counter
    i=1
    print("ready - start transcribing with F2 ...\n")
    while True:
        while file_ready_counter<i:
            time.sleep(0.01)

        result = model.transcribe("test"+str(i)+".wav")
        print(result["text"]+"\n")
        text = result["text"]+"\n"

        ans = bard.get_answer(text)
        print(ans['content'])

        engine.say(result['content'])
        engine.runAndWait()

        os.remove("test"+str(i)+".wav")
        i=i+1

#keyboard events
pressed = set()

COMBINATIONS = [
    {
        "keys": [
            #{keyboard.Key.ctrl ,keyboard.Key.shift, keyboard.KeyCode(char="r")},
            #{keyboard.Key.ctrl ,keyboard.Key.shift, keyboard.KeyCode(char="R")},
            {keyboard.Key.f2},
        ],
        "command": "start record",
    },
]

#------------

#record audio
def record_speech():
    global file_ready_counter
    global stop_recording
    global is_recording

    is_recording=True
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

    frames = []  # Initialize array to store frames

    print("Start recording...\n")
    playsound("sounds/on.wav")

    while stop_recording==False:
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()
    playsound("sounds/off.wav")
    print('Finish recording')

    # Save the recorded data as a WAV file
    wf = wave.open("test"+str(file_ready_counter+1)+".wav", 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    stop_recording=False
    is_recording=False
    file_ready_counter=file_ready_counter+1

#------------

#transcribe speech in infinte loop
t2 = threading.Thread(target=transcribe_speech)
t2.start()

#hot key events
def on_press(key):
    pressed.add(key)

def on_release(key):
    global pressed
    global stop_recording
    global is_recording
    for c in COMBINATIONS:
        for keys in c["keys"]:
            if keys.issubset(pressed):
                if c["command"]=="start record" and stop_recording==False and is_recording==False:
                    t1 = threading.Thread(target=record_speech)
                    t1.start()
                else:
                    if c["command"]=="start record" and is_recording==True:
                        stop_recording=True
                pressed = set()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()