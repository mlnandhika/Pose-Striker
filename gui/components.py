import tkinter as tk
from tkinter import ttk

class ScrollableLeaderboard(tk.Frame):
    def __init__(self, parent,width=550,height=550):
        super().__init__(parent)
        self.canvas = tk.Canvas(self,width=width,height=height,bg="gold2")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def update_leaderboard(self, data):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        for index, (name, score) in enumerate(data):
            tk.Label(self.scrollable_frame,font='Arial 17 bold',bg="#B28D09",fg="snow",text=f"{index + 1}.   {name[0]}  |  {name[1]}  |  {score} Points                                                 ").pack(anchor="w", pady=2,)

class DropdownMenu(ttk.Combobox):
    def __init__(self, parent, values, label_text="CLUSTER  :", width=40):
        super().__init__(parent, values=values, state="readonly")
        self.label = tk.Label(parent,font='Arial 17 bold', text=label_text,fg="#384987",bg="gold2")
        self.label.pack(side=tk.LEFT)
        self.config(width=width)
        self.pack(side=tk.LEFT, padx=10, pady=10)
