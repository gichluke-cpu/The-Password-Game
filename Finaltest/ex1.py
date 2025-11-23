import tkinter as tk
import string
import pygame
def check_rules(event=None):
    """Kiểm tra mật khẩu ngay khi nhập"""
    password = entry_password.get()
    length_label.config(text=str(len(password)))  # Cập nhật số ký tự
    rules = {
        
        "Ít nhất một chữ hoa": any(c.isupper() for c in password),
        "Ít nhất một số": any(c.isdigit() for c in password),
        "Ít nhất một ký tự đặc biệt": any(c in string.punctuation for c in password),
        "Tổng các số phải bằng 25": sum(int(c) for c in password if c.isdigit()) == 25,
        "Không chứa từ 'password'": "password" not in password.lower(),
    }
    for rule, label in rule_labels.items():
        if rules[rule]:
            label.config(text=f"✔ {rule}", fg="green", bg="#d4edda")
        else:
            label.config(text=f"✖ {rule}", fg="red", bg="#f8d7da")
# Giao diện ứng dụng
root = tk.Tk()
root.title("The Password Game")
root.geometry("500x400")
root.configure(bg="#fdf8e4")
# Tiêu đề
tk.Label(root, text="* The Password Game", font=("Georgia", 18, "bold"),
bg="#fdf8e4").pack(pady=5)
tk.Label(root, text="Please choose a password", font=("Georgia", 12),
bg="#fdf8e4").pack()
# Ô nhập mật khẩu + số ký tự
frame_input = tk.Frame(root, bg="#fdf8e4")
frame_input.pack(pady=15)
entry_password = tk.Entry(frame_input, width=30, font=("Georgia", 12))
entry_password.pack(side="left", padx=5)
entry_password.bind("<KeyRelease>", check_rules)
length_label = tk.Label(frame_input, text="0", font=("Georgia", 12), bg="#fdf8e4")
length_label.pack(side="left")

# Hiển thị trạng thái kiểm tra quy tắc
frame_rules = tk.Frame(root, bg="#fdf8e4")
frame_rules.pack()
rule_labels = {}
for rule in ["Ít nhất một chữ hoa", "Ít nhất một số", "Ít nhất một ký tự đặc biệt", "Tổng các số phải bằng 25", "Không chứa từ 'password'"]:
    label = tk.Label(frame_rules, text=f"✖ {rule}", fg="red", bg="#f8d7da",
font=("Georgia", 10), width=40, anchor="w", padx=10, pady=3)
    label.pack(pady=2, fill="x")
    rule_labels[rule] = label
root.mainloop()