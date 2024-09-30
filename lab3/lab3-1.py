import asyncio
import tkinter as tk
from tkinter import scrolledtext


async def factorial(name, number, output_text):
    f = 1
    for i in range(2, number + 1):
        output_text.insert(tk.END, f"Task {name}: Compute factorial({i})...\n")
        output_text.see(tk.END)
        output_text.update()
        await asyncio.sleep(1)
        f *= i
    output_text.insert(tk.END, f"Task {name}: factorial({number}) = {f}\n")
    output_text.see(tk.END)
    output_text.update()


async def main(output_text):
    await asyncio.gather(
        factorial("A", 2, output_text),
        factorial("B", 3, output_text),
        factorial("C", 4, output_text),
    )


def start_computation():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(output_text))
    loop.close()


root = tk.Tk()
root.title("Factorial Computation")


output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
output_text.pack(padx=10, pady=10)


start_button = tk.Button(root, text="Start Computation", command=start_computation)
start_button.pack(pady=10)


root.mainloop()