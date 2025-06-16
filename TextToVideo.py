import os
import asyncio
import edge_tts
from moviepy.video.VideoClip import ColorClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from pydub import AudioSegment

INPUT_TEXT_FILE = 'input.txt'
OUTPUT_AUDIO_FILE = 'final_audio.mp3'
OUTPUT_VIDEO_FILE = 'output_video.mp4'
TEMP_AUDIO_FOLDER = 'temp_audio'
VOICE = "en-US-AriaNeural"

def read_text_from_file(file_path):
    print(f"Reading text from {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return text
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        print("Creating a sample 'input.txt' file. Please edit it with your text.")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("Hello, world. This is a sample text file. ")
            f.write("Please replace this content with the text you want to convert to video.")
        return read_text_from_file(file_path)

def split_text(text, max_length=4000):
    print("Splitting text into smaller chunks...")
    paragraphs = text.split('\n')
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) + 1 < max_length:
            current_chunk += paragraph + "\n"
        else:
            chunks.append(current_chunk)
            current_chunk = paragraph + "\n"
    
    if current_chunk:
        chunks.append(current_chunk)
        
    print(f"Text split into {len(chunks)} chunks.")
    return chunks

async def convert_text_to_speech(text_chunks):
    if not os.path.exists(TEMP_AUDIO_FOLDER):
        os.makedirs(TEMP_AUDIO_FOLDER)

    audio_files = []
    for i, chunk in enumerate(text_chunks):
        if not chunk.strip():
            continue
            
        output_filename = os.path.join(TEMP_AUDIO_FOLDER, f'chunk_{i}.mp3')
        print(f'Converting chunk {i+1}/{len(text_chunks)} to audio: {output_filename}')
        
        try:
            communicate = edge_tts.Communicate(chunk, VOICE)
            await communicate.save(output_filename)
            audio_files.append(output_filename)
        except Exception as e:
            print(f"Could not process chunk {i}. Error: {e}")
            
    return audio_files

def combine_audio_files(audio_files, output_path):
    print("Combining audio files...")
    combined_audio = AudioSegment.empty()
    
    for file_path in audio_files:
        try:
            segment = AudioSegment.from_mp3(file_path)
            combined_audio += segment
        except Exception as e:
            print(f"Could not process audio file {file_path}. Error: {e}")

    combined_audio.export(output_path, format="mp3")
    print(f"Combined audio saved to {output_path}")

def create_video_from_audio(audio_path, video_path):
    print("Creating video file...")

    try:
        audio_clip = AudioFileClip(audio_path)
        audio_duration = audio_clip.duration
    except Exception as e:
        print(f"Error loading audio clip: {e}")
        return

    final_clip = ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=audio_duration)

    final_video = final_clip.with_audio(audio_clip)

    final_video.write_videofile(video_path, fps=24, codec='libx264')
    print(f"Video saved to {video_path}")


def cleanup(files_to_delete):
    print("Cleaning up temporary files...")
    for item in files_to_delete:
        if os.path.isfile(item):
            os.remove(item)
        elif os.path.isdir(item):
            for f in os.listdir(item):
                os.remove(os.path.join(item, f))
            os.rmdir(item)
    print("Cleanup complete.")

async def main():
    full_text = read_text_from_file(INPUT_TEXT_FILE)
    if not full_text:
        return

    text_chunks = split_text(full_text)

    temp_audio_files = await convert_text_to_speech(text_chunks)
    if not temp_audio_files:
        print("No audio files were generated. Exiting.")
        return

    combine_audio_files(temp_audio_files, OUTPUT_AUDIO_FILE)

    create_video_from_audio(OUTPUT_AUDIO_FILE, OUTPUT_VIDEO_FILE)

    files_to_remove = temp_audio_files + [OUTPUT_AUDIO_FILE]
    cleanup(files_to_remove + [TEMP_AUDIO_FOLDER])

if __name__ == '__main__':
    asyncio.run(main())
