import tkinter as tk
from PIL import Image, ImageTk
import threading
import time
import pygame
import random


def on_closing():
    print("Окно не может быть закрыто через кнопку 'Закрыть'.")


def play_gif(root, label, frames):
    frame_index = 0

    def update_frame():
        nonlocal frame_index
        label.imgtk = frames[frame_index]  # Сохраняем ссылку на изображение
        label.configure(image=frames[frame_index])
        frame_index = (frame_index + 1) % len(frames)
        root.after(100, update_frame)  # Задержка между кадрами (100 мс)
    update_frame()


def create_new_window(frames):
    new_root = tk.Toplevel()
    new_root.title("Незакрываемое окно")
    new_root.protocol("WM_DELETE_WINDOW", on_closing)
    new_root.resizable(False, False)  # Запрет изменения размеров окна

    # Генерация случайных координат для нового окна
    screen_width = new_root.winfo_screenwidth()
    screen_height = new_root.winfo_screenheight()
    x = random.randint(0, screen_width - 300)  # 300 - примерная ширина окна
    y = random.randint(0, screen_height - 200)  # 200 - примерная высота окна
    new_root.geometry(f"+{x}+{y}")

    new_label = tk.Label(new_root)
    new_label.pack(pady=20)

    play_gif(new_root, new_label, frames)


def create_windows_periodically(root, frames):
    while True:
        root.after(2500, create_new_window, frames)  # Создаем новое окно каждые 0.5 секунд
        time.sleep(0.5)  # Ждем 0.5 секунды перед созданием нового окна


def play_music():
    pygame.mixer.init()
    pygame.mixer.music.load('static/chipi-chapa.mp3')
    pygame.mixer.music.play(-1)  # Воспроизводим музыку в цикле


root = tk.Tk()
root.title("Незакрываемое окно")
root.protocol("WM_DELETE_WINDOW", on_closing)
root.resizable(False, False)  # Запрет изменения размеров окна

label = tk.Label(root)
label.pack(pady=20)

gif_path = 'static/chipi-chapa.gif'
gif = Image.open(gif_path)
frames = []

try:
    while True:
        frames.append(ImageTk.PhotoImage(gif.copy()))
        gif.seek(len(frames))  # Переход к следующему кадру
except EOFError:
    pass  # Конец GIF

play_gif(root, label, frames)
threading.Thread(target=create_windows_periodically, args=(root, frames), daemon=True).start()
threading.Thread(target=play_music, daemon=True).start()

root.mainloop()