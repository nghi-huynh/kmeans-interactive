import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class KmeansInteractive:
    
    def __init__(self):
        
        self.master = tk.Tk()

        # Height and width
        screen_height = self.master.winfo_screenheight()
        self.HEIGHT = int(screen_height * 0.7)
        self.WIDTH = int((4/3) * self.HEIGHT)

        # Window customization : Title + geometry
        self.master.title("Interactive K-means")
        self.master.geometry("{}x{}".format(self.WIDTH, self.HEIGHT))
        self.master.minsize(self.WIDTH, self.HEIGHT)
        self.master.maxsize(self.WIDTH, self.HEIGHT)
        self.master.config(bg="#D8EEED")       

        # Matplotlib Canvas
        self.figure = Figure(figsize=((3*self.WIDTH/4)/102, (self.HEIGHT)/102))
        self.ax = self.figure.add_subplot(1,1,1)
        self.ax.axis("off")
        self.canvas = FigureCanvasTkAgg(self.figure, self.master)
        self.canvas.get_tk_widget().configure(highlightbackground="black", highlightthickness=2)
        self.canvas.get_tk_widget().grid(row=0, column=1)
        self.figure.tight_layout()

        # Left frame
        self.left_frame = tk.Frame(self.master, height=self.HEIGHT, width=self.WIDTH/4, bg="#D8EEED")
        self.left_frame.grid(row=0, column=0)

        # Kmeans step frame
        self.km_label = tk.Label(self.left_frame, text="K-means Steps", bg="#D8EEED", 
                                 font=("Helvetica", int(screen_height/60), "bold"))
        self.km_label.place(relx=0, rely=0.05, relheight=0.05, relwidth=1)

        self.km_next_button = tk.Button(self.left_frame, text="NEXT")
        self.km_next_button.place(relx=0.3, rely=0.1, relheight=0.05, relwidth=0.4)

        # New sample
        self.centroids_label = tk.Label(self.left_frame, text="Number of centroids :", bg="#D8EEED", anchor="se")
        self.centroids_label.place(relx=0.05, rely=0.3, relheight=0.03, relwidth=0.6)

        values_centroid = [2, 3, 4, 5]
        self.centroids_cb = ttk.Combobox(self.left_frame, values=values_centroid)
        self.centroids_cb.current(1)
        self.centroids_cb.place(relx=0.70, rely=0.3, relheight=0.03, relwidth=0.15)

        self.clusters_label = tk.Label(self.left_frame, text="Number of clusters :", bg="#D8EEED", anchor="se")
        self.clusters_label.place(relx=0.05, rely=0.33, relheight=0.03, relwidth=0.6)

        values_cluster = [2, 3, 4, 5]
        self.clusters_cb = ttk.Combobox(self.left_frame, values=values_cluster)
        self.clusters_cb.current(1)
        self.clusters_cb.place(relx=0.7, rely=0.33, relheight=0.03, relwidth=0.15)

        self.newsample_button = tk.Button(self.left_frame, text="NEW SAMPLE")
        self.newsample_button.place(relx=0.2, rely=0.37, relheight=0.05, relwidth=0.6)

        # Clear Button
        self.clear_button = tk.Button(self.left_frame, text="CLEAR")
        self.clear_button.place(relx=0.2, rely=0.9, relheight=0.05, relwidth=0.6)

        self.master.mainloop()


if __name__ == "__main__":
    KmeansInteractive()
