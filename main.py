import numpy as np
import tkinter as tk
import math

def bezier_curve(points, num=100):
    n = len(points)
    if n < 2:
        return np.array([])
    b_points = np.zeros((num, 2))
    for i in range(num):
        t = i / (num - 1)
        b_point = np.zeros(2)
        for j in range(n):
            b_coeff = math.factorial(n - 1) / (math.factorial(j) * math.factorial(n - 1 - j)) * (t ** j) * ((1 - t) ** (n - 1 - j))
            b_point += b_coeff * points[j]
        b_points[i] = b_point
    return b_points

class DotCanvas(tk.Tk):
    def __init__(self):
        super().__init__()
        self.canvas = tk.Canvas(self, bg='white', width=800, height=800)
        self.canvas.pack(padx=10, pady=10)

        self.canvas.bind('<Button-1>', self.check_dot)
        self.canvas.bind('<B1-Motion>', self.move_dot)
        self.canvas.bind('<ButtonRelease-1>', self.release_dot)

        self.dots = {}
        self.selected_dot = None

    def add_dot(self, x, y):
        dot_id = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='black')
        self.dots[dot_id] = (x, y)
        self.redraw_curve()

    def check_dot(self, event):
        dot_id = self.canvas.find_closest(event.x, event.y)
        if dot_id and self.canvas.type(dot_id) == 'oval' and self.canvas.coords(dot_id[0])[0] <= event.x <= self.canvas.coords(dot_id[0])[2] and self.canvas.coords(dot_id[0])[1] <= event.y <= self.canvas.coords(dot_id[0])[3]:
            self.selected_dot = dot_id[0]
        else:
            self.add_dot(event.x, event.y)

    def move_dot(self, event):
        if self.selected_dot:
            self.canvas.coords(self.selected_dot, event.x - 5, event.y - 5, event.x + 5, event.y + 5)
            self.dots[self.selected_dot] = (event.x, event.y)
            self.redraw_curve()

    def release_dot(self, event):
        self.selected_dot = None

    def redraw_curve(self):
        self.canvas.delete('curve')  # Удаляем предыдущую кривую
        self.canvas.delete('polyline')  # Удаляем предыдущие линии
        points = np.array(list(self.dots.values()))
        if len(points) > 1:
            curve_points = bezier_curve(points, 100)
            for i in range(len(curve_points) - 1):
                self.canvas.create_line(curve_points[i][0], curve_points[i][1], curve_points[i+1][0], curve_points[i+1][1], tags='curve', fill='blue')
            for i in range(len(points) - 1):
                self.canvas.create_line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], tags='polyline', fill='red')

if __name__ == "__main__":
    app = DotCanvas()
    app.title('Drag & Drop Dots and Bezier Curve')
    app.mainloop()
