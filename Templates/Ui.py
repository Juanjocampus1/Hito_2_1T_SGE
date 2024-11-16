# Ui.py
import tkinter as tk
from tkinter import Menu
from tkinter import ttk
from Repository import EncuestaDAO, filters
import pandas as pd
from Graph.GraphTab import GraphTab

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Encuestas de Consumo de Alcohol")

        self.menu_bar = Menu(root)
        root.config(menu=self.menu_bar)

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

        # Graphs tab
        self.graph_tab = GraphTab(self.notebook)
        self.notebook.add(self.graph_tab.frame, text='Gráficos')

        # Add buttons to generate different types of graphs at the top
        graph_button_frame = ttk.Frame(self.graph_tab.frame)
        graph_button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        average_age_button = ttk.Button(graph_button_frame, text="Average Age", command=self.graph_tab.plot_age_statistics)
        average_age_button.pack(side=tk.LEFT, padx=5, pady=5)

        gender_distribution_button = ttk.Button(graph_button_frame, text="Gender Distribution", command=self.graph_tab.plot_gender_distribution)
        gender_distribution_button.pack(side=tk.LEFT, padx=5, pady=5)

        average_drinks_button = ttk.Button(graph_button_frame, text="Average Drinks per Week", command=self.graph_tab.plot_average_drinks_per_week)
        average_drinks_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Table in the main tab
        self.tree = ttk.Treeview(self.main_frame, columns=("idEncuesta", "edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana", "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"), show='headings')
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.bind("<ButtonRelease-1>", self.on_row_select)

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

        form_frame = ttk.LabelFrame(self.main_frame, text="Formulario")
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

        self.fields = ["idEncuesta", "edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana",
                       "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol",
                       "ProblemasDigestivos", "TensionAlta", "DolorCabeza"]
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

        self.filter_tree = ttk.Treeview(self.filter_frame, columns=("idEncuesta", "edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana", "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"), show='headings')
        self.filter_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        for col in self.filter_tree["columns"]:
            self.filter_tree.heading(col, text=col)
            self.filter_tree.column(col, width=100)

        filter_controls_frame = ttk.LabelFrame(self.filter_frame, text="Controles de Filtros")
        filter_controls_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        filter_canvas = tk.Canvas(filter_controls_frame)
        filter_scrollbar = ttk.Scrollbar(filter_controls_frame, orient="vertical", command=filter_canvas.yview)
        filter_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        filter_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        filter_canvas.configure(yscrollcommand=filter_scrollbar.set)

        filter_controls_inner_frame = ttk.Frame(filter_canvas)
        filter_canvas.create_window((0, 0), window=filter_controls_inner_frame, anchor='nw')

        filter_controls_inner_frame.bind("<Configure>",
                                         lambda e: filter_canvas.configure(scrollregion=filter_canvas.bbox("all")))

        def on_mouse_wheel(event):
            filter_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        filter_canvas.bind_all("<MouseWheel>", on_mouse_wheel)

        self.filter_entries = {}
        for field in self.fields:
            label = ttk.Label(filter_controls_inner_frame, text=f"Filtrar por {field}:")
            label.grid(row=self.fields.index(field), column=0, padx=5, pady=5, sticky='w')
            entry = ttk.Entry(filter_controls_inner_frame)
            entry.grid(row=self.fields.index(field), column=1, padx=5, pady=5, sticky='ew')
            self.filter_entries[field] = entry

        self.apply_filter_button = ttk.Button(filter_controls_inner_frame, text="Aplicar Filtro",
                                              command=self.apply_filter)
        self.apply_filter_button.grid(row=len(self.fields), column=0, padx=5, pady=5, sticky='ew')

        self.download_filtered_button = ttk.Button(filter_controls_inner_frame, text="Descargar Estado Actual",
                                                   command=self.download_filtered_state)
        self.download_filtered_button.grid(row=len(self.fields), column=1, padx=5, pady=5, sticky='ew')

        self.search_label = ttk.Label(filter_controls_inner_frame, text="Buscar por id:")
        self.search_label.grid(row=len(self.fields) + 1, column=0, padx=5, pady=5, sticky='w')
        self.search_entry = ttk.Entry(filter_controls_inner_frame)
        self.search_entry.grid(row=len(self.fields) + 1, column=1, padx=5, pady=5, sticky='ew')
        self.search_button = ttk.Button(filter_controls_inner_frame, text="Buscar", command=self.search_records)
        self.search_button.grid(row=len(self.fields) + 2, column=0, padx=5, pady=5, sticky='ew')

        self.sort_label = ttk.Label(filter_controls_inner_frame, text="Ordenar por:")
        self.sort_label.grid(row=len(self.fields) + 2, column=1, padx=5, pady=5, sticky='w')
        self.sort_combobox = ttk.Combobox(filter_controls_inner_frame, values=self.fields)
        self.sort_combobox.grid(row=len(self.fields) + 3, column=0, padx=5, pady=5, sticky='ew')
        self.sort_button = ttk.Button(filter_controls_inner_frame, text="Ordenar", command=self.sort_records)
        self.sort_button.grid(row=len(self.fields) + 3, column=1, padx=5, pady=5, sticky='ew')

        self.reload_label = ttk.Label(filter_controls_inner_frame, text="Recargar Datos:")
        self.reload_label.grid(row=len(self.fields) + 4, column=0, padx=5, pady=5, sticky='w')
        self.reload_button = ttk.Button(filter_controls_inner_frame, text="Recargar", command=self.reload_records)
        self.reload_button.grid(row=len(self.fields) + 4, column=1, padx=5, pady=5, sticky='ew')

        # Create "Archivo" menu
        self.archivo_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Archivo", menu=self.archivo_menu)
        self.archivo_menu.add_command(label="Descargar DB en Excel", command=self.download_db_to_excel)
        self.archivo_menu.add_separator()
        for field in self.fields:
            self.archivo_menu.add_command(label=f"Descargar {field} en Excel", command=lambda f=field: self.download_column_to_excel(f))

        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

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

        records = EncuestaDAO.Database().read_records()
        sorted_records = sorted(records, key=lambda x: x[self.fields.index(sort_column)])

        for row in self.filter_tree.get_children():
            self.filter_tree.delete(row)

        new_columns = ["idEncuesta", sort_column] + [col for col in self.fields if
                                                    col not in ["idEncuesta", sort_column]]
        self.filter_tree["columns"] = new_columns

        for col in new_columns:
            self.filter_tree.heading(col, text=col)
            self.filter_tree.column(col, width=100)

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
        self.tree["columns"] = self.fields
        self.filter_tree["columns"] = self.fields

        for col in self.fields:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
            self.filter_tree.heading(col, text=col)
            self.filter_tree.column(col, width=100)

        self.read_records()
        self.read_filter_records()