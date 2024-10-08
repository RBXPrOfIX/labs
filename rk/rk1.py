import threading
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from queue import Queue


class AssemblyMachine:
    def __init__(self, machine_id, component_type, assembly_time, total_components):
        self.machine_id = machine_id
        self.component_type = component_type
        self.assembly_time = assembly_time
        self.total_components = total_components
        self.total_time = 0

    def assemble(self):
        time.sleep(self.assembly_time)
        self.total_time += self.assembly_time

    def start_production(self, output_queue):
        for _ in range(self.total_components):
            self.assemble()
        message = f"Machine {self.machine_id} finished assembling {self.total_components} {self.component_type} in {self.total_time} seconds."
        output_queue.put(message)
        print(message)


class FinalAssemblyMachine:
    def __init__(self, machine_id):
        self.machine_id = machine_id
        self.final_time = 0

    def assemble_final_product(self, components, output_queue):
        message = f"Final machine {self.machine_id} assembling final product with components: {components} in {self.final_time} seconds."
        output_queue.put(message)
        print(message)


class Factory:
    def __init__(self):
        self.machines = []
        self.final_machine = None

    def add_machine(self, machine):
        self.machines.append(machine)

    def set_final_machine(self, final_machine):
        self.final_machine = final_machine

    def start_production(self, output_queue):
        threads = []
        for machine in self.machines:
            thread = threading.Thread(target=machine.start_production, args=(output_queue,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        components = {machine.component_type: machine.total_components for machine in self.machines}
        final_time = max(machine.total_time for machine in self.machines) + 0.5
        self.final_machine.final_time = final_time
        self.final_machine.assemble_final_product(components, output_queue)


class FactoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Factory Production Simulator")

        self.factory = Factory()
        self.machine_entries = []
        self.final_machine_frame = None
        self.output_queue = Queue()

        self.output_text = scrolledtext.ScrolledText(root, width=80, height=10)
        self.output_text.pack(pady=10)

        self.add_machine_button = tk.Button(root, text="Добавить машину", command=self.add_machine)
        self.add_machine_button.pack(pady=10)

        self.set_final_machine_button = tk.Button(root, text="Назначить финальную машину", command=self.set_final_machine, state=tk.DISABLED)
        self.set_final_machine_button.pack(pady=10)

        self.start_button = tk.Button(root, text="Запустить сборку", command=self.start_production, state=tk.DISABLED)
        self.start_button.pack(pady=10)

        self.machine_frame = tk.Frame(root)
        self.machine_frame.pack(pady=10)

        self.machine_scroll = scrolledtext.ScrolledText(self.machine_frame, width=80, height=10)
        self.machine_scroll.pack(pady=10)

        self.update_output()

    def add_machine(self):
        machine_id = len(self.machine_entries) + 1
        frame = tk.Frame(self.machine_scroll)
        frame.pack(pady=5)

        tk.Label(frame, text=f"Машина {machine_id}").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame, text="Тип детали:").grid(row=0, column=1, padx=5, pady=5)
        component_type_entry = tk.Entry(frame)
        component_type_entry.grid(row=0, column=2, padx=5, pady=5)

        tk.Label(frame, text="Время сборки (сек):").grid(row=0, column=3, padx=5, pady=5)
        assembly_time_entry = tk.Entry(frame)
        assembly_time_entry.grid(row=0, column=4, padx=5, pady=5)

        tk.Label(frame, text="Количество деталей:").grid(row=0, column=5, padx=5, pady=5)
        total_components_entry = tk.Entry(frame)
        total_components_entry.grid(row=0, column=6, padx=5, pady=5)

        remove_button = tk.Button(frame, text="Убрать", command=lambda: self.remove_machine(frame))
        remove_button.grid(row=0, column=7, padx=5, pady=5)

        self.machine_entries.append((component_type_entry, assembly_time_entry, total_components_entry, frame))

        if len(self.machine_entries) >= 2:
            self.set_final_machine_button.config(state=tk.NORMAL)

    def remove_machine(self, frame):
        for i, (component_type_entry, assembly_time_entry, total_components_entry, entry_frame) in enumerate(self.machine_entries):
            if entry_frame == frame:
                self.machine_entries.pop(i)
                entry_frame.destroy()
                break

        if len(self.machine_entries) < 2:
            self.set_final_machine_button.config(state=tk.DISABLED)

    def set_final_machine(self):
        if self.final_machine_frame is not None:
            messagebox.showwarning("Предупреждение", "Финальная машина уже назначена")
            return

        final_machine_id = len(self.factory.machines) + 1
        frame = tk.Frame(self.machine_scroll)
        frame.pack(pady=5)

        tk.Label(frame, text=f"Финальная машина {final_machine_id}").grid(row=0, column=0, padx=5, pady=5)
        remove_button = tk.Button(frame, text="Убрать", command=lambda: self.remove_final_machine(frame))
        remove_button.grid(row=0, column=1, padx=5, pady=5)

        self.final_machine_frame = frame
        self.factory.set_final_machine(FinalAssemblyMachine(final_machine_id))
        self.start_button.config(state=tk.NORMAL)

    def remove_final_machine(self, frame):
        if self.final_machine_frame == frame:
            self.final_machine_frame.destroy()
            self.final_machine_frame = None
            self.factory.final_machine = None
            self.start_button.config(state=tk.DISABLED)

    def start_production(self):
        self.output_text.delete(1.0, tk.END)

        for i, (component_type_entry, assembly_time_entry, total_components_entry, _) in enumerate(self.machine_entries):
            component_type = component_type_entry.get()
            assembly_time = float(assembly_time_entry.get())
            total_components = int(total_components_entry.get())
            machine = AssemblyMachine(i + 1, component_type, assembly_time, total_components)
            self.factory.add_machine(machine)

        thread = threading.Thread(target=self.factory.start_production, args=(self.output_queue,))
        thread.start()

    def update_output(self):
        try:
            while True:
                message = self.output_queue.get_nowait()
                self.output_text.insert(tk.END, message + "\n")
                self.output_text.see(tk.END)
        except:
            pass

        self.root.after(100, self.update_output)


if __name__ == "__main__":
    root = tk.Tk()
    app = FactoryGUI(root)
    root.mainloop()