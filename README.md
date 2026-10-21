# ChronoFloat — Floating Watch \& Productivity Studio

**ChronoFloat** is a lightweight desktop companion built with Python and Tkinter. Its always-on-top floating watch keeps the essentials close at hand: elegant analog and digital clocks, quick notes, countdown timers, synthesized chimes, and audio-reactive visualizers—without taking over your workspace.

!\[Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square\&logo=python)
!\[Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)
!\[License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

\---

## Features

### ⌚ Twelve distinctive watch faces

Choose from six analog designs:

* Royal Chronograph — Gold / Obsidian
* Devanagari Heritage — Ivory / Bronze
* Aviator Pilot
* Cyber HUD
* Emerald Diver
* Bauhaus Minimal

Or switch to one of six digital designs:

* Chrono Ring (Smart Dial)
* Flip-Clock Studio
* Tactical G-LCD
* Devanagari Heritage Slate
* Cyber HUD Telemetry
* Imperial Roman Plaque

**Numeral styles:** switch between English numerals (`0–9` / `1–12`), Hindi/Devanagari numerals (`०–९` / `१–१२`), and Roman numerals. Calendar display options can be toggled independently for day, date, month, and year.

### 👻 A clean, floating interface

* **Round watch presentation:** chroma-key transparency can hide the rectangular window background and title bar, leaving the watch face visible.
* **Hover controls:** move the pointer over the watch to reveal the drag bar, pin toggle, and settings button.
* **Always on top:** keep the clock visible while working in other applications.

> Window transparency and always-on-top behavior can vary slightly by operating system and desktop window manager.

### 📝 Auto-saving sticky notes

* Create and manage multiple note tabs.
* Notes save automatically as you type.
* Rename a tab with a double-click.
* Switch between tabs or delete notes you no longer need.
* Each note includes a **Last Written** heading with the modification day, date, and time.

### ⏱️ Countdown timer and synthesized chimes

* Quick presets: **2, 5, 10, 15, 25, 30, 45, and 60 minutes**.
* Set a custom duration with hour, minute, and second controls.
* Choose from **16 built-in synthesized chime patterns**, from Tibetan singing-bowl and Westminster-style sounds to retro arcade tones and lo-fi chords.
* Watch the countdown progress on a radial arc around the clock face.
* Built-in chimes do not require external WAV or MP3 files.

### 🎵 Audio-reactive visualizers

ChronoFloat can react to music playback from desktop sources such as Spotify, YouTube, and VLC, with visual effects selected for the current watch style. NOTE: STILL UNDER PROGRESS 

**Digital watch effects**

* Spectrum equalizer bars
* Oscilloscope soundwave
* Cyberpunk neon fireflies
* Matrix digital rain

**Analog watch effects**

* Fire particle ring
* Fluid water waves
* Circular audio starburst
* Pulsing vinyl-groove ring

\---

## Installation

### Option 1: Download the Windows executable

1. Open the repository's [Releases](../../releases) page.
2. Download the latest `floating\_clock.exe` release asset.
3. Double-click the file to launch ChronoFloat.

On first launch, Windows SmartScreen may display a warning for an unrecognized application. Only continue if you trust the source of the executable. If you choose to run it, select **More info → Run anyway**.

### Option 2: Run from source

**Requirements:** Python 3.10 or later, with Tkinter available in your Python installation.

1. Clone the repository:

```bash
   git clone https://github.com/YOUR\_USERNAME/floating-clock.git
   cd floating-clock
   ```

2. Create a virtual environment:

```bash
   python -m venv .venv
   ```

3. Activate it:

   **Windows PowerShell**

```powershell
   .\\.venv\\Scripts\\Activate.ps1
   ```

   **Windows Command Prompt**

```bat
   .venv\\Scripts\\activate.bat
   ```

   **macOS / Linux**

```bash
   source .venv/bin/activate
   ```

4. If the repository includes a `requirements.txt` file, install the listed dependencies:

```bash
   python -m pip install -r requirements.txt
   ```

5. Launch the application's main Python entry-point script. For example, if it is named `floating\_clock.py`:

```bash
   python floating\_clock.py
   ```

   Use the actual entry-point filename if your checkout names it differently.

To verify that Tkinter is available, run:

```bash
python -m tkinter
```

\---

## Usage

* **Choose a watch face:** select an analog or digital design from the available styles.
* **Personalize numerals and date fields:** choose a numeral system and toggle calendar fields independently.
* **Keep the watch out of the way:** use the pin control and hover-revealed controls to position and manage the widget.
* **Capture a quick thought:** create a sticky-note tab and continue working; edits save automatically.
* **Focus with a timer:** choose a preset or enter a custom countdown, then select a chime style.
* **Add ambient motion:** enable an audio-reactive visualizer that matches the selected watch mode.

\---

## Troubleshooting

**The application will not start from source**  
Confirm that you are using Python 3.10 or later and that Tkinter is included in your Python installation. If the project contains a `requirements.txt`, install its dependencies in the active virtual environment.

**Transparency does not look fully round**  
Chroma-key transparency depends on platform and window-manager support. Check the desktop environment's handling of transparent windows and ensure the configured background color is not being altered by other display settings.

**The visualizer does not react to audio**  
Start audio playback in a supported desktop application and check any application or operating-system audio permissions and configuration required by your environment.

\---

## Contributing

Bug reports, reproducible issue descriptions, and thoughtful improvements are welcome. When reporting a problem, include your operating system, Python version (if running from source), steps to reproduce it, and any relevant error output. Avoid including personal information in logs or screenshots.

## License

ChronoFloat is distributed under the **MIT License**. See the repository's `LICENSE` file for the full license text.

\---

*Keep time visible. Keep your workspace focused.*

