import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from random import sample
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler

class KmeansInteractive:
    """ Interactive K-means """

    COLORS = ["firebrick", "mediumpurple", "forestgreen", "lightsalmon", "gray"]

    def __init__(self):
        
        self.master = tk.Tk()
        
        # Kmeans step
        self.km_step = 1

        # Height and width
        self.screen_height = self.master.winfo_screenheight()
        self.screen_width = self.master.winfo_screenwidth()
        self.HEIGHT = int(self.screen_height * 0.7)
        self.WIDTH = int((4/3) * self.HEIGHT)

        # Window customization : Title + geometry
        self.master.title("Interactive K-means")
        self.master.geometry("{}x{}+{}+{}".format(self.WIDTH, self.HEIGHT, int((self.screen_width-self.WIDTH)/2), int((self.screen_height-2*self.HEIGHT)/2)))
        self.master.minsize(self.WIDTH, self.HEIGHT)
        self.master.maxsize(self.WIDTH, self.HEIGHT)
        self.master.config(bg="#D8EEED")       

        # Matplotlib Canvas
        self.figure = Figure(figsize=((3*self.WIDTH/4)/102, (self.HEIGHT)/102))
        self.ax = self.figure.add_subplot(1,1,1)
        self.canvas = FigureCanvasTkAgg(self.figure, self.master)
        self.canvas.get_tk_widget().configure(highlightbackground="black", highlightthickness=2)
        self.canvas.get_tk_widget().grid(row=0, column=1)

        # Message k-means step (placed with kmeans_step() func)
        self.km_step_label = tk.Label(self.canvas.get_tk_widget(), font=("Helvetica", int(self.screen_height/90)), bg="white")

        # Left frame
        self.left_frame = tk.Frame(self.master, height=self.HEIGHT, width=self.WIDTH/4, bg="#D8EEED")
        self.left_frame.grid(row=0, column=0)

        # New sample
        self.clusters_label = tk.Label(self.left_frame, text="Number of clusters :", bg="#D8EEED", anchor="se")
        self.clusters_label.place(relx=0.05, rely=0.05, relheight=0.03, relwidth=0.6)

        values_cluster = [2, 3, 4, 5]
        self.clusters_cb = ttk.Combobox(self.left_frame, values=values_cluster, state="readonly")
        self.clusters_cb.current(1)
        self.clusters_cb.place(relx=0.7, rely=0.05, relheight=0.03, relwidth=0.15)

        self.newsample_button = tk.Button(self.left_frame, text="NEW SAMPLE", command=self.new_sample)
        self.newsample_button.place(relx=0.2, rely=0.09, relheight=0.05, relwidth=0.6)

        # Initialisation centroid
        self.centroids_label = tk.Label(self.left_frame, text="Number of centroids :", bg="#D8EEED", anchor="se")
        self.centroids_label.place(relx=0.05, rely=0.20, relheight=0.03, relwidth=0.6)

        values_centroid = [2, 3, 4, 5]
        self.centroids_cb = ttk.Combobox(self.left_frame, values=values_centroid, state="readonly")
        self.centroids_cb.current(1)
        self.centroids_cb.place(relx=0.70, rely=0.20, relheight=0.03, relwidth=0.15)

        self.initcentroid_button = tk.Button(self.left_frame, text="INIT CENTROIDS", command=self.init_centroids)
        self.initcentroid_button.place(relx=0.2, rely=0.24, relheight=0.05, relwidth=0.6)

        # Kmeans step frame
        self.km_label = tk.Label(self.left_frame, text="K-means Steps", bg="#D8EEED", 
                                 font=("Helvetica", int(self.screen_height/60), "bold"))
        self.km_label.place(relx=0, rely=0.50, relheight=0.05, relwidth=1)

        self.km_next_button = tk.Button(self.left_frame, text="NEXT", state="disable", command=self.kmeans_step)
        self.km_next_button.place(relx=0.3, rely=0.55, relheight=0.05, relwidth=0.4)

        # Inertia label (placed with _get_inertia func)
        self.inertia_label = tk.Label(self.left_frame, font=("Helvetica", int(self.screen_height/80)), bg="#D8EEED")

        # Clear Button
        self.clear_button = tk.Button(self.left_frame, text="CLEAR", command=self.clear_canvas)
        self.clear_button.place(relx=0.2, rely=0.9, relheight=0.05, relwidth=0.6)

        # Randomize
        self.new_sample()
        self.master.mainloop()

    def new_sample(self):
        """ Generate new sample """

        self.n_samples = 100
        nb_clusters = int(self.clusters_cb.get())

        # hide inertia label and km_step_label
        self.inertia_label.place_forget()
        self.km_step_label.place_forget()

        # enable centroids init
        self.centroids_label.configure(state="normal")
        self.centroids_cb.configure(state="readonly")
        self.initcentroid_button.configure(state="normal")

        # dinable kmeans steps
        self.km_next_button.configure(state="disable")

        # randomize depending of clusters
        if nb_clusters == 2:
            self.X , _ = make_blobs(n_samples=100, centers=[(0,5), (5,0)], n_features=2)
        elif nb_clusters == 3:
            self.X , _ = make_blobs(n_samples=100, centers=[(3.5,0), (0,7), (7,7)], n_features=2)
        elif nb_clusters == 4:
            self.X , _ = make_blobs(n_samples=100, centers=[(0,0), (7,0), (0,7), (7,7)], n_features=2)
        elif nb_clusters == 5:
            self.X , _ = make_blobs(n_samples=100, centers=[(0,0), (9,0), (0,9), (9,9), (4.5,4.5)], n_features=2)

        # Scaler
        self.X = StandardScaler().fit_transform(self.X)

        self.ax.clear()
        self.ax.scatter(self.X[:, 0], self.X[:, 1], c="white", s=100, edgecolors="black")
        self._clear_axis()

    def clear_canvas(self):
        """ Clear canvas """

        # hide inertia label and km_step_label
        self.inertia_label.place_forget()
        self.km_step_label.place_forget()

        # disabled centroids init
        self.centroids_label.configure(state="disabled")
        self.centroids_cb.configure(state="disabled")
        self.initcentroid_button.configure(state="disabled")

        # dinable kmeans steps
        self.km_next_button.configure(state="disable")
        
        # clear canvas
        self.ax.clear()
        self._clear_axis()

    def init_centroids(self):
        """ Centroids initialisation """

        self.nb_centroids = int(self.centroids_cb.get())
        self.idx_centroids = sample(range(self.n_samples), self.nb_centroids)
        self.centroids = self.X[self.idx_centroids, :]

        # hide inertia label and init km_step_label
        self.inertia_label.place_forget()
        self.km_step_label.config(text = "0. Centroids initialization", fg="black")
        self.km_step_label.place(relx=0.01, rely=0.965, relheight=0.03)
        
        # enable kmeans steps
        self.km_next_button.configure(state="normal")

        # plot
        self.ax.clear()
        self.ax.scatter(self.X[:, 0], self.X[:, 1], c="white", s=100, edgecolors="black")
        self._plot_centroids()
        self.km_step = 1

    def kmeans_step(self):
        """ A k-means step """

        if self.km_step == 1:
            # assign point to nearest centroid
            self.distance_matrix = np.zeros((self.n_samples, self.nb_centroids))
            
            for j in range(self.nb_centroids):
                for i in range(self.n_samples):
                    self.distance_matrix[i,j] = self._euclidian_distance(self.centroids[j], self.X[i,:])
            self.classes = np.argmin(self.distance_matrix, axis=1)
            self._assign_points()
            self._get_inertia()
            self.km_step_label.config(text = "1. Assign points to nearest centroids", fg="black")
            self.km_step_label.place(relx=0.01, rely=0.965, relheight=0.03)
            self.km_step = 2
        
        elif self.km_step == 2:
            # update centroid
            self.new_centroids = np.zeros((self.nb_centroids, 2))

            for i in range(self.nb_centroids):
                self.new_centroids[i, :] = self.X[np.where(self.classes == i)[0], :].mean(axis=0)
                self.ax.plot([self.centroids[i, 0], self.new_centroids[i,0]], [self.centroids[i, 1], self.new_centroids[i,1]],
                             c="black", linewidth=2)
                self._clear_axis()

            # Check if kmeans converged
            if np.array_equal(self.new_centroids, self.centroids):
                self.km_next_button.configure(state="disabled")
                self.km_step_label.config(text = "K-means algorithm converged !", fg="red")
                self.km_step_label.place(relx=0.01, rely=0.965, relheight=0.03) 
            else:
                self.centroids = self.new_centroids
                self._plot_centroids()
                self.km_step_label.config(text = "2. Update centroids to cluster means", fg="black")
                self.km_step_label.place(relx=0.01, rely=0.965, relheight=0.03)            
                self.km_step = 1

    def _get_inertia(self):
        """ Calculation of inertia """
        
        self.inertia = 0

        for j in range(self.nb_centroids):
            ind_class_j = self.X[np.where(self.classes == j)[0], :]
            for i in range(ind_class_j.shape[0]):
                self.inertia += self._euclidian_distance(self.centroids[j], ind_class_j[i, :])
        
        self.inertia = round(self.inertia, 2)
        self.inertia_label.config(text = "Inertia : {}".format(self.inertia))
        self.inertia_label.place(relx=0, rely=0.61, relheight=0.04, relwidth=1)

    def _assign_points(self):
        """ Assign points to nearest centroid and plot them """
        
        self.classes_color = list(self.classes)[:]
        for i in range(self.nb_centroids):
            self.classes_color = self._replace_list(self.classes_color, i, self.COLORS[i])

        self.ax.clear()
        self.ax.scatter(self.X[:, 0], self.X[:, 1], c=self.classes_color, s=100, edgecolors="black", linewidths=1)
        self._plot_centroids()

    def _plot_centroids(self):
        """ Plot centroids """

        centroids_color = self.COLORS[:self.nb_centroids]
        self.ax.scatter(self.centroids[:, 0], self.centroids[:, 1], c="black", s=200, edgecolors=centroids_color,
                        linewidths=4)
        self._clear_axis()

    @staticmethod
    def _replace_list(l, old, new):
        """ replace element in list """
        
        return [new if item == old else item for item in l]

    @staticmethod
    def _euclidian_distance(point1, point2):
        """ Euclidian distance between point1 and point2 """

        distance = 0
        for i in range(len(point1)):
            distance += (point1[i] - point2[i])**2
        
        return distance

    def _clear_axis(self):
        """ Clear axis and draw """

        self.ax.axis("off")
        self.ax.axis("equal")
        self.figure.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    KmeansInteractive()
