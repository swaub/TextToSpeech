Text-to-Video AI Narration
This project contains a Python script that automates the process of converting a text document (.txt) into a video file (.mp4) with a natural-sounding AI-generated voiceover. It's perfect for creating simple "audiobook-style" videos from written content.

Features
High-Quality Narration: Utilizes Microsoft Edge's online text-to-speech service for voices that are clear and natural-sounding.

Handles Long Texts: Automatically splits long documents into smaller chunks to work with the TTS service limits.

Automated Video Creation: Combines the generated audio with a simple background to produce a standard .mp4 video file.

Easy to Use: Simply add your text to input.txt and run the script.

How It Works
The script performs the following steps:

Reads Text: It opens and reads all the content from the input.txt file.

Generates Audio: The text is sent to the edge-tts service, which returns the corresponding audio. This audio is saved into temporary files.

Combines Audio: The individual audio chunks are stitched together into a single final_audio.mp3 file.

Creates Video: Using moviepy, the script generates a simple video clip (a black background with a title) and sets its duration to match the audio length.

Merges and Exports: The audio track is merged with the video clip, and the final result is saved as output_video.mp4.

Cleans Up: All temporary files are deleted, leaving only your final video.

Setup and Usage
Follow these steps to get the project running.

1. Prerequisites
Python 3.9+

pip (Python's package installer)

FFMPEG: The moviepy library depends on this powerful multimedia tool. If you don't have it, you can download it from the official FFMPEG website. Make sure to add it to your system's PATH so the script can find it.

(Optional) ImageMagick: To display text on the video, moviepy uses ImageMagick. If it's not installed, the script will fall back to a plain black background. You can download it from the official ImageMagick website.

2. Installation
Clone or download the project files into a directory on your computer. Then, open a terminal or command prompt in that directory and install the required Python packages using the requirements.txt file:

pip install -r requirements.txt

3. Add Your Text
Open the input.txt file and replace the placeholder content with the text you want to be narrated. Save the file.

4. Run the Script
Execute the main script from your terminal:

python main.py

The script will print its progress to the console. When it's finished, you will find the output_video.mp4 file in the same directory.