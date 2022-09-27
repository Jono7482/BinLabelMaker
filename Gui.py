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
        # self.canvas.grid(columnspan=1, rowspan=1, column=0, row=0, sticky='news')
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
        # self.mainloop()

    def jtk_label(self, barcode1='BLANK', barcode2='BLANK'):
        Draw_Labels.add_labels_to_canvas(self.canvas, barcode1)
        if barcode2 != 'BLANK':
            Draw_Labels.add_labels_to_canvas(self.canvas, barcode2, label=2)
        self.save_labels(barcode1, barcode2)

        # destroy canvas
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
        self.grab_release()
        self.destroy()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('300x200')
        self.title('Main Window')
        # place a button on the root window
        ttk.Button(self,
                   text='Make Labels',
                   command=self.open_window).pack(expand=True)

    def open_window(self):
        window = Window(self)
        window.grab_set()


if __name__ == "__main__":
    app = App()
    app.mainloop()
