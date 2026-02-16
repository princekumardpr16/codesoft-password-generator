import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import string
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BG_PATH = os.path.join(BASE_DIR, "bg.png")


def generate_password():
    try:
        length = int(length_entry.get())
        if length < 4:
            messagebox.showerror("Error", "Password length must be at least 4")
            return
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number")
        return

    sets = []
    if var_upper.get():
        sets.append(string.ascii_uppercase)
    if var_lower.get():
        sets.append(string.ascii_lowercase)
    if var_digits.get():
        sets.append(string.digits)
    if var_symbols.get():
        sets.append(string.punctuation)

    if not sets:
        messagebox.showerror("Error", "Select at least one option")
        return

    password_chars = [random.choice(s) for s in sets]
    all_chars = "".join(sets)

    while len(password_chars) < length:
        password_chars.append(random.choice(all_chars))

    random.shuffle(password_chars)
    password = "".join(password_chars)

    result_entry.delete(0, tk.END)
    result_entry.insert(0, password)
    update_strength(password)

def update_strength(password):
    score = 0
    if any(c.islower() for c in password): score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1
    if len(password) >= 12: score += 1

    if score <= 2:
        strength_label.config(text="Strength: Weak", fg="red")
    elif score == 3:
        strength_label.config(text="Strength: Medium", fg="orange")
    else:
        strength_label.config(text="Strength: Strong", fg="green")

def copy_password():
    pwd = result_entry.get()
    if not pwd:
        messagebox.showwarning("Warning", "Generate password first")
        return
    root.clipboard_clear()
    root.clipboard_append(pwd)
    messagebox.showinfo("Copied", "Password copied to clipboard")


root = tk.Tk()
root.title("Password Generator")
root.geometry("450x550")
root.resizable(False, False)


bg_img = Image.open(BG_PATH).resize((450, 550))
bg_photo = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


card = tk.Frame(root, bg="white")
card.place(relx=0.5, rely=0.5, anchor="center", width=360, height=460)


tk.Label(
    card,
    text="🔐 Password Generator",
    font=("Segoe UI", 18, "bold"),
    bg="white"
).pack(pady=15)


tk.Label(card, text="Password Length", bg="white", font=("Segoe UI", 10)).pack()
length_entry = tk.Entry(card, width=10, justify="center", font=("Segoe UI", 11))
length_entry.pack(pady=6)
length_entry.insert(0, "12")


var_upper = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=False)

options = tk.Frame(card, bg="white")
options.pack(pady=10)

tk.Checkbutton(options, text=" Uppercase (A-Z)", variable=var_upper, bg="white").pack(anchor="w")
tk.Checkbutton(options, text=" Lowercase (a-z)", variable=var_lower, bg="white").pack(anchor="w")
tk.Checkbutton(options, text=" Numbers (0-9)", variable=var_digits, bg="white").pack(anchor="w")
tk.Checkbutton(options, text=" Symbols (!@#)", variable=var_symbols, bg="white").pack(anchor="w")


tk.Button(
    card,
    text="Generate Password",
    bg="#4CAF50",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    width=26,
    command=generate_password
).pack(pady=12)


result_entry = tk.Entry(card, width=32, justify="center", font=("Consolas", 11))
result_entry.pack(pady=5)

strength_label = tk.Label(card, text="Strength: ", bg="white", font=("Segoe UI", 10))
strength_label.pack(pady=4)


tk.Button(
    card,
    text="Copy to Clipboard",
    bg="#2196F3",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    width=26,
    command=copy_password
).pack(pady=10)

root.mainloop()
