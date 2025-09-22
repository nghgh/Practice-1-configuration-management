import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import getpass
import socket
import os
import shlex
class Emulator:
    def __init__(self, root):
        bg_color = "#000000"
        pr_color = "#293133"
        fg_color = "#ffffff"
        scroll_color = "#00FF00"
        font_style = ("Courier New", 10)

        self.root = root
        username = getpass.getuser()
        hostname = socket.gethostname()
        self.root.title(f"Эмулятор - [{username}@{hostname}]")
        self.root.configure(bg=bg_color)

        self.output_area = ScrolledText(root, state='disabled', height=25, width=50, bg= pr_color, fg = fg_color)
        self.output_area.pack(padx=5, pady=5)

        self.output_area.configure(bg=bg_color, fg=fg_color)
        self.output_area.vbar.configure(troughcolor=bg_color, bg=scroll_color)


        self.input_entry = tk.Entry(root, width=55, bg=pr_color, fg=fg_color)
        self.input_entry.pack(padx=10, pady=(0, 10))
        self.input_entry.bind('<Return>', self.process_input)


        self.prompt = f"[{username}@{hostname}]$ "
        self.print_output(self.prompt)

        self.current_path = "/"

    def print_output(self, text):
        """Вспомогательная функция для вывода текста в область вывода."""
        self.output_area.configure(state='normal')
        self.output_area.insert(tk.END, text)
        self.output_area.see(tk.END)
        self.output_area.configure(state='disabled')

    def process_input(self, event):
        """Основная функция обработки ввода пользователя."""
        command_str = self.input_entry.get()
        self.input_entry.delete(0, tk.END)
        self.print_output(command_str + "\n")

        try:
            parts = shlex.split(command_str)
        except ValueError as e:
            self.print_output(f"Ошибка разбора команды: {e}\n")
            self.print_output(self.prompt)
            return

        if not parts:
            self.print_output(self.prompt)
            return

        command = parts[0]
        args = parts[1:]

        result = ""
        if command == "exit":
            self.root.destroy()
            return
        elif command == "ls":
            result = f"Команда 'ls' вызвана с аргументами: {args}\n"
        elif command == "cd":
            result = f"Команда 'cd' вызвана с аргументами: {args}\n"
            if args:
                self.current_path = args[0]
        else:
            result = f"Ошибка: команда '{command}' не найдена.\n"

        self.print_output(result)
        self.print_output(self.prompt)

if __name__ == "__main__":
    root = tk.Tk()
    app = Emulator(root)
    root.mainloop()