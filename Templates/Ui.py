import tkinter as tk
from tkinter import ttk
from Repository import EncuestaDAO, filters


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Encuestas de Consumo de Alcohol")

        # Apply a theme
        style = ttk.Style()
        style.theme_use('clam')

        # Create Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        # Main tab
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text='Principal')

        # Filters tab
        self.filter_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.filter_frame, text='Filtros')

        # Table in the main tab
        self.tree = ttk.Treeview(self.main_frame, columns=("idEncuesta", "edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana", "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"), show='headings')
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.bind("<ButtonRelease-1>", self.on_row_select)

        # Buttons in the main tab
        button_frame = ttk.LabelFrame(self.main_frame, text="Operaciones")
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.create_button = ttk.Button(button_frame, text="Crear", command=self.create_record)
        self.create_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.read_button = ttk.Button(button_frame, text="Leer", command=self.read_records)
        self.read_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.update_button = ttk.Button(button_frame, text="Actualizar", command=self.update_record)
        self.update_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = ttk.Button(button_frame, text="Eliminar", command=self.delete_record)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Form for creating/updating records
        form_frame = ttk.LabelFrame(self.main_frame, text="Formulario")
        form_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.scrollbar = tk.Scrollbar(form_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.form_canvas = tk.Canvas(form_frame, yscrollcommand=self.scrollbar.set)
        self.form_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.form_canvas.yview)

        self.form_inner_frame = ttk.Frame(self.form_canvas)
        self.form_canvas.create_window((0, 0), window=self.form_inner_frame, anchor='nw')

        self.form_inner_frame.bind("<Configure>", lambda e: self.form_canvas.configure(scrollregion=self.form_canvas.bbox("all")))

        # Form fields in a grid
        self.fields = ["idEncuesta", "edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana", "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"]
        self.entries = {}
        for i, field in enumerate(self.fields):
            label = ttk.Label(self.form_inner_frame, text=field)
            label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
            entry = ttk.Entry(self.form_inner_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            if field == "idEncuesta":
                entry.config(state='disabled')
            self.entries[field] = entry

        self.form_inner_frame.columnconfigure(1, weight=1)

        # Table in the filters tab
        self.filter_tree = ttk.Treeview(self.filter_frame, columns=("idEncuesta", "edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana", "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"), show='headings')
        self.filter_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        for col in self.filter_tree["columns"]:
            self.filter_tree.heading(col, text=col)
            self.filter_tree.column(col, width=100)

        # Filter controls
        filter_controls_frame = ttk.LabelFrame(self.filter_frame, text="Controles de Filtros")
        filter_controls_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.search_label = ttk.Label(filter_controls_frame, text="Buscar:")
        self.search_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.search_entry = ttk.Entry(filter_controls_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.search_button = ttk.Button(filter_controls_frame, text="Buscar", command=self.search_records)
        self.search_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.sort_label = ttk.Label(filter_controls_frame, text="Ordenar por:")
        self.sort_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.sort_combobox = ttk.Combobox(filter_controls_frame, values=self.fields)
        self.sort_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.sort_button = ttk.Button(filter_controls_frame, text="Ordenar", command=self.sort_records)
        self.sort_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.sort_label = ttk.Label(filter_controls_frame, text="Recargar Datos:")
        self.sort_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.sort_button = ttk.Button(filter_controls_frame, text="Recargar", command=self.reload_records)
        self.sort_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Load data on startup
        self.read_records()
        self.read_filter_records()

    def on_row_select(self, event):
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item, 'values')
        for i, field in enumerate(self.fields):
            self.entries[field].delete(0, tk.END)
            self.entries[field].insert(0, values[i])

    def create_record(self):
        data = tuple(self.entries[field].get() for field in self.fields[1:])
        EncuestaDAO.Database().create_record(data)
        self.read_records()
        self.clear_form()

    def read_records(self):
        records = EncuestaDAO.Database().read_records()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for record in records:
            self.tree.insert("", tk.END, values=record)

    def read_filter_records(self):
        records = EncuestaDAO.Database().read_records()
        for row in self.filter_tree.get_children():
            self.filter_tree.delete(row)
        for record in records:
            self.filter_tree.insert("", tk.END, values=record)

    def update_record(self):
        selected_item = self.tree.selection()[0]
        idEncuesta = self.tree.item(selected_item, 'values')[0]
        data = tuple(self.entries[field].get() for field in self.fields[1:])
        EncuestaDAO.Database().update_record(idEncuesta, data)
        self.read_records()
        self.clear_form()

    def delete_record(self):
        selected_item = self.tree.selection()[0]
        idEncuesta = self.tree.item(selected_item, 'values')[0]
        EncuestaDAO.Database().delete_record(idEncuesta)
        self.read_records()
        self.clear_form()

    def clear_form(self):
        for field, entry in self.entries.items():
            entry.config(state='normal')
            entry.delete(0, tk.END)
            if field == "idEncuesta":
                entry.config(state='disabled')

    def search_records(self):
        idEncuesta = self.search_entry.get()
        results = filters.search_by_id(idEncuesta)
        for row in self.filter_tree.get_children():
            self.filter_tree.delete(row)
        for record in results:
            self.filter_tree.insert("", tk.END, values=record)

    def sort_records(self):
        # Implement sort logic here
        pass

    def reload_records(self):
        self.read_records()
        self.read_filter_records()