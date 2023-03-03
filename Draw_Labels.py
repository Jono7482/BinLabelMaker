from PIL import Image, ImageTk
import qrcode
import tkinter as tk
import io
import Anag
import Label_specs
import ctypes
import PilImage



class LabelWindow(tk.Toplevel):
    def __init__(self, parent, label_type, label_string):
        super().__init__(parent)
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
        self.qr_image_list = []
        self.logo_image_list = []
        self.label_string = label_string
        self.label_type = label_type
        self.form = Label_specs.label_formats[self.label_type]
        self.lpp = self.form['lpp']
        self.canvas_height = self.form['canvas_height'] * self.form['scale']
        self.canvas_width = self.form['canvas_width'] * self.form['scale']
        self.qr_size = self.form['qr_size']
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()
        self.binlist, self.total = Anag.create_bins_from_string(self.label_string)
        self.pil = None
        self.prepare_labels()

    def prepare_labels(self):
        each = None
        self.pil = PilImage.PI(label_type=self.label_type)    # pil image
        self.pil.create_canvas()
        for count, each in enumerate(self.binlist):
            self.generate_qr(each)
            self.create_label_canvas(each, label_num=count % self.lpp)

            if count % self.lpp == self.lpp - 1:
                self.save_labels(each, self.label_type)
                self.canvas.delete('all')
                self.pil.create_canvas()
        if len(self.binlist) % self.lpp != 0:
            self.save_labels(each, self.label_type)
            self.canvas.delete('all')
            self.pil.create_canvas()
        self.close_window()

    def create_label_canvas(self, label_id, label_num=0):
        qr_x = self.form['qr_x'] + self.form['x_shift'] * label_num
        qr_y = self.form['qr_y'] + self.form['y_shift'] * label_num
        text_x = self.form['text_x'] - len(label_id) * self.form['font_width'] + self.form['x_shift'] * label_num
        text_y = self.form['text_y'] + self.form['y_shift'] * label_num
        logo_x = self.form['logo_x'] + self.form['x_shift'] * label_num
        logo_y = self.form['logo_y'] + self.form['y_shift'] * label_num

        self.qr_image_list.insert(label_num, ImageTk.PhotoImage(Image.open(f'QRCodes/{label_id}.png')))
        self.pil.load_qr(f'QRCodes/{label_id}.png')     # pil image
        self.canvas.create_image(qr_x, qr_y, image=self.qr_image_list[label_num], anchor='w')
        self.pil.paste_images(qr_x, qr_y, label_num, l_type='qr')

        logo = Image.open(Label_specs.logo_path)
        logo = logo.resize((self.form['logo'], self.form['logo']))
        logo = ImageTk.PhotoImage(logo)
        self.logo_image_list.insert(label_num, logo)
        self.pil.load_logo()
        self.canvas.create_image(logo_x, logo_y, image=self.logo_image_list[label_num], anchor='w')
        self.pil.paste_images(logo_x, logo_y, label_num, l_type='logo')

        self.canvas.create_text(text_x, text_y, anchor='nw', text=label_id,
                                font=(Label_specs.font_type, self.form['font_size']), fill='black')

    def generate_qr(self, name):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=self.qr_size,
            border=1,
        )
        qr.add_data(name)
        img = qr.make_image(fill_color="black", back_color="white")
        filename = f'QRCodes/{name}.png'
        img.save(filename)

    def save_labels(self, barcode1, barcode2):
        self.canvas.update()


        # Create canvas .ps
        ps = self.canvas.postscript(colormode='color')

        # convert canvas.ps to .png readable
        img = Image.open(io.BytesIO(ps.encode('utf-8')))

        # save .png
        img.save(f'labels/{barcode1}_{barcode2}.png')
        self.pil.save_image(f'labels/{barcode1}_{barcode2}.png')

    def close_window(self):
        self.destroy()
