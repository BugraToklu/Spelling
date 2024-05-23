import speech_recognition as sr
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np  # NumPy kütüphanesini ekledik

rec=sr.Recognizer()

with sr.Microphone() as mic:
    rec.adjust_for_ambient_noise(mic)
    print("Let's talk abaout something...")
    audio=rec.listen(mic)

    try:
        print("you've said:"+rec.recognize_google(audio))
    except Exception as e:
        print("error"+str(e))
    with open ("unammed.wav","wb") as f:
        f.write(audio.get_wav_data())
        print("saved succesfuly")        

# Ses dosyasını yükle
audio_path = 'unammed.wav'  # Dosya adını "unnamed.wav" olarak düzelttik
y, sr = librosa.load(audio_path)

# Ses dosyasının zaman-frekans spektrogramunu oluştur
D = librosa.amplitude_to_db(librosa.stft(y), ref=np.max)
plt.figure(figsize=(10, 5))
librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Ses Dosyasının Zaman-Frekans Spektrogramı')
plt.show()

# Ses dosyasının enerji histogramını oluştur
plt.figure(figsize=(10, 5))
plt.hist(y, bins=100)
plt.title('Ses Dosyasının Enerji Histogramı')
plt.xlabel('Amplitude')
plt.ylabel('Frequency')
plt.show()    

import speech_recognition as sr

def ses_dosyasini_metne_cevir_ve_kaydet(ses_dosyasi_yolu, hedef_dosya_yolu):
    recognizer = sr.Recognizer()
    with sr.AudioFile(ses_dosyasi_yolu) as ses_dosyasi:
        ses = recognizer.record(ses_dosyasi)
    
    try:
        metin = recognizer.recognize_google(ses, language="en-US")
        with open(hedef_dosya_yolu, "w") as hedef_dosya:
            hedef_dosya.write(metin)
        return "Ses dosyasından çevrilen metin başarıyla '{}' dosyasına kaydedildi.".format(hedef_dosya_yolu)
    except sr.UnknownValueError:
        return "Ses tanınamadı"
    except sr.RequestError:
        return "Google'a bağlanılamadı"

# Ses dosyasının yolu
ses_dosyasi_yolu = "unammed.wav"  # Ses dosyasının gerçek yolu ile değiştirin

# Hedef metin dosyasının yolu
hedef_dosya_yolu = "ses_metni.txt"  # Kaydedilecek metin dosyasının yolu

# Ses dosyasını metne çevirme ve kaydetme
sonuc = ses_dosyasini_metne_cevir_ve_kaydet(ses_dosyasi_yolu, hedef_dosya_yolu)
print(sonuc)
import pyphen

def metni_hecele_ve_kaydet(dosya_yolu, hedef_dosya_yolu):
    # İngilizce dil modeli yükleme
    dic = pyphen.Pyphen(lang='en')
    
    # Metni metin dosyasından okuma
    with open(dosya_yolu, 'r') as dosya:
        metin = dosya.read().strip()
    
    # Metni heceleme
    heceler = dic.inserted(metin).split('-')
    
    # Heceleme sonuçlarını bir metin dosyasına yazma
    with open(hedef_dosya_yolu, 'w') as dosya:
        dosya.write(' '.join(heceler))

# Heceleme yapılacak metin dosyasının yolu
metin_dosyasi_yolu = "ses_metni.txt"

# Hedef dosyanın yolu
hedef_dosya_yolu = "hecelenen_metin.txt"

# Metni hecele ve dosyaya kaydet
metni_hecele_ve_kaydet(metin_dosyasi_yolu, hedef_dosya_yolu)
print("Metin hecelenerek", hedef_dosya_yolu, "dosyasına kaydedildi.")
import pyttsx3
import os

def seslendir_txt_dosyasi(dosya_yolu, kayit_dosya_adi):
    # Engine oluşturma
    engine = pyttsx3.init()
    
    # Sesi ayarlama (isteğe bağlı)
    engine.setProperty('rate', 100)  # Söylenen hız
    engine.setProperty('volume', 0.9) # Ses seviyesi (0.0 - 1.0 arası)
    
    # Metin dosyasını okuma ve seslendirme
    with open(dosya_yolu, 'r') as dosya:
        metin = dosya.read()
        engine.say(metin)
        engine.runAndWait()
    
    # Sesli dosyayı WAV formatında kaydetme
    engine.save_to_file(metin, kayit_dosya_adi)
    engine.runAndWait()

# Seslendirilecek metin dosyasının yolu
dosya_yolu = "hecelenen_metin.txt"
# Kaydedilecek ses dosyasının adı ve yolu
kayit_dosya_adi = "sesli_metin.wav"

# Metni seslendirme ve kaydetme
seslendir_txt_dosyasi(dosya_yolu, kayit_dosya_adi)
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np  # NumPy kütüphanesini ekledik

# Ses dosyasını yükle
audio_path = 'unammed.wav'  # Dosya adını "unnamed.wav" olarak düzelttik
y, sr = librosa.load(audio_path)

# Ses dosyasının zaman-frekans spektrogramunu oluştur
D = librosa.amplitude_to_db(librosa.stft(y), ref=np.max)
plt.figure(figsize=(10, 5))
librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Ses Dosyasının Zaman-Frekans Spektrogramı')
plt.show()

# Ses dosyasının enerji histogramını oluştur
plt.figure(figsize=(10, 5))
plt.hist(y, bins=100)
plt.title('Ses Dosyasının Enerji Histogramı')
plt.xlabel('Amplitude')
plt.ylabel('Frequency')
plt.show()
