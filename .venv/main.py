import tkinter as tk
from tkinter import simpledialog
from table import Table
from file_operations import load_file, load_folder, parse_file
from menu_operations import get_user_name, set_user_name
import os

def create_window():
    root = tk.Tk()
    root.title("Окно с меню")
    root.geometry("600x625")

    text_widget = tk.Text(root, height=5, state=tk.DISABLED)
    text_widget.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    Table(root)

    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Загрузить файл", command=lambda: load_file(text_widget))
    file_menu.add_command(label="Загрузить папку", command=lambda: load_folder(text_widget))
    file_menu.add_command(label="Обработать файл", command=lambda: parse_file(text_widget))

    file_menu.add_separator()
    file_menu.add_command(label="Выход", command=root.quit)

    user_menu = tk.Menu(menu_bar, tearoff=0)
    user_menu.add_command(label="Изменить пользователя", command=set_user_name)

    menu_bar.add_cascade(label="Файл", menu=file_menu)
    menu_bar.add_cascade(label="Пользователь", menu=user_menu)

    root.config(menu=menu_bar)

    root.mainloop()


if __name__ == "__main__":
    create_window()
