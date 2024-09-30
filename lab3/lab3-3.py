import tkinter as tk
from tkinter import messagebox
from collections import namedtuple
import asyncio
from concurrent.futures import FIRST_COMPLETED
import aiohttp

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query')
)


async def fetch_ip(service):
    async with aiohttp.ClientSession() as session:
        async with session.get(service.url) as response:
            data = await response.json()
            return data[service.ip_attr]


async def asynchronous():
    tasks = [asyncio.create_task(fetch_ip(service)) for service in SERVICES]

    done, pending = await asyncio.wait(tasks, return_when=FIRST_COMPLETED)

    for task in done:
        try:
            ip = task.result()
            return ip
        except Exception as e:
            print(f"Error fetching IP: {e}")

    for task in pending:
        task.cancel()


def get_ip():
    try:
        ip = asyncio.run(asynchronous())
        ip_label.config(text=f"Your IP address is: {ip}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get IP address: {e}")


root = tk.Tk()
root.title("Get IP Address")

button = tk.Button(root, text="Get IP", command=get_ip)
button.pack(pady=10)

ip_label = tk.Label(root, text="", font=("Arial", 14))
ip_label.pack(pady=10)

root.mainloop()