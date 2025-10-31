# Virtual-assistant
A minimalist desktop AI assistant built with Python and Tkinter. It features speech recognition, voice replies, moods, hotkey controls, memory for names and tasks, and simple GUI animations. It can open apps like YouTube, Notepad, or Calculator. Still in development—expect future upgrades for smarter responses and visuals.
# Desktop AI Assistant (Python)

A personal desktop AI assistant built using **Python** and **Tkinter**, designed to be compact, responsive, and a little expressive. The assistant listens, talks, remembers your name, keeps track of your tasks, and interacts with your system through simple voice commands.

---

## Features
- **Interactive Voice System**  
  Uses `speech_recognition` and `pyttsx3` for real-time listening and speaking.  
  Responds to greetings, tasks, and app-opening commands.
- **Memory Functionality**  
  Remembers your name and a list of tasks using a `memory.json` file.
- **Dynamic Personality & Mood System**  
  Randomly switches between happy, grumpy, sleepy, or crazy moods.  
  Voice pitch and rate change accordingly.
- **Compact GUI**  
  Built with Tkinter featuring:  
  - Draggable floating window  
  - Custom canvas glow  
  - Minimalist face expression animations  
  - Always-on-top behavior  
- **Hotkey Controls**  
  - Press **H** to hide  
  - Press **S** to show  
- **Voice Commands Supported**  
  - “Hello” / “Hi”  
  - “How are you”  
  - “My name is …”  
  - “Remember to …”  
  - “Show tasks”  
  - “Open YouTube / Notepad / Calculator/chatgpt”  
  - “Bye”
---
## ⚙️ Requirements
Install dependencies before running:
pip install pyttsx3 speechrecognition keyboard pyaudio

Known Issues / Limitations
Speech recognition requires a stable internet connection.
Occasional delays during listening or speaking.
Cannot currently execute complex commands or maintain long-term memory across restarts beyond name and tasks.
GUI might appear slightly misaligned on some display resolutions.
Hotkeys may conflict if other software captures “H” or “S”.

Planned Updates
Customizable themes and shapes for the assistant.
More personality types and smarter dialogue responses.
Local offline recognition support.
Integration with external APIs (e.g., weather, news, reminders).
Task management improvements with due times.
