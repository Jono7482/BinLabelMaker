from PIL import Image, ImageTk
import qrcode
import tkinter as tk
import io
import Anag

global qr_image
global barcode_image1
global barcode_image2
global logo_image1
global logo_image2


def default_label_canvas(canvas, barcode_png, label=1):
    global barcode_image1
    global barcode_image2
    global logo_image1
    global logo_image2

    # Label settings
    barcode_x = 100
    barcode2_shift = 590
    barcode_y = 200
    text_spacing_x = 120
    text_spacing_y = 70
    text_shift_down = 375
    font_size = 60
    label2_text_shift_right = 590
    logo_x = 190
    logo_y = 650
    font_type = 'Raleway'

    if label == 2:
        text_spacing_x = text_spacing_x + label2_text_shift_right
        barcode_x = barcode_x + barcode2_shift
        barcode_image2 = ImageTk.PhotoImage(Image.open(f'QRCodes/{barcode_png}.png'))
        canvas.create_image(barcode_x, barcode_y, image=barcode_image2, anchor='w')
        logo_image2 = ImageTk.PhotoImage(Image.open(f'QRCodes/LagunaLogo3.png'))
        canvas.create_image(logo_x + barcode2_shift, logo_y, image=logo_image2, anchor='w')
    else:
        barcode_image1 = ImageTk.PhotoImage(Image.open(f'QRCodes/{barcode_png}.png'))
        canvas.create_image(barcode_x, barcode_y, image=barcode_image1, anchor='w')
        logo_image1 = ImageTk.PhotoImage(Image.open(f'QRCodes/LagunaLogo3.png'))
        canvas.create_image(logo_x, logo_y, image=logo_image1, anchor='w')
    canvas.create_text(text_spacing_x, (text_spacing_y * 1 + text_shift_down), anchor='nw',
                       text=barcode_png, font=(font_type, font_size), fill='teal')


def full_page_label_canvas(canvas, label_id):
    global qr_image
    global logo_image1
    # Label settings
    barcode_x = 0
    barcode_y = 420
    logo_x = 310
    logo_y = 1090
    text_spacing_x = 100
    text_spacing_y = 820
    font_size = 120
    font_type = 'Raleway'

    qr_image = ImageTk.PhotoImage(Image.open(f'QRCodes/{label_id}.png'))
    canvas.create_image(barcode_x, barcode_y, image=qr_image, anchor='w')
    logo_image1 = ImageTk.PhotoImage(Image.open(f'QRCodes/LagunaLogo3.png'))
    canvas.create_image(logo_x, logo_y, image=logo_image1, anchor='w')
    canvas.create_text(text_spacing_x, text_spacing_y, anchor='nw',
                       text=label_id, font=(font_type, font_size), fill='black')


# Create QR codes and save as PNGs
def generate_qr(name, size=18):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=1,
    )
    qr.add_data(name)
    img = qr.make_image(fill_color="black", back_color="white")
    filename = f'QRCodes/{name}.png'
    img.save(filename)


class LabelWindow(tk.Toplevel):
    def __init__(self, parent, label_type='default', label_string='default'):
        super().__init__(parent)
        self.label_string = label_string
        self.label_type = label_type

        if self.label_type == 'default':
            canvas_height = 800
            canvas_width = 1200
            self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, bg='white')
            self.canvas.pack()
            bin_index = 0
            qr1 = ''
            bin_list, total = Anag.create_bins_from_string(label_string)
            for each in bin_list:
                if bin_index == 0:
                    qr1 = each
                    generate_qr(name=each)
                    bin_index = 1
                else:
                    qr2 = each
                    generate_qr(name=each)
                    bin_index = 0
                    # Create Labels as .PNGs
                    default_label_canvas(self.canvas, qr1)
                    default_label_canvas(self.canvas, qr2, label=2)
                    self.save_labels(qr1, qr2)
                    self.canvas.delete('all')
            #  If binlist length is odd create a PNG with only 1 label
            if len(bin_list) % 2 == 1:
                # Create a Label as .PNG
                default_label_canvas(self.canvas, qr1)
                self.save_labels(qr1, 'BLANK')
                self.canvas.delete('all')
            self.close_window()

        elif self.label_type == '8by10':
            canvas_height = 1200
            canvas_width = 800
            qr_size = 35
            self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, bg='white')
            self.canvas.pack()
            bin_list, total = Anag.create_bins_from_string(self.label_string)
            for each in bin_list:
                generate_qr(name=each, size=qr_size)
                full_page_label_canvas(self.canvas, each)
                self.save_labels(each, '8by10')
                self.canvas.delete('all')
            self.close_window()

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


