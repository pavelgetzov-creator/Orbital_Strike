# 🌌 Orbital Strike

**Orbital Strike** is a classic 2D arcade space shooter game built in Python using the **Pygame** library. Take control of your spaceship, shoot down incoming enemy vessels, level up as your score climbs, and survive as long as possible to achieve the highest score!

---

## 🎮 Gameplay & Features

* **Main Menu:** Start a new game or quit straight from a clean title screen.
* **Smooth Movement:** Move your spaceship left and right to dodge and line up shots.
* **Laser Combat:** Fire laser projectiles — complete with a proper bullet sprite and an immersive fire sound effect (`piw.wav`).
* **Lives System:** You start with **3 lives**. Every time an enemy ship reaches the bottom of the screen, you lose one life instead of an instant game over — the enemy respawns and the fight continues.
* **Leveling Up:** Reach **20 points** to hit Level 2, and **40 points** to hit Level 3. Each level increase pauses the action with a glowing "Level Up!" screen and speeds up the enemy ship's descent.
* **Power-Ups:** Destroying an enemy has a chance to drop a random power-up:
  * ❤️ **Health** — restores one life.
  * ⏳ **Slow** — cuts the enemy's current speed in half.
  Fly your ship into a power-up to collect it before it falls off-screen.
* **Live HUD:** Track your current score and remaining lives in real time in the top-left corner.
* **Game Over Screen:** Features a dark blurred overlay with a glowing red "GAME OVER!" warning.
* **Instant Restart:** Click **"Play Again"** to jump straight back into a new match, or **"Back to Menu"** to return to the title screen — no need to close the app.
* **Audio Atmosphere:** Looping space background music plus dedicated sound effects for firing.
* **Starfield Backdrop:** A full space-themed background image behind all the action.

---

## ⌨️ Controls

* ⬅️ **Left Arrow:** Move spaceship left
* ➡️ **Right Arrow:** Move spaceship right
* ⎵ **Spacebar:** Fire laser
* 🖱️ **Left Click:** Used throughout the menus — Start / Quit on the title screen, Continue on the Level Up screen, and Play Again / Back to Menu on the Game Over screen.

---

## 🛠️ Requirements & Installation

> ⚠️ **Important:** To run the game properly, you must download **all files and folders** from this repository (including the `Assets/` directory) and keep them in the same project folder.

1. **Download or Clone the Project:**
   Ensure you have downloaded the entire project. If you use Git, run:
```bash
git clone https://github.com/pavelgetzov-creator/Orbital_Strike
cd orbital-strike
```

2. **Install Pygame:**
   Make sure you have Python installed, then run the following command in your terminal:
```bash
pip install pygame
```

3. **Run the Game:**
   Launch the main script to start playing:
```bash
python main.py
```