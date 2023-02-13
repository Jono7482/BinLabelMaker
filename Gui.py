import tkinter as tk
from tkinter import ttk
import saved
from PIL import Image
import io
import Draw_Labels
import Anag


class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        canvas_height = 800
        canvas_width = 1200
        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, bg='white')
        self.canvas.pack()

        bin_index = 0
        qr1 = ''
        bin_list, total = Anag.get_bin_list('custom')
        for each in bin_list:
            if bin_index == 0:
                qr1 = each
                Draw_Labels.generate_qr(name=each)
                bin_index = 1
            else:
                qr2 = each
                Draw_Labels.generate_qr(name=each)
                bin_index = 0
                # Create Labels as .PNGs
                self.jtk_label(barcode1=qr1, barcode2=qr2)
        #  If binlist length is odd create a PNG with only 1 label
        if len(bin_list) % 2 == 1:
            # Create a Label as .PNG
            self.jtk_label(barcode1=qr1)

        self.close_window()

    def jtk_label(self, barcode1='BLANK', barcode2='BLANK'):
        Draw_Labels.add_labels_to_canvas(self.canvas, barcode1)
        if barcode2 != 'BLANK':
            Draw_Labels.add_labels_to_canvas(self.canvas, barcode2, label=2)
        self.save_labels(barcode1, barcode2)
        self.canvas.delete('all')

    def save_labels(self, barcode1, barcode2):
        self.canvas.update()

        # Create canvas .ps
        ps = self.canvas.postscript(colormode='color')

        # convert canvas.ps to .png readable
        img = Image.open(io.BytesIO(ps.encode('utf-8')))

        # save .png
        img.save(f'labels/{barcode1}_{barcode2}.png')

    def close_window(self):
        self.destroy()


def get_bin_list_text(list_name):
    bin_list, total = Anag.get_bin_list(list_name)
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

        defaults = saved.get_defualts()
        self.aisle_start_var = tk.StringVar()
        self.aisle_start_var.set(defaults['a_start'])
        self.aisle_end_var = tk.StringVar()
        self.aisle_end_var.set(defaults['a_end'])
        self.section_start_var = tk.StringVar()
        self.section_start_var.set(defaults['s_start'])
        self.section_end_var = tk.StringVar()
        self.section_end_var.set(defaults['s_end'])
        self.bin_start_var = tk.StringVar()
        self.bin_start_var.set(defaults['b_start'])
        self.bin_end_var = tk.StringVar()
        self.bin_end_var.set(defaults['b_end'])
        self.pos_start_var = tk.StringVar()
        self.pos_start_var.set(defaults['p_start'])
        self.pos_end_var = tk.StringVar()
        self.pos_end_var.set(defaults['p_end'])

        # place a button on the root window
        label_top = ttk.Label(text='Aisle [][] Section [] Bin [][] Position[]', justify='center')
        label_top.grid(row=0, columnspan=6, column=0, pady=10)

        self.text_widget = tk.Text(self, height=20, width=24)
        scroll_bar = tk.Scrollbar(self, orient='vertical', command=self.text_widget.yview)
        self.text_widget.config(yscrollcommand=scroll_bar.set)
        scroll_bar.grid(rowspan=12, row=1, column=6, sticky='ns')
        self.text_widget.grid(rowspan=12, row=1, column=5, sticky='nw')
        self.text_widget.insert(tk.END, get_bin_list_text('default'))

        self.combo_box_var = tk.StringVar()
        combo_box = ttk.Combobox(self, textvariable=self.combo_box_var)
        combo_box['values'] = ('<DEFAULT>', )
        combo_box.set('<DEFAULT>')
        combo_box.grid(row=1, columnspan=4, column=0)

        def c_box_changed(event):
            combo_box.bind('<<ComboboxSelected>>', c_box_changed)

        label_aisle = ttk.Label(text='Aisle', justify='center')
        label_aisle.grid(row=2, columnspan=4, column=0, pady=4)
        label_aisle_start = ttk.Label(text='Start:', justify='center')
        label_aisle_start.grid(row=3, column=0, padx=8)
        entry_aisle_start = ttk.Entry(self, textvariable=self.aisle_start_var)
        entry_aisle_start.grid(row=3, column=1)
        label_aisle_end = ttk.Label(text='End:', justify='center')
        label_aisle_end.grid(row=3, column=2)
        entry_aisle_end = ttk.Entry(self, textvariable=self.aisle_end_var)
        entry_aisle_end.grid(row=3, column=3)

        label_section = ttk.Label(text='Section', justify='center')
        label_section.grid(row=4, columnspan=4, column=0, pady=4)
        label_section_start = ttk.Label(text='Start:', justify='center')
        label_section_start.grid(row=5, column=0, padx=8)
        entry_section_start = ttk.Entry(self, textvariable=self.section_start_var)
        entry_section_start.grid(row=5, column=1)
        label_section_end = ttk.Label(text='End:', justify='center')
        label_section_end.grid(row=5, column=2, padx=8)
        entry_section_end = ttk.Entry(self, textvariable=self.section_end_var)
        entry_section_end.grid(row=5, column=3)

        label_bin = ttk.Label(text='Bin', justify='center')
        label_bin.grid(row=6, columnspan=4, column=0, pady=4)
        label_bin_start = ttk.Label(text='Start:', justify='center')
        label_bin_start.grid(row=7, column=0)
        entry_bin_start = ttk.Entry(self, textvariable=self.bin_start_var)
        entry_bin_start.grid(row=7, column=1)
        label_bin_end = ttk.Label(text='End:', justify='center')
        label_bin_end.grid(row=7, column=2)
        entry_bin_end = ttk.Entry(self, textvariable=self.bin_end_var)
        entry_bin_end.grid(row=7, column=3)

        label_position = ttk.Label(text='Position', justify='center')
        label_position.grid(row=8, columnspan=4, column=0, pady=4)
        label_position_start = ttk.Label(text='Start:', justify='center')
        label_position_start.grid(row=9, column=0)
        entry_position_start = ttk.Entry(self, textvariable=self.pos_start_var)
        entry_position_start.grid(row=9, column=1)
        label_position_end = ttk.Label(text='End:', justify='center')
        label_position_end.grid(row=9, column=2)
        entry_position_end = ttk.Entry(self, textvariable=self.pos_end_var)
        entry_position_end.grid(row=9, column=3)

        button1 = ttk.Button(text='Create Labels', command=self.open_window)
        button1.grid(row=11, columnspan=4, column=0, pady=4)
        button2 = ttk.Button(text='Create List of Bins', command=lambda: self.get_bin_list_from_fields())
        button2.grid(row=10, columnspan=4,  column=0, pady=4)
        button3 = ttk.Button(text='Exit', command=self.destroy)
        button3.grid(row=12, columnspan=4,  column=0, pady=4)

        vertical_seperator = ttk.Separator(orient='vertical')
        vertical_seperator.grid(rowspan=12, row=1, column=4, sticky='nsew', padx=10)

    def open_window(self):
        Window(self)

    def get_bin_list_from_fields(self):
        saved.a_start = self.aisle_start_var.get()
        saved.a_end = self.aisle_end_var.get()
        saved.s_start = self.section_start_var.get()
        saved.s_end = self.section_end_var.get()
        saved.b_start = self.bin_start_var.get()
        saved.b_end = self.bin_end_var.get()
        saved.p_start = self.pos_start_var.get()
        saved.p_end = self.pos_end_var.get()
        self.text_widget.delete('1.0', 'end')
        self.text_widget.insert('end', get_bin_list_text('custom'))



