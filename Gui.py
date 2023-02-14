import tkinter as tk
from tkinter import ttk
import saved
import Draw_Labels
import Anag


def get_bin_list_text(list_name):
    bin_list, total = Anag.create_bins_from_string(list_name)
    lst = ''
    for each in bin_list:
        lst += f'{each}\n'
    lst += f'Total= {total}\n'
    return lst


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry('600x380')
        self.maxsize(590, 380)
        self.title('Jono Label Maker')
        self.grid()

        self.entry_string_var = tk.StringVar()
        self.entry_string_var.set(saved.get_default_string())

        # place a button on the root window
        label_top = ttk.Label(text='LABEL TYPE:', justify='center')
        label_top.grid(row=0, columnspan=4, column=0, pady=5)

        self.text_widget = tk.Text(self, height=20, width=24)
        scroll_bar = tk.Scrollbar(self, orient='vertical', command=self.text_widget.yview)
        self.text_widget.config(yscrollcommand=scroll_bar.set)
        scroll_bar.grid(rowspan=12, row=1, column=6, sticky='ns')
        self.text_widget.grid(rowspan=12, row=1, column=5, sticky='nw')
        self.text_widget.insert(tk.END, get_bin_list_text(self.entry_string_var.get()))

        self.combo_box_var = tk.StringVar()
        combo_box = ttk.Combobox(self, textvariable=self.combo_box_var)
        combo_box['values'] = ('4 X 6', '8 X 10', )
        combo_box.set('4 X 6')
        combo_box.grid(row=1, columnspan=4, column=0)

        def c_box_changed(event):
            combo_box.bind('<<ComboboxSelected>>', c_box_changed)

        label_string = ttk.Label(text='Enter Bin String:', justify='center')
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
        if self.combo_box_var.get() == '4 X 6':
            lbl_type = 'default'
        elif self.combo_box_var.get() == '8 X 10':
            lbl_type = '8by10'
        else:
            print('Label Type not Implemented')
            lbl_type = 'default'
        # Draw_Labels.LabelWindow(self)
        Draw_Labels.LabelWindow(self, lbl_type, self.entry_string_var.get())

    def get_bin_list_from_field(self):
        self.text_widget.delete('1.0', 'end')
        self.text_widget.insert('end', get_bin_list_text(self.entry_string_var.get()))



