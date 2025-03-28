import tkinter as tk
import os
from tkinter import simpledialog

USER_DELETED = False

def get_user_name():
    global USER_DELETED
    if USER_DELETED:
        return ""

    if os.path.exists('user.txt'):
        with open('user.txt', 'r') as file:
            user_name = file.read().strip()
            if user_name:
                return user_name
    return ""

def set_user_name(update_callback=None):
    global USER_DELETED
    USER_DELETED = False
    user_name = simpledialog.askstring("😊", "Введите имя игрока:")
    if user_name:
        with open('user.txt', 'w') as file:
            file.write(user_name)
        if update_callback:
            update_callback()

def delete_user_name(update_callback=None):
    global USER_DELETED
    USER_DELETED = True
    if os.path.exists('user.txt'):
        os.remove('user.txt')
    if update_callback:
        update_callback()