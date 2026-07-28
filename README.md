# ⚡ Speed Sudoku 6x6 (Multiplayer WebSockets Engine)

A real-time, competitive $6 \times 6$ multiplayer Sudoku game inspired by the LinkedIn Mini Sudoku layout. Built with an asynchronous **FastAPI** backend, persistent **WebSockets** for live synchronization, and a custom **Backtracking Algorithm** for puzzle generation.

---

## 🚀 Live Demo

🎮 **Play the game live:** [https://speed-sudoku-game.onrender.com/](https://speed-sudoku-game.onrender.com/)

---

## ✨ Features

* **Real-Time Multiplayer Race:** Connect with friends via custom Room Codes to compete on identical boards simultaneously.
* **Deterministic Algorithmic Generation:** Custom $6 \times 6$ Sudoku puzzle generator and solver powered by a recursive Backtracking algorithm.
* **Low-Latency State Synchronization:** Bi-directional communication over persistent WebSockets streams live opponent progress, move accuracy, and match state.
* **Interactive Hints & Validation:** Instant visual feedback (green/red highlights) for valid and invalid inputs with error/mistake tracking.
* **Post-Match Analytics:** Real-time game timer, total move counting, accuracy percentage calculations, and one-click rematch functionality.

---

## 🛠️ Tech Stack & Architecture

* **Backend:** Python 3.10+, FastAPI, Uvicorn
* **Communication Protocol:** WebSockets (JSON payload streaming)
* **Frontend:** HTML5, CSS3 (Modern Glassmorphism Design), Vanilla JavaScript (ES6+)
* **Deployment:** Render (Automated Continuous Deployment), Git
