import tkinter as tk
from Templates import Ui

if __name__ == "__main__":
    root = tk.Tk()
    root.state("zoomed")
    app = Ui.App(root)
    root.mainloop()