import sys
import os
import speech_recognition as sr
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pyphen
import pyttsx3
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog, QTextEdit

class SpeechApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Speech Processing Application")
        self.setGeometry(100, 100, 800, 600)
        
        self.layout = QVBoxLayout()

        self.label = QLabel("Click 'Record' to start recording:")
        self.layout.addWidget(self.label)
        
        self.record_button = QPushButton("Record")
        self.record_button.clicked.connect(self.record_audio)
        self.layout.addWidget(self.record_button)
        
        self.save_text_button = QPushButton("Save Audio as Text")
        self.save_text_button.clicked.connect(self.save_audio_as_text)
        self.layout.addWidget(self.save_text_button)
        
        self.hyphenate_button = QPushButton("Hyphenate Text")
        self.hyphenate_button.clicked.connect(self.hyphenate_text)
        self.layout.addWidget(self.hyphenate_button)
        
        self.synthesize_speech_button = QPushButton("Synthesize Speech")
        self.synthesize_speech_button.clicked.connect(self.synthesize_speech)
        self.layout.addWidget(self.synthesize_speech_button)
        
        self.plot_spectrogram_button = QPushButton("Plot Spectrogram")
        self.plot_spectrogram_button.clicked.connect(self.plot_spectrogram)
        self.layout.addWidget(self.plot_spectrogram_button)
        
        self.plot_histogram_button = QPushButton("Plot Histogram")
        self.plot_histogram_button.clicked.connect(self.plot_histogram)
        self.layout.addWidget(self.plot_histogram_button)
        
        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)
        
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def record_audio(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic)
            self.label.setText("Recording... Please speak.")
            audio = recognizer.listen(mic)
            self.label.setText("Recording completed.")
            with open("unnamed.wav", "wb") as f:
                f.write(audio.get_wav_data())
                self.label.setText("Audio saved as 'unnamed.wav'")

    def save_audio_as_text(self):
        recognizer = sr.Recognizer()
        audio_path = "unnamed.wav"
        try:
            with sr.AudioFile(audio_path) as audio_file:
                audio = recognizer.record(audio_file)
                text = recognizer.recognize_google(audio, language="en-US")
                with open("audio_text.txt", "w") as text_file:
                    text_file.write(text)
                self.label.setText("Audio transcribed and saved as 'audio_text.txt'")
                self.text_edit.setText(text)
        except Exception as e:
            self.label.setText("Error: " + str(e))

    def hyphenate_text(self):
        dic = pyphen.Pyphen(lang='en')
        try:
            with open("audio_text.txt", 'r') as file:
                text = file.read().strip()
            hyphenated_text = dic.inserted(text).replace('-', ' ')
            with open("hyphenated_text.txt", "w") as file:
                file.write(hyphenated_text)
            self.label.setText("Text hyphenated and saved as 'hyphenated_text.txt'")
            self.text_edit.setText(hyphenated_text)
        except Exception as e:
            self.label.setText("Error: " + str(e))

    def synthesize_speech(self):
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 100)
            engine.setProperty('volume', 0.9)
            with open("hyphenated_text.txt", 'r') as file:
                text = file.read()
            engine.save_to_file(text, "synthesized_speech.wav")
            engine.runAndWait()
            self.label.setText("Text synthesized and saved as 'synthesized_speech.wav'")
        except Exception as e:
            self.label.setText("Error: " + str(e))

    def plot_spectrogram(self):
        try:
            audio_path = "unnamed.wav"
            y, sr = librosa.load(audio_path)
            D = librosa.amplitude_to_db(librosa.stft(y), ref=np.max)
            plt.figure(figsize=(10, 5))
            librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
            plt.colorbar(format='%+2.0f dB')
            plt.title('Spectrogram')
            plt.show()
        except Exception as e:
            self.label.setText("Error: " + str(e))

    def plot_histogram(self):
        try:
            audio_path = "unnamed.wav"
            y, sr = librosa.load(audio_path)
            plt.figure(figsize=(10, 5))
            plt.hist(y, bins=100)
            plt.title('Energy Histogram')
            plt.xlabel('Amplitude')
            plt.ylabel('Frequency')
            plt.show()
        except Exception as e:
            self.label.setText("Error: " + str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeechApp()
    window.show()
    sys.exit(app.exec_())
