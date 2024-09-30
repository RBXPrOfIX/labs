import multiprocessing
import tkinter as tk
from tkinter import messagebox


def worker(lst):
    lst.append('item')


def run_processes():
    manager = multiprocessing.Manager()
    LIST = manager.list()

    processes = [
        multiprocessing.Process(target=worker, args=(LIST,))
        for _ in range(5)
    ]
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    result = " ".join(LIST)
    messagebox.showinfo("Результат", f"Список после выполнения процессов: {result}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Многопроцессорное приложение")

    # Создаем кнопку для запуска процессов
    start_button = tk.Button(root, text="Запустить процессы", command=run_processes)
    start_button.pack(pady=20)

    root.mainloop()