import tkinter as tk
from tkinter import simpledialog

def get_user_name():
    if os.path.exists('user.txt'):
        with open('user.txt', 'r') as file:
            user_name = file.read().strip()
            if user_name:
                return user_name
    return None


def set_user_name():
    user_name = simpledialog.askstring("Имя пользователя", "Введите ваше имя:")
    if user_name:
        with open('user.txt', 'w') as file:
            file.write(user_name)