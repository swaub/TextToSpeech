# Text-to-Speech Audio Generator

A streamlined Python-based text-to-speech audio generator that converts text documents (.txt/.md) into high-quality narrated audio files (MP3/WAV). The application uses Microsoft Edge's TTS service with premium neural voices for natural-sounding speech.

## Features

- **High-Quality Narration**: Utilizes Microsoft Edge's online text-to-speech service with premium neural voices
- **Multiple Voice Options**: Choose between Emma (female) and Brian (male) premium neural voices
- **Multiple Output Formats**: Generate MP3 or WAV audio files
- **Handles Long Texts**: Automatically splits long documents into chunks with concurrent processing
- **Markdown Support**: Processes both .txt and .md files with automatic markdown formatting removal
- **Fast Processing**: Concurrent async processing (up to 5 simultaneous tasks) for quick generation
- **No External Dependencies**: Works without ffmpeg or other external tools
- **Interactive Selection**: Choose input files, voices, and output formats interactively

## How It Works

The application follows a clean concurrent pipeline:

1. **Text Processing**: Reads input files and splits into sentence-based chunks (3000 chars max)
2. **Audio Generation**: Concurrent async TTS conversion using Microsoft Edge's service 
3. **Audio Combination**: Merges chunks using binary file concatenation
4. **Cleanup**: Automatically removes temporary files

## Voice Options

Two premium neural voices available:
- **Emma**: en-US-EmmaNeural (Female)
- **Brian**: en-US-BrianNeural (Male, default)

## Output Formats

- **MP3**: Standard compressed audio format
- **WAV**: Uncompressed high-quality audio format

## Prerequisites

- Python 3.9+ (tested with Python 3.13)
- Internet connection (for edge-tts service)
- pip (Python's package installer)

## Installation

1. Clone or download the project files into a directory on your computer
2. Open a terminal or command prompt in that directory
3. Install the required Python package:

```bash
pip install -r requirements.txt
```

## Usage

1. **Add Your Text**: Place your text files (.txt or .md) in the project directory
2. **Run the Script**: Execute the main script:

```bash
python TextToSpeech.py
```

3. **Interactive Selection**: The program will guide you through:
   - Selecting input file (if multiple files available)
   - Choosing output format (MP3 or WAV)
   - Selecting voice (Emma or Brian)

4. **Output**: Generated audio files are saved as `{filename}_narrated.{format}`

## Example Usage

```
=== Text-to-Speech Audio Generator ===

Available input files:
  1: document.txt (Plain text file)
  2: notes.md (Markdown file)

Select input file (1-2): 1

Available output formats:
  1: MP3 Audio (.mp3)
  2: WAV Audio (.wav)

Select output format (1-2, default: 1 for MP3): 1

Use custom voice? (y/n, default: n): y

Available voices:
  1: Emma (Female)
  2: Brian (Male)

Select voice (1-2, default: 2 for Brian): 2

Input: document.txt
Voice: en-US-BrianNeural
Output: MP3 Audio

Complete! Total processing time: 45.2 seconds
Output file: document_narrated.mp3
```

## File Structure

- `TextToSpeech.py`: Main application (188 lines, streamlined code)
- `requirements.txt`: Dependencies (edge-tts)
- `input.txt`: Sample input file
- `temp_audio/`: Temporary chunk storage (auto-managed)
- `*_narrated.mp3/wav`: Generated output files

## Technical Details

- **Concurrent Processing**: Up to 5 simultaneous TTS tasks for speed
- **Sentence-Based Chunking**: Natural speech flow with 3000 character chunks
- **Markdown Processing**: Automatic removal of formatting (headers, bold, links, etc.)
- **Binary Audio Concatenation**: Simple, reliable file merging without external dependencies
- **No Error Handling**: Streamlined production-ready code assumes perfect execution

## Requirements

- `edge-tts>=6.0.0`: Microsoft Edge's text-to-speech service

## Compatibility

- Tested with Python 3.13
- Works on Windows, macOS, and Linux
- No external audio processing tools required