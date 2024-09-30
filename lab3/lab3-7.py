import threading
import time
import random
import tkinter as tk
from tkinter import ttk


def sum_array_part(array, start, end, result):
    result.append(sum(array[start:end]))


def calculate_sum(N, array, result_label):
    start_time = time.time()

    threads = []
    results = []
    chunk_size = len(array) // N

    for i in range(N):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < N - 1 else len(array)
        result = []
        thread = threading.Thread(target=sum_array_part, args=(array, start, end, result))
        threads.append(thread)
        results.append(result)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(sum(result) for result in results)
    end_time = time.time()

    result_label.config(text=f"N = {N}, Total sum: {total_sum}, Time taken: {end_time - start_time:.4f} seconds")


def main():
    array_size = 10000000
    array = [random.randint(1, 100) for _ in range(array_size)]

    root = tk.Tk()
    root.title("Array Sum Calculator")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="Select number of threads (N):").grid(row=0, column=0, sticky=tk.W)

    N_values = [1, 2, 4, 8, 16]
    N_var = tk.IntVar(value=N_values[0])
    N_combobox = ttk.Combobox(frame, textvariable=N_var, values=N_values)
    N_combobox.grid(row=0, column=1, sticky=tk.W)

    result_label = ttk.Label(frame, text="")
    result_label.grid(row=1, column=0, columnspan=2, sticky=tk.W)

    def on_calculate():
        N = N_var.get()
        calculate_sum(N, array, result_label)

    calculate_button = ttk.Button(frame, text="Calculate", command=on_calculate)
    calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()