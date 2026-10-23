# ChronoFloat — Floating Watch & Productivity Studio

**ChronoFloat** is a lightweight desktop companion built with Python and Tkinter. Its always-on-top floating watch keeps the essentials close at hand: elegant analog and digital clocks, smart battery health alerts, quick notes with automatic list formatting, countdown timers, synthesized chimes, and audio-reactive visualizers—without taking over your workspace.

![Version](https://img.shields.io/badge/Release-v.2.0-brightgreen?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🚀 What's New in v2.0 (Distinct from v1.0)

| Feature Area | v1.0 Foundation | v2.0 Upgrades |
| :--- | :--- | :--- |
| **Battery Monitoring** | Passive battery percentage indicator & sub-dial | **🔋 Smart Battery Guardian Studio:** Active upper (`100%` default) & lower (`15%` default) limit alarms with custom melodies and flashing watch-face alerts |
| **Sticky Notes Editor** | Multi-tab auto-saving plain text notes | **📝 Smart Lists & Terminal Clipboard:** Auto-indenting & auto-incrementing numbered (`1.`) and bulleted (`•`) lists, plus **Select-to-Copy** and **Right-Click (RMB) to Paste** |
| **First-Launch Experience** | Opened in Royal Chronograph / Chrono Ring with visualizer on | **⌚ Refined Out-of-the-Box Defaults:** Opens in **Aviator Pilot** (Analog) and **Flip-Clock Studio** (Digital) with the visualizer disabled by default until enabled by the user |
| **UI & Dialect Fixes** | Standard calendar & preset labels | High-contrast **Devanagari Heritage** calendar badge & cleaned-up timer preset labels (`25 Min`) |

---

## Features

### ⌚ Twelve distinctive watch faces

Choose from six analog designs:

- **Aviator Pilot** *(Default Analog)*
- Royal Chronograph — Gold / Obsidian
- Devanagari Heritage — Ivory / Bronze
- Cyber HUD
- Emerald Diver
- Bauhaus Minimal

Or switch to one of six digital designs:

- **Flip-Clock Studio** *(Default Digital)*
- Chrono Ring (Smart Dial)
- Tactical G-LCD
- Devanagari Heritage Slate
- Cyber HUD Telemetry
- Imperial Roman Plaque

**Numeral styles:** switch between English numerals (`0–9` / `1–12`), Hindi/Devanagari numerals (`०–९` / `१–१२`), and Roman numerals. Calendar display options can be toggled independently for day, date, month, and year.

### 👻 A clean, floating interface

- **Round watch presentation:** chroma-key transparency can hide the rectangular window background and title bar, leaving the watch face visible.
- **Hover controls:** move the pointer over the watch to reveal the drag bar, pin toggle, battery guardian, notes, timer, and settings buttons.
- **Always on top:** keep the clock visible while working in other applications.

> Window transparency and always-on-top behavior can vary slightly by operating system and desktop window manager.

### 🔋 Smart Battery Guardian Studio *(New in v2.0)*

- **Upper Limit Alert (Overcharge Protection):** Notifies you when your charger is plugged in (`⚡`) and the battery reaches your target ceiling (configurable from `50%` to `100%`, default `100%`).
- **Lower Limit Alert (Low Battery Warning):** Notifies you when running on battery power (`🔋`) and charge drops to your threshold (configurable from `5%` to `50%`, default `15%`).
- **Independent Custom Tones:** Pick separate chimes from the 16 built-in synthesized melodies for high and low battery alerts, complete with individual test buttons.
- **Smart State Reset & One-Click Dismiss:** Click the flashing badge directly on the watch face (or unplug/plug in your charger) to silence active alerts immediately without repetitive alarm spam.

### 📝 Auto-saving sticky notes with smart formatting *(Upgraded in v2.0)*

- **Smart Auto-Lists:**
  - Type `1.` followed by `Space` to automatically indent (`  1. `). Press `Enter` to automatically increment to `2.`, `3.`, and so on.
  - Type `-` or `*` followed by `Space` to convert into an indented bullet list (`  • `) that continues on `Enter`.
  - Press `Enter` on an empty numbered or bulleted line to exit the list cleanly.
- **Fast Terminal-Style Clipboard:**
  - **Select to Auto-Copy:** Highlight any text with your mouse and release left-click to copy it immediately to your clipboard.
  - **Right-Click (RMB) to Paste:** Right-click anywhere inside the note editor to paste clipboard text directly at the cursor position.
- **Multi-Tab Management:** Create, switch, rename (via double-click), and delete tabs. Every keystroke saves automatically with a live **Last Written** timestamp.

### ⏱️ Countdown timer and synthesized chimes

- Quick presets: **2, 5, 10, 15, 25, 30, 45, 60, and 120 minutes**.
- Set a custom duration with hour, minute, and second controls.
- Choose from **16 built-in synthesized chime patterns**, from Tibetan singing-bowl and Westminster-style sounds to retro arcade tones and lo-fi chords.
- Watch the countdown progress on a radial arc around the clock face.
- Built-in chimes do not require external WAV or MP3 files.

### 🎵 Audio-reactive visualizers *(🚧 Experimental / In Development Phase)*

> **Development Status Note:** The **Audio-Reactive Visualizer** is currently in its **active development phase**. It currently uses process-level media detection alongside a procedural animation engine (plus an optional *Always-On Audio Simulation* test toggle) and is disabled by default on first launch. Full real-time system WASAPI loopback FFT frequency analysis is planned for upcoming releases.

ChronoFloat adapts its visualizer styles automatically based on whether you are in Digital or Analog watch mode:

**Digital watch effects**

- Spectrum equalizer bars (EQ)
- Oscilloscope soundwave
- Cyberpunk neon fireflies
- Matrix digital rain

**Analog watch effects**

- Fire particle ring 🔥
- Fluid water waves 🌊
- Circular audio starburst
- Pulsing vinyl-groove ring

---

## Installation

### Option 1: Download the Windows executable

1. Open the repository's [Releases](https://github.com/hemnathsah/floating-clock/releases) page.
2. Download the latest `floating_clock.exe` release asset (under **`v.2.0`**).
3. Double-click the file to launch ChronoFloat.

On first launch, Windows SmartScreen may display a warning for an unrecognized application. Only continue if you trust the source of the executable. If you choose to run it, select **More info → Run anyway**.

### Option 2: Run from source

**Requirements:** Python 3.10 or later, with Tkinter available in your Python installation.

1. Clone the repository:

   ```bash
   git clone https://github.com/hemnathsah/floating-clock.git
   cd floating-clock

2. Create a virtual environment:

   ```bash
   python -m venv .venv

3. Activate it:

   * Windows PowerShell:
      
      ```bash
      .\.venv\Scripts\Activate.ps1

   * Windows Command Prompt
      
      ```bash
      .venv\Scripts\activate.bat

   * macOS / Linux

      ```bash
      source .venv/bin/activate

4. Install dependencies (psutil):

   ```bash
   python -m pip install psutil

5. Launch the application:    

   ```bash
   python floating_clock.py

To verify that Tkinter is available, run:

   ```bash
   python -m tkinter

🛠️ Building the Standalone .exe

To package the script into a single standalone Windows executable using PyInstaller:

   PowerShell

   ```bash
   pip install pyinstaller
   pyinstaller --noconsole --onefile floating_clock.py

The compiled floating_clock.exe binary will be placed inside the dist/ directory.

Usage

    Choose a watch face (⚙): select an analog or digital design from the available styles.

    Personalize numerals and date fields (⚙): choose a numeral system and toggle calendar fields independently.

    Configure Battery Guardian (🔋): set upper and lower battery percentage limits and test your alert chimes.

    Capture a quick thought (📝): create a sticky-note tab, use 1. or - for auto-lists, select text to copy, and right-click to paste.

    Focus with a timer (⏱): choose a preset or enter a custom countdown, then select a chime style.

    Add ambient motion (⚙): enable an audio-reactive visualizer (or test simulation mode) that matches the selected watch mode.

Troubleshooting

The application will not start from source

Confirm that you are using Python 3.10 or later, that Tkinter is included in your Python installation, and that psutil is installed in your active environment.

Transparency does not look fully round

Chroma-key transparency depends on platform and window-manager support. Check the desktop environment's handling of transparent windows and ensure the configured background color is not being altered by other display settings.

The visualizer does not react to audio

Because the Audio-Reactive Visualizer is currently in development, ensure you have checked Enable Music Visualizer in the ⚙ Watch Studio settings. You can also check Always-On Audio Simulation (Test Mode) to preview the animations continuously even when no media player is active.
Contributing

Bug reports, reproducible issue descriptions, and thoughtful improvements are welcome. When reporting a problem, include your operating system, Python version (if running from source), steps to reproduce it, and any relevant error output. Avoid including personal information in logs or screenshots.
License

ChronoFloat is distributed under the MIT License. See the repository's LICENSE file for the full license text.

Keep time visible. Keep your workspace focused.