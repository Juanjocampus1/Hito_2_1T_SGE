# GraphTab.py
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
            "average_drinks_per_week": np.mean(data_np[:, 2:].astype(float), axis=0),
            "average_consumption_by_age_group": self.calculate_average_consumption_by_age_group(data_np),
            "alcohol_consumption": np.sum(data_np[:, 2:].astype(float), axis=1),
            "health_problems": np.sum(data_np[:, 7:].astype(float), axis=1)
        }
        return statistics

    def calculate_average_consumption_by_age_group(self, data):
        age_groups = [(0, 18), (19, 25), (26, 35), (36, 50), (51, 65), (66, 100)]
        age_group_labels = ["0-18", "19-25", "26-35", "36-50", "51-65", "66-100"]
        average_consumption = []

        for group in age_groups:
            group_data = data[(data[:, 0].astype(float) >= group[0]) & (data[:, 0].astype(float) <= group[1])]
            if group_data.size > 0:
                avg_consumption = np.mean(group_data[:, 2:].astype(float), axis=0)
                average_consumption.append(np.mean(avg_consumption))
            else:
                average_consumption.append(0)

        return age_group_labels, average_consumption

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

    def plot_average_consumption_by_age_group(self):
        self.clear_graph()
        statistics = self.fetch_and_process_data()
        labels, values = statistics["average_consumption_by_age_group"]
        ax = self.figure.add_subplot(111)
        ax.bar(labels, values)
        ax.set_title("Average Consumption by Age Group")
        ax.set_xlabel("Age Group")
        ax.set_ylabel("Average Consumption")
        self.canvas.draw()

    def plot_correlation(self):
        self.clear_graph()
        statistics = self.fetch_and_process_data()
        ax = self.figure.add_subplot(111)
        ax.scatter(statistics["alcohol_consumption"], statistics["health_problems"])
        ax.set_title("Correlation between Alcohol Consumption and Health Problems")
        ax.set_xlabel("Total Alcohol Consumption")
        ax.set_ylabel("Total Health Problems")
        self.canvas.draw()