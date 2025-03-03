import tkinter as tk
from tkinter import ttk
import os

class App:
    def __init__(self, name=None, resolution=None, theme=None, icon=None):
        self.root = tk.Tk()
        self.root.title(name)
        self.root.geometry(resolution)

        if (icon is None):
            icon = os.path.join(os.path.dirname(__file__), "GladUI.ico")
            if (os.path.exists(icon)):
                self.root.iconbitmap(icon)
            else:
                print(f"Icon not found at '{icon}', using default system icon.")
        else:
            if (os.path.exists(icon)):
                self.root.iconbitmap(icon)
            else:
                raise TypeError(f"Icon not found at '{icon}'.")

        if (name is None):
            name = "GladUI"
        if (resolution is None):
            resolution = "240x120"
        if (theme is None):
            theme = "dark"
        if (theme.lower() == "dark"):
            self.bg = "#222222"
            self.fg = "white"
        elif (theme.lower() == "light"):
            self.bg = "white"
            self.fg = "black"
        else:
            raise ValueError("Invalid theme. Valid themes are: 'light', 'dark'")
        
        self.root.configure(bg=self.bg)
        self.style = ttk.Style()
        self.style.theme_use("clam")

    def run(self):
        self.root.mainloop()
