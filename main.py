import tkinter as tk
from gui.main_menu import MainMenu
from game_logic.leaderboard import Leaderboard

# Function to toggle fullscreen mode
def toggle_fullscreen(event=None):
    is_fullscreen = root.attributes("-fullscreen")
    root.attributes("-fullscreen", not is_fullscreen)  # Toggle fullscreen

# Function to exit fullscreen mode (bound to the Escape key)
def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)  # Exit fullscreen

def main():
    global root
    root = tk.Tk()
    root.title("Pose Striker")
    root.geometry("800x600")

    # Start the app in fullscreen
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", exit_fullscreen)  # Bind Escape to exit fullscreen

    # Shared leaderboard instance
    leaderboard = Leaderboard()

    # Initialize Main Menu
    main_menu = MainMenu(root, leaderboard)
    main_menu.pack(fill=tk.BOTH, expand=True)

    # Bind F11 to toggle fullscreen
    root.bind("<F11>", toggle_fullscreen)

    root.mainloop()

if __name__ == "__main__":
    main()
