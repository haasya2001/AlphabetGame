import tkinter as tk
from tkinter import messagebox

def select_player(player):
    global current_player
    current_player = player
    if current_player == "Player1":
        generate_button.config(state="normal")
    else:
        generate_button.config(state="disabled")
    messagebox.showinfo("Player Selected", f"{current_player} selected.")

def generate_random_letter():
    if current_player == "Player1":
        random_letter.set(chr(random.randint(65, 90)))  # Generates a random uppercase letter
    else:
        messagebox.showwarning("Permission Denied", "Only Player1 can generate the random letter!")

# Initialize the GUI window
root = tk.Tk()
root.title("Player Selection Game")

current_player = None  # Track the current player
random_letter = tk.StringVar()

# Create Player Selection Buttons
player1_button = tk.Button(root, text="Player1", command=lambda: select_player("Player1"))
player2_button = tk.Button(root, text="Player2", command=lambda: select_player("Player2"))
player1_button.pack(pady=10)
player2_button.pack(pady=10)

# Create Random Letter Generation Button
generate_button = tk.Button(root, text="Generate Random Letter", command=generate_random_letter, state="disabled")
generate_button.pack(pady=20)

# Display Random Letter
letter_label = tk.Label(root, textvariable=random_letter, font=("Helvetica", 24))
letter_label.pack(pady=20)

# Run the main loop
root.mainloop()
