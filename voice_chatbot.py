import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import cohere
import pyttsx3



COHERE_API_KEY = "your own key here !" 

DURATION = 5  
SAMPLE_RATE = 44100  
AUDIO_FILENAME = "input.wav"  



def record_audio():
    print(" Speak now...")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    write(AUDIO_FILENAME, SAMPLE_RATE, audio)
    print(" Audio recorded")



def transcribe_audio():
    model = whisper.load_model("base") 
    result = model.transcribe(AUDIO_FILENAME)
    return result["text"]



def get_bot_response(prompt):
    co = cohere.Client(COHERE_API_KEY)
    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=100
    )
    return response.generations[0].text.strip()



def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()



def main():
    while True:
        record_audio()
        user_input = transcribe_audio()
        print(" You said:", user_input)

        if user_input.lower() in ["exit", "quit", "stop"]:
            print(" Goodbye!")
            break

        response = get_bot_response(user_input)
        print(" Bot:", response)
        speak_text(response)

        print("\nSay something else or type Ctrl+C to quit.")

if __name__ == "__main__":
    main()
