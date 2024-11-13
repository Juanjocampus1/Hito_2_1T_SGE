import tkinter as tk
from tkinter import ttk
import EncuestaDAO

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Encuestas de Consumo de Alcohol")

        # Menú
        menu = tk.Menu(root)
        root.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Salir", command=root.quit)

        # Botones
        button_frame = tk.Frame(root)
        button_frame.pack(side=tk.TOP, fill=tk.X)

        self.create_button = tk.Button(button_frame, text="Crear", command=self.create_record)
        self.create_button.pack(side=tk.LEFT)

        self.read_button = tk.Button(button_frame, text="Leer", command=self.read_records)
        self.read_button.pack(side=tk.LEFT)

        self.update_button = tk.Button(button_frame, text="Actualizar", command=self.update_record)
        self.update_button.pack(side=tk.LEFT)

        self.delete_button = tk.Button(button_frame, text="Eliminar", command=self.delete_record)
        self.delete_button.pack(side=tk.LEFT)

        # Tabla
        self.tree = ttk.Treeview(root, columns=("idEncuesta", "edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana", "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"), show='headings')
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Load data on startup
        self.read_records()

    def create_record(self):
        # Implementar la lógica para crear un registro
        pass

    def read_records(self):
        records = EncuestaDAO.Database().read_records()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for record in records:
            self.tree.insert("", tk.END, values=record)

    def update_record(self):
        # Implementar la lógica para actualizar un registro
        pass

    def delete_record(self):
        # Implementar la lógica para eliminar un registro
        pass