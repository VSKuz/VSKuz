import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import json
import os

class Stopwatch:
    def __init__(self, name):
        self.name = name
        self.start_time = 0
        self.elapsed_time = 0
        self.running = False
        self.history = []

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True

    def pause(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.running = False

    def save(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.running = False
        self.history.append(self.elapsed_time)

    def get_elapsed_time(self):
        if self.running:
            return time.time() - self.start_time
        else:
            return self.elapsed_time

    def set_elapsed_time(self, seconds):
        self.elapsed_time = seconds
        if self.running:
            self.start_time = time.time() - self.elapsed_time

    def reset(self):
        self.elapsed_time = 0
        if self.running:
            self.start_time = time.time()

class StopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление секундомерами")
        self.stopwatches = {}
        self.load_stopwatches()

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.listbox = tk.Listbox(self.frame, width=50, height=10)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.update_listbox()

        self.open_button = tk.Button(self.root, text="Открыть секундомер", command=self.open_stopwatch)
        self.open_button.pack(pady=5)

        self.add_button = tk.Button(self.root, text="Добавить секундомер", command=self.add_stopwatch)
        self.add_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text="Удалить секундомер", command=self.delete_stopwatch)
        self.delete_button.pack(pady=5)

        self.reset_button = tk.Button(self.root, text="Сбросить время", command=self.reset_stopwatch)
        self.reset_button.pack(pady=5)

    def add_stopwatch(self):
        name = simpledialog.askstring("Добавить секундомер", "Введите имя секундомера:")
        if name and name not in self.stopwatches:
            self.stopwatches[name] = Stopwatch(name)
            self.update_listbox()
            self.save_stopwatches()

    def open_stopwatch(self):
        selected = self.listbox.curselection()
        if selected:
            name = self.listbox.get(selected)
            stopwatch = self.stopwatches[name]
            StopwatchWindow(self.root, stopwatch, self.save_stopwatches)

    def delete_stopwatch(self):
        selected = self.listbox.curselection()
        if selected:
            name = self.listbox.get(selected)
            del self.stopwatches[name]
            self.update_listbox()
            self.save_stopwatches()

    def reset_stopwatch(self):
        selected = self.listbox.curselection()
        if selected:
            name = self.listbox.get(selected)
            stopwatch = self.stopwatches[name]
            stopwatch.reset()
            self.save_stopwatches()
            messagebox.showinfo("Сброс времени", f"Время секундомера '{name}' сброшено до нуля.")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for name in self.stopwatches:
            self.listbox.insert(tk.END, name)

    def save_stopwatches(self):
        with open("stopwatches.json", "w") as f:
            json.dump({name: sw.__dict__ for name, sw in self.stopwatches.items()}, f)

    def load_stopwatches(self):
        if os.path.exists("stopwatches.json"):
            with open("stopwatches.json", "r") as f:
                data = json.load(f)
                for name, sw_data in data.items():
                    sw = Stopwatch(name)
                    sw.__dict__.update(sw_data)
                    self.stopwatches[name] = sw

class StopwatchWindow:
    def __init__(self, root, stopwatch, save_callback):
        self.root = root
        self.stopwatch = stopwatch
        self.save_callback = save_callback

        self.window = tk.Toplevel(self.root)
        self.window.title(stopwatch.name)

        self.time_label = tk.Label(self.window, text="00:00:00", font=("Arial", 48))
        self.time_label.pack(pady=20)

        self.start_button = tk.Button(self.window, text="Старт", command=self.start_stopwatch)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.pause_button = tk.Button(self.window, text="Пауза", command=self.pause_stopwatch)
        self.pause_button.pack(side=tk.LEFT, padx=10)

        self.edit_button = tk.Button(self.window, text="Редактировать", command=self.edit_stopwatch)
        self.edit_button.pack(side=tk.LEFT, padx=10)

        self.update_time()

    def start_stopwatch(self):
        self.stopwatch.start()
        self.update_time()

    def pause_stopwatch(self):
        self.stopwatch.pause()
        self.update_time()
        self.stopwatch.save()
        self.save_callback()

    def edit_stopwatch(self):
        new_time = simpledialog.askinteger("Редактировать время", "Введите новое время в секундах:", minvalue=0)
        if new_time is not None:
            self.stopwatch.set_elapsed_time(new_time)
            self.update_time()

    def update_time(self):
        elapsed_time = self.stopwatch.get_elapsed_time()
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        self.time_label.config(text=time_str)
        if self.stopwatch.running:
            self.window.after(1000, self.update_time)

if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()
