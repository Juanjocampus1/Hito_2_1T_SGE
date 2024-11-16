import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy import stats
from Repository.EncuestaDAO import Database

class GraphTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(expand=True, fill='both')

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def clear_graph(self):
        self.figure.clf()
        self.canvas.draw()

    def fetch_and_process_data(self):

        db = Database()
        data = db.fetch_statistics()
        db.close()

        # Process data to generate statistics
        data_np = np.array(data)
        ages = data_np[:, 0].astype(float)
        mode_age = stats.mode(ages)
        mode_age_value = mode_age.mode[0] if mode_age.count.ndim > 0 else None

        statistics = {
            "average_age": np.mean(ages),
            "highest_age": np.max(ages),
            "lowest_age": np.min(ages),
            "mode_age": mode_age_value,
            "median_age": np.median(ages),
            "std_dev_age": np.std(ages),
            "gender_distribution": np.unique(data_np[:, 1], return_counts=True),
            "average_drinks_per_week": np.mean(data_np[:, 2:].astype(float), axis=0)
        }
        return statistics

    def plot_age_statistics(self):
        self.clear_graph()
        statistics = self.fetch_and_process_data()
        ax = self.figure.add_subplot(111)
        ax.scatter(["Average Age"], [statistics["average_age"]], label="Average Age")
        ax.scatter(["Highest Age"], [statistics["highest_age"]], label="Highest Age")
        ax.scatter(["Lowest Age"], [statistics["lowest_age"]], label="Lowest Age")
        ax.scatter(["Mode Age"], [statistics["mode_age"]], label="Mode Age")
        ax.scatter(["Median Age"], [statistics["median_age"]], label="Median Age")
        ax.scatter(["Std Dev Age"], [statistics["std_dev_age"]], label="Std Dev Age")
        ax.set_title("Age Statistics")
        ax.set_xlabel("Statistics")
        ax.set_ylabel("Values")
        ax.legend()
        self.canvas.draw()

    def plot_gender_distribution(self):
        self.clear_graph()
        statistics = self.fetch_and_process_data()
        labels, counts = statistics["gender_distribution"]
        ax = self.figure.add_subplot(111)
        ax.pie(counts, labels=labels, autopct='%1.1f%%')
        ax.set_title("Gender Distribution")
        self.canvas.draw()

    def plot_average_drinks_per_week(self):
        self.clear_graph()
        statistics = self.fetch_and_process_data()
        labels = ["BebidasSemana", "CervezasSemana", "BebidasFinSemana", "BebidasDestiladasSemana", "VinosSemana"]
        ax = self.figure.add_subplot(111)
        ax.bar(labels, statistics["average_drinks_per_week"])
        ax.set_title("Average Drinks per Week")
        self.canvas.draw()