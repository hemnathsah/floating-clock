import tkinter as tk
from tkinter import ttk, simpledialog
import time
import datetime
import json
import os
import math
import struct
import wave
import tempfile
import random
import re

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

try:
    import psutil
except ImportError:
    print("Please install psutil using: pip install psutil")
    exit()

CONFIG_FILE = "clock_config.json"
NOTES_FILE = "clock_notes.json"
TRANSPARENT_KEY = "#010203"

HINDI_DIGITS = str.maketrans("0123456789", "०१२३४५६७८९")
HINDI_DAYS = ["सोम", "मंगल", "बुध", "गुरु", "शुक्र", "शनि", "रवि"]
HINDI_MONTHS = ["जन", "फ़र", "मार्च", "अप्रै", "मई", "जून", "जुला", "अग", "सितं", "अक्टू", "नवं", "दिसं"]
ENG_DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
ENG_MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

ANALOG_NUMERAL_SETS = {
    "English (0-9)": ["12", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
    "Hindi (०-९)": ["१२", "१", "२", "३", "४", "५", "६", "७", "८", "९", "१०", "११"],
    "Roman (I-XII)": ["XII", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI"]
}

DIGITAL_VIS_TYPES = [
    "1. Spectrum Equalizer Bars (EQ)",
    "2. Oscilloscope Soundwave",
    "3. Cyberpunk Neon Fireflies",
    "4. Matrix Digital Rain"
]

ANALOG_VIS_TYPES = [
    "1. Fire Particle Ring 🔥",
    "2. Fluid Water Waves 🌊",
    "3. Circular Audio Starburst",
    "4. Pulsing Vinyl Groove Ring"
]

TONE_LIBRARY = {
    "1. Zen Tibetan Bowl": [([432, 864, 1296], 1.4, "bell"), ([432, 648], 1.6, "bell")],
    "2. Royal Westminster Chime": [([659], 0.35, "bell"), ([587], 0.35, "bell"), ([523], 0.35, "bell"), ([392], 0.7, "bell"), ([392, 523, 659], 1.1, "bell")],
    "3. Cyberpunk Arpeggio": [([220], 0.12, "retro"), ([277], 0.12, "retro"), ([330], 0.12, "retro"), ([440], 0.12, "retro"), ([554], 0.15, "retro"), ([659], 0.15, "retro"), ([880, 440], 0.55, "retro")],
    "4. Mario 1-Up Coin": [([659], 0.10, "retro"), ([784], 0.10, "retro"), ([1319], 0.10, "retro"), ([1047], 0.10, "retro"), ([1175], 0.10, "retro"), ([1568], 0.35, "retro")],
    "5. Victory Fanfare": [([523, 659], 0.14, "retro"), ([523, 659], 0.14, "retro"), ([523, 659], 0.14, "retro"), ([523, 659, 784], 0.45, "retro"), ([415, 622], 0.30, "retro"), ([466, 700], 0.30, "retro"), ([523, 784, 1046], 0.65, "retro")],
    "6. Morning Marimba": [([523], 0.16, "warm"), ([659], 0.16, "warm"), ([784], 0.16, "warm"), ([1046], 0.25, "warm"), ([784], 0.16, "warm"), ([1046, 659], 0.50, "warm")],
    "7. Crystal Harp Glissando": [([523], 0.09, "bell"), ([587], 0.09, "bell"), ([659], 0.09, "bell"), ([784], 0.09, "bell"), ([880], 0.09, "bell"), ([1046], 0.09, "bell"), ([1175], 0.09, "bell"), ([1319, 659], 0.75, "bell")],
    "8. Classic Digital Watch Beep": [([2048], 0.09, "retro"), ([0], 0.06, "retro"), ([2048], 0.09, "retro"), ([0], 0.25, "retro"), ([2048], 0.09, "retro"), ([0], 0.06, "retro"), ([2048], 0.09, "retro")],
    "9. Space Odyssey Chord": [([261, 392], 0.5, "pad"), ([261, 392, 523], 0.6, "pad"), ([261, 392, 523, 659], 1.1, "pad")],
    "10. Lo-Fi Chill Chords": [([261, 329, 392, 493], 0.55, "warm"), ([220, 261, 329, 392], 0.55, "warm"), ([174, 220, 261, 349], 0.55, "warm"), ([196, 246, 293, 392], 0.70, "warm")],
    "11. Temple Bell Resonance": [([528, 1056, 1584], 1.1, "bell"), ([396, 792, 1188], 1.3, "bell")],
    "12. Submarine Sonar Pulse": [([1350], 0.18, "bell"), ([0], 0.55, "bell"), ([1350], 0.18, "bell"), ([0], 0.55, "bell"), ([1350], 0.25, "bell")],
    "13. Retro Arcade Level Up": [([330], 0.09, "retro"), ([392], 0.09, "retro"), ([659], 0.09, "retro"), ([523], 0.09, "retro"), ([587], 0.09, "retro"), ([784], 0.09, "retro"), ([1046], 0.4, "retro")],
    "14. Soft Piano Triad": [([261, 329, 392], 0.4, "warm"), ([293, 369, 440], 0.4, "warm"), ([329, 415, 493], 0.4, "warm"), ([349, 440, 523], 0.75, "warm")],
    "15. Urgent Radar Klaxon": [([880, 932], 0.22, "retro"), ([440, 466], 0.22, "retro"), ([880, 932], 0.22, "retro"), ([440, 466], 0.22, "retro"), ([880, 932], 0.35, "retro")],
    "16. Starlight Lullaby": [([523, 261], 0.35, "bell"), ([523], 0.35, "bell"), ([784, 392], 0.35, "bell"), ([784], 0.35, "bell"), ([880, 440], 0.35, "bell"), ([880], 0.35, "bell"), ([784, 392, 523], 0.75, "bell")]
}


class SoundEngine:
    def __init__(self):
        self.temp_dir = os.path.join(tempfile.gettempdir(), "floating_clock_tones")
        os.makedirs(self.temp_dir, exist_ok=True)
        self.cached_files = {}

    def get_wav_path(self, tone_name):
        if tone_name in self.cached_files and os.path.exists(self.cached_files[tone_name]):
            return self.cached_files[tone_name]
        safe_name = "".join(c if c.isalnum() else "_" for c in tone_name)
        file_path = os.path.join(self.temp_dir, f"{safe_name}.wav")
        pattern = TONE_LIBRARY.get(tone_name, TONE_LIBRARY["1. Zen Tibetan Bowl"])
        sample_rate = 22050
        frames = bytearray()
        for freqs, dur, style in pattern:
            num_samples = int(sample_rate * dur)
            for i in range(num_samples):
                t = i / sample_rate
                if not freqs or freqs[0] == 0:
                    frames += struct.pack("<h", 0)
                    continue
                attack = min(1.0, i / (sample_rate * 0.012))
                decay = math.exp(-3.2 * t / dur) if style == "bell" else (math.exp(-4.5 * t / dur) if style == "warm" else 1.0)
                env = attack * decay
                val = 0.0
                for f in freqs:
                    w_val = math.sin(2.0 * math.pi * f * t)
                    if style == "bell":
                        w_val += 0.35 * math.sin(2.0 * math.pi * (f * 2.0) * t)
                    val += w_val
                sample = max(-32767, min(32767, int((val / max(1, len(freqs))) * env * 0.45 * 32767)))
                frames += struct.pack("<h", sample)
        with wave.open(file_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(frames)
        self.cached_files[tone_name] = file_path
        return file_path

    def play(self, tone_name, loop=False):
        if not HAS_WINSOUND:
            return
        try:
            wav_file = self.get_wav_path(tone_name)
            flags = winsound.SND_FILENAME | winsound.SND_ASYNC
            if loop:
                flags |= winsound.SND_LOOP
            winsound.PlaySound(wav_file, flags)
        except Exception:
            pass

    def stop(self):
        if HAS_WINSOUND:
            try:
                winsound.PlaySound(None, winsound.SND_PURGE)
            except Exception:
                pass


DIGITAL_STYLES = {
    "Flip-Clock Studio": {
        "bg": "#121214", "card": "#202024", "border": "#323238", "accent": "#f97316",
        "accent2": "#10b981", "fg": "#f4f4f5", "sub": "#a1a1aa", "bar": "#18181b",
        "font": "Segoe UI", "style": "flip", "default_num": "English (0-9)"
    },
    "Chrono Ring (Smart Dial)": {
        "bg": "#0b0f19", "card": "#111827", "border": "#1f2937", "accent": "#38bdf8",
        "accent2": "#f43f5e", "fg": "#f8fafc", "sub": "#94a3b8", "bar": "#111827",
        "font": "Segoe UI", "style": "ring", "default_num": "English (0-9)"
    },
    "Tactical G-LCD": {
        "bg": "#141814", "card": "#222b22", "border": "#3b4d3b", "accent": "#84cc16",
        "accent2": "#eab308", "fg": "#d9f99d", "sub": "#86efac", "bar": "#1a211a",
        "font": "Consolas", "style": "lcd", "default_num": "English (0-9)"
    },
    "Devanagari Heritage Slate": {
        "bg": "#1a120b", "card": "#261a10", "border": "#d4af37", "accent": "#f59e0b",
        "accent2": "#ef4444", "fg": "#fef3c7", "sub": "#fcd34d", "bar": "#1f150d",
        "font": "Nirmala UI", "style": "heritage", "default_num": "Hindi (०-९)"
    },
    "Cyber HUD Telemetry": {
        "bg": "#05050b", "card": "#0b0c1a", "border": "#00f0ff", "accent": "#00f0ff",
        "accent2": "#ff0055", "fg": "#e0f2fe", "sub": "#fcee09", "bar": "#080914",
        "font": "Consolas", "style": "hud", "default_num": "English (0-9)"
    },
    "Imperial Roman Plaque": {
        "bg": "#0f1015", "card": "#171922", "border": "#c5a059", "accent": "#e5c158",
        "accent2": "#e63946", "fg": "#f3e5ab", "sub": "#c5a059", "bar": "#14161e",
        "font": "Times New Roman", "style": "heritage", "default_num": "Roman (I-XII)"
    }
}

ANALOG_STYLES = {
    "Aviator Pilot": {
        "bg": "#0f1419", "bezel": "#3d4852", "bezel_inner": "#22292f",
        "face": "#182026", "ring": "#232e38", "ticks": "#e2e8f0", "minor_ticks": "#64748b",
        "num_color": "#f8fafc", "hour": "#e2e8f0", "minute": "#cbd5e1", "lume": "#4ade80",
        "second": "#f97316", "bar": "#151c21", "sub": "#94a3b8",
        "font": "Segoe UI", "default_num": "English (0-9)", "style_type": "pilot"
    },
    "Royal Chronograph": {
        "bg": "#0b0c10", "bezel": "#d4af37", "bezel_inner": "#8a6d1c",
        "face": "#12131a", "ring": "#262936", "ticks": "#d4af37", "minor_ticks": "#6e5a28",
        "num_color": "#f3e5ab", "hour": "#d4af37", "minute": "#f3e5ab", "lume": "#ffffff",
        "second": "#e63946", "bar": "#161821", "sub": "#d4af37",
        "font": "Times New Roman", "default_num": "Roman (I-XII)", "style_type": "luxury"
    },
    "Devanagari Heritage": {
        "bg": "#1c1410", "bezel": "#cd7f32", "bezel_inner": "#8b4513",
        "face": "#f7efe1", "ring": "#e6d7be", "ticks": "#4a2e1b", "minor_ticks": "#8c6d53",
        "num_color": "#2c1810", "hour": "#3d2314", "minute": "#4a2e1b", "lume": "#cd7f32",
        "second": "#b22222", "bar": "#2c1d16", "sub": "#d2b48c",
        "font": "Nirmala UI", "default_num": "Hindi (०-९)", "style_type": "heritage"
    },
    "Cyber HUD": {
        "bg": "#05050a", "bezel": "#00f0ff", "bezel_inner": "#7000ff",
        "face": "#090a14", "ring": "#12152b", "ticks": "#00f0ff", "minor_ticks": "#3b82f6",
        "num_color": "#00f0ff", "hour": "#ff0055", "minute": "#00f0ff", "lume": "#ffffff",
        "second": "#fcee09", "bar": "#0d0f1f", "sub": "#00f0ff",
        "font": "Consolas", "default_num": "English (0-9)", "style_type": "cyber"
    },
    "Emerald Diver": {
        "bg": "#041a14", "bezel": "#c5a059", "bezel_inner": "#0b3b2d",
        "face": "#072b20", "ring": "#0c3d2e", "ticks": "#e8d8b9", "minor_ticks": "#4f8a76",
        "num_color": "#f5e6c8", "hour": "#d4af37", "minute": "#e8d8b9", "lume": "#a7f3d0",
        "second": "#fbbf24", "bar": "#06241b", "sub": "#a7f3d0",
        "font": "Georgia", "default_num": "Roman (I-XII)", "style_type": "diver"
    },
    "Bauhaus Minimal": {
        "bg": "#e2e8f0", "bezel": "#94a3b8", "bezel_inner": "#cbd5e1",
        "face": "#f8fafc", "ring": "#cbd5e1", "ticks": "#1e293b", "minor_ticks": "#94a3b8",
        "num_color": "#0f172a", "hour": "#0f172a", "minute": "#334155", "lume": "#38bdf8",
        "second": "#ef4444", "bar": "#cbd5e1", "sub": "#334155",
        "font": "Segoe UI", "default_num": "English (0-9)", "style_type": "bauhaus"
    }
}


def to_roman(n):
    n = int(n)
    if n == 0:
        return "0"
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syb = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    roman_num = ""
    i = 0
    while n > 0:
        for _ in range(n // val[i]):
            roman_num += syb[i]
            n -= val[i]
        i += 1
    return roman_num


def current_timestamp():
    return datetime.datetime.now().strftime("%a, %d %b %Y • %I:%M:%S %p")


class FloatingWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("Floating Clock")
        self.root.overrideredirect(True)

        self.sound_engine = SoundEngine()

        self.config = {
            "clock_type": "Analog",
            "digital_theme": "Flip-Clock Studio",
            "analog_style": "Aviator Pilot",
            "numerals": "English (0-9)",
            "format": "12H",
            "show_day": True,
            "show_date": True,
            "show_month": True,
            "show_year": True,
            "show_subdial": True,
            "auto_hide_frame": True,
            "timer_tone": "1. Zen Tibetan Bowl",
            "timer_loop_alert": True,
            "batt_high_enabled": True,
            "batt_high_limit": 100,
            "batt_high_tone": "5. Victory Fanfare",
            "batt_low_enabled": True,
            "batt_low_limit": 15,
            "batt_low_tone": "15. Urgent Radar Klaxon",
            "batt_loop_alert": True,
            "digital_vis": "1. Spectrum Equalizer Bars (EQ)",
            "analog_vis": "1. Fire Particle Ring 🔥",
            "enable_visualizer": False,
            "always_simulate_audio": False,
            "alpha": 0.96,
            "geometry": "250x270+200+200"
        }
        self.load_config()
        self.load_notes()

        # Timer State
        self.timer_running = False
        self.timer_paused = False
        self.timer_total_sec = 0.0
        self.timer_rem_sec = 0.0
        self.timer_end_ts = 0.0
        self.timer_alerting = False
        self.timer_label_text = "Timer"

        # Battery Guardian State
        self.battery_pct = 100
        self.battery_plugged = False
        self.last_batt_check = 0
        self.batt_alert_mode = None  # None, "HIGH", or "LOW"
        self.batt_high_notified = False
        self.batt_low_notified = False

        self.root.geometry(self.config["geometry"])
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", self.config["alpha"])
        try:
            self.root.attributes("-transparentcolor", TRANSPARENT_KEY)
        except Exception:
            pass

        self.is_always_on_top = True
        self.is_hovered = True
        self._offset_x = 0
        self._offset_y = 0
        self.settings_window = None
        self.notes_window = None
        self.timer_window = None
        self.battery_window = None

        # Visualizer States
        self.vis_bars = [0.0 for _ in range(16)]
        self.fireflies = [{"x": random.random(), "y": random.random(), "vx": (random.random() - 0.5) * 0.02, "vy": -random.random() * 0.03} for _ in range(10)]
        self.fire_particles = [{"x": random.random(), "y": random.random(), "vx": (random.random() - 0.5) * 0.015, "vy": -0.02 - random.random() * 0.03, "size": random.randint(2, 5)} for _ in range(15)]
        self.water_phase = 0.0

        # --- UI Setup ---
        self.main_frame = tk.Frame(self.root, highlightthickness=1)
        self.main_frame.pack(expand=True, fill="both")

        self.canvas = tk.Canvas(self.main_frame, highlightthickness=0)
        self.canvas.pack(expand=True, fill="both")
        self.canvas.bind("<Button-1>", self.click_window)
        self.canvas.bind("<B1-Motion>", self.drag_window)

        # Floating Top Bar
        self.title_bar = tk.Frame(self.main_frame, height=24)
        self.title_bar.bind("<Button-1>", self.click_window)
        self.title_bar.bind("<B1-Motion>", self.drag_window)

        self.pin_btn = tk.Button(self.title_bar, text="📌", bd=0, font=("Segoe UI", 9), command=self.toggle_topmost)
        self.pin_btn.pack(side="left", padx=3)

        self.close_btn = tk.Button(self.title_bar, text="✕", bd=0, font=("Segoe UI", 9, "bold"), command=self.close_app)
        self.close_btn.pack(side="right", padx=3)

        self.settings_btn = tk.Button(self.title_bar, text="⚙", bd=0, font=("Segoe UI", 10), command=self.open_settings)
        self.settings_btn.pack(side="right", padx=2)

        self.batt_btn = tk.Button(self.title_bar, text="🔋", bd=0, font=("Segoe UI", 9), command=self.open_battery_studio)
        self.batt_btn.pack(side="right", padx=2)

        self.notes_btn = tk.Button(self.title_bar, text="📝", bd=0, font=("Segoe UI", 9), command=self.open_notes)
        self.notes_btn.pack(side="right", padx=2)

        self.timer_btn = tk.Button(self.title_bar, text="⏱", bd=0, font=("Segoe UI", 9), command=self.open_timer)
        self.timer_btn.pack(side="right", padx=2)

        self.sizegrip = tk.Label(self.main_frame, text="◢", font=("Segoe UI", 10), cursor="size_nw_se")
        self.sizegrip.bind("<B1-Motion>", self.resize_window)

        self.show_controls()
        self.apply_theme()
        self.update_widget()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    for key in self.config.keys():
                        if key in saved:
                            self.config[key] = saved[key]
                if self.config["digital_theme"] not in DIGITAL_STYLES:
                    self.config["digital_theme"] = "Flip-Clock Studio"
                if self.config["analog_style"] not in ANALOG_STYLES:
                    self.config["analog_style"] = "Aviator Pilot"
                if self.config["numerals"] not in ANALOG_NUMERAL_SETS:
                    self.config["numerals"] = "English (0-9)"
                if self.config["timer_tone"] not in TONE_LIBRARY:
                    self.config["timer_tone"] = "1. Zen Tibetan Bowl"
                if self.config["batt_high_tone"] not in TONE_LIBRARY:
                    self.config["batt_high_tone"] = "5. Victory Fanfare"
                if self.config["batt_low_tone"] not in TONE_LIBRARY:
                    self.config["batt_low_tone"] = "15. Urgent Radar Klaxon"
                if self.config["digital_vis"] not in DIGITAL_VIS_TYPES:
                    self.config["digital_vis"] = DIGITAL_VIS_TYPES[0]
                if self.config["analog_vis"] not in ANALOG_VIS_TYPES:
                    self.config["analog_vis"] = ANALOG_VIS_TYPES[0]
            except Exception:
                pass

    def save_config(self):
        self.config["geometry"] = self.root.geometry()
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False)
        except Exception:
            pass

    def load_notes(self):
        self.notes_data = {
            "active_tab": 0,
            "tabs": [
                {
                    "title": "Quick Note 1",
                    "timestamp": current_timestamp(),
                    "content": "Write your sticky notes here...\nEverything auto-saves instantly!"
                }
            ]
        }
        if os.path.exists(NOTES_FILE):
            try:
                with open(NOTES_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    if "tabs" in saved and len(saved["tabs"]) > 0:
                        self.notes_data = saved
            except Exception:
                pass

    def save_notes(self):
        try:
            with open(NOTES_FILE, "w", encoding="utf-8") as f:
                json.dump(self.notes_data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def is_round_mode(self):
        if not self.config["auto_hide_frame"]:
            return False
        if self.config["clock_type"] == "Analog":
            return True
        return DIGITAL_STYLES[self.config["digital_theme"]]["style"] == "ring"

    def show_controls(self):
        self.title_bar.place(relx=0.0, rely=0.0, relwidth=1.0, height=24)
        self.sizegrip.place(relx=1.0, rely=1.0, anchor="se")

    def hide_controls(self):
        self.title_bar.place_forget()
        self.sizegrip.place_forget()

    def check_hover_state(self):
        px, py = self.root.winfo_pointerx(), self.root.winfo_pointery()
        rx, ry = self.root.winfo_rootx(), self.root.winfo_rooty()
        rw, rh = self.root.winfo_width(), self.root.winfo_height()

        inside = (rx <= px <= rx + rw) and (ry <= py <= ry + rh)
        if inside != self.is_hovered:
            self.is_hovered = inside
            if self.is_hovered or not self.is_round_mode():
                self.show_controls()
            else:
                self.hide_controls()
            self.apply_theme()

    def apply_theme(self):
        is_digital = self.config["clock_type"] == "Digital"
        colors = DIGITAL_STYLES[self.config["digital_theme"]] if is_digital else ANALOG_STYLES[self.config["analog_style"]]

        bg_col = TRANSPARENT_KEY if (self.is_round_mode() and not self.is_hovered) else colors["bg"]
        border_w = 0 if (self.is_round_mode() and not self.is_hovered) else 1

        self.root.configure(bg=bg_col)
        self.main_frame.configure(bg=bg_col, highlightbackground=colors["bar"], highlightthickness=border_w)
        self.canvas.configure(bg=bg_col)
        self.title_bar.configure(bg=colors["bar"])
        self.sizegrip.configure(bg=bg_col, fg=colors["sub"])

        btn_bg = colors["bar"]
        btn_fg = colors.get("fg", colors.get("num_color", "#ffffff"))
        close_fg = colors.get("accent2", colors.get("second", "#ff5555"))

        for btn, fg in [(self.pin_btn, btn_fg if self.is_always_on_top else "#6c7086"),
                        (self.timer_btn, "#38bdf8"),
                        (self.notes_btn, "#fbbf24"),
                        (self.batt_btn, "#a6e3a1"),
                        (self.settings_btn, btn_fg),
                        (self.close_btn, close_fg)]:
            btn.configure(bg=btn_bg, fg=fg, activebackground=btn_bg, activeforeground=fg)

    # ======================== SMART BATTERY GUARDIAN ENGINE ========================
    def evaluate_battery_limits(self):
        high_lim = int(self.config.get("batt_high_limit", 100))
        low_lim = int(self.config.get("batt_low_limit", 15))

        # Reset notifications when charger state changes or percentage moves away
        if not self.battery_plugged or self.battery_pct < high_lim:
            self.batt_high_notified = False
            if self.batt_alert_mode == "HIGH":
                self.stop_battery_alert()

        if self.battery_plugged or self.battery_pct > low_lim:
            self.batt_low_notified = False
            if self.batt_alert_mode == "LOW":
                self.stop_battery_alert()

        # Check Upper Limit (while charging/plugged in)
        if self.config.get("batt_high_enabled", True) and self.battery_plugged:
            if self.battery_pct >= high_lim and not self.batt_high_notified:
                self.batt_high_notified = True
                self.batt_alert_mode = "HIGH"
                self.sound_engine.play(self.config["batt_high_tone"], loop=self.config["batt_loop_alert"])
                self.refresh_battery_window_ui()

        # Check Lower Limit (while on battery power)
        if self.config.get("batt_low_enabled", True) and not self.battery_plugged:
            if self.battery_pct <= low_lim and not self.batt_low_notified:
                self.batt_low_notified = True
                self.batt_alert_mode = "LOW"
                self.sound_engine.play(self.config["batt_low_tone"], loop=self.config["batt_loop_alert"])
                self.refresh_battery_window_ui()

    def stop_battery_alert(self):
        self.sound_engine.stop()
        self.batt_alert_mode = None
        self.refresh_battery_window_ui()

    def open_battery_studio(self):
        if self.battery_window and self.battery_window.winfo_exists():
            self.battery_window.lift()
            return

        self.battery_window = tk.Toplevel(self.root)
        self.battery_window.title("Battery Guardian Studio")
        self.battery_window.geometry("345x435+{}+{}".format(self.root.winfo_rootx() + 25, self.root.winfo_rooty() + 25))
        self.battery_window.attributes("-topmost", True)
        self.battery_window.configure(bg="#181825")

        # Live Battery Status Card
        status_card = tk.Frame(self.battery_window, bg="#1e1e2e", pady=8, padx=10, highlightbackground="#313244", highlightthickness=1)
        status_card.pack(fill="x", padx=10, pady=(10, 6))

        self.batt_studio_title = tk.Label(status_card, text="LIVE BATTERY TELEMETRY", bg="#1e1e2e", fg="#94a3b8", font=("Segoe UI", 8, "bold"))
        self.batt_studio_title.pack()

        self.batt_studio_big = tk.Label(status_card, text="--%", bg="#1e1e2e", fg="#a6e3a1", font=("Consolas", 22, "bold"))
        self.batt_studio_big.pack()

        self.batt_dismiss_btn = tk.Button(
            status_card, text="🔔 Dismiss Active Battery Alert", bg="#f43f5e", fg="white",
            bd=0, font=("Segoe UI", 8, "bold"), padx=10, pady=4, command=self.stop_battery_alert
        )

        # --- UPPER LIMIT SECTION ---
        high_card = tk.Frame(self.battery_window, bg="#1e1e2e", padx=10, pady=8, highlightbackground="#313244", highlightthickness=1)
        high_card.pack(fill="x", padx=10, pady=4)

        high_top = tk.Frame(high_card, bg="#1e1e2e")
        high_top.pack(fill="x")

        high_en_var = tk.BooleanVar(value=self.config["batt_high_enabled"])
        tk.Checkbutton(
            high_top, text="⚡ Upper Limit Alert (Charged):", variable=high_en_var,
            bg="#1e1e2e", fg="#a6e3a1", selectcolor="#262637", activebackground="#1e1e2e",
            font=("Segoe UI", 9, "bold"),
            command=lambda: self.update_setting("batt_high_enabled", high_en_var.get())
        ).pack(side="left")

        self.spin_high = tk.Spinbox(
            high_top, from_=50, to=100, width=4, bg="#262637", fg="white", bd=0,
            font=("Consolas", 11, "bold"), justify="center"
        )
        self.spin_high.delete(0, "end")
        self.spin_high.insert(0, str(self.config["batt_high_limit"]))
        self.spin_high.pack(side="right", padx=2)
        tk.Label(high_top, text="%", bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 9, "bold")).pack(side="right")

        high_tone_row = tk.Frame(high_card, bg="#1e1e2e")
        high_tone_row.pack(fill="x", pady=(6, 0))

        self.high_tone_var = tk.StringVar(value=self.config["batt_high_tone"])
        high_menu = ttk.Combobox(high_tone_row, textvariable=self.high_tone_var, values=list(TONE_LIBRARY.keys()), state="readonly", width=23)
        high_menu.pack(side="left", fill="x", expand=True, padx=(0, 4))
        high_menu.bind("<<ComboboxSelected>>", lambda e: self.update_setting("batt_high_tone", self.high_tone_var.get()))

        tk.Button(high_tone_row, text="🔊 Test", bg="#a6e3a1", fg="#11111b", bd=0, font=("Segoe UI", 8, "bold"), padx=7, pady=2, command=lambda: self.sound_engine.play(self.high_tone_var.get(), loop=False)).pack(side="left", padx=2)
        tk.Button(high_tone_row, text="🔇", bg="#45475a", fg="white", bd=0, font=("Segoe UI", 8), padx=5, pady=2, command=self.sound_engine.stop).pack(side="left")

        # --- LOWER LIMIT SECTION ---
        low_card = tk.Frame(self.battery_window, bg="#1e1e2e", padx=10, pady=8, highlightbackground="#313244", highlightthickness=1)
        low_card.pack(fill="x", padx=10, pady=4)

        low_top = tk.Frame(low_card, bg="#1e1e2e")
        low_top.pack(fill="x")

        low_en_var = tk.BooleanVar(value=self.config["batt_low_enabled"])
        tk.Checkbutton(
            low_top, text="🪫 Lower Limit Alert (Low Batt):", variable=low_en_var,
            bg="#1e1e2e", fg="#f43f5e", selectcolor="#262637", activebackground="#1e1e2e",
            font=("Segoe UI", 9, "bold"),
            command=lambda: self.update_setting("batt_low_enabled", low_en_var.get())
        ).pack(side="left")

        self.spin_low = tk.Spinbox(
            low_top, from_=5, to=50, width=4, bg="#262637", fg="white", bd=0,
            font=("Consolas", 11, "bold"), justify="center"
        )
        self.spin_low.delete(0, "end")
        self.spin_low.insert(0, str(self.config["batt_low_limit"]))
        self.spin_low.pack(side="right", padx=2)
        tk.Label(low_top, text="%", bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 9, "bold")).pack(side="right")

        low_tone_row = tk.Frame(low_card, bg="#1e1e2e")
        low_tone_row.pack(fill="x", pady=(6, 0))

        self.low_tone_var = tk.StringVar(value=self.config["batt_low_tone"])
        low_menu = ttk.Combobox(low_tone_row, textvariable=self.low_tone_var, values=list(TONE_LIBRARY.keys()), state="readonly", width=23)
        low_menu.pack(side="left", fill="x", expand=True, padx=(0, 4))
        low_menu.bind("<<ComboboxSelected>>", lambda e: self.update_setting("batt_low_tone", self.low_tone_var.get()))

        tk.Button(low_tone_row, text="🔊 Test", bg="#f43f5e", fg="white", bd=0, font=("Segoe UI", 8, "bold"), padx=7, pady=2, command=lambda: self.sound_engine.play(self.low_tone_var.get(), loop=False)).pack(side="left", padx=2)
        tk.Button(low_tone_row, text="🔇", bg="#45475a", fg="white", bd=0, font=("Segoe UI", 8), padx=5, pady=2, command=self.sound_engine.stop).pack(side="left")

        def save_limits(*args):
            try:
                h_val = max(50, min(100, int(self.spin_high.get() or 100)))
                l_val = max(5, min(50, int(self.spin_low.get() or 15)))
                self.config["batt_high_limit"] = h_val
                self.config["batt_low_limit"] = l_val
                self.batt_high_notified = False
                self.batt_low_notified = False
                self.save_config()
                self.evaluate_battery_limits()
            except Exception:
                pass

        self.spin_high.config(command=save_limits)
        self.spin_low.config(command=save_limits)
        self.spin_high.bind("<KeyRelease>", save_limits)
        self.spin_low.bind("<KeyRelease>", save_limits)

        # Loop Alert Checkbox & Save Button
        bot_row = tk.Frame(self.battery_window, bg="#181825")
        bot_row.pack(fill="x", padx=10, pady=6)

        loop_b_var = tk.BooleanVar(value=self.config["batt_loop_alert"])
        tk.Checkbutton(
            bot_row, text="Loop alert tone until dismissed", variable=loop_b_var,
            bg="#181825", fg="#cdd6f4", selectcolor="#262637", activebackground="#181825",
            command=lambda: self.update_setting("batt_loop_alert", loop_b_var.get())
        ).pack(side="left")

        tk.Button(
            bot_row, text="✓ Apply Limits", bg="#89b4fa", fg="#11111b", bd=0,
            font=("Segoe UI", 8, "bold"), padx=8, pady=3, command=save_limits
        ).pack(side="right")

        self.refresh_battery_window_ui()

    def refresh_battery_window_ui(self):
        if not (self.battery_window and self.battery_window.winfo_exists()):
            return
        state_str = "⚡ Charging" if self.battery_plugged else "🔋 On Battery"
        self.batt_studio_big.config(text=f"{self.battery_pct}% ({state_str})")

        if self.batt_alert_mode == "HIGH":
            self.batt_studio_title.config(text=f"⚡ TARGET REACHED ({self.config['batt_high_limit']}%) - UNPLUG CHARGER!", fg="#a6e3a1")
            self.batt_dismiss_btn.pack(pady=(4, 0))
        elif self.batt_alert_mode == "LOW":
            self.batt_studio_title.config(text=f"🪫 LOW BATTERY ({self.battery_pct}%) - PLUG IN CHARGER!", fg="#f43f5e")
            self.batt_dismiss_btn.pack(pady=(4, 0))
        else:
            self.batt_studio_title.config(text=f"GUARDIAN ACTIVE • HIGH: {self.config['batt_high_limit']}% | LOW: {self.config['batt_low_limit']}%", fg="#94a3b8")
            self.batt_dismiss_btn.pack_forget()

    # ======================== MUSIC VISUALIZER ENGINE ========================
    def check_active_audio(self):
        if self.config["always_simulate_audio"]:
            return True
        try:
            audio_apps = ["spotify.exe", "chrome.exe", "msedge.exe", "vlc.exe", "discord.exe", "firefox.exe", "wmplayer.exe"]
            for proc in psutil.process_iter(attrs=['name']):
                name = proc.info.get('name', '').lower()
                if any(app in name for app in audio_apps):
                    return True
        except Exception:
            pass
        return False

    def draw_music_visualizer(self, cx, cy, r_scale, accent_color):
        if not self.config["enable_visualizer"]:
            return

        is_digital = self.config["clock_type"] == "Digital"
        vis_type = self.config["digital_vis"] if is_digital else self.config["analog_vis"]

        audio_active = self.check_active_audio()
        target_multiplier = 1.0 if audio_active else 0.0

        for i in range(len(self.vis_bars)):
            target = random.random() * target_multiplier
            self.vis_bars[i] += (target - self.vis_bars[i]) * 0.40

        if is_digital:
            if "Spectrum Equalizer" in vis_type:
                num_bars = 12
                bar_w = max(2, r_scale * 0.055)
                spacing = bar_w * 1.4
                total_w = num_bars * spacing
                start_x = cx - total_w / 2
                base_y = cy + r_scale * 0.72

                for i in range(num_bars):
                    h_val = self.vis_bars[i] * (r_scale * 0.38)
                    bx = start_x + (i * spacing)
                    self.canvas.create_rectangle(bx, base_y - h_val, bx + bar_w, base_y, fill=accent_color, outline="")

            elif "Oscilloscope" in vis_type:
                wave_y = cy + r_scale * 0.64
                points = []
                num_pts = 24
                step = (r_scale * 1.3) / num_pts
                start_x = cx - (r_scale * 0.65)

                for i in range(num_pts):
                    px = start_x + (i * step)
                    py = wave_y + math.sin(i * 0.6 + time.time() * 12) * (self.vis_bars[i % len(self.vis_bars)] * r_scale * 0.18)
                    points.append((px, py))

                flat_pts = [coord for pt in points for coord in pt]
                if len(flat_pts) >= 4:
                    self.canvas.create_line(flat_pts, fill=accent_color, width=max(2, int(r_scale * 0.03)), smooth=True)

            elif "Fireflies" in vis_type:
                for f in self.fireflies:
                    f["x"] += f["vx"] * (1.5 if audio_active else 0.3)
                    f["y"] += f["vy"] * (1.5 if audio_active else 0.3)
                    if f["y"] < 0 or f["x"] < 0 or f["x"] > 1:
                        f["x"] = random.random()
                        f["y"] = 1.0
                        f["vy"] = -random.random() * 0.03

                    fx = cx + (f["x"] - 0.5) * (r_scale * 1.6)
                    fy = cy + (f["y"] - 0.5) * (r_scale * 1.6)
                    sz = max(2, r_scale * 0.035)
                    self.canvas.create_oval(fx - sz, fy - sz, fx + sz, fy + sz, fill=accent_color, outline="")

            elif "Matrix Digital Rain" in vis_type:
                chars = ["0", "1", "२", "Ω", "⚡", "Δ", "Ψ", "7"]
                for i in range(8):
                    rx = cx + (i - 4) * (r_scale * 0.28)
                    ry = cy + ((time.time() * 60 + i * 25) % (r_scale * 1.4)) - (r_scale * 0.7)
                    ch = random.choice(chars)
                    self.canvas.create_text(rx, ry, text=ch, fill=accent_color, font=("Consolas", max(8, int(r_scale * 0.12)), "bold"))
        else:
            if "Fire Particle Ring" in vis_type:
                for p in self.fire_particles:
                    p["x"] += p["vx"]
                    p["y"] += p["vy"] * (2.0 if audio_active else 0.5)
                    if p["y"] < 0:
                        p["y"] = 1.0
                        p["x"] = random.random()

                    px = cx + (p["x"] - 0.5) * (r_scale * 1.4)
                    py = cy + r_scale * 0.7 - (p["y"] * r_scale * 1.2)
                    sz = p["size"] * (1.5 if audio_active else 0.8)
                    col = "#f43f5e" if random.random() > 0.4 else "#fbbf24"
                    self.canvas.create_oval(px - sz, py - sz, px + sz, py + sz, fill=col, outline="")

            elif "Fluid Water Waves" in vis_type:
                self.water_phase += 0.12 if audio_active else 0.03
                wave_y = cy + r_scale * 0.50
                points = []
                for i in range(20):
                    px = cx - r_scale * 0.8 + (i * (r_scale * 1.6) / 19)
                    py = wave_y + math.sin(i * 0.4 + self.water_phase) * (r_scale * 0.12 * (sum(self.vis_bars) / len(self.vis_bars) if audio_active else 0.2))
                    points.append((px, py))
                flat_pts = [coord for pt in points for coord in pt]
                if len(flat_pts) >= 4:
                    self.canvas.create_line(flat_pts, fill="#38bdf8", width=max(2, int(r_scale * 0.035)), smooth=True)

            elif "Circular Audio Starburst" in vis_type:
                num_spokes = 16
                inner_r = r_scale * 0.82
                max_len = r_scale * 0.28 * (1.0 if audio_active else 0.15)

                for i in range(num_spokes):
                    ang = math.radians(i * (360 / num_spokes))
                    length = inner_r + (self.vis_bars[i % len(self.vis_bars)] * max_len)
                    x1 = cx + inner_r * math.cos(ang)
                    y1 = cy + inner_r * math.sin(ang)
                    x2 = cx + length * math.cos(ang)
                    y2 = cy + length * math.sin(ang)
                    self.canvas.create_line(x1, y1, x2, y2, fill=accent_color, width=max(1, int(r_scale * 0.025)), capstyle=tk.ROUND)

            elif "Pulsing Vinyl Groove Ring" in vis_type:
                avg_val = (sum(self.vis_bars) / len(self.vis_bars)) if audio_active else 0.05
                pulse_r = r_scale * 0.88 + (avg_val * r_scale * 0.08)
                self.canvas.create_oval(cx - pulse_r, cy - pulse_r, cx + pulse_r, cy + pulse_r, outline=accent_color, width=max(1, int(r_scale * 0.02)), dash=(4, 4))

    # ======================== TIMER STUDIO ========================
    def start_preset_timer(self, seconds, label="Timer"):
        self.sound_engine.stop()
        self.timer_alerting = False
        self.timer_total_sec = float(seconds)
        self.timer_rem_sec = float(seconds)
        self.timer_end_ts = time.time() + self.timer_rem_sec
        self.timer_running = True
        self.timer_paused = False
        self.timer_label_text = label
        self.refresh_timer_window_ui()

    def start_custom_timer(self):
        try:
            h = int(self.spin_h.get() or 0)
            m = int(self.spin_m.get() or 0)
            s = int(self.spin_s.get() or 0)
            total = h * 3600 + m * 60 + s
            if total > 0:
                self.start_preset_timer(total, label="Custom")
        except Exception:
            pass

    def add_timer_seconds(self, extra_sec):
        if self.timer_alerting:
            self.stop_timer_alert()
        if not self.timer_running and not self.timer_paused:
            self.start_preset_timer(extra_sec, label="Quick +")
            return
        self.timer_total_sec += extra_sec
        self.timer_rem_sec += extra_sec
        if self.timer_running:
            self.timer_end_ts += extra_sec
        self.refresh_timer_window_ui()

    def toggle_pause_timer(self):
        if self.timer_alerting:
            self.stop_timer_alert()
            return
        if self.timer_running:
            self.timer_rem_sec = max(0.0, self.timer_end_ts - time.time())
            self.timer_running = False
            self.timer_paused = True
        elif self.timer_paused and self.timer_rem_sec > 0:
            self.timer_end_ts = time.time() + self.timer_rem_sec
            self.timer_running = True
            self.timer_paused = False
        self.refresh_timer_window_ui()

    def reset_timer(self):
        self.sound_engine.stop()
        self.timer_running = False
        self.timer_paused = False
        self.timer_alerting = False
        self.timer_rem_sec = 0.0
        self.timer_total_sec = 0.0
        self.refresh_timer_window_ui()

    def stop_timer_alert(self):
        self.sound_engine.stop()
        self.timer_alerting = False
        self.refresh_timer_window_ui()

    def format_timer_hms(self, sec_val):
        s = max(0, int(math.ceil(sec_val)))
        hrs = s // 3600
        mins = (s % 3600) // 60
        secs = s % 60
        if hrs > 0:
            return f"{self.format_num(hrs, 2)}:{self.format_num(mins, 2)}:{self.format_num(secs, 2)}"
        return f"{self.format_num(mins, 2)}:{self.format_num(secs, 2)}"

    def tick_timer(self):
        if self.timer_running:
            rem = self.timer_end_ts - time.time()
            if rem <= 0:
                self.timer_rem_sec = 0.0
                self.timer_running = False
                self.timer_paused = False
                self.timer_alerting = True
                self.sound_engine.play(self.config["timer_tone"], loop=self.config["timer_loop_alert"])
            else:
                self.timer_rem_sec = rem
        self.refresh_timer_window_ui()

    def open_timer(self):
        if self.timer_window and self.timer_window.winfo_exists():
            self.timer_window.lift()
            return

        self.timer_window = tk.Toplevel(self.root)
        self.timer_window.title("Timer & Chime Studio")
        self.timer_window.geometry("335x430+{}+{}".format(self.root.winfo_rootx() + 25, self.root.winfo_rooty() + 25))
        self.timer_window.attributes("-topmost", True)
        self.timer_window.configure(bg="#181825")

        disp_card = tk.Frame(self.timer_window, bg="#1e1e2e", pady=8, padx=10, highlightbackground="#313244", highlightthickness=1)
        disp_card.pack(side="top", fill="x", padx=10, pady=(10, 6))

        self.timer_status_lbl = tk.Label(disp_card, text="READY", bg="#1e1e2e", fg="#94a3b8", font=("Segoe UI", 8, "bold"))
        self.timer_status_lbl.pack()

        self.timer_big_lbl = tk.Label(disp_card, text="00:00", bg="#1e1e2e", fg="#38bdf8", font=("Consolas", 26, "bold"))
        self.timer_big_lbl.pack()

        ctrl_row = tk.Frame(self.timer_window, bg="#181825")
        ctrl_row.pack(fill="x", padx=10, pady=2)

        self.pause_btn = tk.Button(ctrl_row, text="⏸ Pause", bg="#f59e0b", fg="#11111b", bd=0, font=("Segoe UI", 8, "bold"), padx=8, pady=4, command=self.toggle_pause_timer)
        self.pause_btn.pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(ctrl_row, text="+1 Min", bg="#313244", fg="#cdd6f4", bd=0, font=("Segoe UI", 8, "bold"), padx=6, pady=4, command=lambda: self.add_timer_seconds(60)).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(ctrl_row, text="+5 Min", bg="#313244", fg="#cdd6f4", bd=0, font=("Segoe UI", 8, "bold"), padx=6, pady=4, command=lambda: self.add_timer_seconds(300)).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(ctrl_row, text="⏹ Reset", bg="#f38ba8", fg="#11111b", bd=0, font=("Segoe UI", 8, "bold"), padx=8, pady=4, command=self.reset_timer).pack(side="left", expand=True, fill="x", padx=2)

        tk.Label(self.timer_window, text="Instant Preset Timers:", bg="#181825", fg="#a6adc8", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=12, pady=(8, 3))
        presets_frame = tk.Frame(self.timer_window, bg="#181825")
        presets_frame.pack(fill="x", padx=10)

        presets = [("2 Min", 120), ("5 Min", 300), ("10 Min", 600), ("15 Min", 900), ("25 Min", 1500), ("30 Min", 1800), ("45 Min", 2700), ("1 Hour", 3600), ("2 Hours", 7200)]
        for idx, (lbl, secs) in enumerate(presets):
            r, c = divmod(idx, 3)
            tk.Button(
                presets_frame, text=lbl, bg="#262637", fg="#89b4fa", activebackground="#38bdf8",
                activeforeground="#11111b", bd=0, font=("Segoe UI", 8, "bold"), pady=5,
                command=lambda s=secs, l=lbl: self.start_preset_timer(s, l)
            ).grid(row=r, column=c, sticky="ew", padx=2, pady=2)
        for c in range(3):
            presets_frame.columnconfigure(c, weight=1)

        tk.Label(self.timer_window, text="Custom Duration (Hrs : Mins : Secs):", bg="#181825", fg="#a6adc8", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=12, pady=(8, 3))
        cust_frame = tk.Frame(self.timer_window, bg="#181825")
        cust_frame.pack(fill="x", padx=12)

        self.spin_h = tk.Spinbox(cust_frame, from_=0, to=99, width=4, bg="#262637", fg="white", bd=0, font=("Consolas", 11, "bold"), justify="center")
        self.spin_h.pack(side="left", padx=2)
        tk.Label(cust_frame, text="h", bg="#181825", fg="#6c7086").pack(side="left")

        self.spin_m = tk.Spinbox(cust_frame, from_=0, to=59, width=4, bg="#262637", fg="white", bd=0, font=("Consolas", 11, "bold"), justify="center")
        self.spin_m.delete(0, "end")
        self.spin_m.insert(0, "7")
        self.spin_m.pack(side="left", padx=2)
        tk.Label(cust_frame, text="m", bg="#181825", fg="#6c7086").pack(side="left")

        self.spin_s = tk.Spinbox(cust_frame, from_=0, to=59, width=4, bg="#262637", fg="white", bd=0, font=("Consolas", 11, "bold"), justify="center")
        self.spin_s.pack(side="left", padx=2)
        tk.Label(cust_frame, text="s", bg="#181825", fg="#6c7086").pack(side="left")

        tk.Button(cust_frame, text="▶ Start Custom", bg="#a6e3a1", fg="#11111b", bd=0, font=("Segoe UI", 8, "bold"), padx=10, pady=4, command=self.start_custom_timer).pack(side="right", padx=2)

        tk.Label(self.timer_window, text="Completion Tone / Short Music (16 Tones):", bg="#181825", fg="#a6adc8", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=12, pady=(10, 3))
        tone_row = tk.Frame(self.timer_window, bg="#181825")
        tone_row.pack(fill="x", padx=12)

        self.tone_var = tk.StringVar(value=self.config["timer_tone"])
        tone_menu = ttk.Combobox(tone_row, textvariable=self.tone_var, values=list(TONE_LIBRARY.keys()), state="readonly", width=25)
        tone_menu.pack(side="left", fill="x", expand=True, padx=(0, 4))
        tone_menu.bind("<<ComboboxSelected>>", lambda e: self.update_setting("timer_tone", self.tone_var.get()))

        tk.Button(tone_row, text="🔊 Test", bg="#89b4fa", fg="#11111b", bd=0, font=("Segoe UI", 8, "bold"), padx=8, pady=3, command=lambda: self.sound_engine.play(self.tone_var.get(), loop=False)).pack(side="left", padx=2)
        tk.Button(tone_row, text="🔇", bg="#45475a", fg="white", bd=0, font=("Segoe UI", 8), padx=5, pady=3, command=self.sound_engine.stop).pack(side="left")

        loop_var = tk.BooleanVar(value=self.config["timer_loop_alert"])
        tk.Checkbutton(self.timer_window, text="Repeat music continuously until dismissed", variable=loop_var, bg="#181825", fg="#cdd6f4", selectcolor="#262637", activebackground="#181825", activeforeground="white", command=lambda: self.update_setting("timer_loop_alert", loop_var.get())).pack(anchor="w", padx=10, pady=6)

        self.refresh_timer_window_ui()

    def refresh_timer_window_ui(self):
        if not (self.timer_window and self.timer_window.winfo_exists()):
            return
        if self.timer_alerting:
            self.timer_status_lbl.config(text="🔔 TIME'S UP! CLICK TO DISMISS", fg="#f43f5e")
            self.timer_big_lbl.config(text="00:00", fg="#f43f5e")
            self.pause_btn.config(text="🔔 Dismiss Alert", bg="#f43f5e", fg="white")
        elif self.timer_running:
            self.timer_status_lbl.config(text=f"RUNNING • {self.timer_label_text.upper()}", fg="#a6e3a1")
            self.timer_big_lbl.config(text=self.format_timer_hms(self.timer_rem_sec), fg="#a6e3a1")
            self.pause_btn.config(text="⏸ Pause", bg="#f59e0b", fg="#11111b")
        elif self.timer_paused:
            self.timer_status_lbl.config(text="PAUSED", fg="#f59e0b")
            self.timer_big_lbl.config(text=self.format_timer_hms(self.timer_rem_sec), fg="#f59e0b")
            self.pause_btn.config(text="▶ Resume", bg="#a6e3a1", fg="#11111b")
        else:
            self.timer_status_lbl.config(text="READY", fg="#94a3b8")
            self.timer_big_lbl.config(text="00:00", fg="#38bdf8")
            self.pause_btn.config(text="⏸ Pause", bg="#f59e0b", fg="#11111b")

    # ======================== STICKY NOTES ========================
    def open_notes(self):
        if self.notes_window and self.notes_window.winfo_exists():
            self.notes_window.lift()
            return

        self.notes_window = tk.Toplevel(self.root)
        self.notes_window.title("Sticky Notes")
        self.notes_window.geometry("340x320+{}+{}".format(self.root.winfo_rootx() + 30, self.root.winfo_rooty() + 30))
        self.notes_window.attributes("-topmost", True)
        self.notes_window.configure(bg="#1e1e2e")

        top_bar = tk.Frame(self.notes_window, bg="#181825", pady=4, padx=4)
        top_bar.pack(side="top", fill="x")

        self.tabs_frame = tk.Frame(top_bar, bg="#181825")
        self.tabs_frame.pack(side="left", fill="x", expand=True)

        ctrl_frame = tk.Frame(top_bar, bg="#181825")
        ctrl_frame.pack(side="right")

        tk.Button(ctrl_frame, text="+ Tab", bg="#a6e3a1", fg="#11111b", bd=0, font=("Segoe UI", 8, "bold"), padx=6, pady=2, command=self.add_note_tab).pack(side="left", padx=2)
        tk.Button(ctrl_frame, text="🗑", bg="#f38ba8", fg="#11111b", bd=0, font=("Segoe UI", 8, "bold"), padx=5, pady=2, command=self.delete_note_tab).pack(side="left", padx=2)

        header_frame = tk.Frame(self.notes_window, bg="#262637", padx=8, pady=5)
        header_frame.pack(side="top", fill="x")

        self.note_title_lbl = tk.Label(header_frame, text="", bg="#262637", fg="#f9e2af", font=("Segoe UI", 9, "bold"), anchor="w")
        self.note_title_lbl.pack(side="top", fill="x")
        self.note_time_lbl = tk.Label(header_frame, text="", bg="#262637", fg="#a6adc8", font=("Segoe UI", 8), anchor="w")
        self.note_time_lbl.pack(side="top", fill="x")

        editor_frame = tk.Frame(self.notes_window, bg="#1e1e2e")
        editor_frame.pack(expand=True, fill="both", padx=6, pady=6)

        scrollbar = tk.Scrollbar(editor_frame)
        scrollbar.pack(side="right", fill="y")

        self.note_text = tk.Text(editor_frame, bg="#1e1e2e", fg="#cdd6f4", insertbackground="#f9e2af", selectbackground="#45475a", font=("Segoe UI", 10), bd=0, wrap="word", yscrollcommand=scrollbar.set)
        self.note_text.pack(side="left", expand=True, fill="both")
        scrollbar.config(command=self.note_text.yview)
        self.note_text.bind("<KeyRelease>", self.on_note_typed)

        # --- NEW BINDINGS FOR SMART LISTS & CLIPBOARD ---
        self.note_text.bind("<Return>", self.handle_note_return)
        self.note_text.bind("<space>", self.handle_note_space)
        self.note_text.bind("<ButtonRelease-1>", self.auto_copy_selection)
        self.note_text.bind("<Button-3>", self.rmb_paste)

        tk.Label(self.notes_window, text="✓ Auto-Save | Select=Copy | RMB=Paste | Smart Lists", bg="#11111b", fg="#6c7086", font=("Segoe UI", 7), pady=3).pack(side="bottom", fill="x")
        tk.Label(self.notes_window, text="✓ Auto-Save Active  |  Double-click any tab to rename", bg="#11111b", fg="#6c7086", font=("Segoe UI", 7), pady=3).pack(side="bottom", fill="x")

        self.render_note_tabs()
        self.load_active_note_into_editor()

    def render_note_tabs(self):
        for widget in self.tabs_frame.winfo_children():
            widget.destroy()

        active_idx = self.notes_data.get("active_tab", 0)
        for idx, tab in enumerate(self.notes_data["tabs"]):
            is_active = (idx == active_idx)
            btn = tk.Button(
                self.tabs_frame, text=tab["title"], bg="#f9e2af" if is_active else "#313244",
                fg="#11111b" if is_active else "#cdd6f4", bd=0, font=("Segoe UI", 8, "bold" if is_active else "normal"),
                padx=8, pady=2, command=lambda i=idx: self.switch_note_tab(i)
            )
            btn.pack(side="left", padx=2)
            btn.bind("<Double-Button-1>", lambda e, i=idx: self.rename_note_tab(i))

    def load_active_note_into_editor(self):
        idx = self.notes_data.get("active_tab", 0)
        if idx >= len(self.notes_data["tabs"]):
            idx = 0
            self.notes_data["active_tab"] = 0
        tab = self.notes_data["tabs"][idx]
        self.note_title_lbl.config(text=f"📌 {tab['title']}")
        self.note_time_lbl.config(text=f"🕒 Last Written: {tab['timestamp']}")
        self.note_text.delete("1.0", tk.END)
        self.note_text.insert("1.0", tab["content"])

    def on_note_typed(self, event=None):
        idx = self.notes_data.get("active_tab", 0)
        content = self.note_text.get("1.0", "end-1c")
        stamp = current_timestamp()
        self.notes_data["tabs"][idx]["content"] = content
        self.notes_data["tabs"][idx]["timestamp"] = stamp
        self.note_time_lbl.config(text=f"🕒 Last Written: {stamp}")
        self.save_notes()

    def handle_note_space(self, event=None):
        """Auto-indents when typing '1.' or '-' or '*' followed by Space."""
        line_text = self.note_text.get("insert linestart", "insert")
    
        # If user types '1.' + Space -> becomes '  1. '
        if re.match(r"^\d+\.$", line_text):
            self.note_text.delete("insert linestart", "insert")
            self.note_text.insert("insert", f"  {line_text} ")
            self.on_note_typed()
            return "break"
        
        # If user types '-' or '*' + Space -> becomes '  • '
        elif line_text in ("-", "*"):
            self.note_text.delete("insert linestart", "insert")
            self.note_text.insert("insert", "  • ")
            self.on_note_typed()
            return "break"

    def handle_note_return(self, event=None):
        """Continues numbered lists or bullets on Enter; exits list if pressed on an empty item."""
        line_text = self.note_text.get("insert linestart", "insert")

        # 1. Check for Numbered List pattern (e.g., "  1. Buy milk")
        num_match = re.match(r"^(\s*)(\d+)\.\s+(.*)$", line_text)
        if num_match:
            indent, num_str, rest_of_line = num_match.groups()
            if not rest_of_line.strip():
                # Line is empty (user pressed Enter twice) -> clear bullet to exit list
                self.note_text.delete("insert linestart", "insert")
                self.on_note_typed()
                return "break"
            next_num = int(num_str) + 1
            self.note_text.insert("insert", f"\n{indent}{next_num}. ")
            self.note_text.see("insert")
            self.on_note_typed()
            return "break"

        # 2. Check for Bullet List pattern (e.g., "  • Task item")
        bul_match = re.match(r"^(\s*)([•\-\*])\s+(.*)$", line_text)
        if bul_match:
            indent, bullet, rest_of_line = bul_match.groups()
            if not rest_of_line.strip():
                # Line is empty -> clear bullet to exit list
                self.note_text.delete("insert linestart", "insert")
                self.on_note_typed()
                return "break"
            self.note_text.insert("insert", f"\n{indent}{bullet} ")
            self.note_text.see("insert")
            self.on_note_typed()
            return "break"

    def auto_copy_selection(self, event=None):
        """Automatically copies highlighted text to clipboard when mouse button is released."""
        try:
            if self.note_text.tag_ranges("sel"):
                selected_text = self.note_text.get("sel.first", "sel.last")
                if selected_text:
                    self.root.clipboard_clear()
                    self.root.clipboard_append(selected_text)
                    self.note_time_lbl.config(text="📋 Copied selection to clipboard!")
        except Exception:
            pass

    def rmb_paste(self, event):
        """Pastes clipboard contents at the mouse cursor position on Right-Click (RMB)."""
        try:
            # Move cursor to exact point where user right-clicked
            click_index = self.note_text.index(f"@{event.x},{event.y}")
            self.note_text.mark_set("insert", click_index)
            self.note_text.focus_set()

            clip_text = self.root.clipboard_get()
            if clip_text:
                if self.note_text.tag_ranges("sel"):
                    self.note_text.delete("sel.first", "sel.last")
                self.note_text.insert("insert", clip_text)
                self.on_note_typed()
        except Exception:
            pass
        return "break"

    def switch_note_tab(self, idx):
        self.notes_data["active_tab"] = idx
        self.save_notes()
        self.render_note_tabs()
        self.load_active_note_into_editor()

    def add_note_tab(self):
        new_num = len(self.notes_data["tabs"]) + 1
        self.notes_data["tabs"].append({"title": f"Note {new_num}", "timestamp": current_timestamp(), "content": ""})
        self.notes_data["active_tab"] = len(self.notes_data["tabs"]) - 1
        self.save_notes()
        self.render_note_tabs()
        self.load_active_note_into_editor()
        self.note_text.focus_set()

    def rename_note_tab(self, idx):
        old_title = self.notes_data["tabs"][idx]["title"]
        new_title = simpledialog.askstring("Rename Tab", "Enter tab name:", initialvalue=old_title, parent=self.notes_window)
        if new_title and new_title.strip():
            self.notes_data["tabs"][idx]["title"] = new_title.strip()[:18]
            self.save_notes()
            self.render_note_tabs()
            self.load_active_note_into_editor()

    def delete_note_tab(self):
        if len(self.notes_data["tabs"]) <= 1:
            self.notes_data["tabs"][0]["content"] = ""
            self.notes_data["tabs"][0]["timestamp"] = current_timestamp()
        else:
            idx = self.notes_data.get("active_tab", 0)
            self.notes_data["tabs"].pop(idx)
            self.notes_data["active_tab"] = max(0, idx - 1)
        self.save_notes()
        self.render_note_tabs()
        self.load_active_note_into_editor()

    # ======================== HELPERS ========================
    def format_num(self, val, pad=2):
        script = self.config["numerals"]
        if script == "Roman (I-XII)":
            return to_roman(val)
        s = f"{int(val):0{pad}d}" if pad > 0 else str(int(val))
        if script == "Hindi (०-९)":
            return s.translate(HINDI_DIGITS)
        return s

    def get_calendar_string(self):
        now = datetime.datetime.now()
        script = self.config["numerals"]
        parts = []

        if self.config["show_day"]:
            parts.append(HINDI_DAYS[now.weekday()] if script == "Hindi (०-९)" else ENG_DAYS[now.weekday()])

        date_parts = []
        if self.config["show_date"]:
            date_parts.append(self.format_num(now.day, pad=2 if script != "Roman (I-XII)" else 0))
        if self.config["show_month"]:
            if script == "Hindi (०-९)":
                date_parts.append(HINDI_MONTHS[now.month - 1])
            elif script == "Roman (I-XII)":
                date_parts.append(to_roman(now.month))
            else:
                date_parts.append(ENG_MONTHS[now.month - 1])
        if self.config["show_year"]:
            date_parts.append(self.format_num(now.year, pad=0))

        if date_parts:
            sep = " · " if script == "Roman (I-XII)" else " "
            parts.append(sep.join(date_parts))

        return "  |  ".join(parts)

    def has_active_overlay(self):
        return self.timer_running or self.timer_paused or self.timer_alerting or (self.batt_alert_mode is not None)

    def draw_timer_overlay_badge(self, cx, y_pos, r_scale):
        if self.timer_alerting:
            pulse = int(time.time() * 4) % 2 == 0
            bg_c = "#f43f5e" if pulse else "#fbbf24"
            tag_id = "dismiss_alert"
            self.canvas.create_rectangle(cx - max(58, r_scale * 0.65), y_pos - max(11, r_scale * 0.13), cx + max(58, r_scale * 0.65), y_pos + max(11, r_scale * 0.13), fill=bg_c, outline="#ffffff", width=1, tags=tag_id)
            self.canvas.create_text(cx, y_pos, text="🔔 TIME UP! (CLICK)", fill="#11111b", font=("Segoe UI", max(7, int(r_scale * 0.095)), "bold"), tags=tag_id)
            self.canvas.tag_bind(tag_id, "<Button-1>", lambda e: self.stop_timer_alert())
        elif self.batt_alert_mode is not None:
            pulse = int(time.time() * 4) % 2 == 0
            if self.batt_alert_mode == "HIGH":
                bg_c = "#10b981" if pulse else "#fbbf24"
                txt = f"⚡ {self.battery_pct}% FULL! (CLICK)"
            else:
                bg_c = "#f43f5e" if pulse else "#fbbf24"
                txt = f"🪫 {self.battery_pct}% LOW! (CLICK)"
            tag_id = "dismiss_batt_alert"
            bw, bh = max(62, r_scale * 0.68), max(11, r_scale * 0.13)
            self.canvas.create_rectangle(cx - bw, y_pos - bh, cx + bw, y_pos + bh, fill=bg_c, outline="#ffffff", width=1, tags=tag_id)
            self.canvas.create_text(cx, y_pos, text=txt, fill="#11111b", font=("Segoe UI", max(7, int(r_scale * 0.095)), "bold"), tags=tag_id)
            self.canvas.tag_bind(tag_id, "<Button-1>", lambda e: self.stop_battery_alert())
        elif self.timer_running or self.timer_paused:
            col = "#38bdf8" if self.timer_running else "#f59e0b"
            self.canvas.create_rectangle(cx - max(42, r_scale * 0.48), y_pos - max(9, r_scale * 0.105), cx + max(42, r_scale * 0.48), y_pos + max(9, r_scale * 0.105), fill="#0f172a", outline=col, width=1)
            self.canvas.create_text(cx, y_pos, text=f"⏱ {self.format_timer_hms(self.timer_rem_sec)}", fill=col, font=("Consolas", max(7, int(r_scale * 0.09)), "bold"))

    # ======================== DIGITAL DIAL ENGINE ========================
    def draw_digital(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.canvas.delete("all")
        if w <= 20 or h <= 20:
            return

        theme = DIGITAL_STYLES[self.config["digital_theme"]]
        style = theme["style"]
        now = datetime.datetime.now()
        sec_float = now.second + now.microsecond / 1_000_000.0

        raw_hr = now.hour
        ampm = ""
        if self.config["format"] == "12H":
            ampm = ("पूर्वाह्न" if raw_hr < 12 else "अपराह्न") if self.config["numerals"] == "Hindi (०-९)" else ("AM" if raw_hr < 12 else "PM")
            raw_hr = raw_hr % 12 or 12

        hr_str = self.format_num(raw_hr, pad=2)
        min_str = self.format_num(now.minute, pad=2)
        sec_str = self.format_num(now.second, pad=2)
        cal_str = self.get_calendar_string()

        batt_icon = "⚡" if self.battery_plugged else "🔋"
        batt_str = f"{batt_icon} {self.format_num(self.battery_pct, pad=0)}%"

        top_offset = 14 if (self.is_hovered or not self.is_round_mode()) else 0
        cx, cy = w / 2, (h + top_offset) / 2
        scale = min(w / 260.0, (h - top_offset) / 160.0)

        if style == "ring":
            r = min(w, h - top_offset) / 2 * 0.88
            self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=theme["card"], outline=theme["border"], width=max(3, int(r * 0.08)))
            sec_ext = -(sec_float / 60.0) * 360
            self.canvas.create_arc(cx - r, cy - r, cx + r, cy + r, start=90, extent=sec_ext, style=tk.ARC, outline=theme["accent"], width=max(3, int(r * 0.06)))

            self.draw_music_visualizer(cx, cy, r, theme["accent"])

            if (self.timer_running or self.timer_paused) and self.timer_total_sec > 0:
                r_tm = r * 1.05
                tm_ext = -(self.timer_rem_sec / self.timer_total_sec) * 360
                self.canvas.create_arc(cx - r_tm, cy - r_tm, cx + r_tm, cy + r_tm, start=90, extent=tm_ext, style=tk.ARC, outline="#a6e3a1", width=max(2, int(r * 0.04)))

            if self.config["show_subdial"]:
                r_in = r * 0.86
                batt_ext = -(self.battery_pct / 100.0) * 360
                self.canvas.create_oval(cx - r_in, cy - r_in, cx + r_in, cy + r_in, outline=theme["border"], width=max(1, int(r * 0.02)))
                self.canvas.create_arc(cx - r_in, cy - r_in, cx + r_in, cy + r_in, start=90, extent=batt_ext, style=tk.ARC, outline=theme["accent2"], width=max(2, int(r * 0.035)))

            if cal_str:
                self.canvas.create_text(cx, cy - r * 0.42, text=cal_str, fill=theme["sub"], font=(theme["font"], max(7, int(r * 0.10)), "bold"))

            t_font = max(12, int(r * 0.30)) if self.config["numerals"] != "Roman (I-XII)" else max(10, int(r * 0.22))
            self.canvas.create_text(cx, cy - r * 0.04, text=f"{hr_str}:{min_str}", fill=theme["fg"], font=(theme["font"], t_font, "bold"))
            self.canvas.create_text(cx, cy + r * 0.24, text=f":{sec_str}  {ampm}".strip(), fill=theme["accent"], font=(theme["font"], max(8, int(r * 0.13)), "bold"))

            if self.has_active_overlay():
                self.draw_timer_overlay_badge(cx, cy + r * 0.54, r)
            elif self.config["show_subdial"]:
                self.canvas.create_text(cx, cy + r * 0.56, text=batt_str, fill=theme["accent2"], font=(theme["font"], max(7, int(r * 0.11)), "bold"))

        elif style == "flip":
            pad_x = w * 0.06
            if cal_str:
                self.canvas.create_text(cx, 34, text=cal_str, fill=theme["sub"], font=(theme["font"], max(8, int(10 * scale)), "bold"))

            card_top, card_bot = max(46, h * 0.28), h * 0.74
            card_w = (w - pad_x * 2 - 16) / 3
            units = [(hr_str, theme["fg"]), (min_str, theme["fg"]), (sec_str, theme["accent"])]

            for idx, (val, col) in enumerate(units):
                x1 = pad_x + idx * (card_w + 8)
                x2 = x1 + card_w
                self.canvas.create_rectangle(x1, card_top, x2, card_bot, fill=theme["card"], outline=theme["border"], width=2)
                f_sz = max(12, int(min(card_w * 0.42, (card_bot - card_top) * 0.45)))
                if self.config["numerals"] == "Roman (I-XII)":
                    f_sz = int(f_sz * 0.72)
                self.canvas.create_text((x1 + x2) / 2, (card_top + card_bot) / 2, text=val, fill=col, font=(theme["font"], f_sz, "bold"))
                mid_y = (card_top + card_bot) / 2
                self.canvas.create_line(x1 + 1, mid_y, x2 - 1, mid_y, fill=theme["bg"], width=2)

            self.draw_music_visualizer(cx, h * 0.82, min(w, h) * 0.35, theme["accent"])

            if self.has_active_overlay():
                self.draw_timer_overlay_badge(cx, h * 0.87, min(w, h) * 0.45)
            else:
                footer_txt = f"{ampm}   {batt_str if self.config['show_subdial'] else ''}".strip()
                self.canvas.create_text(cx, h * 0.88, text=footer_txt, fill=theme["accent2"], font=(theme["font"], max(8, int(9 * scale)), "bold"))

        else:
            m = 10
            top_m = 28
            self.canvas.create_rectangle(m, top_m, w - m, h - m, fill=theme["card"], outline=theme["border"], width=2)

            if style == "heritage":
                self.canvas.create_rectangle(m + 5, top_m + 5, w - m - 5, h - m - 5, outline=theme["accent"], width=1)
            elif style == "hud":
                bl = 18
                for bx, by, dx, dy in [(m, top_m, 1, 1), (w - m, top_m, -1, 1), (m, h - m, 1, -1), (w - m, h - m, -1, -1)]:
                    self.canvas.create_line(bx, by, bx + dx * bl, by, fill=theme["accent"], width=3)
                    self.canvas.create_line(bx, by, bx, by + dy * bl, fill=theme["accent"], width=3)

            if cal_str:
                self.canvas.create_text(cx, top_m + (h - top_m) * 0.18, text=cal_str, fill=theme["sub"], font=(theme["font"], max(8, int(10 * scale)), "bold"))
                self.canvas.create_line(m + 15, top_m + (h - top_m) * 0.28, w - m - 15, top_m + (h - top_m) * 0.28, fill=theme["border"], width=1)

            main_t = f"{hr_str}:{min_str}:{sec_str}"
            t_sz = max(14, int(24 * scale)) if self.config["numerals"] != "Roman (I-XII)" else max(11, int(17 * scale))
            self.canvas.create_text(cx, top_m + (h - top_m) * 0.50, text=main_t, fill=theme["fg"], font=(theme["font"], t_sz, "bold"))

            self.draw_music_visualizer(cx, top_m + (h - top_m) * 0.72, min(w, h) * 0.35, theme["accent"])

            if self.has_active_overlay():
                self.draw_timer_overlay_badge(cx, top_m + (h - top_m) * 0.80, min(w, h) * 0.45)
            elif self.config["show_subdial"]:
                bar_w = (w - m * 4) * 0.55
                bx1, bx2 = cx - bar_w / 2, cx + bar_w / 2
                by = top_m + (h - top_m) * 0.74
                self.canvas.create_rectangle(bx1, by - 4, bx2, by + 4, fill=theme["bg"], outline=theme["border"])
                self.canvas.create_rectangle(bx1, by - 4, bx1 + bar_w * (self.battery_pct / 100.0), by + 4, fill=theme["accent"], outline="")
                self.canvas.create_text(cx, top_m + (h - top_m) * 0.85, text=f"{ampm}  {batt_str}".strip(), fill=theme["sub"], font=(theme["font"], max(8, int(9 * scale)), "bold"))

    # ======================== ANALOG DIAL ENGINE ========================
    def draw_polygon_hand(self, cx, cy, angle, length, tail, base_w, mid_w, fill_color, outline_color, lume_color=None):
        ux, uy = math.cos(angle), math.sin(angle)
        px, py = -uy, ux
        pts = [
            cx - ux * tail, cy - uy * tail,
            cx + px * base_w, cy + py * base_w,
            cx + ux * (length * 0.78) + px * mid_w, cy + uy * (length * 0.78) + py * mid_w,
            cx + ux * length, cy + uy * length,
            cx + ux * (length * 0.78) - px * mid_w, cy + uy * (length * 0.78) - py * mid_w,
            cx - px * base_w, cy - py * base_w
        ]
        self.canvas.create_polygon(pts, fill=fill_color, outline=outline_color, width=1)
        if lume_color and length > 25:
            self.canvas.create_line(
                cx + ux * (length * 0.18), cy + uy * (length * 0.18),
                cx + ux * (length * 0.74), cy + uy * (length * 0.74),
                fill=lume_color, width=max(1, int(mid_w * 0.7)), capstyle=tk.ROUND
            )

    def draw_analog(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.canvas.delete("all")
        if w <= 20 or h <= 20:
            return

        style = ANALOG_STYLES[self.config["analog_style"]]
        numerals = ANALOG_NUMERAL_SETS[self.config["numerals"]]
        stype = style["style_type"]

        cx, cy = w / 2, (h + 20) / 2
        r = min(w, h - 24) / 2 * 0.92

        is_flashing = (self.timer_alerting or self.batt_alert_mode is not None) and (int(time.time() * 4) % 2 == 0)
        bezel_col = ("#10b981" if self.batt_alert_mode == "HIGH" else "#f43f5e") if is_flashing else style["bezel"]
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=style["bezel_inner"], outline=bezel_col, width=max(2, int(r * 0.04)))
        face_r = r * 0.92
        self.canvas.create_oval(cx - face_r, cy - face_r, cx + face_r, cy + face_r, fill=style["face"], outline=bezel_col, width=1)

        self.draw_music_visualizer(cx, cy, face_r, style["lume"])

        if (self.timer_running or self.timer_paused) and self.timer_total_sec > 0:
            tm_ext = -(self.timer_rem_sec / self.timer_total_sec) * 360
            arc_c = "#38bdf8" if self.timer_running else "#f59e0b"
            self.canvas.create_arc(cx - face_r, cy - face_r, cx + face_r, cy + face_r, start=90, extent=tm_ext, style=tk.ARC, outline=arc_c, width=max(3, int(r * 0.045)))

        ring_r = r * 0.60
        if stype in ("luxury", "heritage", "cyber"):
            self.canvas.create_oval(cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r, outline=style["ring"], width=1, dash=(4, 2) if stype == "cyber" else None)

        track_outer = face_r * 0.96
        for i in range(60):
            ang = math.radians(i * 6 - 90)
            ca, sa = math.cos(ang), math.sin(ang)
            if i % 5 == 0:
                inner = face_r * 0.86
                self.canvas.create_line(cx + inner * ca, cy + inner * sa, cx + track_outer * ca, cy + track_outer * sa, fill=style["ticks"], width=max(2, int(r * 0.025)), capstyle=tk.ROUND)
            else:
                inner = face_r * 0.91
                self.canvas.create_line(cx + inner * ca, cy + inner * sa, cx + track_outer * ca, cy + track_outer * sa, fill=style["minor_ticks"], width=1)

        num_r = face_r * 0.72
        font_sz = max(8, int(r * 0.12))
        for i in range(12):
            ang = math.radians(i * 30 - 90)
            self.canvas.create_text(
                cx + num_r * math.cos(ang), cy + num_r * math.sin(ang),
                text=numerals[i], fill=style["num_color"], font=(style["font"], font_sz, "bold")
            )

        cal_str = self.get_calendar_string()
        if cal_str and r > 50:
            cal_y = cy - face_r * 0.33
            cal_w = min(face_r * 0.68, max(36, len(cal_str) * (r * 0.042)))
            cal_h = r * 0.095
            badge_bg = style["ring"] if stype == "heritage" else style["bg"]
            badge_fg = style["num_color"]
            self.canvas.create_rectangle(cx - cal_w, cal_y - cal_h, cx + cal_w, cal_y + cal_h, fill=badge_bg, outline=style["bezel"], width=1)
            self.canvas.create_text(cx, cal_y, text=cal_str, fill=badge_fg, font=(style["font"], max(6, int(r * 0.075)), "bold"))

        if self.has_active_overlay():
            self.draw_timer_overlay_badge(cx, cy + face_r * 0.38, r)
        elif self.config["show_subdial"] and r > 48:
            sub_cy = cy + face_r * 0.36
            sub_r = face_r * 0.21
            self.canvas.create_oval(cx - sub_r, sub_cy - sub_r, cx + sub_r, sub_cy + sub_r, fill=style["bg"], outline=style["ring"], width=1)

            extent = -(self.battery_pct / 100.0) * 260
            self.canvas.create_arc(
                cx - sub_r * 0.82, sub_cy - sub_r * 0.82, cx + sub_r * 0.82, sub_cy + sub_r * 0.82,
                start=220, extent=extent, style=tk.ARC, outline=style["lume"], width=max(2, int(r * 0.025))
            )
            b_ang = math.radians(220 - (self.battery_pct / 100.0) * 260)
            self.canvas.create_line(cx, sub_cy, cx + sub_r * 0.65 * math.cos(b_ang), sub_cy - sub_r * 0.65 * math.sin(b_ang), fill=style["second"], width=1.5)

            b_txt = f"{'⚡' if self.battery_plugged else ''}{self.format_num(self.battery_pct, pad=0)}%"
            self.canvas.create_text(cx, sub_cy + sub_r * 0.52, text=b_txt, fill=style["num_color"], font=(style["font"], max(6, int(r * 0.072)), "bold"))

        now = time.time()
        lt = time.localtime(now)
        sec = lt.tm_sec + (now % 1)
        min_val = lt.tm_min + sec / 60.0
        hr_val = (lt.tm_hour % 12) + min_val / 60.0

        h_ang = math.radians(hr_val * 30 - 90)
        m_ang = math.radians(min_val * 6 - 90)
        s_ang = math.radians(sec * 6 - 90)

        self.draw_polygon_hand(cx, cy, h_ang, face_r * 0.54, face_r * 0.10, max(3, r * 0.048), max(2, r * 0.032), style["hour"], style["bg"], style["lume"])
        self.draw_polygon_hand(cx, cy, m_ang, face_r * 0.78, face_r * 0.12, max(2.5, r * 0.036), max(1.5, r * 0.022), style["minute"], style["bg"], style["lume"])

        self.canvas.create_line(
            cx - face_r * 0.20 * math.cos(s_ang), cy - face_r * 0.20 * math.sin(s_ang),
            cx + face_r * 0.86 * math.cos(s_ang), cy + face_r * 0.86 * math.sin(s_ang),
            fill=style["second"], width=max(1, int(r * 0.015))
        )
        cap1, cap2 = max(4, r * 0.055), max(2, r * 0.025)
        self.canvas.create_oval(cx - cap1, cy - cap1, cx + cap1, cy + cap1, fill=style["bezel"], outline=style["bg"])
        self.canvas.create_oval(cx - cap2, cy - cap2, cx + cap2, cy + cap2, fill=style["second"], outline="")

    # ======================== SETTINGS WINDOW ========================
    def open_settings(self):
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return

        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Watch Studio")
        self.settings_window.geometry("290x510")
        self.settings_window.attributes("-topmost", True)
        self.settings_window.configure(bg="#1e1f22")

        tk.Label(self.settings_window, text="Watch Customizer", font=("Segoe UI", 11, "bold"), bg="#1e1f22", fg="white").pack(pady=(8, 4))

        tk.Label(self.settings_window, text="Clock Mode:", bg="#1e1f22", fg="#b5bac1", font=("Segoe UI", 9)).pack()
        type_var = tk.StringVar(value=self.config["clock_type"])
        type_menu = ttk.Combobox(self.settings_window, textvariable=type_var, values=["Analog", "Digital"], state="readonly")
        type_menu.pack(pady=2)

        tk.Label(self.settings_window, text="Sophisticated Dial / Theme:", bg="#1e1f22", fg="#b5bac1", font=("Segoe UI", 9)).pack(pady=(4, 0))
        theme_var = tk.StringVar(value=self.config["digital_theme"] if self.config["clock_type"] == "Digital" else self.config["analog_style"])
        theme_menu = ttk.Combobox(self.settings_window, textvariable=theme_var, state="readonly", width=25)
        theme_menu.pack(pady=2)

        tk.Label(self.settings_window, text="🎵 Music Visualizer Type:", bg="#1e1f22", fg="#a6e3a1", font=("Segoe UI", 9, "bold")).pack(pady=(6, 0))
        vis_var = tk.StringVar(value=self.config["digital_vis"] if self.config["clock_type"] == "Digital" else self.config["analog_vis"])
        vis_menu = ttk.Combobox(self.settings_window, textvariable=vis_var, state="readonly", width=25)
        vis_menu.pack(pady=2)

        def update_vis_choices():
            if type_var.get() == "Digital":
                vis_menu.config(values=DIGITAL_VIS_TYPES)
                vis_var.set(self.config["digital_vis"])
            else:
                vis_menu.config(values=ANALOG_VIS_TYPES)
                vis_var.set(self.config["analog_vis"])

        update_vis_choices()

        def on_vis_selected(event):
            if type_var.get() == "Digital":
                self.config["digital_vis"] = vis_var.get()
            else:
                self.config["analog_vis"] = vis_var.get()
            self.save_config()

        vis_menu.bind("<<ComboboxSelected>>", on_vis_selected)

        vis_toggle_var = tk.BooleanVar(value=self.config["enable_visualizer"])
        tk.Checkbutton(
            self.settings_window, text="Enable Music Visualizer", variable=vis_toggle_var,
            bg="#1e1f22", fg="#a6e3a1", selectcolor="#2b2d31", activebackground="#1e1f22",
            command=lambda: self.update_setting("enable_visualizer", vis_toggle_var.get())
        ).pack(pady=1)

        sim_toggle_var = tk.BooleanVar(value=self.config["always_simulate_audio"])
        tk.Checkbutton(
            self.settings_window, text="Always-On Audio Simulation (Test Mode)", variable=sim_toggle_var,
            bg="#1e1f22", fg="#89b4fa", selectcolor="#2b2d31", activebackground="#1e1f22",
            command=lambda: self.update_setting("always_simulate_audio", sim_toggle_var.get())
        ).pack(pady=1)

        tk.Label(self.settings_window, text="Numeral Script (Digital & Analog):", bg="#1e1f22", fg="#b5bac1", font=("Segoe UI", 9)).pack(pady=(4, 0))
        num_var = tk.StringVar(value=self.config["numerals"])
        num_menu = ttk.Combobox(self.settings_window, textvariable=num_var, values=list(ANALOG_NUMERAL_SETS.keys()), state="readonly")
        num_menu.pack(pady=2)
        num_menu.bind("<<ComboboxSelected>>", lambda e: self.update_setting("numerals", num_var.get()))

        def update_type(event):
            self.config["clock_type"] = type_var.get()
            if self.config["clock_type"] == "Digital":
                theme_menu.config(values=list(DIGITAL_STYLES.keys()))
                theme_var.set(self.config["digital_theme"])
            else:
                theme_menu.config(values=list(ANALOG_STYLES.keys()))
                theme_var.set(self.config["analog_style"])
            update_vis_choices()
            self.apply_theme()
            self.save_config()

        def update_theme(event):
            sel = theme_var.get()
            if self.config["clock_type"] == "Digital":
                self.config["digital_theme"] = sel
                def_num = DIGITAL_STYLES[sel]["default_num"]
            else:
                self.config["analog_style"] = sel
                def_num = ANALOG_STYLES[sel]["default_num"]
            self.config["numerals"] = def_num
            num_var.set(def_num)
            self.apply_theme()
            self.save_config()

        theme_menu.config(values=list(DIGITAL_STYLES.keys()) if self.config["clock_type"] == "Digital" else list(ANALOG_STYLES.keys()))
        type_menu.bind("<<ComboboxSelected>>", update_type)
        theme_menu.bind("<<ComboboxSelected>>", update_theme)

        tk.Label(self.settings_window, text="Calendar Options:", bg="#1e1f22", fg="#b5bac1", font=("Segoe UI", 9)).pack(pady=(4, 2))
        cal_frame = tk.Frame(self.settings_window, bg="#1e1f22")
        cal_frame.pack()

        for label, key in [("Day", "show_day"), ("Date", "show_date"), ("Month", "show_month"), ("Year", "show_year")]:
            var = tk.BooleanVar(value=self.config[key])
            tk.Checkbutton(
                cal_frame, text=label, variable=var, bg="#1e1f22", fg="white",
                selectcolor="#2b2d31", activebackground="#1e1f22", activeforeground="white",
                command=lambda k=key, v=var: self.update_setting(k, v.get())
            ).pack(side="left", padx=2)

        hide_var = tk.BooleanVar(value=self.config["auto_hide_frame"])
        tk.Checkbutton(
            self.settings_window, text="Auto-Hide Surroundings on Mouse Leave", variable=hide_var,
            bg="#1e1f22", fg="#a6e3a1", selectcolor="#2b2d31", activebackground="#1e1f22",
            command=lambda: self.update_setting("auto_hide_frame", hide_var.get())
        ).pack(pady=2)

        tk.Label(self.settings_window, text="Transparency:", bg="#1e1f22", fg="#b5bac1", font=("Segoe UI", 9)).pack(pady=(2, 0))
        alpha_slider = ttk.Scale(self.settings_window, from_=0.25, to=1.0, value=self.config["alpha"], command=self.update_alpha)
        alpha_slider.pack(fill="x", padx=30, pady=2)

    def update_setting(self, key, value):
        self.config[key] = value
        self.apply_theme()
        self.save_config()

    def update_alpha(self, val):
        self.config["alpha"] = float(val)
        self.root.attributes("-alpha", self.config["alpha"])
        self.save_config()

    def click_window(self, event):
        self._offset_x = event.x_root - self.root.winfo_rootx()
        self._offset_y = event.y_root - self.root.winfo_rooty()

    def drag_window(self, event):
        x = self.root.winfo_pointerx() - self._offset_x
        y = self.root.winfo_pointery() - self._offset_y
        self.root.geometry(f"+{x}+{y}")

    def resize_window(self, event):
        new_width = max(160, self.root.winfo_pointerx() - self.root.winfo_rootx())
        new_height = max(140, self.root.winfo_pointery() - self.root.winfo_rooty())
        self.root.geometry(f"{new_width}x{new_height}")
        self.save_config()

    def toggle_topmost(self):
        self.is_always_on_top = not self.is_always_on_top
        self.root.attributes("-topmost", self.is_always_on_top)
        self.apply_theme()

    def update_widget(self):
        self.check_hover_state()
        self.tick_timer()

        now = time.time()
        if now - self.last_batt_check > 3:
            self.last_batt_check = now
            if hasattr(psutil, "sensors_battery"):
                battery = psutil.sensors_battery()
                if battery:
                    self.battery_pct = int(battery.percent)
                    self.battery_plugged = bool(battery.power_plugged)
                    self.evaluate_battery_limits()
                    self.refresh_battery_window_ui()

        if self.config["clock_type"] == "Digital":
            self.draw_digital()
            self.root.after(45, self.update_widget)
        else:
            self.draw_analog()
            self.root.after(40, self.update_widget)

    def close_app(self):
        self.sound_engine.stop()
        self.save_config()
        self.save_notes()
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = FloatingWidget(root)
    root.mainloop()