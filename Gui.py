import tkinter as tk
from tkinter import ttk

import Label_specs
import Anag
import Make_Labels


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        size = (760, 500)
        self.tk.call('tk', 'scaling', 2.0)
        self.geometry(f'{size[0]}x{size[1]}')
        self.maxsize(size[0], size[1])
        self.title('Jono Label Maker')
        self.grid()

        self.entry_string_var = tk.StringVar()
        self.entry_string_var.set(Label_specs.DEFAULT)

        # place a button on the root window
        label_top = ttk.Label(text='Label Size:', justify='center', font='bold')
        label_top.grid(row=0, columnspan=4, column=0, pady=5)

        self.text_widget = tk.Text(self, height=20, width=24)
        scroll_bar = tk.Scrollbar(self, orient='vertical', command=self.text_widget.yview)
        self.text_widget.config(yscrollcommand=scroll_bar.set)
        scroll_bar.grid(rowspan=12, row=1, column=6, sticky='ns')
        self.text_widget.grid(rowspan=12, row=1, column=5, sticky='nw')
        self.text_widget.insert(tk.END, Anag.get_bin_list_text(self.entry_string_var.get()))

        self.combo_box_var = tk.StringVar()
        combo_box = ttk.Combobox(self, textvariable=self.combo_box_var)
        combo_box['values'] = list(Label_specs.LABELS.keys())
        combo_box.set(list(Label_specs.LABELS.keys())[0])
        combo_box.grid(row=1, columnspan=4, column=0)

        def c_box_changed(event):
            combo_box.bind('<<ComboboxSelected>>', c_box_changed)

        label_string = ttk.Label(text='Enter Bin String:', justify='center', font='bold')
        label_string.grid(row=2, columnspan=4, column=0, pady=0)
        label_string_box = ttk.Label(text='String:', justify='center')
        label_string_box.grid(row=3, column=0, padx=8)
        entry_string = ttk.Entry(self, textvariable=self.entry_string_var)
        entry_string.grid(row=3, column=1, columnspan=1, ipadx=85)
        label_string = ttk.Label(text='Use "-" to separate groups', justify='center')
        label_string.grid(row=4, columnspan=4, column=0, pady=0)
        label_string = ttk.Label(text='Use "..." to denote a range', justify='center')
        label_string.grid(row=5, columnspan=4, column=0, pady=0)
        label_string = ttk.Label(text='Ranges can be numbers OR letters', justify='center')
        label_string.grid(row=6, columnspan=4, column=0, pady=0)
        label_string = ttk.Label(text="Jono'23  v1.0", justify='center')
        label_string.grid(row=13, columnspan=2, column=4, pady=0)

        button1 = ttk.Button(text='Create Labels', command=self.open_window)
        button1.grid(row=11, columnspan=4, column=0, pady=4)
        button2 = ttk.Button(text='Create List of Bins', command=lambda: self.get_bin_list_from_field())
        button2.grid(row=10, columnspan=4,  column=0, pady=4)
        button3 = ttk.Button(text='Exit', command=self.destroy)
        button3.grid(row=12, columnspan=4,  column=0, pady=4)

        vertical_seperator = ttk.Separator(orient='vertical')
        vertical_seperator.grid(rowspan=12, row=1, column=4, sticky='nsew', padx=10)

    def open_window(self):
        Make_Labels.Labels(self.combo_box_var.get(), self.entry_string_var.get())
        # Draw_Labels.LabelWindow(self, self.combo_box_var.get(), self.entry_string_var.get())

    def get_bin_list_from_field(self):
        self.text_widget.delete('1.0', 'end')
        self.text_widget.insert('end', Anag.get_bin_list_text(self.entry_string_var.get()))



