import tkinter as tk
from tkinter import simpledialog
ROOT = tk.Tk()

ROOT.withdraw()
# the input dialog
USER_INP = simpledialog.askstring(title="",
                                  prompt="Number of Players(Max 4):")
noPlayers = int(USER_INP)
blocks = 40
