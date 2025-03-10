import os
from tkinter import filedialog, simpledialog, Tk, Text
import re
import time
from сardConverter import convert_card_format
from collections import Counter
from table import Table
import threading

lock = threading.Lock()
global_card_counter = Counter()
last_selected_folder = None

def get_user_name():
    if os.path.exists('user.txt'):
        with open('user.txt', 'r') as file:
            user_name = file.read().strip()
            if user_name:
                return user_name
    user_name = simpledialog.askstring("Имя пользователя", "Введите ваше имя:")
    if user_name:
        with open('user.txt', 'w') as file:
            file.write(user_name)
        return user_name
    return None

def parse_file(text_widget, table):
    user_name = get_user_name()
    if not user_name:
        return

    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    text_widget_update(text_widget, "Начинается обработка файла...\n")
    clear_statistics()

    start_time = time.time()

    try:
        matches = extract_card_data(file_path, user_name)
        save_converted_data(matches)

        elapsed_time = time.time() - start_time
        text_widget_update(text_widget, f"Обработка завершена за {elapsed_time:.2f} секунд.\n")
        table.update_statistics(text_widget)
    except Exception as e:
        text_widget_update(text_widget, f"Ошибка при обработке файла: {e}\n")


def parse_folder(text_widget, table):
    global last_selected_folder

    user_name = get_user_name()
    if not user_name:
        return

    initial_dir = os.path.dirname(last_selected_folder) if last_selected_folder else None
    folder_path = filedialog.askdirectory(initialdir=initial_dir)

    if not folder_path:
        return

    last_selected_folder = folder_path

    text_widget_update(text_widget, "Начинается обработка файлов в папке...\n")
    clear_statistics()

    global global_card_counter
    global_card_counter.clear()

    files_to_process = get_files_to_process(folder_path)

    start_time = time.time()
    process_files_in_threads(files_to_process, user_name, text_widget)

    save_converted_data(global_card_counter)
    elapsed_time = time.time() - start_time
    text_widget_update(text_widget, f"Обработка всех файлов завершена за {elapsed_time:.2f} секунд.\n")

    table.update_statistics(text_widget)


def get_files_to_process(folder_path):
    files_to_process = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.xml'):
                files_to_process.append(os.path.join(root, file))
    return files_to_process


def process_files_in_threads(files_to_process, user_name, text_widget):
    threads = []
    for file_path in files_to_process:
        thread = threading.Thread(target=process_file, args=(file_path, user_name, text_widget))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def process_file(file_path, user_name, text_widget):
    try:
        matches = extract_card_data(file_path, user_name)
        local_counter = Counter()

        for match in matches:
            converted_match = convert_card_format(match.strip())
            if converted_match:
                local_counter[converted_match] += 1

        with lock:
            global global_card_counter
            global_card_counter.update(local_counter)

    except Exception as e:
        text_widget_update(text_widget, f"Ошибка при обработке файла {file_path}: {e}\n")


def extract_card_data(file_path, user_name):
    pattern = fr'<cards[^>]*\bplayer="{user_name}"[^>]*>(.*?)</cards>'

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    return re.findall(pattern, content)


def save_converted_data(data):
    card_counter = Counter()

    if isinstance(data, list):
        for match in data:
            converted_match = convert_card_format(match.strip())
            if converted_match:
                card_counter[converted_match] += 1
    elif isinstance(data, Counter):
        card_counter = data

    if card_counter:
        with open("statistics.txt", "a", encoding="utf-8") as stat_file:
            for card, count in card_counter.items():
                stat_file.write(f"{card} {count}\n")


def text_widget_update(text_widget, message):
    text_widget.config(state="normal")
    text_widget.delete(1.0, "end")
    text_widget.insert("end", message)
    text_widget.config(state="disabled")
    text_widget.update_idletasks()


def clear_statistics():
    if os.path.exists("statistics.txt"):
        with open("statistics.txt", "w", encoding="utf-8") as file:
            file.truncate(0)


