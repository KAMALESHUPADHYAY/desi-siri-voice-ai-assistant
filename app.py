import pyttsx3
import requests
import pygame
import time
import os
import speech_recognition as sr  # 🧠 Fix: Import added

# Text-to-speech
engine = pyttsx3.init()

def speak(text):
    print(f"🤖: {text}")
    engine.say(text)
    engine.runAndWait()

# Play intro sound using pygame
def play_intro_sound():
    try:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("intro.mp3")  # 🎵 Make sure this file exists in the same folder
        pygame.mixer.music.play()
        time.sleep(3)
        pygame.mixer.music.stop()
    except Exception as e:
        print("🔇 Intro sound play nahi hua:", e)

# Speech-to-text
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Bol bhai...")
        speak("Boliye, main sun rahi hoon.")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language="en-IN")
        print(f"👦: {query}")
        return query.lower()
    except:
        speak("Sorry bhai, samajh nahi aaya.")
        return ""

# Typing input
def type_input():
    query = input("⌨️  Type karo bhai: ")
    print(f"👦: {query}")
    return query.lower()

# Weather API function
def get_weather(city):
    api_key = "3ca77b989f6a547048b86c9bfebb467e"  # 🔐 Your OpenWeatherMap API key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        res = requests.get(url)
        data = res.json()

        if data["cod"] != 200:
            return f"City '{city}' nahi mila bhai."

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"{city} mein temperature hai {temp}°C aur weather hai '{desc}'."
    except Exception as e:
        print(f"Weather API error: {e}")
        return "Bhai kuch gadbad ho gayi weather laate waqt."

# OpenRouter GPT response function
def get_ai_response(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",  # 🔐 Your API key
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Tum ek helpful aur friendly Hindi assistant ho."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        data = res.json()
        if res.status_code != 200:
            return f"AI se jawab laate waqt error aaya: {data.get('error', {}).get('message', 'Unknown error')}"

        if "choices" in data and len(data["choices"]) > 0:
            reply = data["choices"][0]["message"]["content"]
            return reply.strip()
        else:
            return "AI se sahi jawab nahi aaya bhai."
    except Exception as e:
        print(f"AI API error: {e}")
        return "AI se jawab laate waqt kuch error aaya bhai."

# Main loop
def main():
    play_intro_sound()
    speak("Namastey! Main hoon Desi Siri.")

    # Input mode selection
    speak("Mic se baat karni hai ya keyboard se? (bolo 'mic' ya 'type')")
    mode = input("🔵 Mic ya Type? (mic/type): ").strip().lower()

    if mode == "mic":
        input_method = listen
    else:
        input_method = type_input

    while True:
        query = input_method()

        if "weather" in query or "mausam" in query:
            speak("Kaun se city ka weather chahiye bhai?")
            city = input_method()
            if city:
                report = get_weather(city)
                speak(report)

        elif "band kar" in query or "exit" in query or "quit" in query:
            speak("Bye bhai, milte hain phir.")
            break

        elif query:
            response = get_ai_response(query)
            speak(response)

if __name__ == "__main__":
    main()
