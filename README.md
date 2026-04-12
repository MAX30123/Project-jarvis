Jarvis Voice Assistant (v0.2)

Overview
 Jarvis v0.2 is a lightweight voice-controlled assistant implemented in Python. The application integrates speech recognition and text-to-speech technologies to enable basic voice interaction and execution of system-level commands.
 The assistant is designed as an educational project demonstrating how to work with audio input, command parsing, and automation in Python.

Key Features
 Speech Processing
 Speech-to-Text using Google Speech Recognition
 Text-to-Speech using pyttsx3
Multilingual Support
 English (en-US)
 Russian (ru-RU)
Date and Time Functions
 Provides current system time
 Provides current system date
 Birthday recognition with automated greeting
File Operations
 Voice-driven creation of Python project files
Application and Web Control
 Launches local applications via subprocess
 Opens web resources via default browser

Supported targets include:
 Google Chrome
 YouTube
 Discord
 Roblox
 Steam
 Visual Studio Code

System Requirements
 Python 3.x
 Microphone device
 Internet connection (required for speech recognition)
 Dependencies

Install required packages:
 pip install pyttsx3 SpeechRecognition

Command Examples:
General Interaction
 "hello jarvis"
 "jarvis how are you"
 "jarvis exit"
Application Control
 "jarvis open google"
 "jarvis open youtube"
 "jarvis open discord"
 "jarvis open steam"
 "jarvis open vscode"
Russian Commands
 "джарвис открой ютуб"
 "джарвис создай проект"
 "который час"
 "какое сегодня число"