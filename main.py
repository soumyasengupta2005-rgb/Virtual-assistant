import tkinter as tk
import random
import threading
import time
import pyttsx3
import keyboard
import speech_recognition as sr
import webbrowser
import os
import json
from threading import Lock

engine = pyttsx3.init()
speak_lock = Lock()
memory_file = "memory.json"

def load_memory():
    try:
        if os.path.exists(memory_file):
            with open(memory_file, "r") as f:
                return json.load(f)
    except json.JSONDecodeError:
        pass
    return {"name": None, "tasks": []}

def save_memory():
    with open(memory_file, "w") as f:
        json.dump(memory, f)

memory = load_memory()

root = tk.Tk()
root.title("Desktop Assistant")
root.geometry("320x180+100+100")
root.attributes("-topmost", True)
root.overrideredirect(True)

canvas_w, canvas_h = 320, 180
canvas = tk.Canvas(root, width=canvas_w, height=canvas_h, bg="#1e1e1e", highlightthickness=0)
canvas.pack(fill="both", expand=True)

label = tk.Label(root, text="(•◡•)\nReady to help!",
                 font=("Comic Sans MS", 16, "bold"),
                 bg="#1e1e1e", fg="white", justify="center")

BUBBLE_TAG = "bubble_bg"
GLOW_TAG = "bubble_glow"

def draw_bubble_and_glow():
    canvas.delete(BUBBLE_TAG)
    canvas.delete(GLOW_TAG)

    w = canvas.winfo_width() or canvas_w
    h = canvas.winfo_height() or canvas_h

    pad_x, pad_y = 20, 20
    left = pad_x
    top = pad_y
    right = max(w - pad_x, pad_x + 10)
    bottom = max(h - pad_y, pad_y + 10)

    glow_steps = 8
    base_r, base_g, base_b = 70, 40, 130  # purple-ish
    for i in range(glow_steps, 0, -1):
        extra = i * 3
        outline_width = max(1, i // 2)
        r = min(255, base_r + i * 6)
        g = min(255, base_g + i * 3)
        b = min(255, base_b + i * 2)
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_oval(left - extra, top - extra, right + extra, bottom + extra,
                           outline=color, width=outline_width, tags=GLOW_TAG)


    canvas.create_oval(left, top, right, bottom, fill="#1e1e1e", outline="#444444", width=2, tags=BUBBLE_TAG)

    existing = canvas.find_withtag("label_window")
    if existing:
        canvas.coords(existing[0], w//2, h//2)
    else:
        canvas.create_window(w//2, h//2, window=label, tags=("label_window",))

def on_canvas_configure(event):
    draw_bubble_and_glow()

canvas.bind("<Configure>", on_canvas_configure)

root.after(30, draw_bubble_and_glow)

def close():
    root.destroy()

close_btn = tk.Button(root, text="✖", font=("Arial", 10),
                      command=close, bg="#444444", fg="white",
                      bd=0, relief="flat",
                      activebackground="red", activeforeground="white")
close_btn.place(x=290, y=10)

personalities = {
    "happy": {"voice_id": 1, "rate": 190, "lines": ["You're amazing!", "Let's do this!", "You're unstoppable!"]},
    "grumpy": {"voice_id": 0, "rate": 150, "lines": ["Ugh. What now?", "Can we not?", "Do I have to?"]},
    "sleepy": {"voice_id": 0, "rate": 120, "lines": ["I was dreaming of clouds...", "Zzz... huh?", "Are we done yet?"]},
    "crazy": {"voice_id": 1, "rate": 220, "lines": ["WAHAHAHAA!", "Reality is an illusion!", "Behold my power!"]}
}

def speak(text, mood="happy"):
    with speak_lock:
        p = personalities.get(mood, personalities["happy"])
        engine.setProperty('voice', engine.getProperty('voices')[p["voice_id"]].id)
        engine.setProperty('rate', p["rate"])
        engine.say(text)
        engine.runAndWait()

def update_label_safe(text):
    root.after(0, lambda: label.config(text=text))

is_listening = False

def mood_loop():
    global is_listening
    while True:
        if not is_listening:
            mood = random.choice(list(personalities.keys()))
            line = random.choice(personalities[mood]["lines"])
            update_label_safe(f"(•◡•)\n{line}")
            speak(line, mood)
        time.sleep(random.randint(20, 40))

def blink():
    faces = ["(•◡•)", "(•﹏•)", "(•◡•)"]
    while True:
        for face in faces:
            current = label.cget("text").split("\n")[-1]
            update_label_safe(f"{face}\n{current}")
            time.sleep(0.4)

def hotkeys():
    while True:
        if keyboard.is_pressed("h"):
            root.withdraw()
            time.sleep(0.5)
        elif keyboard.is_pressed("s"):
            root.deiconify()
            time.sleep(0.5)

def listen():
    global is_listening
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)
    while True:
        try:
            with mic as source:
                is_listening = True
                print("🎤 Listening...")
                audio = r.listen(source, phrase_time_limit=5, timeout=5)
                command = r.recognize_google(audio, language='en-IN').lower()
                print(f"🔊 Heard: {command}")
                is_listening = False
                if "hello" in command or "hi" in command:
                    reply = "Hello there!"
                elif "how are you" in command:
                    reply = "I'm feeling like a floating emoji today!"
                elif "my name is" in command:
                    name = command.split("my name is")[-1].strip().capitalize()
                    memory["name"] = name
                    save_memory()
                    reply = f"Nice to meet you, {name}!"
                elif "what's my name" in command:
                    reply = f"Your name is {memory['name']}" if memory["name"] else "I don't know your name yet!"
                elif "remember to" in command:
                    task = command.split("remember to")[-1].strip()
                    memory["tasks"].append(task)
                    save_memory()
                    reply = f"I'll remember: {task}"
                elif "show tasks" in command:
                    reply = "Here are your tasks:\n" + ", ".join(memory["tasks"]) if memory["tasks"] else "You have no tasks."
                elif "open youtube" in command:
                    webbrowser.open("https://www.youtube.com")
                    reply = "Opening YouTube for you "
                elif "open notepad" in command:
                    os.system("start notepad")
                    reply = "Opening Notepad "
                elif "open calculator" in command:
                    os.system("start calc")
                    reply = "Here comes the calculator! "
                elif "open chatgpt" in command:
                    webbrowser.open("https://www.chatgpt.com")
                    reply = "Opening chatgpt for you "
                elif "bye" in command:
                    reply = "Goodbye, see you soon!"
                    update_label_safe(f"(•◡•)\n{reply}")
                    speak(reply)
                    time.sleep(2)
                    root.destroy()
                    break
                else:
                    reply = "I heard you, but I don't know how to respond yet."

                update_label_safe(f"(•◡•)\n{reply}")
                speak(reply)

        except sr.WaitTimeoutError:
            is_listening = False
        except sr.UnknownValueError:
            print("Didn't understand.")
        except sr.RequestError:
            print("Network issue with voice service.")

threading.Thread(target=mood_loop, daemon=True).start()
threading.Thread(target=blink, daemon=True).start()
threading.Thread(target=hotkeys, daemon=True).start()
threading.Thread(target=listen, daemon=True).start()

root.mainloop()
