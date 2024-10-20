import tkinter as tk
import random
from tkinter import messagebox
import os
import sys

class RussianRoulette:
    def __init__(self, root):
        self.root = root
        self.root.title("Russian Roulette")
        self.root.configure(bg="#2E2E2E")

        self.is_kid_mode = tk.BooleanVar(value=False)

        self.buttons = []
        for i in range(10):
            button = tk.Button(root, text="?", width=10, height=5,
                               bg="#3C3F41", fg="#FFFFFF",
                               activebackground="#5C5F61", activeforeground="#FFFFFF",
                               font=("Arial", 14),
                               command=lambda i=i: self.check_result(i))
            button.grid(row=i // 5, column=i % 5, padx=10, pady=10)
            self.buttons.append(button)

        self.shuffle_cells()

        self.footer_label = tk.Label(root, text="Version 0.1 | Authors: Scody & Chel",
                                      bg="#2E2E2E", fg="#FFFFFF", font=("Arial", 10))
        self.footer_label.grid(row=2, column=0, columnspan=5, pady=(10, 0))

        self.kid_mode_label = tk.Label(root, text="Children's mode", bg="#2E2E2E", fg="#FFFFFF", font=("Arial", 10))
        self.kid_mode_label.grid(row=3, column=0, columnspan=5, pady=(10, 0))

        self.kid_mode_scale = tk.Scale(root, from_=0, to=1, orient=tk.HORIZONTAL, length=200,
                                        bg="#2E2E2E", fg="#FFFFFF", troughcolor="#5C5F61", 
                                        command=self.toggle_kid_mode)
        self.kid_mode_scale.grid(row=4, column=0, columnspan=5, pady=(0, 10))

    def toggle_kid_mode(self, value):
        self.is_kid_mode.set(int(value) == 1)

    def shuffle_cells(self):
        
        self.safe_cells = random.sample(range(10), 6)
        self.dangerous_cells = [i for i in range(10) if i not in self.safe_cells]

    def check_result(self, index):
        if index in self.dangerous_cells:
            if self.is_kid_mode.get():
                messagebox.showinfo("Game over", "You've lost! But don't worry, it's just a game.")
            else:
                messagebox.showinfo("Game over", "You've lost! The computer will be turned off.")
                self.shutdown_computer()
        else:
            messagebox.showinfo("Lucky you!", "It's safe!")
            self.buttons[index].config(state="disabled", bg="#2E7D32", fg="#FFFFFF")
            if all(self.buttons[i].cget('state') == 'disabled' for i in self.safe_cells):
                messagebox.showinfo("Congratulations!", "You have passed the game!")
                self.root.quit()

    def shutdown_computer(self):
        if sys.platform == "win32":
            os.system("shutdown /s /t 1")
        elif sys.platform == "darwin":
            os.system("sudo shutdown -h now")
        elif sys.platform == "linux":
            os.system("sudo shutdown -h now")
root = tk.Tk()

root.configure(bg="#2E2E2E")

game = RussianRoulette(root)
root.mainloop()
