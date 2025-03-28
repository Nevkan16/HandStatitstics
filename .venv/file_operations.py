import os
from tkinter import filedialog, simpledialog, Text, messagebox
import re
import time
from сardConverter import convert_card_format
from menu_operations import get_user_name, set_user_name
from collections import Counter
from table import Table
import threading

class Operations:
    def __init__(self, progress=None):
        self.lock = threading.Lock()
        self.global_card_counter = Counter()
        self.last_selected_folder = None
        self.user_name = None
        self.progress = progress

    def ensure_user_name(self, update_callback=None):
        self.user_name = get_user_name()

        if not self.user_name:
            set_user_name(update_callback)
            self.user_name = get_user_name()

        return bool(self.user_name)

    def process_pars_file(self, text_widget, table, clear_stats=True):
        if not self.ensure_user_name(table.update_user_name):
            return

        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.text_widget_update(text_widget, "Начинается обработка файла...\n")
        if clear_stats:
            self.clear_statistics()

        start_time = time.time()

        try:
            if self.progress:
                self.progress["value"] = 0
                self.progress.update()

            matches = self.extract_card_data(file_path)
            self.save_converted_data(matches)

            if self.progress:
                self.progress["value"] = 100
                self.progress.update()

            elapsed_time = time.time() - start_time
            self.text_widget_update(text_widget, f"Обработка завершена за {elapsed_time:.2f} секунд.\n")
            table.update_statistics(text_widget)
        except Exception as e:
            self.text_widget_update(text_widget, f"Ошибка при обработке файла: {e}\n")

        if self.progress:
            time.sleep(0.5)
            self.progress["value"] = 0
            self.progress.update()

    def parse_file(self, text_widget, table):
        self.process_pars_file(text_widget, table, clear_stats=True)

    def add_parse_file(self, text_widget, table):
        self.process_pars_file(text_widget, table, clear_stats=False)

    def process_folder(self, text_widget, table, clear_stats=True):
        if not self.ensure_user_name(table.update_user_name):
            return

        initial_dir = os.path.dirname(self.last_selected_folder) if self.last_selected_folder else None
        folder_path = filedialog.askdirectory(initialdir=initial_dir)

        if not folder_path:
            return

        self.last_selected_folder = folder_path

        self.text_widget_update(text_widget, "Начинается обработка файлов в папке...\n")

        if clear_stats:
            self.clear_statistics()

        self.global_card_counter.clear()
        files_to_process = self.get_files_to_process(folder_path)

        start_time = time.time()
        self.process_files_in_threads(files_to_process, text_widget)

        self.save_converted_data(self.global_card_counter)
        elapsed_time = time.time() - start_time
        self.text_widget_update(text_widget, f"Обработка всех файлов завершена за {elapsed_time:.2f} секунд.\n")

        table.update_statistics(text_widget)

    def parse_folder(self, text_widget, table):
        self.process_folder(text_widget, table, clear_stats=True)

    def add_parse_folder(self, text_widget, table):
        self.process_folder(text_widget, table, clear_stats=False)

    def get_files_to_process(self, folder_path):
        files_to_process = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.xml'):
                    files_to_process.append(os.path.join(root, file))
        return files_to_process

    def process_files_in_threads(self, files_to_process, text_widget):
        threads = []
        total_files = len(files_to_process)

        for index, file_path in enumerate(files_to_process):
            thread = threading.Thread(target=self.process_file, args=(file_path, text_widget))
            threads.append(thread)
            thread.start()

            if self.progress:
                self.progress["value"] = (index + 1) / total_files * 100
                self.progress.update()

        for thread in threads:
            thread.join()

        if self.progress:
            self.progress["value"] = 100
            self.progress.update()

            time.sleep(0.5)
            self.progress["value"] = 0
            self.progress.update()

    def process_file(self, file_path, text_widget):
        try:
            matches = self.extract_card_data(file_path)
            local_counter = Counter()

            for match in matches:
                converted_match = convert_card_format(match.strip())
                if converted_match:
                    local_counter[converted_match] += 1

            with self.lock:
                self.global_card_counter.update(local_counter)

        except Exception as e:
            self.text_widget_update(text_widget, f"Ошибка при обработке файла {file_path}: {e}\n")

    def extract_card_data(self, file_path):
        pattern = fr'<cards[^>]*\bplayer="{self.user_name}"[^>]*>(.*?)</cards>'

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        return re.findall(pattern, content)

    def save_converted_data(self, data):
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

    def text_widget_update(self, text_widget, message):
        text_widget.config(state="normal")
        text_widget.delete(1.0, "end")
        text_widget.insert("end", message)
        text_widget.config(state="disabled")
        text_widget.update_idletasks()

    def clear_statistics(self):
        if os.path.exists("statistics.txt"):
            with open("statistics.txt", "w", encoding="utf-8") as file:
                file.truncate(0)

    def clear(self, text_widget, table):
        confirm = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить статистику?")
        if confirm:
            self.clear_statistics()
            table.update_statistics(text_widget)
            self.text_widget_update(text_widget, "Статистика очищена\n")