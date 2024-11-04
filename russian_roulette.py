import tkinter as tk
import random
import os
import sys
import pygame
from tkinter import messagebox

class RussianRoulette:
    def __init__(self, root):
        self.root = root
        self.root.title("Russian Roulette")
        self.root.configure(bg="#2E2E2E")
        self.root.resizable(False, False)

        pygame.mixer.init()

        self.language = tk.StringVar(value="en")
        self.is_kid_mode = tk.BooleanVar(value=False)

        # Переключатель языка
        self.language_label = tk.Label(root, text="Language:", bg="#2E2E2E", fg="#FFFFFF", font=("Arial", 10))
        self.language_label.grid(row=0, column=0, columnspan=2, pady=(10, 0))

        self.language_select = tk.OptionMenu(root, self.language, "en", "ru", command=self.update_texts)
        self.language_select.config(bg="#3C3F41", fg="#FFFFFF", font=("Arial", 10))
        self.language_select.grid(row=0, column=2, columnspan=3, pady=(10, 0))

        # Создание кнопок (карточек)
        self.buttons = []
        for i in range(10):
            button = tk.Button(root, text="?", width=10, height=5,
                               bg="#3C3F41", fg="#FFFFFF",
                               activebackground="#5C5F61", activeforeground="#FFFFFF",
                               font=("Arial", 14),
                               command=lambda i=i: self.flip_card(i))
            button.grid(row=i // 5 + 1, column=i % 5, padx=10, pady=10)
            self.buttons.append(button)

        self.shuffle_cells()

        self.footer_label = tk.Label(root, text="Version 0.2 | Authors: Scody & Chel",
                                     bg="#2E2E2E", fg="#FFFFFF", font=("Arial", 10))
        self.footer_label.grid(row=4, column=0, columnspan=5, pady=(10, 0))

        # Метка и ползунок для выбора детского режима
        self.kid_mode_label = tk.Label(root, text="Children's mode", bg="#2E2E2E", fg="#FFFFFF", font=("Arial", 10))
        self.kid_mode_label.grid(row=5, column=0, columnspan=5, pady=(10, 0))

        self.kid_mode_scale = tk.Scale(root, from_=0, to=1, orient=tk.HORIZONTAL, length=200,
                                       bg="#2E2E2E", fg="#FFFFFF", troughcolor="#5C5F61",
                                       command=self.toggle_kid_mode)
        self.kid_mode_scale.grid(row=6, column=0, columnspan=5, pady=(0, 10))

        # Установка обработчика закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_texts(self, value):
        """Обновляет текст интерфейса в зависимости от выбранного языка."""
        if self.language.get() == "en":
            self.root.title("Russian Roulette")
            self.footer_label.config(text="Version 0.1 | Authors: Scody & Chel")
            self.kid_mode_label.config(text="Children's mode")
        elif self.language.get() == "ru":
            self.root.title("Русская Рулетка")
            self.footer_label.config(text="Версия 0.1 | Авторы: Scody и Chel")
            self.kid_mode_label.config(text="Детский режим")

    def toggle_kid_mode(self, value):
        """Обработка переключения детского режима."""
        self.is_kid_mode.set(int(value) == 1)

    def shuffle_cells(self):
        """Генерация безопасных и опасных ячеек."""
        self.safe_cells = random.sample(range(10), 6)
        self.dangerous_cells = [i for i in range(10) if i not in self.safe_cells]

    def flip_card(self, index):
        """Запуск анимации переворота карточки и воспроизведение звука."""
        pygame.mixer.music.load("sounds/click.mp3")
        pygame.mixer.music.play()

        self.animate_flip(index)

    def animate_flip(self, index):
        """Анимация сжимания карточки."""
        def shrink(step):
            if step <= 5:
                self.buttons[index].config(width=10 - step)
                self.root.after(50, lambda: shrink(step + 1))
            else:
                self.reveal_card(index)

        shrink(0)

    def reveal_card(self, index):
        """Изменение содержимого карточки после переворота."""
        if index in self.dangerous_cells:
            self.buttons[index].config(text="💀", bg="#D32F2F", fg="#FFFFFF")
            if not self.is_kid_mode.get():
                self.shutdown_computer()
        else:
            self.buttons[index].config(text="✅", bg="#2E7D32", fg="#FFFFFF")
            self.buttons[index].config(state="disabled")

            # Проверка, нашёл ли игрок все безопасные карточки
            if all(self.buttons[i].cget('state') == 'disabled' for i in self.safe_cells):
                self.end_game()

        self.root.after(50, lambda: self.animate_grow(index))

    def animate_grow(self, index):
        """Анимация расширения карточки."""
        def grow(step):
            if step <= 5:
                self.buttons[index].config(width=5 + step)
                self.root.after(50, lambda: grow(step + 1))

        grow(0)

    def end_game(self):
        """Завершение игры при нахождении всех безопасных карточек."""
        messagebox.showinfo(self.get_translation("Congratulations!"), self.get_translation("You've won the game!"))
        self.root.quit()

    def get_translation(self, text):
        """Функция для перевода текста в зависимости от выбранного языка."""
        translations = {
            "en": {
                "Congratulations!": "Congratulations!",
                "You've won the game!": "You've won the game!",
                "Warning": "Warning",
                "Closing the game will restart your computer. Do you want to continue?": "Do you really want to exit the game?",
                "Yes - Restart": "Yes - Restart",
                "No - Continue": "No - Continue"
            },
            "ru": {
                "Congratulations!": "Поздравляем!",
                "You've won the game!": "Вы выиграли игру!",
                "Warning": "Предупреждение",
                "Closing the game will restart your computer. Do you want to continue?": "Вы действительно хотите выйти из игры?",
                "Yes - Restart": "Да - Перезагрузить",
                "No - Continue": "Нет - Продолжить"
            }
        }
        return translations[self.language.get()][text]

    def shutdown_computer(self):
        """Выключение компьютера при проигрыше в обычном режиме."""
        if sys.platform == "win32":
            os.system("shutdown /s /t 1")
        elif sys.platform == "darwin":
            os.system("sudo shutdown -h now")
        elif sys.platform == "linux":
            os.system("sudo shutdown -h now")

    def on_close(self):
        """Показ пользовательского диалога с кнопками 'Перезагрузить' и 'Продолжить игру'."""
        warning_message = self.get_translation("Closing the game will restart your computer. Do you want to continue?")
        
        # Создаем новое окно предупреждения
        custom_dialog = tk.Toplevel(self.root)
        custom_dialog.title(self.get_translation("Warning"))
        custom_dialog.geometry("300x150")
        custom_dialog.configure(bg="#2E2E2E")
        custom_dialog.resizable(False, False)  # Блокируем изменение размера
        custom_dialog.protocol("WM_DELETE_WINDOW", lambda: None)  # Блокируем закрытие окна
        
        # Текст предупреждения
        label = tk.Label(custom_dialog, text=warning_message, bg="#2E2E2E", fg="#FFFFFF", font=("Arial", 10))
        label.pack(pady=20)
        
        # Кнопка "Да - Перезагрузить компьютер"
        restart_button = tk.Button(custom_dialog, text=self.get_translation("Yes - Restart"),
                                   command=lambda: [custom_dialog.destroy(), self.shutdown_computer()],
                                   bg="#D32F2F", fg="#FFFFFF", font=("Arial", 10), width=12)
        restart_button.pack(side="left", padx=10, pady=10)
        
        # Кнопка "Нет - Продолжить игру"
        continue_button = tk.Button(custom_dialog, text=self.get_translation("No - Continue"),
                                    command=custom_dialog.destroy,
                                    bg="#2E7D32", fg="#FFFFFF", font=("Arial", 10), width=12)
        continue_button.pack(side="right", padx=10, pady=10)

# Создание графического интерфейса
root = tk.Tk()
root.configure(bg="#2E2E2E")

game = RussianRoulette(root)
root.mainloop()
