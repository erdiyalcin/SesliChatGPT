import speech_recognition as sr #pip install SpeechRecognition
import openai #pip install openai
from gtts import gTTS #pip install gTTS
import vlc #pip install python-vlc
import time
import eyed3 #pip install eyed3
# ses için pip install PyAudio

#İlk ayarlar
messages = [{"role" : "system", "content":"Sen nazik bir asistanımsın."}]
openai.api_key = "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" # https://platform.openai.com/ Adresinden alabilirsiniz.
r = sr.Recognizer()

#Fonksiyonlar
def SesiOku(dosyaAdi):
    saniye = eyed3.load(dosyaAdi).info.time_secs # ses dosyasının kaç saniye olduğunu öğren
    ses = vlc.MediaPlayer(dosyaAdi) # ses dosyasını vlc programı yardımı ile yükle
    ses.play() # ses dosyasını çalıştır.
    time.sleep(saniye) # ses dosyasının saniyesi kadar bekle
    ses.stop() # ses dosyasını durdur.

def YaziyiSesOlarakKaydet(dosyaAdi,yanit):
    cikti = gTTS(text =yanit , lang="tr", slow=False) # gelen yanıtı ses dosyasına dönüştür.
    cikti.save(dosyaAdi) # ses dosyasını kaydet

def Dinle():
    #sesiOku("sizidinliyorum.mp3") # Sizi dinliyorum sesi ile kullanıcı bildilendiriliyor.
    print("Konuşun:")
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        mesaj = r.recognize_google(audio, language='tr-tr') #audio içerisinde olan ses dosyası google apisi ile yazıya dönüştürülüyor.
        print("Söylediğiniz: " + mesaj)     
    except sr.UnknownValueError:
        mesaj="Anlaşılamadı"
    except sr.RequestError: #as e
        mesaj="Hata"
    return mesaj

def ChatGPTyeGonder(mesaj):
    messages.append({"role" : "user", "content" : mesaj})
    chat = openai.ChatCompletion.create(model = "gpt-3.5-turbo",messages = messages) # mesajı chatgpt apisine gönder ve yanıtı al
    yanit = chat.choices[0].message.content
    print("Chatgpt : ", yanit)
    messages.append({"role" : "assistant", "content":yanit})
    return yanit
    
    
if __name__ == "__main__":   
    while True:   
        mesaj = Dinle()
        if mesaj == "Hata" or mesaj == "Anlaşılamadı": # Alınan ses yazıya dönüştürülürken hata alındıysa aşağıdaki kodları atla ve tekrar dinle
            continue
        else:
            sayac = 0
            yanit = ChatGPTyeGonder(mesaj)
            YaziyiSesOlarakKaydet("ses.mp3",yanit)
            SesiOku("ses.mp3")
            if(mesaj=="teşekkürler"): # Eğer kullanıcı teşekkürler dediyse uygulamayı kapat.
                break
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
