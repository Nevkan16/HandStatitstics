import tkinter as tk
from tkinter import Toplevel
from menu_operations import get_user_name

def load_statistics(text_widget):
    statistics = {}
    total_sum = 0

    try:
        with open("statistics.txt", "r") as file:
            for line in file:
                hand, value = line.split()
                value = int(value)
                statistics[hand] = value
                total_sum += value
    except FileNotFoundError:
        text_widget.config(state=tk.NORMAL)  # Включаем редактирование
        text_widget.insert(tk.END, "Здравствуйте! Приятного пользования! :-)\n")
        text_widget.config(state=tk.DISABLED)

    return statistics, total_sum

class Table:
    def __init__(self, root, statistics, total_sum):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.place(x=20, y=110)
        self.cells = []
        self.statistics = statistics
        self.total_sum = total_sum

        self.status_label = tk.Label(
            root,
            font=("Arial", 12),
            bg="lightgray",
            fg="black",
            relief="solid",
            borderwidth=2,
        )
        self.status_label.pack(pady=0, padx=0)
        self.status_label.place(x=30, y=520, width=300, height=30)

        self.total_label = tk.Label(
            root,
            text=f"Hands: {self.total_sum}",
            font=("Arial", 12),
            bg="lightgray",
            fg="black",
            relief="solid",
            borderwidth=2,
        )
        self.total_label.place(x=420, y=520, height=30)

        self.user_name = get_user_name()
        self.user_label = tk.Label(
            root,
            text=f"{self.user_name}",
            font=("Arial", 11)
        )
        self.user_label.place(relx=1.0, rely=1.0, anchor="se", x=0, y=0, height=30)

        self.create_table()
        self.create_legend()

    def update_user_name(self):
        self.user_name = get_user_name()
        self.user_label.config(text=f"{self.user_name}")

    def calculate_expected_count_and_diff(self, hand, value):
        if hand.endswith("s"):
            expected_count = self.total_sum / 331.5
        elif hand.endswith("o"):
            expected_count = self.total_sum / 110.5
        else:
            expected_count = self.total_sum / 221

        diff_percentage = 0
        if expected_count > 0:
            diff_percentage = (value - expected_count) / expected_count * 100
        return expected_count, diff_percentage

    def determine_text_color(self, diff_percentage):
        if abs(diff_percentage) <= 2:
            return "black"
        elif 2 < abs(diff_percentage) <= 5:
            if diff_percentage > 0:
                return "#ee7fee"
            else:
                return "#7abf51"
        elif abs(diff_percentage) > 5:
            if diff_percentage > 0:
                return "#de5151"
            else:
                return "#166f16"

    def create_table(self):
        hands = ["AA", "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                 "AKo", "KK", "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s",
                 "AQo", "KQo", "QQ", "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s",
                 "AJo", "KJo", "QJo", "JJ", "JTs", "J9s", "J8s", "J7s", "J6s", "J5s", "J4s", "J3s", "J2s",
                 "ATo", "KTo", "QTo", "JTo", "TT", "T9s", "T8s", "T7s", "T6s", "T5s", "T4s", "T3s", "T2s",
                 "A9o", "K9o", "Q9o", "J9o", "T9o", "99", "98s", "97s", "96s", "95s", "94s", "93s", "92s",
                 "A8o", "K8o", "Q8o", "J8o", "T8o", "98o", "88", "87s", "86s", "85s", "84s", "83s", "82s",
                 "A7o", "K7o", "Q7o", "J7o", "T7o", "97o", "87o", "77", "76s", "75s", "74s", "73s", "72s",
                 "A6o", "K6o", "Q6o", "J6o", "T6o", "96o", "86o", "76o", "66", "65s", "64s", "63s", "62s",
                 "A5o", "K5o", "Q5o", "J5o", "T5o", "95o", "85o", "75o", "65o", "55", "54s", "53s", "52s",
                 "A4o", "K4o", "Q4o", "J4o", "T4o", "94o", "84o", "74o", "64o", "54o", "44", "43s", "42s",
                 "A3o", "K3o", "Q3o", "J3o", "T3o", "93o", "83o", "73o", "63o", "53o", "43o", "33", "32s",
                 "A2o", "K2o", "Q2o", "J2o", "T2o", "92o", "82o", "72o", "62o", "52o", "42o", "32o", "22"]

        for i in range(13):
            row = []
            for j in range(13):
                hand = hands[i * 13 + j]

                if hand.endswith("s"):
                    bg_color = "#fff7cb"
                elif hand.endswith("o"):
                    bg_color = "#f9e1de"
                else:
                    bg_color = "#d2ebfa"

                value = self.statistics.get(hand, 0)

                expected_count, diff_percentage = self.calculate_expected_count_and_diff(hand, value)

                text_color = self.determine_text_color(diff_percentage)

                label = tk.Label(
                    self.frame,
                    text=hand,
                    borderwidth=1,
                    font=("Arial", 14),
                    padx=3,
                    pady=3,
                    relief="solid",
                    width=3,
                    height=1,
                    bg=bg_color,
                    fg=text_color
                )

                label.grid(row=i, column=j)
                row.append(label)

                label.bind("<Enter>", lambda event, hand=hand: self.update_status(event, hand))

            self.cells.append(row)

    def update_status(self, event, hand):
        value = self.statistics.get(hand, 0)
        expected_count, diff_percentage = self.calculate_expected_count_and_diff(hand, value)

        percentage = (value / self.total_sum * 100) if self.total_sum > 0 else 0

        self.status_label.config(
            text=f"Hand: {hand} | {percentage:.2f}% | {value} | Exp: {expected_count:.1f}"
        )

    def update_statistics(self, text_widget):
        self.statistics, self.total_sum = load_statistics(text_widget)
        self.total_label.config(text=f"Hands: {self.total_sum}")

        for i, row in enumerate(self.cells):
            for j, label in enumerate(row):
                hand = label.cget("text")

                value = self.statistics.get(hand, 0)
                expected_count, diff_percentage = self.calculate_expected_count_and_diff(hand, value)

                text_color = self.determine_text_color(diff_percentage)

                label.config(fg=text_color)

    def create_legend(self):
        legend_button = tk.Label(self.root, text="🐦", font=("Arial", 20), fg="blue", cursor="hand2")
        legend_button.place(x=360, y=518)

        legend_button.bind("<Enter>", self.show_tooltip)
        legend_button.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        tooltip = Toplevel(self.root)
        tooltip.wm_overrideredirect(True)
        tooltip.geometry(f"+{event.x_root + 20}+{event.y_root + 20}")

        # Создаем метки с разными цветами, выравнивание по левому краю
        label_black = tk.Label(tooltip, text="0-2%: Норма", font=("Arial", 10), fg="black", anchor="w", padx=10)
        label_black.pack(fill="x")

        label_pink = tk.Label(tooltip, text="2-5%: Превышено", font=("Arial", 10), fg="#ee7fee", anchor="w", padx=10)
        label_pink.pack(fill="x")

        label_green = tk.Label(tooltip, text="2-5%: Занижено", font=("Arial", 10), fg="#7abf51", anchor="w", padx=10)
        label_green.pack(fill="x")

        label_red = tk.Label(tooltip, text=">5%: Сильно превышено", font=("Arial", 10), fg="#de5151", anchor="w",
                             padx=10)
        label_red.pack(fill="x")

        label_darkgreen = tk.Label(tooltip, text="<5%: Сильно занижено", font=("Arial", 10), fg="#166f16", anchor="w",
                                   padx=10)
        label_darkgreen.pack(fill="x")

    def hide_tooltip(self, event):

        for widget in self.root.winfo_children():
            if isinstance(widget, Toplevel):
                widget.destroy()
