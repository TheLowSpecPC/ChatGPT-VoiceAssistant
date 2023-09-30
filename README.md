# YouChat Voice Assistant
This is a python script using [AssemblyAI/assemblyai-python-sdk](https://github.com/AssemblyAI/assemblyai-python-sdk) to convert your voice to text which is then passed on through YouChat AI and then the result is sent back using a text to speech code.

After you start the script you just press **F2** to start/stop recording. After the record is finsihed, it will give you the desired answer.

# Setup Instructions

**Step 1 (Linux - Ubuntu,Debian):**

    sudo apt-get install python3 python3-pip git ffmpeg

**Step 1 (Windows):**

- Download ffmpeg from https://ffmpeg.org/ , unpack it and paste "ffmpeg.exe" in this folder
- Download and Install git from https://git-scm.com/download/win
- Download and Install python3 from https://www.python.org/downloads/windows/

**Step 1 (MAC OS - not tested):**

Download and Install ffmpeg, git and python3

**Step 2:**

    pip install -r requirements.txt

**Step 3:**

Before starting, you need to set the API key. If you don't have one yet, [sign up for one](https://www.assemblyai.com/dashboard/signup)!

    pip install -U assemblyai
