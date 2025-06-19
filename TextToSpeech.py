import os
import asyncio
import edge_tts
import time
import glob
import re
import shutil

TEMP_AUDIO_FOLDER = 'temp_audio'
VOICE_OPTIONS = {"emma": "en-US-EmmaNeural", "brian": "en-US-BrianNeural"}
INPUT_FORMATS = {"txt": "Plain text file", "md": "Markdown file"}
MAX_CONCURRENT_TASKS = 5

def find_input_file():
    available_files = []
    for ext in INPUT_FORMATS.keys():
        files = glob.glob(f"*.{ext}")
        available_files.extend(files)
    return available_files

def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    if file_path.lower().endswith('.md'):
        lines = text.split('\n')
        processed_lines = []
        for line in lines:
            line = line.lstrip('#').strip()
            line = line.replace('**', '').replace('*', '').replace('_', '')
            line = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line)
            if line.strip():
                processed_lines.append(line)
        text = '\n'.join(processed_lines)
    
    text = fix_pronunciation(text)
    return text

def fix_pronunciation(text):
    decade_names = {
        '00': 'hundreds', '10': 'tens', '20': 'twenties', '30': 'thirties', 
        '40': 'forties', '50': 'fifties', '60': 'sixties', '70': 'seventies',
        '80': 'eighties', '90': 'nineties'
    }
    
    def replace_decade(match):
        decade = match.group(1)
        return decade_names.get(decade, decade + 'ies')
    
    def replace_full_year(match):
        century = match.group(1)
        decade = match.group(2)
        decade_name = decade_names.get(decade, decade + 'ies')
        
        if century == '19':
            return f'nineteen {decade_name}'
        elif century == '20':
            return f'twenty {decade_name}'
        elif century == '18':
            return f'eighteen {decade_name}'
        else:
            return f'{century} {decade_name}'
    
    text = re.sub(r'\b(\d{2})s\b', replace_decade, text)
    text = re.sub(r'\b(\d{2})(\d{2})s\b', replace_full_year, text)
    
    return text

def split_text(text, max_length=3000):
    sentences = text.replace('\n', ' ').split('. ')
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if not sentence.endswith('.') and not sentence.endswith('!') and not sentence.endswith('?'):
            sentence += '.'
        if len(current_chunk) + len(sentence) + 2 < max_length:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

async def convert_single_chunk(chunk_data):
    i, chunk = chunk_data
    if not chunk.strip():
        return None
    output_filename = os.path.join(TEMP_AUDIO_FOLDER, f'chunk_{i:03d}.mp3')
    communicate = edge_tts.Communicate(chunk, VOICE)
    await communicate.save(output_filename)
    return output_filename

async def convert_text_to_speech(text_chunks):
    if not os.path.exists(TEMP_AUDIO_FOLDER):
        os.makedirs(TEMP_AUDIO_FOLDER)

    semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
    
    async def process_with_semaphore(chunk_data):
        async with semaphore:
            return await convert_single_chunk(chunk_data)
    
    chunk_data = [(i, chunk) for i, chunk in enumerate(text_chunks)]
    tasks = [process_with_semaphore(data) for data in chunk_data]
    results = await asyncio.gather(*tasks)
    audio_files = [f for f in results if f]
    
    return sorted(audio_files)

def combine_audio_files(audio_files, output_path, output_format="mp3"):
    if len(audio_files) == 1:
        shutil.copy2(audio_files[0], output_path)
        return
    
    with open(output_path, 'wb') as outfile:
        for audio_file in audio_files:
            with open(audio_file, 'rb') as infile:
                outfile.write(infile.read())

def select_voice():
    print("\nAvailable voices:")
    print("  1: Emma (Female)")
    print("  2: Brian (Male)")
    
    choice = input(f"\nSelect voice (1-2, default: 2 for Brian): ").strip()
    if not choice or choice == "2":
        return VOICE_OPTIONS["brian"]
    elif choice == "1":
        return VOICE_OPTIONS["emma"]
    return VOICE_OPTIONS["brian"]

def select_input_file():
    available_files = find_input_file()
    
    if not available_files:
        return "input.txt"
    
    if len(available_files) == 1:
        return available_files[0]
    
    print("\nAvailable input files:")
    for i, file in enumerate(available_files, 1):
        file_ext = file.split('.')[-1]
        desc = INPUT_FORMATS.get(file_ext, "Unknown format")
        print(f"  {i}: {file} ({desc})")
    
    choice = input(f"\nSelect input file (1-{len(available_files)}): ").strip()
    if not choice:
        return available_files[0]
    idx = int(choice) - 1
    if 0 <= idx < len(available_files):
        return available_files[idx]
    return available_files[0]

def select_output_format():
    print("\nAvailable output formats:")
    print("  1: MP3 Audio (.mp3)")
    print("  2: WAV Audio (.wav)")
    
    choice = input(f"\nSelect output format (1-2, default: 1 for MP3): ").strip()
    if not choice or choice == "1":
        return "mp3"
    elif choice == "2":
        return "wav"
    return "mp3"

def cleanup(files_to_delete):
    for item in files_to_delete:
        if os.path.isfile(item):
            os.remove(item)
        elif os.path.isdir(item):
            for f in os.listdir(item):
                os.remove(os.path.join(item, f))
            os.rmdir(item)

async def main():
    print("=== Text-to-Speech Audio Generator ===")
    start_time = time.time()
    
    input_file = select_input_file()
    output_format = select_output_format()
    
    use_custom_voice = input("\nUse custom voice? (y/n, default: n): ").strip().lower()
    if use_custom_voice == 'y':
        voice = select_voice()
    else:
        voice = VOICE_OPTIONS["brian"]
    
    print(f"\nInput: {input_file}")
    print(f"Voice: {voice}")
    print(f"Output: {output_format.upper()} Audio")
    
    base_name = os.path.splitext(input_file)[0]
    output_ext = ".mp3" if output_format == "mp3" else ".wav"
    output_file = f"{base_name}_narrated{output_ext}"
    
    full_text = read_text_from_file(input_file)
    text_chunks = split_text(full_text)

    global VOICE
    VOICE = voice
    temp_audio_files = await convert_text_to_speech(text_chunks)
    combine_audio_files(temp_audio_files, output_file, output_format)
    cleanup(temp_audio_files + [TEMP_AUDIO_FOLDER])
    
    total_time = time.time() - start_time
    print(f"\nComplete! Total processing time: {total_time:.1f} seconds")
    print(f"Output file: {output_file}")

if __name__ == '__main__':
    asyncio.run(main())
