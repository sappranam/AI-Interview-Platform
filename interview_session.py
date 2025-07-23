import os
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import time
import re

# Recording settings
SAMPLE_RATE = 16000
CHANNELS = 1

def record_audio(filename):
    print("➡️ Press Enter to start recording your answer...")
    input()
    print("🎙️ Recording... Press Enter again to stop.")
    recording = []

    def callback(indata, frames, time, status):
        recording.append(indata.copy())

    stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback)
    with stream:
        input()  # Wait until Enter is pressed again
    audio_data = np.concatenate(recording, axis=0)
    wav.write(filename, SAMPLE_RATE, audio_data)
    print("✅ Recording saved.")

def transcribe_audio(filename):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
        print("📝 Transcribing...")
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "❌ Could not understand the audio."
    except sr.RequestError as e:
        return f"❌ Could not request results; {e}"

def load_questions(file_path="interview_questions.txt"):
    questions = []
    collect = False

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if re.match(r"^1\.", line):  # Start collecting from question 1
                collect = True
            if collect and re.match(r"^\d+\.", line):  # Only numbered questions
                questions.append(line)

    return questions

def run_session():
    print("\n🎤 Welcome to the AI Interview Session!\n")
    questions = load_questions()

    if not questions:
        print("⚠️ No valid interview questions found.")
        return

    for idx, question in enumerate(questions, start=1):
        print(f"\n❓ Question {idx}:\n{question}")
        audio_file = f"answer_{idx}.wav"
        record_audio(audio_file)
        answer = transcribe_audio(audio_file)
        print(f"\n🗣️ Your Answer:\n{answer}")
        time.sleep(1)

    print("\n✅ Interview session completed.")

if __name__ == "__main__":
    run_session()
