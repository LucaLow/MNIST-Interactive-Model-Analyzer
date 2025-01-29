import tensorflow as tf
import numpy as np
import tkinter as tk
from tkinter import ttk
import utils as utils



class NumberCreatorWindow:

    def __init__(self, root, model, blur=0.1):
        self.root = root
        self.root.title("MNIST Drawing App")

        self.label = ttk.Label(self.root, text="Draw a number")
        
        self.drawing = False
        self.removing = False
        self.blur = blur
        self.grid_data = np.zeros((28, 28), dtype=np.float32)
        
        self._create_widgets()
        self._create_canvas()

        self.model = model
        self.predict()
    
    def _create_widgets(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.clear_button = ttk.Button(self.main_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.grid(row=0, column=0, sticky=(tk.W, tk.E))

        self.prediction_label = ttk.Label(self.main_frame, text="Prediction: ")
        self.prediction_label.grid(row=0, column=2, padx=5, pady=5)

    def _create_canvas(self):
        self.canvas = tk.Canvas(self.root, width=280, height=280, bg="black")
        self.canvas.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        self.canvas.bind('<Button-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.stop_drawing)
        self.canvas.bind('<Button-2>', self.start_removing)
        self.canvas.bind('<B2-Motion>', self.remove)
        self.canvas.bind('<ButtonRelease-1>', self.stop_removing)


        utils.drawGridLines(self.canvas)
        
    def start_drawing(self, event):
        self.drawing = True
        self.draw(event)
    
    def stop_drawing(self, event):
        self.drawing = False
        self.predict()
    
    def draw(self, event):
        if self.drawing:
            grid_x = event.x // 10
            grid_y = event.y // 10

            if 0 <= grid_x < 28 and 0 <= grid_y < 28:
                x1 = grid_x * 10
                y1 = grid_y * 10
                x2 = x1 + 10
                y2 = y1 + 10
                if self.grid_data[grid_y, grid_x] != 1.0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#FFFFFF", outline="grey")
                    self.grid_data[grid_y, grid_x] = 1.0

                blur_coords = [
                    (grid_y-1, grid_x, x1, x2, y1-10, y2-10),  # Top
                    (grid_y+1, grid_x, x1, x2, y1+10, y2+10),  # Bottom
                    (grid_y, grid_x-1, x1-10, x2-10, y1, y2),  # Left
                    (grid_y, grid_x+1, x1+10, x2+10, y1, y2),  # Right
                    (grid_y-1, grid_x-1, x1-10, x2-10, y1-10, y2-10),  # Top-Left
                    (grid_y-1, grid_x+1, x1+10, x2+10, y1-10, y2-10),  # Top-Right
                    (grid_y+1, grid_x-1, x1-10, x2-10, y1+10, y2+10),  # Bottom-Left
                    (grid_y+1, grid_x+1, x1+10, x2+10, y1+10, y2+10)   # Bottom-Right
                ]

                for y, x, bx1, bx2, by1, by2 in blur_coords:
                    self.grid_data = utils.addBlur(
                        self.grid_data, self.canvas,
                        y, x, bx1, bx2, by1, by2,
                        self.blur
                    )
                

                
    
    def start_removing(self, event):
        self.removing = True
        self.remove(event)

    def stop_removing(self, event):
        self.removing = False
        self.predict()

    def remove(self, event): 
        if self.removing:
            grid_x = event.x // 10
            grid_y = event.y // 10

            if 0 <= grid_x < 28 and 0 <= grid_y < 28:
                x1 = grid_x * 10
                y1 = grid_y * 10
                x2 = x1 + 10
                y2 = y1 + 10
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#000000", outline="grey")
                self.grid_data[grid_y, grid_x] = 0
        
    def clear_canvas(self):
        self.canvas.delete("all")
        self.grid_data = np.zeros((28, 28), dtype=np.float32)
        utils.drawGridLines(self.canvas)
        self.predict()


    def predict(self):
        prediction, confidence = utils.predict(self.model, self.grid_data)
        self.prediction_label.config(text=f"Prediction: {prediction} Confidence: {confidence:.2f}")
        self.root.update()



