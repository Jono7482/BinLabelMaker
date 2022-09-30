import tkinter as tk
from tkinter import ttk
import Draw_Labels
import Anag
from PIL import Image
import io


class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        canvas_height = 800
        canvas_width = 1200
        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, bg='white')
        self.canvas.pack()

        bin_index = 0
        qr1 = ''
        bin_list = Anag.get_bin_list()
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


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('600x380')
        self.maxsize(590, 380)
        self.title('Jono Label Maker')
        self.grid()

        # place a button on the root window
        label_top = ttk.Label(text='Aisle [][] Section [] Bin [][] Position[]', justify='center')
        label_top.grid(row=0, columnspan=6, column=0, pady=10)

        text_widget = tk.Text(self, height=20, width=24)
        scroll_bar = tk.Scrollbar(self, orient='vertical', command=text_widget.yview)
        text_widget.config(yscrollcommand=scroll_bar.set)
        scroll_bar.grid(rowspan=12, row=1, column=6, sticky='ns')
        text_widget.grid(rowspan=12, row=1, column=5, sticky='nw')
        long_text = """This is a multiline string.
We can write this in multiple lines too!
Hello from AskPython. This is the third line.
This is the fourth line. Although the length of the text is longer than
the width, we can use tkinteis is the fourth line. Although the length of the text is longer than
the width, we can use tkinter's scrollbar to solve this problem!This is a multiline string.
We can write this in multiple lines too!
Hello from AskPython. This is the third line.
This is the fourtr's scrollbar to solve this problem!This is a multiline string.
We can write this in multiple lines too!
Hello from AskPython. This is the third line.
This is the fourth line. Although the length of the text is longer than
the width, we can use tkinter's scrollbar to solve this problem!
"""
        text_widget.insert(tk.END, long_text)

        combo_box = ttk.Combobox()
        combo_box.grid(row=1, columnspan=4, column=0)

        label_aisle = ttk.Label(text='Aisle', justify='center')
        label_aisle.grid(row=2, columnspan=4, column=0, pady=4)
        label_aisle_start = ttk.Label(text='Start:', justify='center')
        label_aisle_start.grid(row=3, column=0, padx=8)
        entry_aisle_start = ttk.Entry()
        entry_aisle_start.grid(row=3, column=1)
        label_aisle_end = ttk.Label(text='End:', justify='center')
        label_aisle_end.grid(row=3, column=2)
        entry_aisle_end = ttk.Entry()
        entry_aisle_end.grid(row=3, column=3)

        label_section = ttk.Label(text='Section', justify='center')
        label_section.grid(row=4, columnspan=4, column=0, pady=4)
        label_section_start = ttk.Label(text='Start:', justify='center')
        label_section_start.grid(row=5, column=0, padx=8)
        entry_section_start = ttk.Entry()
        entry_section_start.grid(row=5, column=1)
        label_section_end = ttk.Label(text='End:', justify='center')
        label_section_end.grid(row=5, column=2, padx=8)
        entry_section_end = ttk.Entry()
        entry_section_end.grid(row=5, column=3)

        label_bin = ttk.Label(text='Bin', justify='center')
        label_bin.grid(row=6, columnspan=4, column=0, pady=4)
        label_bin_start = ttk.Label(text='Start:', justify='center')
        label_bin_start.grid(row=7, column=0)
        entry_bin_start = ttk.Entry()
        entry_bin_start.grid(row=7, column=1)
        label_bin_end = ttk.Label(text='End:', justify='center')
        label_bin_end.grid(row=7, column=2)
        entry_bin_end = ttk.Entry()
        entry_bin_end.grid(row=7, column=3)

        label_position = ttk.Label(text='Position', justify='center')
        label_position.grid(row=8, columnspan=4, column=0, pady=4)
        label_position_start = ttk.Label(text='Start:', justify='center')
        label_position_start.grid(row=9, column=0)
        entry_position_start = ttk.Entry()
        entry_position_start.grid(row=9, column=1)
        label_position_end = ttk.Label(text='End:', justify='center')
        label_position_end.grid(row=9, column=2)
        entry_position_end = ttk.Entry()
        entry_position_end.grid(row=9, column=3)

        button1 = ttk.Button(text='Create Labels', command=self.open_window)
        button1.grid(row=11, columnspan=4, column=0, pady=4)
        button2 = ttk.Button(text='Create List of Bins')
        button2.grid(row=10, columnspan=4,  column=0, pady=4)
        button3 = ttk.Button(text='Exit')
        button3.grid(row=12, columnspan=4,  column=0, pady=4)

        vertical_seperator = ttk.Separator(orient='vertical')
        vertical_seperator.grid(rowspan=12, row=1, column=4, sticky='nsew', padx=10)

    def open_window(self):
        Window(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
