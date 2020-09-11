import numpy as np
import tkinter as tk

class KmeansInteractive:
    
    def __init__(self):
        
        self.master = tk.Tk()
        
        # Window customization
        self.master.title("Interactive K-means")

        self.master.mainloop()


if __name__ == "__main__":
    KmeansInteractive()
