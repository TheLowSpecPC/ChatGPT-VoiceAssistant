from pynput import keyboard
import time
import threading
import pyaudio
import wave
import os
from playsound import playsound
import assemblyai as aai
from youchat import you_message
import pyttsx3

aai.settings.api_key = f"0c2d74579e344525be8703da2850b894"
transcriber = aai.Transcriber()

file_ready_counter=0
stop_recording=False
is_recording=False
pykeyboard= keyboard.Controller()

def transcribe_speech():
    global file_ready_counter
    i=1
    print("ready - start transcribing with F2 ...\n")
    playsound("sounds/model_loaded.wav")
    while True:
        while file_ready_counter<i:
            time.sleep(0.01)

        result = transcriber.transcribe("test"+str(i)+".wav")
        print(result.text)
        text = result.text

        ans = you_message(text=text, out_type="string")
        print(ans)

        pyttsx3.speak(ans)

        os.remove("test"+str(i)+".wav")
        i=i+1

#keyboard events
pressed = set()

COMBINATIONS = [
    {
        "keys": [
            #{keyboard.Key.ctrl ,keyboard.Key.shift, keyboard.KeyCode(char="r")},
            #{keyboard.Key.ctrl ,keyboard.Key.shift, keyboard.KeyCode(char="R")},
            {keyboard.Key.f2}, {keyboard.KeyCode(char="q")}
        ],
        "command": ["start record", "stop"]
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
                if c["command"][0]=="start record" and stop_recording==False and is_recording==False:
                    t1 = threading.Thread(target=record_speech)
                    t1.start()
                else:
                    if c["command"][0]=="start record" and is_recording==True:
                        stop_recording=True
                pressed = set()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()