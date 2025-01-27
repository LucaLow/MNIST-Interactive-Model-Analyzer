import numpy as np
import tkinter as tk
from tkinter import ttk
import numberCreatorWindow as ncw

root = tk.Tk()
app = ncw.NumberCreatorWindow(root, blur=0.15)
root.mainloop()