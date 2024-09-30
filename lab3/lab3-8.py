import urllib.request
import time
import threading
import tkinter as tk
from tkinter import messagebox

urls = [
    'https://www.yandex.ru', 'https://www.google.com',
    'https://habrahabr.ru', 'https://www.python.org',
    'https://isocpp.org',
]


def read_url(url):
    with urllib.request.urlopen(url) as u:
        return u.read()


def fetch_url(url):
    read_url(url)


def run_without_threads():
    start = time.time()
    for url in urls:
        read_url(url)
    time_taken = time.time() - start
    messagebox.showinfo("Result", f"Time taken without threads: {time_taken:.4f} seconds")


def run_with_threads():
    start = time.time()
    threads = []
    for url in urls:
        thread = threading.Thread(target=fetch_url, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    time_taken = time.time() - start
    messagebox.showinfo("Result", f"Time taken with threads: {time_taken:.4f} seconds")


root = tk.Tk()
root.title("URL Fetcher")

btn_without_threads = tk.Button(root, text="Run without threads", command=run_without_threads)
btn_with_threads = tk.Button(root, text="Run with threads", command=run_with_threads)

btn_without_threads.pack(pady=10)
btn_with_threads.pack(pady=10)

root.mainloop()