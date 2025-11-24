
# --- Death GIF Sequence ---
def play_death_gif_then_gameover(reason):
    stop_game()
    stop_background_music()
    sekirosnakesound()
    howlsound()
    try:
        import tkinter as tk
        from PIL import Image, ImageTk

        top = tk.Toplevel(root)
        top.overrideredirect(True)
        top.geometry("800x600")
        top.configure(bg="black")

        gif_path = "snakebitedeathscreen.gif"
        gif = Image.open(gif_path)
        frames = []
        try:
            while True:
                frames.append(ImageTk.PhotoImage(gif.copy().resize((800,600))))
                gif.seek(len(frames))
        except EOFError:
            pass

        lbl = tk.Label(top, bg="black")
        lbl.pack(expand=True, fill="both")

        def animate(i=0):
            if i < len(frames):
                lbl.config(image=frames[i])
                top.after(80, animate, i+1)
            else:
                top.destroy()
                show_game_over_screen_final(reason)

        animate()

    except Exception:
        show_game_over_screen_final(reason)

# Original game over screen renamed

# test25_updated.py
# Complete merged file with difficulty selection, per-difficulty high scores,
# Joker (clown), pie (food), and Batman cooldown adjusted per difficulty.
# Based on user's original test25.py and the requested changes.

import string
import tkinter as tk
from tkinter import messagebox
import re
import random
import time
import csv
import os
import pygame
from PIL import Image, ImageTk
from tkinter import filedialog

# ----------------------------
# BANE (ENEMY) SYSTEM
# ----------------------------
BANE_FIRST_APPEAR = 120  # 2 minutes
BANE_INTERVAL_BASE = 90  # 1:30 (base)
bane_last_spawn = -1
bane_spawn_loop_id = None
bane_disabled_until = 0.0
clown_hold_until = 0.0  # when Joker is held due to Bane outcome
# Minigame starting times per difficulty (seconds)
BANE_MINIGAME_START = {1:40, 2:30, 3:23, 4:17, 5:10}
# Images for Bane sequences (use exact filenames)
BANE_IMG_1 = "aWildBaneAppear.jpg"       # initial encounter
BANE_IMG_2 = "BatmanVsBane1.avif"        # fight/minigame background
BANE_IMG_3 = "batmanbreaksbane.avif"     # player victory image
BANE_IMG_4 = "banebreaksjoker.avif"      # Bane busy with Joker
BANE_IMG_5 = "breakbatman.jpg"           # player defeat image


def show_batman_beats_joker_screen():
    try:
        import tkinter as tk
        from PIL import Image, ImageTk

        top = tk.Toplevel(root)
        top.overrideredirect(True)
        top.geometry("800x600")
        top.configure(bg="black")

        # Skip button (top-right corner)
        skip_btn = tk.Button(
            top,
            text="Skip",
            font=("Arial", 14),
            bg="red",
            fg="white",
            command=top.destroy
        )
        skip_btn.place(relx=1.0, rely=0.0, anchor="ne")

        gif_path = "batmanbeatsjoker.gif"
        gif = Image.open(gif_path)
        frames = []

        try:
            while True:
                frames.append(ImageTk.PhotoImage(gif.copy().resize((800, 600))))
                rapidpunchsound()
                gif.seek(len(frames))
        except EOFError:
            pass

        lbl = tk.Label(top, bg="black")
        lbl.pack(expand=True, fill="both")

        def animate(i=0):
            # If user pressed Skip → stop animation early
            if not top.winfo_exists():
                return

            if i < len(frames):
                lbl.config(image=frames[i])
                top.after(80, animate, i + 1)
            else:
                top.after(2000, top.destroy)

        animate()

    except Exception:
        pass



# ----------------------------
# GLOBAL GAME / PLAYER STATE
# ----------------------------
PLAYER_NAME = ""
PLAYER_IMAGE_PATH = ""
PLAYER_IMAGE_LABEL = None

# Initialize pygame mixer safely
try:
    pygame.init()
    pygame.mixer.init()
except Exception:
    pass

def start_background_music():
    try:
        pygame.mixer.music.load(r"C:\WebScrapingLibrary_NeoM2\REDASH _ the redhood mog ver. [GODDESS OF VICTORY_ NIKKE OST].mp3")
        pygame.mixer.music.play(loops=-1)
    except Exception:
        pass

def stop_background_music():
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass

def play_sound(path, loops=0):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops=loops)
    except Exception:
        pass

def slap():
    play_sound(r"C:\WebScrapingLibrary_NeoM2\slapping-sound.mp3", loops=0)
def deathsound():
    play_sound(r"C:\WebScrapingLibrary_NeoM2\deathsound.mp3", loops=0)
def clicksound():
    play_sound(r"C:\WebScrapingLibrary_NeoM2\click-sound-for-gd.mp3", loops=0)
def eatsound():
    play_sound("heavyeater.mp3", loops=0)
def laughsound():
    play_sound("hahaha.mp3", loops=0)
def victory_sound():
    play_sound("marios.mp3", loops=0)
def burningsound():
    play_sound("fire-burning.mp3", loops=0)
def batsound():
    play_sound(r"C:\WebScrapingLibrary_NeoM2\cus-im-batman.mp3", loops=0)
def snoresound():
    play_sound("snoring.mp3", loops=0)
def sekirosnakesound():
    play_sound(r"C:\WebScrapingLibrary_NeoM2\sekirodeath.mp3")
def howlsound():
    play_sound(r"C:\WebScrapingLibrary_NeoM2\sekiro-kite-man.mp3")
def rapidpunchsound():
    play_sound(r"rapidpunches.mp3")
# ----------------------------
# FILE & HIGHSCORE CONFIG
# ----------------------------
HIGHSCORE_FILE = "highscore_data.csv"
HIGH_SCORES = []

# Difficulty
CURRENT_DIFFICULTY = 2  # default Normal

DIFFICULTY_SETTINGS = {
    0: { "name": "Peaceful", "joker_first": None, "joker_interval": None, "pie_interval": 60, "bat_cd": 20 },
    1: { "name": "Easy",    "joker_first": 90,   "joker_interval": 35,   "pie_interval": 45, "bat_cd": 20 },
    2: { "name": "Normal",  "joker_first": 60,   "joker_interval": 30,   "pie_interval": 30, "bat_cd": 20 },
    3: { "name": "Hard",    "joker_first": 45,   "joker_interval": 20,   "pie_interval": 30, "bat_cd": 20 },
    4: { "name": "Extreme", "joker_first": 30,   "joker_interval": 15,   "pie_interval": 20, "bat_cd": 15 },
    5: { "name": "Batman",    "joker_first": 20,   "joker_interval": 10,   "pie_interval": 20, "bat_cd": 10 },
}

# Runtime variables populated from difficulty
CLOWN_FIRST_APPEAR = DIFFICULTY_SETTINGS[CURRENT_DIFFICULTY]["joker_first"] if DIFFICULTY_SETTINGS[CURRENT_DIFFICULTY]["joker_first"] is not None else -1
CLOWN_INTERVAL = DIFFICULTY_SETTINGS[CURRENT_DIFFICULTY]["joker_interval"] if DIFFICULTY_SETTINGS[CURRENT_DIFFICULTY]["joker_interval"] is not None else -1
PIE_RULE_INTERVAL = DIFFICULTY_SETTINGS[CURRENT_DIFFICULTY]["pie_interval"]
BAT_COOLDOWN = DIFFICULTY_SETTINGS[CURRENT_DIFFICULTY]["bat_cd"]

PIE_EMOJI = '🥧'
PIE_EMOJI_COUNT = 0
last_pie_time = time.time()
PIE_CHECK_ID = None

# Track how many pie-consumption events have already occurred (since game start)
PIE_CONSUMED_TOTAL = 0

CLOWN_EMOJI = "🤡"
FIRE_EMOJI = "🔥"
BAT_EMOJI = "🦇"

clown_last_spawn = -1
clown_spawn_loop_id = None
clown_burn_loop_id = None

last_bat_time = 0

# Rule-related globals
REQUIRED_REVERSED_STRING = ""
REVERSED_HINT = ""

MONTHS = ["january","february","march","april","may","june",
          "july","august","september","october","november","december"]
BRANDS = ["pepsi","pedro","starbuck"]
justice_league = ["batman","superman","flash","wonderwoman","aquaman",
                  "greenlantern","martianmanhunter","cyborg","plasticman","greenarrow"]
capitals = ["hanoi","bangkok","vientiane","phnompenh","naypyidaw","kualalumpur",
            "jakarta","manila","bandarseribegawan","singapore"]

# GUI root
root = tk.Tk()
root.title("The Password Game")
root.geometry("800x600")
root.configure(bg="#fdf8e4")

# ----------------------------
# HIGHSCORE
# ----------------------------
def load_high_scores():
    global HIGH_SCORES
    HIGH_SCORES = []
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        row_score = float(row.get('score', 0))
                        row_name = row.get('name', "")
                        row_path = row.get('image_path', "")
                        diff_raw = row.get('difficulty', "")
                        diff = int(diff_raw) if diff_raw != "" else 2
                        HIGH_SCORES.append({
                            "score": row_score,
                            "name": row_name,
                            "image_path": row_path,
                            "difficulty": diff
                        })
                    except Exception:
                        continue
        except Exception:
            HIGH_SCORES = []
    HIGH_SCORES.sort(key=lambda x: x['score'])

def save_high_scores_to_file():
    global HIGH_SCORES
    try:
        HIGH_SCORES.sort(key=lambda x: x['score'])
        fieldnames = ['score', 'name', 'image_path', 'difficulty']
        with open(HIGHSCORE_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in HIGH_SCORES:
                writer.writerow({
                    'score': r.get('score', 0),
                    'name': r.get('name', ""),
                    'image_path': r.get('image_path', ""),
                    'difficulty': r.get('difficulty', 2)
                })
    except Exception:
        pass

def save_high_score(score):
    global HIGH_SCORES, PLAYER_NAME, PLAYER_IMAGE_PATH, CURRENT_DIFFICULTY
    entry = {
        "score": float(score),
        "name": PLAYER_NAME or "No-Name",
        "image_path": PLAYER_IMAGE_PATH or "",
        "difficulty": int(CURRENT_DIFFICULTY)
    }
    HIGH_SCORES.append(entry)
    HIGH_SCORES.sort(key=lambda x: x['score'])
    HIGH_SCORES = HIGH_SCORES[:200]
    save_high_scores_to_file()

# ----------------------------
# UTILS
# ----------------------------
def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0:
            return False
    return True

def generate_random_string(length=6):
    global REQUIRED_REVERSED_STRING, REVERSED_HINT
    chars = string.ascii_letters + string.digits
    gen = ''.join(random.choice(chars) for _ in range(length))
    REQUIRED_REVERSED_STRING = gen
    REVERSED_HINT = gen[::-1]
    return gen[::-1]

def apply_difficulty_settings():
    global CLOWN_FIRST_APPEAR, CLOWN_INTERVAL, PIE_RULE_INTERVAL, BAT_COOLDOWN, CURRENT_DIFFICULTY
    cfg = DIFFICULTY_SETTINGS.get(int(CURRENT_DIFFICULTY), DIFFICULTY_SETTINGS[2])
    CLOWN_FIRST_APPEAR = cfg["joker_first"] if cfg["joker_first"] is not None else -1
    CLOWN_INTERVAL = cfg["joker_interval"] if cfg["joker_interval"] is not None else -1
    PIE_RULE_INTERVAL = cfg["pie_interval"]
    BAT_COOLDOWN = cfg["bat_cd"]

# ----------------------------
# PROFILE IMAGE SELECTOR
# ----------------------------
def select_profile_image():
    global PLAYER_IMAGE_PATH, PLAYER_IMAGE_LABEL
    path = filedialog.askopenfilename(
        title="Chọn Ảnh Đại Diện (PNG/JPG)",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
    )
    if path:
        PLAYER_IMAGE_PATH = path
        try:
            img = Image.open(path)
            label_width = PLAYER_IMAGE_LABEL.winfo_width()
            label_height = PLAYER_IMAGE_LABEL.winfo_height()
            if label_width <= 1 or label_height <= 1:
                label_width, label_height = 150, 150
            img = img.resize((label_width, label_height), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            PLAYER_IMAGE_LABEL.config(image=img_tk, text="")
            PLAYER_IMAGE_LABEL.image = img_tk
        except Exception as e:
            messagebox.showerror("Lỗi Ảnh", f"Không thể tải ảnh: {e}")
            PLAYER_IMAGE_PATH = ""

# ----------------------------
# TIMER
# ----------------------------
timer_label = None
timer_running = False
start_time = 0.0
game_running = False

def update_timer():
    global timer_running
    if timer_running and timer_label:
        elapsed = time.time() - start_time
        m = int(elapsed // 60)
        s = int(elapsed % 60)
        ms = int((elapsed - int(elapsed)) * 100)
        timer_label.config(text=f"⏱️ {m:02d}:{s:02d}.{ms:02d}")
        root.after(10, update_timer)

def reset_timer():
    global start_time, timer_running
    timer_running = False
    start_time = time.time()
    if timer_label:
        timer_label.config(text="⏱️ 00:00.00")

def continue_timer():
    global timer_running, start_time
    if game_running and not timer_running:
        start_time = time.time() - get_current_elapsed_time()
        timer_running = True
        update_timer()

def get_current_elapsed_time():
    try:
        text = timer_label.cget("text").replace("⏱️", "").strip()
        m, rest = text.split(":")
        s, ms = rest.split(".")
        return int(m)*60 + int(s) + int(ms)/100
    except Exception:
        return 0

def stop_timer():
    global timer_running
    timer_running = False

# ----------------------------
# RULES
# ----------------------------
def get_rule_status(password):
    global REVERSED_HINT, PIE_EMOJI_COUNT, PIE_EMOJI
    pw_lower = password.lower()

    total_len = len(password)
    count_upper = sum(1 for c in password if c.isupper())
    count_lower = sum(1 for c in password if c.islower())

    rule_double_check = (count_lower == count_upper * 2)
    rule_prime_check = is_prime(count_upper)

    sum_of_digits = 0
    rule_length_end = False

    temp_pw = password.rstrip(PIE_EMOJI)
    match = re.search(r'(\D|^)(\d+)$', temp_pw)
    password_for_sum_calc = password

    sum_of_digits_from_length = 0
    if match:
        length_digits_str = match.group(2)
        try:
            length_as_number = int(length_digits_str)
            if length_as_number == total_len:
                rule_length_end = True
                start_idx = match.start(2)
                pw_before_length = temp_pw[:start_idx]
                pies = password[len(temp_pw):]
                password_for_sum_calc = pw_before_length + pies
                sum_of_digits_from_length = sum(int(c) for c in length_digits_str)
        except Exception:
            pass

    sum_rest = sum(int(c) for c in password_for_sum_calc if c.isdigit())
    if rule_length_end:
        sum_of_digits = sum_rest + sum_of_digits_from_length
    else:
        sum_of_digits = sum(int(c) for c in password if c.isdigit())

    rule_sum_check = (sum_of_digits == 25)
    reversed_check = REVERSED_HINT in password if REVERSED_HINT else False
    curr_pie = password.count(PIE_EMOJI)
    rule_pie_check = (curr_pie == PIE_EMOJI_COUNT)

    return {
        "Phải có thành viên Justice League": any(j in pw_lower for j in justice_league),
        "Kí tự đặc biệt ít hơn chữ thường 5": (sum(1 for c in password if c in string.punctuation) +5 == count_lower),
        "Tổng các số phải bằng 25": rule_sum_check,
        "Phải có tên một tháng (Eng)": any(m in pw_lower for m in MONTHS),
        "Phải có tên một thủ đô ASEAN (Eng-Viết liền)": any(m in pw_lower for m in capitals),
        "Phải chứa 'Pepsi', 'Pedro', hoặc 'Starbuck'": any(b in pw_lower for b in BRANDS),
        "Phải có dòng chữ ngược": reversed_check,
        "Chữ thường phải gấp đôi chữ hoa": rule_double_check,
        "Tổng số chữ hoa là số nguyên tố": rule_prime_check,
        "Phải có tổng số kí tự ở cuối": rule_length_end,
        "Quy tắc bánh (🥧)": rule_pie_check
    }

# ----------------------------
# PIE / HUNGER
# ----------------------------
def add_pie_emoji():
    global PIE_EMOJI_COUNT, last_pie_time
    pw = entry_password.get()
    if pw.count(PIE_EMOJI) >= 3:
        stop_game()
        play_death_gif_then_gameover("Bạn đã ăn quá nhiều bánh!")
        return
    eatsound()
    pw += PIE_EMOJI
    entry_password.delete(0, tk.END)
    entry_password.insert(0, pw)
    PIE_EMOJI_COUNT = pw.count(PIE_EMOJI)
    check_rules()


def check_pie_rule():
    global PIE_EMOJI_COUNT, last_pie_time, PIE_CHECK_ID, PIE_CONSUMED_TOTAL
    # Only run when the game is active and timer is running
    if not game_running or not timer_running:
        return

    pw = entry_password.get()
    PIE_EMOJI_COUNT = pw.count(PIE_EMOJI)

    # How many interval boundaries have been reached since game start
    try:
        elapsed = get_current_elapsed_time()
    except Exception:
        elapsed = 0

    intervals_passed = int(elapsed // PIE_RULE_INTERVAL)

    # The number of consumption events that SHOULD have happened
    target_consumptions = intervals_passed

    # If more consumption events should have happened than we've recorded, consume pies now
    if target_consumptions > PIE_CONSUMED_TOTAL:
        need = target_consumptions - PIE_CONSUMED_TOTAL
        # Try to consume 'need' pies one by one
        for _ in range(need):
            pw = entry_password.get()
            current_pies = pw.count(PIE_EMOJI)
            if current_pies > 0:
                idx = pw.find(PIE_EMOJI)
                pw = pw[:idx] + pw[idx+1:]
                entry_password.delete(0, tk.END)
                entry_password.insert(0, pw)
                PIE_EMOJI_COUNT = pw.count(PIE_EMOJI)
                PIE_CONSUMED_TOTAL += 1
                check_rules()
            else:
                # Not enough pies to consume → death by starvation
                stop_game()
                play_death_gif_then_gameover("Bạn đã chết đói vì không có bánh!")
                return

    # schedule next check only if game still running and timer running
    if game_running and timer_running:
        PIE_CHECK_ID = root.after(1000, check_pie_rule)


def cancel_pie_check():
    global PIE_CHECK_ID
    if PIE_CHECK_ID:
        try:
            root.after_cancel(PIE_CHECK_ID)
        except Exception:
            pass
        PIE_CHECK_ID = None

# ----------------------------
# JOKER / CLOWN SYSTEM
# ----------------------------
def add_clown_emoji():
    laughsound()
    pw = entry_password.get()
    pw += CLOWN_EMOJI
    entry_password.delete(0, tk.END)
    entry_password.insert(0, pw)

def clown_spawn_loop():
    global clown_last_spawn, clown_spawn_loop_id
    if not game_running:
        return
    # disabled?
    if CLOWN_FIRST_APPEAR is None or CLOWN_FIRST_APPEAR < 0:
        return
    elapsed = get_current_elapsed_time()
    if clown_last_spawn == -1 and elapsed >= CLOWN_FIRST_APPEAR:
        add_clown_emoji()
        clown_last_spawn = elapsed
    if clown_last_spawn >= 0 and CLOWN_INTERVAL > 0 and elapsed - clown_last_spawn >= CLOWN_INTERVAL:
        add_clown_emoji()
        clown_last_spawn = elapsed
    clown_spawn_loop_id = root.after(500, clown_spawn_loop)

def clown_burn_loop():
    global clown_burn_loop_id
    if not game_running:
        return
    pw = entry_password.get()
    chars = list(pw)
    clown_positions = [i for i,c in enumerate(chars) if c == CLOWN_EMOJI]
    if not clown_positions:
        clown_burn_loop_id = root.after(1000, clown_burn_loop)
        return
    all_burned = True
    for pos in clown_positions:
        left = pos - 1
        if left < 0:
            play_death_gif_then_gameover(" Joker 🤡 đã bắt cóc mẹ bạn! ")
            return
        while left >= 0 and chars[left] == FIRE_EMOJI:
            burningsound()
            left -= 1
        if left < 0:
            play_death_gif_then_gameover("Bạn đã bị Joker 🤡 đốt bỏng đít!🔥")
            return
        if chars[left] != FIRE_EMOJI:
            chars[left] = FIRE_EMOJI
            all_burned = False
    entry_password.delete(0, tk.END)
    entry_password.insert(0, "".join(chars))
    if all_burned:
        play_death_gif_then_gameover("Bạn đã bị Joker 🤡 đốt bỏng đít!")
        return
    clown_burn_loop_id = root.after(1000, clown_burn_loop)

# ----------------------------
# BATMAN
# ----------------------------
def summon_batman():
    global last_bat_time
    now = time.time()
    if now - last_bat_time < BAT_COOLDOWN:
        show_batman_sleeping()
        snoresound()
        return
    last_bat_time = now
    pw = entry_password.get()
    pw += BAT_EMOJI
    batsound()
    entry_password.delete(0, tk.END)
    entry_password.insert(0, pw)
    def cleanse(): 
        p_original = entry_password.get()

        p = entry_password.get().replace(BAT_EMOJI,"")
        p = p.replace(FIRE_EMOJI,"").replace(CLOWN_EMOJI,"")
        entry_password.delete(0, tk.END)
        entry_password.insert(0, p)
    
        if '🤡' in p_original:
            show_batman_beats_joker_screen()
    root.after(500, cleanse)


# ----------------------------
# Bane encounter & minigame
# ----------------------------
def show_bane_encounter():
    """Display initial Bane image with Accept/Decline buttons beneath it."""
    try:
        top = tk.Toplevel(root)
        top.title("BANE APPEARS")
        top.geometry("620x460")
        top.transient(root)
        top.grab_set()
        frame = tk.Frame(top, bg="#000")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        try:
            img = Image.open(BANE_IMG_1)
            img = img.resize((580,300), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            lbl = tk.Label(frame, image=img_tk, bg="#000")
            lbl.image = img_tk
            lbl.pack(pady=6)
        except Exception:
            tk.Label(frame, text="BANE APPEARS!", font=("Georgia", 20, "bold"), bg="#000", fg="white").pack(pady=20)

        btn_frame = tk.Frame(frame, bg="#000")
        btn_frame.pack(pady=6)
        # Decline button
        def decline():
            top.destroy()
            handle_bane_decline()

        # Accept button
        def accept():
            top.destroy()
            handle_bane_accept()

        tk.Button(btn_frame, text="Decline", width=12, command=decline, bg="#f8d7da").pack(side="left", padx=8)
        tk.Button(btn_frame, text="Accept", width=12, command=accept, bg="#a3d9a5").pack(side="left", padx=8)
    except Exception:
        pass

def handle_bane_decline():
    """Handle decline: 35% chance scramble password and blur rules, 100% remove pies."""
    try:
        # remove all pie emojis
        pw = entry_password.get()
        new_pw = pw.replace(PIE_EMOJI, "")
        entry_password.delete(0, tk.END)
        entry_password.insert(0, new_pw)
        # 35% chance scramble and blur rules
        if random.random() < 0.35:
            # scramble password characters
            s = list(entry_password.get())
            random.shuffle(s)
            entry_password.delete(0, tk.END)
            entry_password.insert(0, "".join(s))
            # blur rules: set text to asterisks
            for k, lbl in rule_labels.items():
                try:
                    lbl.config(text="*******", fg="gray", bg="#fdf8e4")
                except Exception:
                    pass
        check_rules()
    except Exception:
        pass

def handle_bane_accept():
    """Start minigame: freeze main time and run number-typing minigame."""
    try:
        # freeze main time and game loops
        global timer_running, game_running, bane_disabled_until, clown_hold_until, last_bat_time
        timer_was_running = timer_running
        timer_running = False
        # Setup minigame Toplevel
        mg = tk.Toplevel(root)
        mg.title("Bane Duel")
        mg.geometry("620x420")
        mg.transient(root)
        mg.grab_set()
        frame = tk.Frame(mg, bg="#000")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        # show battle image
        try:
            img = Image.open(BANE_IMG_2)
            img = img.resize((580,260), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            img_lbl = tk.Label(frame, image=img_tk, bg="#000")
            img_lbl.image = img_tk
            img_lbl.pack(pady=6)
        except Exception:
            tk.Label(frame, text="BATTLE", font=("Georgia", 20, "bold"), bg="#000", fg="white").pack(pady=10)
        # minigame timer
        start_val = BANE_MINIGAME_START.get(int(CURRENT_DIFFICULTY), 30)
        current_val = {"v": start_val}
        timer_display = tk.Label(frame, text=f"{current_val['v']}", font=("Georgia", 36, "bold"), fg="white", bg="#000")
        timer_display.pack(pady=6)
        info = tk.Label(frame, text="Type digits 0-9 to add. Bane will subtract.", fg="white", bg="#000")
        info.pack()
        # input entry for digits
        entry = tk.Entry(frame, width=10, font=("Georgia", 18))
        entry.pack(pady=6)
        entry.focus_set()
        # prevent typing same number thrice: track last two entries
        last_inputs = []
        # flag to stop loops
        stop_flags = {"stop": False}
        # function to update display
        def update_display():
            timer_display.config(text=f"{current_val['v']}")
        # player's input handler (auto-send when number entered)
        def on_input(event=None):
            if stop_flags["stop"]: return
            val = entry.get().strip()
            if not val: return
            ch = val[-1]
            if ch not in "0123456789":
                entry.delete(0, tk.END)
                return
            # enforce cannot type same number thrice in a row
            if len(last_inputs) >= 2 and last_inputs[-1] == last_inputs[-2] == ch:
                # ignore this input
                entry.delete(0, tk.END)
                return
            # register input
            last_inputs.append(ch)
            if len(last_inputs) > 10:
                last_inputs.pop(0)
            entry.delete(0, tk.END)
            # Bane picks a random digit
            bane_choice = str(random.randint(0,9))
            # if both same -> cancel both (no effect)
            if bane_choice == ch:
                pass
            else:
                # apply player's add
                try:
                    current_val['v'] += int(ch)
                except Exception:
                    pass
                # apply bane subtract
                try:
                    current_val['v'] -= int(bane_choice)
                except Exception:
                    pass
            # clamp and update
            if current_val['v'] > 999: current_val['v'] = 999
            update_display()
            # check win/lose
            if current_val['v'] >= 60:
                stop_flags["stop"] = True
                mg.after(200, lambda: end_minigame_win(mg))
            elif current_val['v'] <= 0:
                stop_flags["stop"] = True
                mg.after(200, lambda: end_minigame_lose(mg))
        entry.bind("<KeyRelease>", on_input)
        # Also let Bane act periodically to keep pressure (every 800ms)
        def bane_tick():
            if stop_flags["stop"]: return
            # Bane randomly generates number and applies as subtraction
            bch = str(random.randint(0,9))
            # Apply subtraction
            try:
                current_val['v'] -= int(bch)
            except Exception:
                pass
            update_display()
            if current_val['v'] <= 0:
                stop_flags["stop"] = True
                mg.after(200, lambda: end_minigame_lose(mg))
                return
            mg.after(800, bane_tick)
        mg.after(800, bane_tick)
    except Exception:
        # restore timer if fail
        try:
            timer_running = timer_was_running
        except Exception:
            pass

def end_minigame_win(mg_window):
    """Player wins the minigame: show victory image, banish Bane for 4 minutes, chance to delay Joker."""
    try:
        mg_window.destroy()
    except Exception:
        pass
    # show image 3 for 2 seconds
    try:
        top = tk.Toplevel(root)
        top.overrideredirect(True)
        top.geometry("800x600")
        frame = tk.Frame(top, bg="black")
        frame.pack(fill="both", expand=True)
        img = Image.open(BANE_IMG_3)
        img = img.resize((800,600), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        lbl = tk.Label(frame, image=img_tk, bg="black")
        lbl.image = img_tk
        lbl.pack()
        # Banefor 4 minutes
        now = get_current_elapsed_time()
        global bane_disabled_until, clown_hold_until
        bane_disabled_until = now + 240.0
        # 65% chance to delay Joker's next appearance by difficulty amount
        if random.random() < 0.65:
            add = 60 if int(CURRENT_DIFFICULTY) in (1,2) else (40 if int(CURRENT_DIFFICULTY)==3 else 30)
            clown_hold_until = get_current_elapsed_time() + add
            # show image 4 briefly
            try:
                img2 = Image.open(BANE_IMG_4)
                img2 = img2.resize((800,600), Image.LANCZOS)
                img2_tk = ImageTk.PhotoImage(img2)
                lbl2 = tk.Label(top, image=img2_tk, bg="black")
                lbl2.image = img2_tk
                lbl2.place(relx=0.5, rely=0.5, anchor="center")
            except Exception:
                pass
        top.after(2000, top.destroy)
    except Exception:
        pass
    # resume game loops
    continue_timer()
    check_pie_rule()
    try:
        clown_spawn_loop()
        clown_burn_loop()
    except Exception:
        pass

def end_minigame_lose(mg_window):
    """Player loses: disable Batman for 1 minute and show defeat image."""
    try:
        mg_window.destroy()
    except Exception:
        pass
    try:
        top = tk.Toplevel(root)
        top.overrideredirect(True)
        top.geometry("800x600")
        frame = tk.Frame(top, bg="black")
        frame.pack(fill="both", expand=True)
        img = Image.open(BANE_IMG_5)
        img = img.resize((800,600), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        lbl = tk.Label(frame, image=img_tk, bg="black")
        lbl.image = img_tk
        lbl.pack()
        top.after(2000, top.destroy)
    except Exception:
        pass
    # disable Batman for 60 seconds
    global last_bat_time, bane_disabled_until
    last_bat_time = time.time()  # push last bat time so summon is on cooldown
    bane_disabled_until = time.time() + 60.0
    # resume game loops
    continue_timer()
    check_pie_rule()
    try:
        clown_spawn_loop()
        clown_burn_loop()
    except Exception:
        pass

def bane_spawn_loop():
    """Loop that triggers Bane appearances. Avoid overlap with Joker by checking clown_hold_until and clown_last_spawn."""
    global bane_last_spawn, bane_spawn_loop_id, bane_disabled_until, clown_hold_until, clown_last_spawn
    if not game_running:
        return
    if int(CURRENT_DIFFICULTY) == 0:
        # peaceful mode: do not spawn
        return
    elapsed = get_current_elapsed_time()
    # initial spawn at 2:00
    if bane_last_spawn == -1 and elapsed >= BANE_FIRST_APPEAR and elapsed < bane_disabled_until:
        # ensure not within 20s of clown_last_spawn or being held
        if (clown_last_spawn != -1 and abs(clown_last_spawn - elapsed) < 20) or elapsed < clown_hold_until:
            # defer slightly, don't spawn now
            pass
        else:
            bane_last_spawn = elapsed
            show_bane_encounter()
    # subsequent spawns: schedule roughly every BANE_INTERVAL_BASE +/- 30s
    if bane_last_spawn != -1 and elapsed - bane_last_spawn >= (BANE_INTERVAL_BASE + random.randint(-30,30)):
        if (clown_last_spawn != -1 and abs(clown_last_spawn - elapsed) < 20) or elapsed < clown_hold_until or elapsed < bane_disabled_until:
            pass
        else:
            bane_last_spawn = elapsed
            show_bane_encounter()
    try:
        bane_spawn_loop_id = root.after(1500, bane_spawn_loop)
    except Exception:
        pass

# ----------------------------
# GAME FLOW CONTROL
# ----------------------------
def stop_game():
    global clown_spawn_loop_id, clown_burn_loop_id, game_running
    game_running = False
    stop_timer()
    cancel_pie_check()
    if clown_spawn_loop_id:
        try:
            root.after_cancel(clown_spawn_loop_id)
        except Exception:
            pass
        clown_spawn_loop_id = None
    if clown_burn_loop_id:
        try:
            root.after_cancel(clown_burn_loop_id)
        except Exception:
            pass
        clown_burn_loop_id = None

# ----------------------------
# UI: menus and screens
# ----------------------------
def show_main_menu():
    reset_timer_quiet()
    stop_game()
    clicksound()
    for w in root.winfo_children():
        w.destroy()
    frame = tk.Frame(root, bg="#fdf8e4")
    frame.pack(expand=True, fill="both")
    tk.Label(frame, text="*** The Password Game ***", font=("Georgia", 24, "bold"), bg="#fdf8e4").pack(pady=(50,20))
    bf = tk.Frame(frame, bg="#fdf8e4")
    bf.pack()
    tk.Button(bf, text="New Game", font=("Georgia", 14), width=20, command=show_difficulty_selection, bg="#a3d9a5").pack(pady=8)
    tk.Button(bf, text="High Score", font=("Georgia", 14), width=20, command=lambda: show_high_score_dialog(filter_diff=None), bg="#99c8e8").pack(pady=8)
    tk.Button(bf, text="Exit Game", font=("Georgia", 14), width=20, command=just_exit, bg="#f4a261", fg="white").pack(pady=8)

def show_difficulty_selection():
    clicksound()
    for w in root.winfo_children():
        w.destroy()
    frame = tk.Frame(root, bg="#fdf8e4")
    frame.pack(expand=True, fill="both")
    tk.Label(frame, text="Select Difficulty", font=("Georgia", 24, "bold"), bg="#fdf8e4").pack(pady=(30,10))
    btn_frame = tk.Frame(frame, bg="#fdf8e4")
    btn_frame.pack(pady=10)
    for idx in range(6):
        cfg = DIFFICULTY_SETTINGS[idx]
        b = tk.Button(btn_frame, text=f"{idx} - {cfg['name']}", width=20, font=("Georgia", 12),
                      command=lambda i=idx: set_difficulty_and_start(i),
                      bg="#a3d9a5" if idx == CURRENT_DIFFICULTY else "#e0e0e0")
        b.grid(row=idx//2, column=idx%2, padx=10, pady=8)
    tk.Button(frame, text="Back to Menu", command=show_main_menu, bg="#f4a261", fg="white").pack(pady=20)

def set_difficulty_and_start(diff):
    global CURRENT_DIFFICULTY
    CURRENT_DIFFICULTY = int(diff)
    clicksound()
    show_player_setup()

def show_player_setup():
    global PLAYER_IMAGE_LABEL, PLAYER_IMAGE_PATH, PLAYER_NAME
    PLAYER_IMAGE_PATH = ""
    clicksound()
    for w in root.winfo_children():
        w.destroy()
    frame = tk.Frame(root, bg="#fdf8e4")
    frame.pack(expand=True, fill="both")
    tk.Label(frame, text="*** Cài Đặt Người Chơi ***", font=("Georgia", 20, "bold"), bg="#fdf8e4").pack(pady=(30, 10))
    tk.Label(frame, text="Tên người chơi:", font=("Georgia", 12), bg="#fdf8e4").pack(pady=(10,0))
    entry_name = tk.Entry(frame, width=30, font=("Georgia", 12))
    entry_name.insert(0, "No-Name")
    entry_name.pack(pady=(0, 10))
    tk.Label(frame, text="Ảnh Đại Diện (Bấm để chọn file):", font=("Georgia", 12), bg="#fdf8e4").pack(pady=(10, 0))
    avatar_frame = tk.Frame(frame, width=150, height=150, bg="#cccccc")
    avatar_frame.pack(pady=10)
    avatar_frame.pack_propagate(False)
    PLAYER_IMAGE_LABEL = tk.Label(avatar_frame, text="Chọn ảnh", bg="#cccccc", fg="#333")
    PLAYER_IMAGE_LABEL.pack(expand=True, fill="both")
    PLAYER_IMAGE_LABEL.bind("<Button-1>", lambda e: select_profile_image())
    def start_game_with_profile():
        nonlocal_entry_name = entry_name.get().strip()
        PLAYER_NAME = nonlocal_entry_name if nonlocal_entry_name else "No-Name"
        apply_difficulty_settings()
        clicksound()
        show_game_screen("")
    tk.Button(frame, text="▶️BẮT ĐẦU GAME!", font=("Georgia", 14, "bold"), width=20, command=start_game_with_profile, bg="#a3d9a5", fg="black").pack(pady=20)
    tk.Button(frame, text="🏠Quay lại Menu", font=("Georgia", 10), command=show_main_menu, bg="#f4a261", fg="white").pack(pady=10)

# ----------------------------
# GAME SCREEN
# ----------------------------
entry_password = None
length_label = None
rule_labels = {}
game_frame = None

def show_game_screen(initial_password=""):
    global game_frame, entry_password, length_label, rule_labels, timer_label, PIE_EMOJI_COUNT, last_pie_time, game_running, clown_last_spawn
    clicksound()
    game_running = True
    clown_last_spawn = -1
    cancel_pie_check()
    stop_timer()
    is_new = (initial_password == "")
    if is_new:
        generate_random_string()
        PIE_EMOJI_COUNT = 0
        last_pie_time = time.time()
    PIE_CONSUMED_TOTAL = 0
    for w in root.winfo_children():
        w.destroy()
    game_frame = tk.Frame(root, bg="#fdf8e4")
    game_frame.pack(expand=True, fill="both")
    timer_label = tk.Label(game_frame, text="⏱️ 00:00.00", font=("Georgia", 14, "bold"), bg="#fdf8e4", fg="#f4a261")
    timer_label.place(x=10, y=10)
    tk.Button(game_frame, text="Exit", font=("Georgia", 10), command=show_exit_dialog, bg="#f4a261", fg="white").place(relx=1.0, x=-10, y=10, anchor="ne")
    music_frame = tk.Frame(game_frame, bg="#fdf8e4")
    music_frame.place(relx=1.0, x=-10, y=40, anchor="ne")
    tk.Button(music_frame, text="▶️Play", command=start_background_music, bg="#a3d9a5", font=("Georgia", 9)).pack(side="left", padx=5)
    tk.Button(music_frame, text="⏹️Stop", command=stop_background_music, bg="#f8d7da", font=("Georgia", 9)).pack(side="left", padx=5)
    tk.Label(game_frame, text="* The Password Game", font=("Georgia", 18, "bold"), bg="#fdf8e4").pack(pady=(50, 5))
    tk.Label(game_frame, text="Please choose a password", font=("Georgia", 12), bg="#fdf8e4").pack()
    frame_input = tk.Frame(game_frame, bg="#fdf8e4")
    frame_input.pack(pady=15)
    pw_scroll_frame = tk.Frame(frame_input, bg="#fdf8e4")
    pw_scroll_frame.pack(side="left")
    entry_password = tk.Entry(pw_scroll_frame, width=30, font=("Georgia", 12))
    entry_password.pack(side="top", fill="x")
    pw_scroll = tk.Scrollbar(pw_scroll_frame, orient="horizontal", command=entry_password.xview)
    pw_scroll.pack(side="bottom", fill="x")
    entry_password.configure(xscrollcommand=pw_scroll.set)
    entry_password.bind("<KeyRelease>", lambda e: check_rules())
    entry_password.insert(0, initial_password)
    length_label = tk.Label(frame_input, text=str(len(initial_password)), font=("Georgia", 12), bg="#fdf8e4")
    length_label.pack(side="left", padx=5)
    tk.Button(frame_input, text="Submit", font=("Georgia", 12, "bold"), command=submit_password, bg="#80a8ff", fg="white").pack(side="left", padx=10)
    frame_rules = tk.Frame(game_frame, bg="#fdf8e4")
    frame_rules.pack(pady=10)
    rule_labels = {}
    all_rules = [
        "Tổng các số phải bằng 25",
        "Phải có tên một tháng (Eng)",
        "Phải có thành viên Justice League",
        "Kí tự đặc biệt ít hơn chữ thường 5",
        "Phải có tên một thủ đô ASEAN (Eng-Viết liền)",
        "Phải chứa 'Pepsi', 'Pedro', hoặc 'Starbuck'",
        "Phải có dòng chữ ngược",
        "Chữ thường phải gấp đôi chữ hoa",
        "Tổng số chữ hoa là số nguyên tố",
        "Phải có tổng số kí tự ở cuối",
        "Quy tắc bánh (🥧)"
    ]
    for rule in all_rules:
        label = tk.Label(frame_rules, text="✖ " + rule, fg="red", bg="#f8d7da", font=("Georgia", 10), width=40, anchor="w", padx=10, pady=3)
        label.pack(pady=2, fill="x")
        rule_labels[rule] = label
    btn_frame = tk.Frame(game_frame, bg="#fdf8e4")
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Gọi Batman 🦇", bg="#b0c4de", font=("Georgia", 10, "bold"), command=summon_batman).pack(side="left", padx=5)
    tk.Button(btn_frame, text=f"Thêm Bánh {PIE_EMOJI}", command=add_pie_emoji, bg="#ffe4b5", font=("Georgia", 10, "bold")).pack(side="left", padx=5)
    continue_timer()
    check_pie_rule()
    check_rules()
    clown_last_spawn = -1
    clown_spawn_loop()
    clown_burn_loop()
    bane_spawn_loop()

# ----------------------------
# SUBMIT & HELPERS
# ----------------------------
def submit_password():
    global start_time
    pw = entry_password.get()
    check_rules()
    if all(get_rule_status(pw).values()):
        stop_game()
        final = get_current_elapsed_time()
        m = int(final // 60)
        s = int(final % 60)
        ms = int((final - int(final)) * 100)
        ts = f"{m:02d}:{s:02d}.{ms:02d}"
        save_high_score(final)
        victory_sound()
        show_victory_screen(ts)
    else:
        show_stupid_image()
        slap()

# ----------------------------
# POPUPS & SCREENS
# ----------------------------
def show_stupid_image():
    win = tk.Toplevel(root)
    win.title("Incorrect!")
    win.geometry("600x400")
    win.resizable(False, False)
    try:
        img = Image.open(r"C:\WebScrapingLibrary_NeoM2\stupidslap.jpg")
        img = img.resize((600,400))
        img_tk = ImageTk.PhotoImage(img)
        win.img_ref = img_tk
        tk.Label(win, image=img_tk).pack(fill="both", expand=True)
    except Exception:
        tk.Label(win, text="Incorrect!", font=("Georgia", 28, "bold")).pack(expand=True)
    win.after(2000, win.destroy)

def show_batman_sleeping():
    win = tk.Toplevel(root)
    win.title("BATMAN IS ASLEEP")
    win.geometry("600x400")
    win.resizable(False, False)
    try:
        img = Image.open("Batmanzzz.jpg")
        img = img.resize((600,400))
        img_tk = ImageTk.PhotoImage(img)
        win.img_ref = img_tk
        tk.Label(win, image=img_tk).pack(fill="both", expand=True)
    except Exception:
        tk.Label(win, text="Batman is sleeping...", font=("Georgia", 24, "bold")).pack(expand=True)
    win.after(2000, win.destroy)

def show_victory_screen(final_time_str):
    stop_game()
    victory_sound()
    for w in root.winfo_children():
        w.destroy()
    canvas = tk.Canvas(root, highlightthickness=0, bd=0)
    canvas.pack(fill="both", expand=True)
    try:
        v_img = Image.open("Victory.png")
        v_img = v_img.resize((root.winfo_width(), root.winfo_height()), Image.LANCZOS)
        v_tk = ImageTk.PhotoImage(v_img)
        canvas.v_img = v_tk
        canvas.create_image(0,0,anchor="nw",image=v_tk)
    except Exception:
        canvas.create_rectangle(0,0,10000,10000, fill="black")
    canvas.create_text(root.winfo_width()//2, root.winfo_height()-80, text=f"⏱ Time: {final_time_str}", fill="white", font=("Georgia",28,"bold"))
    btn = tk.Button(root, text="Return to Menu", font=("Georgia", 14), bg="#a3d9a5", command=show_main_menu)
    canvas.create_window(root.winfo_width()//2, root.winfo_height()-40, window=btn)

GAME_OVER_BG = r"C:\WebScrapingLibrary_NeoM2\Dark-Souls-You-Died.jpg"

def show_game_over_screen_final(reason):
    stop_game()
    stop_background_music()
    deathsound()
    for w in root.winfo_children():
        w.destroy()
    canvas = tk.Canvas(root, highlightthickness=0, bd=0)
    canvas.pack(fill="both", expand=True)
    try:
        bg = Image.open(GAME_OVER_BG)
        bg = bg.resize((root.winfo_width(), root.winfo_height()), Image.LANCZOS)
        bg_tk = ImageTk.PhotoImage(bg)
        canvas.bg_img = bg_tk
        canvas.create_image(0,0,anchor="nw",image=bg_tk)
    except Exception:
        canvas.create_rectangle(0,0,5000,5000,fill="black")
    canvas.create_text(root.winfo_width()//2, 80, text="💀💀💀", fill="#A00000", font=("Georgia",48,"bold"))
    canvas.create_text(root.winfo_width()//2, 180, text=reason, fill="white", font=("Georgia",24), width=600)
    replay_btn = tk.Button(root, text="Play Again", font=("Georgia",16,"bold"), bg="#dc3545", fg="white", command=show_game_screen)
    canvas.create_window(root.winfo_width()//2, root.winfo_height()//2 + 120, window=replay_btn)
    mf = tk.Frame(root, bg="#000000")
    canvas.create_window(root.winfo_width()-100, 40, anchor="ne", window=mf)
    tk.Button(mf, text="▶️Play", command=start_background_music, bg="#a3d9a5", font=("Georgia",9)).pack(side="left", padx=5)
    tk.Button(mf, text="⏹️Stop", command=stop_background_music, bg="#f8d7da", font=("Georgia",9)).pack(side="left", padx=5)

# ----------------------------
# HIGH SCORE DIALOG (per difficulty)
# ----------------------------
def show_high_score_dialog(filter_diff=None):
    clicksound()
    if filter_diff is None:
        dlg = tk.Toplevel(root)
        dlg.title("High Scores")
        dlg.geometry("400x400")
        dlg.configure(bg="#fdf8e4")
        dlg.transient(root)
        dlg.grab_set()
        tk.Label(dlg, text="Select Difficulty", font=("Georgia",16,"bold"), bg="#fdf8e4").pack(pady=20)
        for d in range(6):
            name = DIFFICULTY_SETTINGS[d]["name"]
            tk.Button(dlg, text=f"{d} - {name}", font=("Georgia",12), width=20, bg="#99c8e8",
                      command=lambda diff=d, win=dlg: [win.destroy(), show_high_score_dialog(diff)]).pack(pady=5)
        tk.Button(dlg, text="Close", command=dlg.destroy, bg="#f4a261", fg="white").pack(pady=10)
        return
    diff = int(filter_diff)
    dlg = tk.Toplevel(root)
    dlg.title(f"High Score — {DIFFICULTY_SETTINGS[diff]['name']}")
    dlg.geometry("700x450")
    dlg.configure(bg="#fdf8e4")
    dlg.transient(root)
    dlg.grab_set()
    tk.Label(dlg, text=f"High Scores — {DIFFICULTY_SETTINGS[diff]['name']}", font=("Georgia",18,"bold"), bg="#fdf8e4").pack(pady=20)
    frame = tk.Frame(dlg, bg="#ffffff")
    frame.pack(pady=10, padx=20, fill="both", expand=True)
    tk.Label(frame, text="Rank", bg="#fff", font=("Georgia",10,"bold")).grid(row=0, column=0, padx=10)
    tk.Label(frame, text="Ảnh", bg="#fff", font=("Georgia",10,"bold")).grid(row=0, column=1, padx=10)
    tk.Label(frame, text="Tên Người Chơi", bg="#fff", font=("Georgia",10,"bold")).grid(row=0, column=2, padx=10)
    tk.Label(frame, text="Thời gian", bg="#fff", font=("Georgia",10,"bold")).grid(row=0, column=3, padx=10)
    scores = [s for s in HIGH_SCORES if s["difficulty"] == diff]
    scores = sorted(scores, key=lambda x: x["score"])[:5]
    if not scores:
        tk.Label(frame, text="Chưa có điểm nào.", bg="#fff").grid(row=1, column=0, columnspan=4, pady=20)
    else:
        for i, s in enumerate(scores):
            score = s["score"]
            name = s["name"]
            path = s["image_path"]
            m = int(score // 60)
            sec = int(score % 60)
            ms = int((score - int(score)) * 100)
            ts = f"{m:02d}:{sec:02d}.{ms:02d}"
            tk.Label(frame, text=f"#{i+1}", bg="#fff").grid(row=i+1, column=0, padx=10, pady=5)
            tk.Label(frame, text=name, bg="#fff").grid(row=i+1, column=2, padx=10)
            tk.Label(frame, text=ts, bg="#fff").grid(row=i+1, column=3, padx=10)
            img_label = tk.Label(frame, bg="#fff", width=50, height=50)
            img_label.grid(row=i+1, column=1, padx=10)
            if path and os.path.exists(path):
                try:
                    img = Image.open(path)
                    img = img.resize((40, 40))
                    img_tk = ImageTk.PhotoImage(img)
                    img_label.config(image=img_tk)
                    img_label.image = img_tk
                except Exception:
                    img_label.config(text="❌")
            else:
                img_label.config(text="👤")
    tk.Button(dlg, text="Close", command=dlg.destroy, bg="#f4a261", fg="white").pack(pady=15)

# ----------------------------
# EXIT DIALOGS
# ----------------------------
def just_exit():
    save_high_scores_to_file()
    stop_game()
    root.destroy()

def show_exit_dialog():
    stop_timer()
    cancel_pie_check()
    clicksound()
    dlg = tk.Toplevel(root)
    dlg.title("Exit")
    dlg.geometry("360x170")
    dlg.configure(bg="#fdf8e4")
    dlg.transient(root)
    dlg.grab_set()
    tk.Label(dlg, text="Bạn muốn làm gì?", font=("Georgia",12), bg="#fdf8e4").pack(pady=15)
    f = tk.Frame(dlg, bg="#fdf8e4")
    f.pack()
    tk.Button(f, text="▶️ Return to Game", width=18, command=lambda: [dlg.destroy(), continue_timer(), check_pie_rule()], bg="#a3d9a5").grid(row=0, column=0, padx=5)
    tk.Button(f, text="🏠 Return to Main Menu", width=18, command=lambda: [dlg.destroy(), show_main_menu()], bg="#fff3b0").grid(row=1, column=0, padx=5, pady=5)
    tk.Button(f, text="❌ Exit Game", width=18, command=lambda: [dlg.destroy(), just_exit()], bg="#f8d7da").grid(row=2, column=0, padx=5)
    dlg.protocol("WM_DELETE_WINDOW", lambda: [dlg.destroy(), continue_timer(), check_pie_rule()])

# ----------------------------
# Helpers used in menus
# ----------------------------
def reset_timer_quiet():
    global start_time, timer_running
    timer_running = False
    start_time = time.time()

def check_rules(event=None):
    global entry_password, rule_labels, PIE_EMOJI
    if entry_password is None:
        return
    password = entry_password.get()
    if password.count(PIE_EMOJI) > 3:
        stop_game()
        try:
            pygame.mixer.init()
            pygame.mixer.Sound(r"C:\WebScrapingLibrary_NeoM2\deathsound.mp3").play()
        except Exception:
            pass
        play_death_gif_then_gameover(f"Mật khẩu không được chứa quá 3 emoji bánh ({PIE_EMOJI}).")
        return
    if length_label:
        length_label.config(text=str(len(password)))
    rules = get_rule_status(password)
    total_len = len(password)
    count_upper = sum(1 for c in password if c.isupper())
    count_lower = sum(1 for c in password if c.islower())
    for rule_key, label in rule_labels.items():
        success = rules.get(rule_key, False)
        if rule_key == "Phải có dòng chữ ngược":
           text = f"Phải có dòng chữ ngược của '{REQUIRED_REVERSED_STRING}'"
        elif rule_key == "Chữ thường phải gấp đôi chữ hoa":
            text = f"Chữ thường ({count_lower}) phải gấp đôi chữ hoa ({count_upper})"
        elif rule_key == "Tổng số chữ hoa là số nguyên tố":
            text = f"Tổng số chữ in hoa ({count_upper}) là số nguyên tố"
        elif rule_key == "Phải có tổng số kí tự ở cuối":
            text = f"Số ở cuối mật khẩu phải là {total_len}"
        elif rule_key == "Quy tắc bánh (🥧)":
            text = f"Hãy nhớ ăn bánh!"
        else:
            text = rule_key
        if success:
            try:
                label.config(text=f"✔ {text}", fg="green", bg="#d4edda")
            except Exception:
                pass
        else:
            try:
                label.config(text=f"✖ {text}", fg="red", bg="#f8d7da")
            except Exception:
                pass

# ----------------------------
# Start
# ----------------------------
load_high_scores()
show_main_menu()

# Ensure proper window close handling
def on_closing():
    show_exit_dialog2()

def show_exit_dialog2():
    stop_timer()
    dlg = tk.Toplevel(root)
    dlg.title("Exit")
    dlg.geometry("360x170")
    dlg.configure(bg="#fdf8e4")
    dlg.transient(root)
    dlg.grab_set()
    tk.Label(dlg, text="Bạn muốn thoát game?", font=("Georgia",12), bg="#fdf8e4").pack(pady=15)
    f = tk.Frame(dlg, bg="#fdf8e4")
    f.pack()
    tk.Button(f, text="❌Không", width=18, command=lambda: [dlg.destroy(), continue_timer()], bg="#f8d7da").grid(row=0, column=0, padx=5)
    tk.Button(f, text="✅Có!", width=18, command=lambda: [dlg.destroy(), just_exit()], bg="#f8d7da").grid(row=2, column=0, padx=5)
    dlg.protocol("WM_DELETE_WINDOW", lambda: [dlg.destroy(), continue_timer(), check_pie_rule()])
    root.wait_window(dlg)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
