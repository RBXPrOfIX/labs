import os
import re
import threading
import tkinter as tk
from tkinter import scrolledtext

received_packages = re.compile(r"(\d) received")
status = ("no response", "alive but losses", "alive")


def ping_ip(ip, output_text):
    ping_out = os.popen(f"ping -q -c2 {ip}", "r")
    output_text.insert(tk.END, f"... pinging {ip}\n")
    while True:
        line = ping_out.readline()
        if not line:
            break
        n_received = received_packages.findall(line)
        if n_received:
            output_text.insert(tk.END, f"{ip}: {status[int(n_received[0])]}\n")
            output_text.see(tk.END)


def start_pinging(output_text):
    for suffix in range(20, 30):
        ip = f"192.168.178.{suffix}"
        thread = threading.Thread(target=ping_ip, args=(ip, output_text))
        thread.start()


def main():
    root = tk.Tk()
    root.title("IP Address Pinger")

    output_text = scrolledtext.ScrolledText(root, width=50, height=20)
    output_text.pack(padx=10, pady=10)

    start_button = tk.Button(root, text="Start Pinging", command=lambda: start_pinging(output_text))
    start_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()