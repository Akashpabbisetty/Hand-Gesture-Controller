# Real-Time Hand Gesture Controller for Gaming 🖐️🎮

This Python project allows you to control PC games, like Subway Surfers, using hand gestures captured through your webcam. It interprets real-time hand movements and poses, translating them into keyboard commands to play the game hands-free.

https://github.com/user-attachments/assets/13dda4f0-29ba-4bc0-af38-24f7a9064fcb

---

## 🛠️ Tech Stack

- **Python**
- **OpenCV:** For capturing and processing the live video feed from the webcam.
  
- **MediaPipe:** For its high-fidelity hand landmark detection model, which forms the core of the gesture recognition engine. (Note : When using mediapipe use pyhton version b/w 3.7 - 3.9. Only until these  vesrions support mediapipe.)
  
- **PyAutoGUI:** For programmatically simulating keyboard presses to control the game.

---
## ✨ Features

- **Real-Time Gesture Recognition:** Uses your webcam to track hand movements with minimal delay.
- 
- **Intuitive Controls:**
    - **Swipe Up:** Jump ⬆️
    - **Swipe Left/Right:** Move left or right ⬅️➡️
    - **Closed Fist:** Roll/Duck ✊
      
- **Customizable Sensitivity:** Easily tune swipe sensitivity and action cooldowns by changing parameters at the top of the script.
  
- **State Management:** A "gesture lock" ensures one continuous swipe results in only one action, preventing input spam.

---

## 🚀 Setup and Installation

Follow these steps to get the project running on your local machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/YourUsername/Your-Repo-Name.git](https://github.com/YourUsername/Your-Repo-Name.git)
cd Your-Repo-Name
