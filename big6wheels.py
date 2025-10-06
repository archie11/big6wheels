import tkinter as tk
from tkinter import ttk, messagebox
import random, math

# === Wheel Segments ===
SEGMENTS = [
    "1", "3", "1", "6", "1", "3", "1", "12", "1", "6", "1", "3", "1", "25",
    "1", "3", "1", "6", "1", "12", "1", "3", "1", "3", "1", "3", "50 Joker",
    "1", "3", "1", "6", "1", "12", "1", "3", "1", "6", "1", "3", "1", "25",
    "1", "3", "1", "6", "1", "12", "1", "3", "6", "1", "3", "1", "50 Flag"
]

# Unique betting segments
BET_SEGMENTS = ["1", "3", "6", "12", "25", "50 Joker", "50 Flag"]

# Multiplier mapping
MULTIPLIER = {
    "1": 1,
    "3": 3,
    "6": 6,
    "12": 12,
    "25": 25,
    "50 Joker": 50,
    "50 Flag": 50
}

# Color mapping
COLOR_MAP = {
    "1": "green",
    "3": "skyblue",
    "6": "yellow",
    "12": "blue",
    "25": "violet",
    "50 Joker": "red",
    "50 Flag": "gray"
}

class BigSixWheelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Big Six Wheel 🎡")
        self.root.geometry("1250x700")

        self.balance = 100
        self.history = []

        # Wheel canvas
        self.wheel_canvas = tk.Canvas(self.root, width=500, height=500, bg="white")
        self.wheel_canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.center_x, self.center_y = 250, 250
        self.radius = 200
        self.segment_count = len(SEGMENTS)
        self.angle_per_segment = 360 / self.segment_count
        self.draw_wheel()

        # Pointer
        self.wheel_canvas.create_polygon(
            [self.center_x, self.center_y - self.radius - 20,
             self.center_x - 20, self.center_y - self.radius - 60,
             self.center_x + 20, self.center_y - self.radius - 60],
            fill="red"
        )

        self.create_ui()

    def draw_wheel(self):
        self.wheel_canvas.delete("segment")
        for i, label in enumerate(SEGMENTS):
            start_angle = i * self.angle_per_segment
            color = COLOR_MAP.get(label, "#d9d9d9")
            self.wheel_canvas.create_arc(
                self.center_x - self.radius, self.center_y - self.radius,
                self.center_x + self.radius, self.center_y + self.radius,
                start=start_angle, extent=self.angle_per_segment,
                fill=color, outline="black", tags="segment"
            )
            angle_rad = math.radians(start_angle + self.angle_per_segment/2)
            text_x = self.center_x + (self.radius - 40) * math.cos(angle_rad)
            text_y = self.center_y - (self.radius - 40) * math.sin(angle_rad)
            self.wheel_canvas.create_text(text_x, text_y, text=label, font=("Arial", 8, "bold"), tags="segment")

    def create_ui(self):
        frame_right = ttk.Frame(self.root)
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Balance
        self.balance_var = tk.StringVar(value=f"Balance: ${self.balance}")
        ttk.Label(frame_right, textvariable=self.balance_var, font=("Arial", 14)).pack(pady=5)

        # Bet entries with Clear buttons
        self.bet_entries = {}
        bet_frame = ttk.Frame(frame_right)
        bet_frame.pack(pady=10)
        ttk.Label(bet_frame, text="Enter bet amounts for each segment:").grid(row=0, column=0, columnspan=3)

        for i, label in enumerate(BET_SEGMENTS):
            ttk.Label(bet_frame, text=f"{label}:").grid(row=i+1, column=0, sticky="e", padx=5, pady=2)
            entry = ttk.Entry(bet_frame, width=10)
            entry.grid(row=i+1, column=1, pady=2)
            self.bet_entries[label] = entry

            # Clear button for each field
            ttk.Button(bet_frame, text="Clear", command=lambda e=entry: e.delete(0, tk.END)).grid(row=i+1, column=2, padx=5)

        # Clear All button
        ttk.Button(bet_frame, text="Clear All", command=self.clear_all_bets).grid(row=len(BET_SEGMENTS)+2, column=0, columnspan=3, pady=10)

        # Spin button
        ttk.Button(bet_frame, text="Spin 🎡", command=self.spin_wheel).grid(row=len(BET_SEGMENTS)+3, column=0, columnspan=3, pady=5)

        # Deposit / Withdraw
        frame_money = ttk.Frame(frame_right)
        frame_money.pack(pady=10)
        self.deposit_entry = ttk.Entry(frame_money, width=10)
        self.deposit_entry.grid(row=0, column=1)
        ttk.Button(frame_money, text="Deposit", command=self.deposit).grid(row=0, column=2, padx=5)
        self.withdraw_entry = ttk.Entry(frame_money, width=10)
        self.withdraw_entry.grid(row=0, column=4)
        ttk.Button(frame_money, text="Withdraw", command=self.withdraw).grid(row=0, column=5, padx=5)
        ttk.Label(frame_money, text="Deposit:").grid(row=0, column=0)
        ttk.Label(frame_money, text="Withdraw:").grid(row=0, column=3)

        # Result
        self.result_var = tk.StringVar(value="Spin result will appear here.")
        ttk.Label(frame_right, textvariable=self.result_var, font=("Arial", 12, "italic")).pack(pady=10)

        # History
        ttk.Label(frame_right, text="📜 Spin History:", font=("Arial", 12, "bold")).pack()
        frame_history = ttk.Frame(frame_right)
        frame_history.pack(fill=tk.BOTH, expand=True)
        self.history_text = tk.Text(frame_history, height=15, wrap="none")
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(frame_history, command=self.history_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_text.configure(yscrollcommand=scrollbar.set)

    def update_balance(self):
        self.balance_var.set(f"Balance: ${int(self.balance)}")

    def deposit(self):
        try:
            amt = float(self.deposit_entry.get())
            if amt <= 0: raise ValueError
            self.balance += int(amt)
            self.update_balance()
            self.deposit_entry.delete(0, tk.END)
        except:
            messagebox.showerror("Error", "Invalid deposit.")

    def withdraw(self):
        try:
            amt = float(self.withdraw_entry.get())
            if amt <= 0 or amt > self.balance: raise ValueError
            self.balance -= int(amt)
            self.update_balance()
            self.withdraw_entry.delete(0, tk.END)
        except:
            messagebox.showerror("Error", "Invalid withdraw.")

    def clear_all_bets(self):
        for entry in self.bet_entries.values():
            entry.delete(0, tk.END)

    def spin_wheel(self):
        bets = {}
        total_bet = 0
        for label, entry in self.bet_entries.items():
            try:
                amt = int(float(entry.get())) if entry.get().strip() else 0
                if amt < 0: raise ValueError
                bets[label] = amt
                total_bet += amt
            except:
                messagebox.showerror("Error", f"Invalid bet for {label}")
                return

        if total_bet > self.balance:
            messagebox.showerror("Error", "Not enough balance for these bets.")
            return

        # Subtract total bets
        self.balance -= total_bet
        self.update_balance()

        # Spin result
        result_index = random.randint(0, self.segment_count-1)
        result_label = SEGMENTS[result_index]

        # Animation
        spin_rounds = 3
        total_steps = spin_rounds * self.segment_count + result_index
        delay = 0.02
        for i in range(total_steps):
            current = i % self.segment_count
            self.highlight_segment(current)
            self.root.update()
            delay *= 1.03
        self.highlight_segment(result_index)
        self.root.update()

        # --- Payouts ---
        total_win = 0
        win_labels = []
        lose_labels = []

        for bet_label, bet_amount in bets.items():
            if bet_amount == 0:
                continue

            if bet_label == result_label:
                multiplier = MULTIPLIER[result_label]
                net_win = bet_amount * multiplier
                total_win += net_win + bet_amount
                win_labels.append(f"{bet_label}+${net_win}")
            else:
                lose_labels.append(f"{bet_label}-${bet_amount}")

        # Update balance
        self.balance += total_win
        self.update_balance()

        # Result text
        result_text = f"🎡 Landed on {result_label} | "
        if win_labels:
            result_text += f"🎉 Won: {', '.join(win_labels)} | "
        if lose_labels:
            result_text += f"❌ Lost: {', '.join(lose_labels)}"
        self.result_var.set(result_text)

        # --- History entry (numbered, integer bets, no duplicate "Landed on") ---
        history_entry = f"{len(self.history)+1}. Bets: {', '.join([f'{l}:{a}' for l,a in bets.items() if a>0])} | {result_text} | Balance: ${int(self.balance)}"
        self.history.append(history_entry)
        self.history_text.insert(tk.END, history_entry + "\n")
        self.history_text.see(tk.END)

    def highlight_segment(self, index):
        self.wheel_canvas.delete("highlight")
        start_angle = index * self.angle_per_segment
        label = SEGMENTS[index]
        color = COLOR_MAP.get(label, "yellow")

        self.wheel_canvas.create_arc(
            self.center_x - self.radius, self.center_y - self.radius,
            self.center_x + self.radius, self.center_y + self.radius,
            start=start_angle, extent=self.angle_per_segment,
            fill=color, outline="black", width=4, tags="highlight"
        )

        angle_rad = math.radians(start_angle + self.angle_per_segment / 2)
        text_x = self.center_x + (self.radius - 40) * math.cos(angle_rad)
        text_y = self.center_y - (self.radius - 40) * math.sin(angle_rad)
        self.wheel_canvas.create_text(text_x, text_y, text=label, font=("Arial", 14, "bold"), tags="highlight")


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = BigSixWheelApp(root)
    root.mainloop()
