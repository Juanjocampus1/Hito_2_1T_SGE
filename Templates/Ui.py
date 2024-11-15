import tkinter as tk
from tkinter import Menu
from tkinter import ttk
from Repository import EncuestaDAO, filters
import pandas as pd
from ttkbootstrap import Style
from ttkbootstrap.constants import *

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Encuestas de Consumo de Alcohol")

        self.menu_bar = Menu(root)
        root.config(menu=self.menu_bar)

        # Apply a modern theme
        style = Style(theme='cosmo')

        # Create Notebook for tabs
        self.notebook = ttk.Notebook(root, bootstyle="primary")
        self.notebook.pack(expand=True, fill='both')

        # Main tab
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text='Principal')

        # Filters tab
        self.filter_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.filter_frame, text='Filtros')

        # Table in the main tab
        self.tree = ttk.Treeview(self.main_frame, columns=(
        "idEncuesta", "edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana", "BebidasDestiladasSemana",
        "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta",
        "DolorCabeza"), show='headings', bootstyle="info")
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.bind("<ButtonRelease-1>", self.on_row_select)

        # Buttons in the main tab
        button_frame = ttk.LabelFrame(self.main_frame, text="Operaciones", bootstyle="success")
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.create_button = ttk.Button(button_frame, text="Crear", command=self.create_record,
                                        bootstyle="success-outline")
        self.create_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.read_button = ttk.Button(button_frame, text="Leer", command=self.read_records, bootstyle="info-outline")
        self.read_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.update_button = ttk.Button(button_frame, text="Actualizar", command=self.update_record,
                                        bootstyle="warning-outline")
        self.update_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = ttk.Button(button_frame, text="Eliminar", command=self.delete_record,
                                        bootstyle="danger-outline")
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Form for creating/updating records
        form_frame = ttk.LabelFrame(self.main_frame, text="Formulario", bootstyle="primary")
        form_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.scrollbar = ttk.Scrollbar(form_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.form_canvas = tk.Canvas(form_frame, yscrollcommand=self.scrollbar.set)
        self.form_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.form_canvas.yview)

        self.form_inner_frame = ttk.Frame(self.form_canvas)
        self.form_canvas.create_window((0, 0), window=self.form_inner_frame, anchor='nw')

        self.form_inner_frame.bind("<Configure>",
                                   lambda e: self.form_canvas.configure(scrollregion=self.form_canvas.bbox("all")))

        # Form fields in a grid
        self.fields = ["idEncuesta", "edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana",
                       "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol",
                       "ProblemasDigestivos", "TensionAlta", "DolorCabeza"]
        self.entries = {}
        for i, field in enumerate(self.fields):
            label = ttk.Label(self.form_inner_frame, text=field, bootstyle="primary")
            label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
            entry = ttk.Entry(self.form_inner_frame, bootstyle="info")
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            if field == "idEncuesta":
                entry.config(state='disabled')
            self.entries[field] = entry

        self.form_inner_frame.columnconfigure(1, weight=1)

        # Table in the filters tab
        self.filter_tree = ttk.Treeview(self.filter_frame, columns=(
        "idEncuesta", "edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana", "BebidasDestiladasSemana",
        "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta",
        "DolorCabeza"), show='headings', bootstyle="info")
        self.filter_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        for col in self.filter_tree["columns"]:
            self.filter_tree.heading(col, text=col)
            self.filter_tree.column(col, width=100)

        # Filter controls
        filter_controls_frame = ttk.LabelFrame(self.filter_frame, text="Controles de Filtros", bootstyle="primary")
        filter_controls_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add a canvas and scrollbar to the filter controls frame
        filter_canvas = tk.Canvas(filter_controls_frame)
        filter_scrollbar = ttk.Scrollbar(filter_controls_frame, orient="vertical", command=filter_canvas.yview)
        filter_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        filter_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        filter_canvas.configure(yscrollcommand=filter_scrollbar.set)

        filter_controls_inner_frame = ttk.Frame(filter_canvas)
        filter_canvas.create_window((0, 0), window=filter_controls_inner_frame, anchor='nw')

        # Ensure the inner frame resizes with the canvas
        filter_controls_inner_frame.bind("<Configure>",
                                         lambda e: filter_canvas.configure(scrollregion=filter_canvas.bbox("all")))

        # Enable mouse wheel scrolling
        def on_mouse_wheel(event):
            filter_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        filter_canvas.bind_all("<MouseWheel>", on_mouse_wheel)

        self.filter_entries = {}
        for field in self.fields:
            label = ttk.Label(filter_controls_inner_frame, text=f"Filtrar por {field}:", bootstyle="primary")
            label.grid(row=self.fields.index(field), column=0, padx=5, pady=5, sticky='w')
            entry = ttk.Entry(filter_controls_inner_frame, bootstyle="info")
            entry.grid(row=self.fields.index(field), column=1, padx=5, pady=5, sticky='ew')
            self.filter_entries[field] = entry

        self.apply_filter_button = ttk.Button(filter_controls_inner_frame, text="Aplicar Filtro",
                                              command=self.apply_filter, bootstyle="success-outline")
        self.apply_filter_button.grid(row=len(self.fields), column=0, padx=5, pady=5, sticky='ew')

        self.download_filtered_button = ttk.Button(filter_controls_inner_frame, text="Descargar Estado Actual",
                                                   command=self.download_filtered_state, bootstyle="info-outline")
        self.download_filtered_button.grid(row=len(self.fields), column=1, padx=5, pady=5, sticky='ew')

        self.search_label = ttk.Label(filter_controls_inner_frame, text="Buscar por id:", bootstyle="primary")
        self.search_label.grid(row=len(self.fields) + 1, column=0, padx=5, pady=5, sticky='w')
        self.search_entry = ttk.Entry(filter_controls_inner_frame, bootstyle="info")
        self.search_entry.grid(row=len(self.fields) + 1, column=1, padx=5, pady=5, sticky='ew')
        self.search_button = ttk.Button(filter_controls_inner_frame, text="Buscar", command=self.search_records,
                                        bootstyle="info-outline")
        self.search_button.grid(row=len(self.fields) + 2, column=0, padx=5, pady=5, sticky='ew')

        self.sort_label = ttk.Label(filter_controls_inner_frame, text="Ordenar por:", bootstyle="primary")
        self.sort_label.grid(row=len(self.fields) + 2, column=1, padx=5, pady=5, sticky='w')
        self.sort_combobox = ttk.Combobox(filter_controls_inner_frame, values=self.fields, bootstyle="info")
        self.sort_combobox.grid(row=len(self.fields) + 3, column=0, padx=5, pady=5, sticky='ew')
        self.sort_button = ttk.Button(filter_controls_inner_frame, text="Ordenar", command=self.sort_records,
                                      bootstyle="info-outline")
        self.sort_button.grid(row=len(self.fields) + 3, column=1, padx=5, pady=5, sticky='ew')

        self.reload_label = ttk.Label(filter_controls_inner_frame, text="Recargar Datos:", bootstyle="primary")
        self.reload_label.grid(row=len(self.fields) + 4, column=0, padx=5, pady=5, sticky='w')
        self.reload_button = ttk.Button(filter_controls_inner_frame, text="Recargar", command=self.reload_records,
                                        bootstyle="info-outline")
        self.reload_button.grid(row=len(self.fields) + 4, column=1, padx=5, pady=5, sticky='ew')

        # Create "Edit" menu
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

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
        sort_column = self.sort_combobox.get()
        if not sort_column:
            return

        # Obtener todos los registros
        records = EncuestaDAO.Database().read_records()

        # Ordenar los registros por la columna seleccionada
        sorted_records = sorted(records, key=lambda x: x[self.fields.index(sort_column)])

        # Limpiar la tabla de filtros
        for row in self.filter_tree.get_children():
            self.filter_tree.delete(row)

        # Reorganizar los encabezados de las columnas
        new_columns = ["idEncuesta", sort_column] + [col for col in self.fields if
                                                    col not in ["idEncuesta", sort_column]]
        self.filter_tree["columns"] = new_columns

        for col in new_columns:
            self.filter_tree.heading(col, text=col)
            self.filter_tree.column(col, width=100)

        # Insertar los registros ordenados en la tabla de filtros
        for record in sorted_records:
            reordered_record = (record[0], record[self.fields.index(sort_column)]) + tuple(
                value for i, value in enumerate(record) if i != 0 and i != self.fields.index(sort_column)
            )
            self.filter_tree.insert("", tk.END, values=reordered_record)

    def apply_filter(self):
        filters = {field: entry.get() for field, entry in self.filter_entries.items() if entry.get()}
        records = EncuestaDAO.Database().read_records()
        filtered_records = [record for record in records if all(str(record[self.fields.index(field)]) == value for field, value in filters.items())]
        for row in self.filter_tree.get_children():
            self.filter_tree.delete(row)
        for record in filtered_records:
            self.filter_tree.insert("", tk.END, values=record)

    def download_db_to_excel(self):
        records = EncuestaDAO.Database().read_records()
        df = pd.DataFrame(records, columns=self.fields)
        df.to_excel("database.xlsx", index=False)
        print("Database downloaded to database.xlsx")

    def download_column_to_excel(self, column):
        records = EncuestaDAO.Database().read_records()
        df = pd.DataFrame(records, columns=self.fields)
        df[[column]].to_excel(f"{column}.xlsx", index=False)
        print(f"Column {column} downloaded to {column}.xlsx")

    def download_filtered_state(self):
        records = [self.filter_tree.item(row)["values"] for row in self.filter_tree.get_children()]
        df = pd.DataFrame(records, columns=self.fields)
        df.to_excel("filtered_state.xlsx", index=False)
        print("Filtered state downloaded to filtered_state.xlsx")

    def reload_records(self):
        # Reset columns to their original order
        self.tree["columns"] = self.fields
        self.filter_tree["columns"] = self.fields

        for col in self.fields:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
            self.filter_tree.heading(col, text=col)
            self.filter_tree.column(col, width=100)

        # Reload records
        self.read_records()
        self.read_filter_records()