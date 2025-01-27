import numpy as np
import tkinter as tk
from tkinter import ttk
import numberCreatorWindow as ncw
import tensorflow as tf

# Load the model
model = tf.keras.models.load_model('sampleModel.keras')

# create the tkinter window
root = tk.Tk()

app = ncw.NumberCreatorWindow(root, blur=0.15, model=model)
root.mainloop()