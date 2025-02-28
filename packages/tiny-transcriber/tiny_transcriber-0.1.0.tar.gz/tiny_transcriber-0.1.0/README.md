# TinyTranscriber: A Lightweight Speech Transcription Tool

A simple, extensible Python tool that records audio from your microphone and transcribes it using OpenAI's Whisper API.

## Features

- Record audio from your microphone
- Save recordings as WAV files
- Transcribe audio to text using OpenAI's Whisper

## Prerequisites

- OpenAI API key

## Installation

Install via pip:
```bash
pip install tiny-transcriber
```

Or install from source:
```bash
git clone https://github.com/brendanm12345/tiny-transcriber
cd tiny-transcriber
pip install -e .
```

Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key'
```

## Quick Start

```python
from tiny_transcriber import TinyTranscriber

transcriber = TinyTranscriber()

# Start recording
transcriber.start_recording()

# Record for as long as needed
input("Press Enter to stop recording...")

# Stop and save recording
audio_file = transcriber.stop_recording("my_recording.wav")

# Transcribe the audio
transcript = transcriber.transcribe(audio_file)
print(transcript)
```

## How It Works

The project uses several key Python libraries:
- `pyaudio`: Handles audio input from the microphone
- `wave`: Saves audio data in WAV format
- `openai`: Interfaces with OpenAI's Whisper API for transcription
- `threading`: Manages continuous audio recording
