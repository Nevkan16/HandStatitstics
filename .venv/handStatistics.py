import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
from table import Table, load_statistics
from file_operations import Operations
from menu_operations import get_user_name, set_user_name, delete_user_name
import os

def create_window():
    root = tk.Tk()
    root.title("Обработчик рук")
    root.geometry("568x580")
    root.resizable(False, False)

    text_widget = tk.Text(root, height=5, state=tk.DISABLED)
    text_widget.place(x=20, y=10, width=530, height=60)
    statistics, total_sum = load_statistics(text_widget)

    progress = ttk.Progressbar(root, orient="horizontal", length=530, mode="determinate")
    progress.place(x=20, y=80, width=530, height=20)

    table = Table(root, statistics, total_sum)
    operations = Operations(progress)

    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Обработать файл", command=lambda: operations.parse_file(text_widget, table))
    file_menu.add_command(label="Добавить файл", command=lambda: operations.add_parse_file(text_widget, table))
    file_menu.add_command(label="Обработать папку", command=lambda: operations.parse_folder(text_widget, table))
    file_menu.add_command(label="Добавить папку", command=lambda: operations.add_parse_folder(text_widget, table))
    file_menu.add_command(label="Очистить статистику", command=lambda: operations.clear(text_widget, table))

    file_menu.add_separator()
    file_menu.add_command(label="Выход", command=root.quit)

    user_menu = tk.Menu(menu_bar, tearoff=0)
    user_menu.add_command(label="Добавить/Изменить пользователя", command=lambda: set_user_name(table.update_user_name))
    user_menu.add_command(label="Удалить пользователя", command=lambda: delete_user_name(table.update_user_name))

    menu_bar.add_cascade(label="Файл", menu=file_menu)
    menu_bar.add_cascade(label="Пользователь", menu=user_menu)

    about_menu = tk.Menu(menu_bar, tearoff=0)
    about_menu.add_command(label="О программе", command=show_about)
    menu_bar.add_cascade(label="О программе", menu=about_menu)

    root.config(menu=menu_bar)

    root.mainloop()

def show_about():
    about_message = "Версия: 1.0\nРазработано: Nevkan16"
    messagebox.showinfo("О программе", about_message)

if __name__ == "__main__":
    create_window()
