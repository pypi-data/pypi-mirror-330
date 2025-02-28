import pyaudio
import wave
from openai import OpenAI
from typing import Optional
import threading

class TinyTranscriber:
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.client = OpenAI()
        self.frames = []
        self.is_recording = False
        self.audio = None
        self.stream = None
        
    def start_recording(self):
        """Start recording audio"""
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        
        self.frames = []
        self.is_recording = True
        
        # Start recording in a separate thread to avoid blocking main script
        self.recording_thread = threading.Thread(target=self._record)
        self.recording_thread.start()
        
    def _record(self):
        """Record audio in chunks"""
        while self.is_recording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
            
    def stop_recording(self, filename: str = "output.wav") -> str:
        """Stop recording and save to file"""
        self.is_recording = False
        self.recording_thread.join()
        
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        
        # Save the recorded data as a WAV file
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.frames))
            
        print(f"Recording saved to {filename}")
        return filename
        
    def transcribe(self, audio_file: str, language: Optional[str] = None) -> str:
        """Transcribe audio file using OpenAI's Whisper API"""
        try:
            with open(audio_file, "rb") as file:
                response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=file,
                    language=language
                )
            return response.text
        except Exception as e:
            print(f"Error during transcription: {e}")
            return ""