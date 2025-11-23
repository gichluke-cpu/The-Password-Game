justice_league = ["batman","superman","flash","wonderwoman","aquaman","greenlantern","martianmanhunter","cyborg","plasticman","greenarrow"]
import string
import tkinter as tk
from tkinter import messagebox
import re
import random 
import time 
import json
import csv
import os
import pygame
from PIL import Image, ImageTk # Cần thiết cho việc hiển thị ảnh
from tkinter import filedialog # Cần thiết cho hộp thoại chọn file

PLAYER_NAME = ""
PLAYER_IMAGE_PATH = "" 
PLAYER_IMAGE_LABEL = None # Label sẽ hiển thị ảnh đại diện

# --- Hàm để chọn ảnh (Đã có, giữ nguyên) ---
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

            # Lấy kích thước của khung label
            label_width = PLAYER_IMAGE_LABEL.winfo_width()
            label_height = PLAYER_IMAGE_LABEL.winfo_height()

            # Nếu label chưa render -> dùng kích thước mặc định
            if label_width <= 1 or label_height <= 1:
                label_width = 150
                label_height = 150

            # Resize ảnh theo kích thước khung
            img = img.resize((label_width, label_height), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)

            PLAYER_IMAGE_LABEL.config(image=img_tk, text="")
            PLAYER_IMAGE_LABEL.image = img_tk

        except Exception as e:
            messagebox.showerror("Lỗi Ảnh", f"Không thể tải ảnh: {e}")
            PLAYER_IMAGE_PATH = ""



# ===== BẮT ĐẦU THÊM NHẠC NỀN =====
pygame.mixer.init()
def start_background_music():
        # SỬA: Thêm 'r' ở đầu để không lỗi đường dẫn
        pygame.mixer.music.load("C:\WebScrapingLibrary_NeoM2\REDASH _ the redhood mog ver. [GODDESS OF VICTORY_ NIKKE OST].mp3")
        #pygame.mixer.music.set_volume(0.7) # Đặt âm lượng (0.0 đến 1.0)
        
        # SỬA: loops=-1 để lặp lại vô hạn
        pygame.mixer.music.play(loops=-1)   
        
# === HÀM MỚI ĐỂ TẮT NHẠC ===
def stop_background_music():
        pygame.mixer.music.stop()

# --- XÓA HẾT PHẦN TẠO CỬA SỔ root, Button, on_closing Ở ĐÂY ---
# (Vì chúng ta sẽ thêm nút nhạc vào màn hình game chính)

# ===== KẾT THÚC THÊM NHẠC NỀN =====
# ===============================================================
#  CONSTANTS & GLOBAL VARIABLES
# ===============================================================

HIGHSCORE_FILE = "highscore_data.csv"

game_frame = None
entry_password = None
length_label = None
rule_labels = {}
pie_button = None

saved_password = ""
save_protection_password = ""
saved_required_string = ""
saved_hint_string = ""

HIGH_SCORES = []
start_time = 0.0
timer_label = None
timer_running = False
game_running = False

PIE_EMOJI = '🥧'
PIE_EMOJI_COUNT = 0
last_pie_time = time.time()
PIE_RULE_INTERVAL = 30
PIE_CHECK_ID = None

MONTHS = ["january", "february", "march", "april", "may", "june", 
          "july", "august", "september", "october", "november", "december"]
BRANDS = ["pepsi", "pedro", "starbuck"]

capitals = ["hanoi",              # Vietnam
    "bangkok",            # Thailand
    "vientiane",          # Laos
    "phnompenh",          # Cambodia
    "naypyidaw",          # Myanmar
    "kualalumpur",        # Malaysia
    "jakarta",            # Indonesia
    "manila",             # Philippines
    "bandarseribegawan",  # Brunei
    "singapore"        ]

REQUIRED_REVERSED_STRING = "" 
REVERSED_HINT = "" 


# ===============================================================
#  HIGH SCORE SYSTEM
# ===============================================================
def load_high_scores():
    global HIGH_SCORES
    HIGH_SCORES = []
    
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Chuyển đổi score từ string sang float khi đọc từ CSV
                    try:
                        row['score'] = float(row['score']) 
                        HIGH_SCORES.append(row)
                    except ValueError:
                        # Bỏ qua các hàng không hợp lệ
                        continue
        except Exception as e:
            print(f"Error loading high scores from CSV: {e}") 
            HIGH_SCORES = []
            
    # Sắp xếp lại điểm cao sau khi load (thời gian thấp là tốt)
    HIGH_SCORES.sort(key=lambda x: x['score'])

def save_high_scores_to_file():
    global HIGH_SCORES
    try:
        # Luôn sắp xếp trước khi lưu để đảm bảo file CSV là top 5 đã sắp xếp
        HIGH_SCORES.sort(key=lambda x: x['score'])
        
        fieldnames = ['score', 'name', 'image_path']
        
        with open(HIGHSCORE_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader() # Ghi tiêu đề cột
            writer.writerows(HIGH_SCORES) # Ghi dữ liệu
            
    except Exception as e:
        print(f"Error saving high scores to CSV: {e}")
        pass

def save_high_score(score):
    global HIGH_SCORES, PLAYER_NAME, PLAYER_IMAGE_PATH
    
    # 🌟 Tạo một đối tượng (dictionary) chứa thông tin điểm số
    score_entry = {
        "score": score,
        "name": PLAYER_NAME,
        "image_path": PLAYER_IMAGE_PATH
    }
    
    HIGH_SCORES.append(score_entry)
    
    # 💡 FIX: Sắp xếp theo score (thời gian thấp là tốt)
    HIGH_SCORES.sort(key=lambda x: x['score'])
    
    # Giữ lại 5 điểm cao nhất
    HIGH_SCORES = HIGH_SCORES[:5]
    
    save_high_scores_to_file() # 🔥 SAVE ALWAYS
def show_high_score():
    global HIGH_SCORES
    load_high_scores() # Luôn load dữ liệu mới nhất từ CSV

    dialog = tk.Toplevel(root)
    dialog.title("🏆 High Score - Top 5")
    dialog.geometry("600x400")
    dialog.configure(bg="#fdf8e4")
    dialog.transient(root)
    dialog.grab_set()
    
    tk.Label(dialog, text="Bảng Xếp Hạng", font=("Georgia", 16, "bold"),
             bg="#fdf8e4", fg="#333").pack(pady=20)

    frame = tk.Frame(dialog, bg="#ffffff", pady=10)
    frame.pack(pady=10, padx=20, fill="x")

    if not HIGH_SCORES:
        tk.Label(frame, text="Chưa có điểm cao nào.", bg="#fff").pack(pady=20)
    else:
        # Tiêu đề cột
        tk.Label(frame, text="Hạng", bg="#fff", font=("Georgia", 10, "bold")).grid(row=0, column=0, padx=10)
        tk.Label(frame, text="Ảnh", bg="#fff", font=("Georgia", 10, "bold")).grid(row=0, column=1, padx=10)
        tk.Label(frame, text="Tên Người Chơi", bg="#fff", font=("Georgia", 10, "bold")).grid(row=0, column=2, padx=10)
        tk.Label(frame, text="Thời gian", bg="#fff", font=("Georgia", 10, "bold")).grid(row=0, column=3, padx=10)

        for i, sc_entry in enumerate(HIGH_SCORES):
            score = sc_entry['score']
            name = sc_entry['name']
            path = sc_entry['image_path']
            
            # Định dạng thời gian
            m = int(score // 60)
            s = int(score % 60)
            ms = int((score - int(score)) * 100)
            ts = f"{m:02d}:{s:02d}.{ms:02d}"

            # Hiển thị Rank, Tên, và Thời gian
            tk.Label(frame, text=f"#{i+1}", bg="#fff").grid(row=i+1, column=0, padx=10, pady=5)
            tk.Label(frame, text=name, bg="#fff").grid(row=i+1, column=2, padx=10)
            tk.Label(frame, text=ts, bg="#fff").grid(row=i+1, column=3, padx=10)

            # Xử lý hiển thị ảnh (nếu có)
            image_label = tk.Label(frame, bg="#fff", width=50, height=50)
            image_label.grid(row=i+1, column=1, padx=10, pady=5)

            if path and os.path.exists(path):
                try:
                    img = Image.open(path)
                    img = img.resize((40, 40))
                    img_tk = ImageTk.PhotoImage(img)
                    
                    image_label.config(image=img_tk)
                    image_label.image = img_tk
                except Exception:
                    image_label.config(text="❌")
            else:
                image_label.config(text="👤")

    tk.Button(dialog, text="Đóng", command=dialog.destroy).pack(pady=15)
    root.wait_window(dialog)

# ===============================================================
#  CORE SUPPORT FUNCTIONS
# ===============================================================

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def generate_random_string(length=6):
    global REQUIRED_REVERSED_STRING, REVERSED_HINT
    chars = string.ascii_letters + string.digits
    gen = ''.join(random.choice(chars) for i in range(length))
    REQUIRED_REVERSED_STRING = gen
    REVERSED_HINT = gen[::-1]
    return gen[::-1]

# ===============================================================
#  CORE GAME LOGIC
# ===============================================================

# ===============================================================
#  CORE GAME LOGIC (Đã sửa đổi cho Yêu cầu mới)
# ===============================================================

def get_rule_status(password):
    global REVERSED_HINT, PIE_EMOJI_COUNT, PIE_EMOJI
    pw_lower = password.lower()

    total_len = len(password)
    count_upper = sum(1 for c in password if c.isupper())
    count_lower = sum(1 for c in password if c.islower())

    rule_double_check = (count_lower == count_upper * 2)
    rule_prime_check = is_prime(count_upper)

    # Khởi tạo tổng số
    sum_of_digits = 0
    rule_length_end = False
    
    # Loại bỏ bánh trước khi tìm số cuối
    temp_pw = password.rstrip(PIE_EMOJI) 

    # --- TÌM SỐ ĐỘ DÀI RIÊNG LẺ (YÊU CẦU 2) ---
    
    # Biểu thức chính quy tìm: (ký tự không phải số) + (một hoặc nhiều số) + (kết thúc chuỗi)
    # Chúng ta tìm số độ dài phải tách biệt.
    # Sử dụng `\D` (không phải số) để đảm bảo số cuối không dính với số khác.
    match = re.search(r'(\D|^)(\d+)$', temp_pw)
    
    # Phần mật khẩu dùng để tính tổng các số ban đầu (mặc định là toàn bộ chuỗi)
    password_for_sum_calc = password 
    
    if match:
        # Số độ dài là nhóm 2
        length_digits_str = match.group(2)
        try:
            length_as_number = int(length_digits_str)
            
            # Kiểm tra Quy tắc Độ dài: Số ở cuối phải bằng tổng độ dài MẬT KHẨU
            if length_as_number == total_len:
                rule_length_end = True
                
                # --- XỬ LÝ TÍNH TỔNG SỐ (YÊU CẦU 1) ---
                
                # Vị trí bắt đầu của các ký tự số độ dài trong temp_pw
                start_index_of_length_digits = match.start(2)
                
                # Phần mật khẩu trước các số độ dài (bao gồm ký tự phân tách nếu có)
                password_before_length_digits = temp_pw[:start_index_of_length_digits]
                
                # Lấy lại các ký tự bánh (nếu có)
                pies = password[len(temp_pw):]
                
                # Phần dùng để tính tổng số ban đầu: chỉ loại bỏ các ký tự số độ dài
                password_for_sum_calc = password_before_length_digits + pies
                
                # Tính tổng các chữ số trong số độ dài (YÊU CẦU 1)
                sum_of_digits_from_length = sum(int(c) for c in length_digits_str)
            
            else:
                # Nếu số cuối không phải là độ dài, nó được coi là số bình thường
                pass
        except:
            # Nếu không thể chuyển số cuối thành int, bỏ qua
            pass 

    # Tính tổng các số chỉ trong phần password_for_sum_calc (các số KHÔNG phải là số độ dài)
    sum_of_digits_from_rest = sum(int(c) for c in password_for_sum_calc if c.isdigit())
    
    # Tổng cuối cùng = Tổng các số còn lại + Tổng các chữ số từ số độ dài (nếu quy tắc độ dài được thỏa mãn)
    if rule_length_end:
        sum_of_digits = sum_of_digits_from_rest + sum_of_digits_from_length
    else:
        # Nếu quy tắc độ dài không thỏa, thì tất cả các số (bao gồm cả số cuối) đều tính vào tổng
        sum_of_digits = sum(int(c) for c in password if c.isdigit())


    rule_sum_check = (sum_of_digits == 25)
    
    # --- KẾT THÚC LOGIC TÍNH TỔNG ---

    # Kiểm tra chính xác chuỗi đảo ngược (bao gồm cả chữ hoa/thường)
    reversed_check = REVERSED_HINT in password if REVERSED_HINT else False

    curr_pie = password.count(PIE_EMOJI)
    rule_pie_check = (curr_pie == PIE_EMOJI_COUNT)

    return {
        "Phải có thành viên Justice League": any(j in pw_lower for j in justice_league),
        "Kí tự đặc biệt ít hơn chữ thường 1": (sum(1 for c in password if c in string.punctuation) +1 == count_lower),

        "Ít nhất một chữ hoa": any(c.isupper() for c in password),
        "Ít nhất một số": any(c.isdigit() for c in password), 
        "Ít nhất một ký tự đặc biệt": any(c in string.punctuation for c in password),
        "Tổng các số phải bằng 25": rule_sum_check,
        "Không chứa từ 'password'": "password" not in pw_lower,
        "Phải có tên một tháng (Eng)": any(m in pw_lower for m in MONTHS),
        "Phải có thành viên Justice League": any(m in pw_lower for m in justice_league),
        "Phải có tên một thủ đô ASEAN (Eng-Viết liền)": any(m in pw_lower for m in capitals),
        "Phải chứa 'Pepsi', 'Pedro', hoặc 'Starbuck'": any(b in pw_lower for b in BRANDS),
        "Phải có dòng chữ ngược": reversed_check,
        "Chữ thường phải gấp đôi chữ hoa": rule_double_check,
        "Tổng số chữ hoa là số nguyên tố": rule_prime_check,
        "Phải có tổng số kí tự ở cuối": rule_length_end,
        "Quy tắc bánh (🥧)": rule_pie_check
    }
def check_rules(event=None):
    global entry_password, rule_labels, PIE_EMOJI

    if entry_password is None: return
    password = entry_password.get()

    # Instant loss: more than 3 pies
    if password.count(PIE_EMOJI) > 3:
        stop_game()
        show_game_over_screen(f"Mật khẩu không được chứa quá 3 emoji bánh ({PIE_EMOJI}).")
        return

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
            label.config(text=f"✔ {text}", fg="green", bg="#d4edda")
        else:
            label.config(text=f"✖ {text}", fg="red", bg="#f8d7da")

# ===============================================================
#  TIMER SYSTEM
# ===============================================================

def update_timer():
    global timer_label, start_time, timer_running
    if timer_running and timer_label:
        elapsed = time.time() - start_time
        m = int(elapsed // 60)
        s = int(elapsed % 60)
        ms = int((elapsed - int(elapsed)) * 100)
        timer_label.config(text=f"⏱️ {m:02d}:{s:02d}.{ms:02d}")
        root.after(10, update_timer)

def reset_timer():
    global start_time
    stop_timer()
    start_time = time.time()
    if timer_label:
        timer_label.config(text="⏱️ 00:00.00")

def continue_timer():
    global timer_running, game_running, start_time
    if game_running and not timer_running:
        start_time = time.time() - get_current_elapsed_time()
        timer_running = True
        update_timer()

def get_current_elapsed_time():
    """Returns the elapsed time currently shown on the timer."""
    text = timer_label.cget("text").replace("⏱️", "").strip()
    try:
        m, rest = text.split(":")
        s, ms = rest.split(".")
        return int(m)*60 + int(s) + int(ms)/100
    except:
        return 0

def stop_timer():
    global timer_running
    timer_running = False

# ===============================================================
#  PIE RULE SYSTEM
# ===============================================================

def add_pie_emoji():
    global PIE_EMOJI_COUNT, last_pie_time

    pw = entry_password.get()
    if pw.count(PIE_EMOJI) >= 3:
        stop_game()
        show_game_over_screen("Bạn đã ăn quá nhiều bánh!")
        return

    pw += PIE_EMOJI
    entry_password.delete(0, tk.END)
    entry_password.insert(0, pw)

    PIE_EMOJI_COUNT = pw.count(PIE_EMOJI)
    last_pie_time = time.time()
    check_rules()


def check_pie_rule():
    global PIE_EMOJI_COUNT, last_pie_time, PIE_CHECK_ID

    if not game_running:
        return

    elapsed = time.time() - last_pie_time
    pw = entry_password.get()
    PIE_EMOJI_COUNT = pw.count(PIE_EMOJI)

    if elapsed >= PIE_RULE_INTERVAL:
        if PIE_EMOJI_COUNT > 0:
            idx = pw.find(PIE_EMOJI)
            if idx != -1:
                pw = pw[:idx] + pw[idx+1:]
                entry_password.delete(0, tk.END)
                entry_password.insert(0, pw)
                PIE_EMOJI_COUNT -= 1
                last_pie_time = time.time()
                check_rules()
        else:
            stop_game()
            show_game_over_screen("Bạn đã chết đói vì không ăn bánh!")
            return

    PIE_CHECK_ID = root.after(1000, check_pie_rule)

def cancel_pie_check():
    global PIE_CHECK_ID
    if PIE_CHECK_ID is not None:
        root.after_cancel(PIE_CHECK_ID)
        PIE_CHECK_ID = None

# ===============================================================
#  GAME FLOW CONTROL
# ===============================================================

def submit_password():
    global start_time

    password = entry_password.get()
    check_rules()
    if all(get_rule_status(password).values()):
        stop_game()
        final = get_current_elapsed_time()

        m = int(final // 60)
        s = int(final % 60)
        ms = int((final - int(final)) * 100)
        ts = f"{m:02d}:{s:02d}.{ms:02d}"

        save_high_score(final)

        messagebox.showinfo("You win!", f"🎉 Thời gian: {ts}")
        show_main_menu()
    else:
        messagebox.showerror("Thất bại", "STUPID!")

def stop_game():
    global game_running
    game_running = False
    stop_timer()
    cancel_pie_check()


# ===============================================================
#  SCREEN & UI MANAGEMENT
#  (ĐÃ SẮP XẾP LẠI THEO YÊU CẦU)
# ===============================================================

def show_main_menu():
    reset_timer()
    stop_game()

    for w in root.winfo_children():
        w.destroy()

    frame = tk.Frame(root, bg="#fdf8e4")
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="*** The Password Game ***", font=("Georgia", 24, "bold"),
             bg="#fdf8e4").pack(pady=(50, 20))

    bf = tk.Frame(frame, bg="#fdf8e4")
    bf.pack()

    #tk.Button(bf, text="New Game", font=("Georgia", 14), width=15,
              #command=lambda: show_game_screen(""),
              #bg="#a3d9a5").pack(pady=10)
    tk.Button(bf, text="New Game", font=("Georgia", 14), width=15,
         command=show_player_setup, # Chỉ gọi tên hàm, KHÔNG CÓ ngoặc đơn () hay đối số
         bg="#a3d9a5").pack(pady=10)
    tk.Button(bf, text="High Score", font=("Georgia", 14), width=15,
              command=show_high_score,
              bg="#99c8e8").pack(pady=10)

    tk.Button(bf, text="Exit Game", font=("Georgia", 14), width=15,
              command=just_exit, bg="#f4a261", fg="white").pack(pady=10)
    
#===================Hàm Setup Người Chơi (Mới)=====================================
def show_player_setup():
    global PLAYER_IMAGE_LABEL, PLAYER_IMAGE_PATH
    
    # Reset biến toàn cục khi bắt đầu màn hình setup
    PLAYER_IMAGE_PATH = "" 
    
    for w in root.winfo_children():
        w.destroy()

    frame = tk.Frame(root, bg="#fdf8e4")
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="*** Cài Đặt Người Chơi ***", font=("Georgia", 20, "bold"),
             bg="#fdf8e4").pack(pady=(50, 20))

    # --- INPUT TÊN ---
    tk.Label(frame, text="Tên người chơi:", font=("Georgia", 12),
             bg="#fdf8e4").pack(pady=(10, 0))
    entry_name = tk.Entry(frame, width=30, font=("Georgia", 12))
    entry_name.insert(0, "No-Name") # Giá trị mặc định
    entry_name.pack(pady=(0, 20))
    
    # --- CHỌN ẢNH ---
# --- CHỌN ẢNH ---
    tk.Label(frame, text="Ảnh Đại Diện (Bấm để chọn file):", font=("Georgia", 12),
            bg="#fdf8e4").pack(pady=(10, 0))


    # Tạo frame bao ảnh (kích thước pixel)
    avatar_frame = tk.Frame(frame, width=150, height=150, bg="#cccccc")
    avatar_frame.pack(pady=10)
    avatar_frame.pack_propagate(False)  # Không cho frame tự co giãn theo nội dung

    # Label ảnh bên trong frame
    PLAYER_IMAGE_LABEL = tk.Label(avatar_frame, text="Chọn ảnh", bg="#cccccc", fg="#333")
    PLAYER_IMAGE_LABEL.pack(expand=True, fill="both")

    PLAYER_IMAGE_LABEL.bind("<Button-1>", lambda e: select_profile_image())



    # --- NÚT BẮT ĐẦU GAME ---
    def start_game_with_profile():
        global PLAYER_NAME
        # Lấy tên và gán giá trị mặc định nếu rỗng
        input_name = entry_name.get().strip()
        PLAYER_NAME = input_name if input_name else "No-Name"
        
        # Chuyển sang màn hình chơi game
        show_game_screen("")

    tk.Button(frame, text="▶️BẮT ĐẦU GAME!", font=("Georgia", 14, "bold"), width=20,
              command=start_game_with_profile, 
              bg="#a3d9a5", fg="black").pack(pady=30)
              
    tk.Button(frame, text="🏠Quay lại Menu", font=("Georgia", 10),
              command=show_main_menu,
              bg="#f4a261", fg="white").pack(pady=10)    


#=====================================================================================================================================================================
def show_game_screen(initial_password=""):
    global game_frame, entry_password, length_label, rule_labels
    global timer_label, PIE_EMOJI_COUNT, last_pie_time, game_running

    game_running = True
    cancel_pie_check()

    is_new = (initial_password == "")
    if is_new:
        generate_random_string()
        PIE_EMOJI_COUNT = 0
        last_pie_time = time.time()

    stop_timer()

    for w in root.winfo_children():
        w.destroy()

    game_frame = tk.Frame(root, bg="#fdf8e4")
    game_frame.pack(expand=True, fill="both")

    timer_label = tk.Label(game_frame, text="⏱️ 00:00.00", font=("Georgia", 14, "bold"),
                           bg="#fdf8e4", fg="#f4a261")
    timer_label.place(x=10, y=10)

    tk.Button(game_frame, text="Exit", font=("Georgia", 10),
              command=show_exit_dialog, bg="#f4a261", fg="white").place(relx=1.0, x=-10, y=10, anchor="ne")
    # <--- BẮT ĐẦU THÊM NÚT NHẠC (GÓC TRÊN PHẢI, DƯỚI EXIT) ---
    music_frame = tk.Frame(game_frame, bg="#fdf8e4")
    # Đặt frame ở góc phải, dưới nút Exit (y=40)
    music_frame.place(relx=1.0, x=-10, y=40, anchor="ne") 

    play_btn = tk.Button(music_frame, text="▶️Play", 
                          command=start_background_music, 
                          bg="#a3d9a5", font=("Georgia", 9))
    play_btn.pack(side="left", padx=5)

    stop_btn = tk.Button(music_frame, text="⏹️Stop", 
                          command=stop_background_music, 
                          bg="#f8d7da", font=("Georgia", 9))
    stop_btn.pack(side="left", padx=5)
    # <--- KẾT THÚC THÊM NÚT NHẠC ---
    tk.Label(game_frame, text="* The Password Game", font=("Georgia", 18, "bold"),
             bg="#fdf8e4").pack(pady=(50, 5))

    tk.Label(game_frame, text="Please choose a password", font=("Georgia", 12),
             bg="#fdf8e4").pack()

    frame_input = tk.Frame(game_frame, bg="#fdf8e4")
    frame_input.pack(pady=15)

    entry_password = tk.Entry(frame_input, width=30, font=("Georgia", 12))
    entry_password.pack(side="left", padx=5)
    entry_password.bind("<KeyRelease>", check_rules)
    entry_password.insert(0, initial_password)

    length_label = tk.Label(frame_input, text=str(len(initial_password)),
                             font=("Georgia", 12), bg="#fdf8e4")
    length_label.pack(side="left", padx=5)

    tk.Button(frame_input, text="Submit", font=("Georgia", 12, "bold"),
              command=submit_password, bg="#80a8ff", fg="white").pack(side="left", padx=10)

    frame_rules = tk.Frame(game_frame, bg="#fdf8e4")
    frame_rules.pack(pady=10)

    rule_labels = {}
    all_rules = [
        "Ít nhất một chữ hoa",
        "Ít nhất một số",
        "Ít nhất một ký tự đặc biệt",
        "Tổng các số phải bằng 25",
        "Không chứa từ 'password'",
        "Phải có tên một tháng (Eng)",
        "Phải có thành viên Justice League",
        "Kí tự đặc biệt ít hơn chữ thường 1",
        "Phải có tên một thủ đô ASEAN (Eng-Viết liền)",
        "Phải chứa 'Pepsi', 'Pedro', hoặc 'Starbuck'",
        "Phải có dòng chữ ngược",
        "Chữ thường phải gấp đôi chữ hoa",
        "Tổng số chữ hoa là số nguyên tố",
        "Phải có tổng số kí tự ở cuối",
        "Quy tắc bánh (🥧)"
    ]

    for rule in all_rules:
        label = tk.Label(frame_rules, text="✖ " + rule, fg="red",
                         bg="#f8d7da", font=("Georgia", 10),
                         width=40, anchor="w", padx=10, pady=3)
        label.pack(pady=2, fill="x")
        rule_labels[rule] = label

    # Pie button
    tk.Button(game_frame, text=f"Thêm Bánh {PIE_EMOJI}",
              command=add_pie_emoji, bg="#ffe4b5",
              font=("Georgia", 10, "bold")).pack(pady=10)
    

    continue_timer()
    check_pie_rule()
    check_rules()


'''def show_high_score():
    global HIGH_SCORES

    dialog = tk.Toplevel(root)
    dialog.title("🏆 High Score - Top 5")
    dialog.geometry("400x300")
    dialog.configure(bg="#fdf8e4")
    dialog.transient(root)
    dialog.grab_set()
    
    tk.Label(dialog, text="Bảng Xếp Hạng", font=("Georgia", 16, "bold"),
             bg="#fdf8e4", fg="#333").pack(pady=20)

    frame = tk.Frame(dialog, bg="#ffffff", pady=10)
    frame.pack(pady=10, padx=20, fill="x")

    if not HIGH_SCORES:
        tk.Label(frame, text="Chưa có điểm cao nào.", bg="#fff").pack(pady=20)
    else:
        tk.Label(frame, text="Hạng", bg="#fff", font=("Georgia", 10, "bold")).grid(row=0, column=0)
        tk.Label(frame, text="Thời gian", bg="#fff", font=("Georgia", 10, "bold")).grid(row=0, column=1)

        for i, sc in enumerate(HIGH_SCORES):
            m = int(sc // 60)
            s = int(sc % 60)
            ms = int((sc - int(sc)) * 100)
            ts = f"{m:02d}:{s:02d}.{ms:02d}"

            tk.Label(frame, text=f"#{i+1}", bg="#fff").grid(row=i+1, column=0)
            tk.Label(frame, text=ts, bg="#fff").grid(row=i+1, column=1)

    tk.Button(dialog, text="Đóng", command=dialog.destroy).pack(pady=15)
    root.wait_window(dialog)'''
# 💡 Thay thế hàm show_high_score cũ bằng hàm sau:
def show_high_score():
    global HIGH_SCORES

    dialog = tk.Toplevel(root)
    dialog.title("🏆 High Score - Top 5")
    dialog.geometry("600x400") # Tăng kích thước cửa sổ để chứa tên và ảnh
    dialog.configure(bg="#fdf8e4")
    dialog.transient(root)
    dialog.grab_set()
    
    tk.Label(dialog, text="Bảng Xếp Hạng", font=("Georgia", 16, "bold"),
             bg="#fdf8e4", fg="#333").pack(pady=20)

    # Khung chứa bảng xếp hạng
    frame = tk.Frame(dialog, bg="#ffffff", pady=10)
    frame.pack(pady=10, padx=20, fill="x")

    if not HIGH_SCORES:
        tk.Label(frame, text="Chưa có điểm cao nào.", bg="#fff").pack(pady=20)
    else:
        # Tiêu đề cột
        tk.Label(frame, text="Hạng", bg="#fff", font=("Georgia", 10, "bold")).grid(row=0, column=0, padx=10)
        tk.Label(frame, text="Ảnh", bg="#fff", font=("Georgia", 10, "bold")).grid(row=0, column=1, padx=10)
        tk.Label(frame, text="Tên Người Chơi", bg="#fff", font=("Georgia", 10, "bold")).grid(row=0, column=2, padx=10)
        tk.Label(frame, text="Thời gian", bg="#fff", font=("Georgia", 10, "bold")).grid(row=0, column=3, padx=10)

        for i, sc_entry in enumerate(HIGH_SCORES):
            score = sc_entry['score']
            name = sc_entry['name']
            path = sc_entry['image_path']
            
            # Định dạng thời gian
            m = int(score // 60)
            s = int(score % 60)
            ms = int((score - int(score)) * 100)
            ts = f"{m:02d}:{s:02d}.{ms:02d}"

            # Hiển thị Rank và Thời gian
            tk.Label(frame, text=f"#{i+1}", bg="#fff").grid(row=i+1, column=0, padx=10, pady=5)
            tk.Label(frame, text=name, bg="#fff").grid(row=i+1, column=2, padx=10)
            tk.Label(frame, text=ts, bg="#fff").grid(row=i+1, column=3, padx=10)

            # Xử lý hiển thị ảnh (nếu có)
            image_label = tk.Label(frame, bg="#fff", width=50, height=50)
            image_label.grid(row=i+1, column=1, padx=10, pady=5)

            if path and os.path.exists(path):
                try:
                    img = Image.open(path)
                    img = img.resize((40, 40)) # Kích thước nhỏ hơn cho bảng điểm
                    img_tk = ImageTk.PhotoImage(img)
                    
                    image_label.config(image=img_tk)
                    image_label.image = img_tk
                except Exception:
                    image_label.config(text="❌") # Hiển thị lỗi nếu không load được ảnh
            else:
                image_label.config(text="👤") # Ảnh đại diện mặc định

    tk.Button(dialog, text="Đóng", command=dialog.destroy).pack(pady=15)
    root.wait_window(dialog)



def show_exit_dialog():
    """Shows the exit-popup with 3 buttons (NEW)."""
    stop_timer()  # FULL STOP

    dialog = tk.Toplevel(root)
    dialog.title("Exit")
    dialog.geometry("360x170")
    dialog.configure(bg="#fdf8e4")
    dialog.transient(root)
    dialog.grab_set()

    tk.Label(dialog, text="Bạn muốn làm gì?", font=("Georgia", 12),
             bg="#fdf8e4").pack(pady=15)

    frame = tk.Frame(dialog, bg="#fdf8e4")
    frame.pack()

    tk.Button(frame, text="▶️ Return to Game", width=18,
              command=lambda: [dialog.destroy(), continue_timer()],
              bg="#a3d9a5").grid(row=0, column=0, padx=5)

    tk.Button(frame, text="🏠 Return to Main Menu", width=18,
              command=lambda: [dialog.destroy(), show_main_menu()],
              bg="#fff3b0").grid(row=1, column=0, padx=5, pady=5)

    tk.Button(frame, text="❌ Exit Game", width=18,
              command=lambda: [dialog.destroy(), just_exit()],
              bg="#f8d7da").grid(row=2, column=0, padx=5)

    dialog.protocol("WM_DELETE_WINDOW", lambda: [dialog.destroy(), continue_timer()])
    root.wait_window(dialog)
GAME_OVER_BG = "C:\WebScrapingLibrary_NeoM2\Dark-Souls-You-Died.jpg"   # <-- rename to match your file


def show_game_over_screen(reason):
    stop_game()

    # Clear old widgets
    for w in root.winfo_children():
        w.destroy()

    # Create canvas for background image
    canvas = tk.Canvas(root, highlightthickness=0, bd=0)
    canvas.pack(fill="both", expand=True)

    # Load & resize background
    bg = Image.open(GAME_OVER_BG)
    bg = bg.resize((root.winfo_width(), root.winfo_height()), Image.LANCZOS)
    bg_tk = ImageTk.PhotoImage(bg)

    # Draw background
    canvas.bg_img = bg_tk
    canvas.create_image(0, 0, anchor="nw", image=bg_tk)

    # === TEXT: YOU DIED ===
    canvas.create_text(
        root.winfo_width() // 2,
        80,
        text="💀💀💀💀💀",
        fill="#A00000",
        font=("Georgia", 48, "bold")
    )

    # === DEATH REASON ===
    canvas.create_text(
        root.winfo_width() // 2,
        160,
        text=reason,
        fill="white",
        font=("Georgia", 25),
        width=600
    )

    # ===== BUTTONS =====

    # Play again
    play_again_btn = tk.Button(
        root,
        text="Play again",
        font=("Georgia", 16, "bold"),
        bg="#dc3545",
        fg="white",
        command=show_game_screen
    )
    canvas.create_window(
        root.winfo_width() // 2,
        root.winfo_height() // 2 + 120,
        window=play_again_btn
    )

    # Music controls frame
    music_frame = tk.Frame(root, bg="#000000")
    canvas.create_window(
        root.winfo_width() - 100,
        40,
        anchor="ne",
        window=music_frame
    )

    # Play music
    play_btn = tk.Button(
        music_frame,
        text="▶️Play",
        command=start_background_music,
        bg="#a3d9a5",
        font=("Georgia", 9)
    )
    play_btn.pack(side="left", padx=5)

    # Stop music
    stop_btn = tk.Button(
        music_frame,
        text="⏹️Stop",
        command=stop_background_music,
        bg="#f8d7da",
        font=("Georgia", 9)
    )
    stop_btn.pack(side="left", padx=5)
    # <--- KẾT THÚC THÊM NÚT NHẠC ---


# ===============================================================
#  EXIT FUNCTION
# ===============================================================

def just_exit():
    save_high_scores_to_file()    # SAVE before exit
    stop_game()
    root.destroy()

# ===============================================================
#  MAIN WINDOW EXECUTION
# ===============================================================
def show_exit_dialog2():
    """Shows the exit-popup with 3 buttons (NEW)."""
    stop_timer()  # FULL STOP

    dialog = tk.Toplevel(root)
    dialog.title("Exit")
    dialog.geometry("360x170")
    dialog.configure(bg="#fdf8e4")
    dialog.transient(root)
    dialog.grab_set()

    tk.Label(dialog, text="Bạn muốn thoát game?", font=("Georgia", 12),
             bg="#fdf8e4").pack(pady=15)

    frame = tk.Frame(dialog, bg="#fdf8e4")
    frame.pack()

    tk.Button(frame, text="❌Không", width=18,
              command=lambda: [dialog.destroy(), continue_timer()],
              bg="#f8d7da").grid(row=0, column=0, padx=5)

    tk.Button(frame, text="✅Có!", width=18,
              command=lambda: [dialog.destroy(), just_exit()],
              bg="#f8d7da").grid(row=2, column=0, padx=5)

    dialog.protocol("WM_DELETE_WINDOW", lambda: [dialog.destroy(), continue_timer()])
    root.wait_window(dialog)
# ================== CLOWN & FIRE SYSTEM (AUTO-MERGED) ==================
CLOWN_EMOJI = "🤡"
FIRE_EMOJI = "🔥"

CLOWN_FIRST_APPEAR = 60
CLOWN_INTERVAL = 20
CLOWN_BURN_INTERVAL = 1

clown_last_spawn = -1
clown_spawn_loop_id = None
clown_burn_loop_id = None

def add_clown_emoji():
    pw = entry_password.get()
    pw += CLOWN_EMOJI
    entry_password.delete(0, tk.END)
    entry_password.insert(0, pw)

def clown_spawn_loop():
    global clown_last_spawn, clown_spawn_loop_id
    if not game_running:
        return
    elapsed = get_current_elapsed_time()
    if clown_last_spawn == -1 and elapsed >= CLOWN_FIRST_APPEAR:
        add_clown_emoji()
        clown_last_spawn = elapsed
    if clown_last_spawn >= 0 and elapsed - clown_last_spawn >= CLOWN_INTERVAL:
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
            show_game_over_screen(" Joker 🤡 đã bắt cóc mẹ bạn! ")
            return
        while left >= 0 and chars[left] == FIRE_EMOJI:
            left -= 1
        if left < 0:
            show_game_over_screen("Bạn đã chết cháy!🔥")
            return
        if chars[left] != FIRE_EMOJI:
            chars[left] = FIRE_EMOJI

            all_burned = False
    entry_password.delete(0, tk.END)
    entry_password.insert(0, "".join(chars))
    if all_burned:
        show_game_over_screen("Bạn đã bị Joker 🤡 đốt bỏng đít!")
        return
    clown_burn_loop_id = root.after(CLOWN_BURN_INTERVAL * 1000, clown_burn_loop)

# Patch stop_game
_old_stop_game = stop_game
def stop_game():
    global clown_spawn_loop_id, clown_burn_loop_id
    if clown_spawn_loop_id:
        root.after_cancel(clown_spawn_loop_id)
        clown_spawn_loop_id = None
    if clown_burn_loop_id:
        root.after_cancel(clown_burn_loop_id)
        clown_burn_loop_id = None
    _old_stop_game()

# Patch show_game_screen
_old_show_game_screen = show_game_screen
def show_game_screen(initial_password=""):
    global clown_last_spawn
    _old_show_game_screen(initial_password)
    clown_last_spawn = -1
    clown_spawn_loop()
    clown_burn_loop()
root = tk.Tk()
root.title("The Password Game")
root.geometry("800x600")
root.configure(bg="#fdf8e4")

root.protocol("WM_DELETE_WINDOW", show_exit_dialog2 )

load_high_scores()  # LOAD HIGH SCORES ON START
show_main_menu()

root.mainloop()





