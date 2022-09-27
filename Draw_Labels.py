import io
import tkinter as tk
from PIL import Image, ImageTk
import Anag
import qrcode


global img1
global img2


def add_labels_to_canvas(canvas, barcode_png, label=1):
    global img1
    global img2
    data = barcode_png.split('-')
    aisle_text = f'Aisle: {data[0]}'
    section_text = f'Section: {data[1]}'
    bin_text = f'Bin: {data[2]}'
    position_text = f'Position: {data[3]}'

    # Label settings
    barcode_x = 100
    barcode2_shift = 590
    barcode_y = 250
    text_spacing_x = 120
    text_spacing_y = 70
    text_shift_down = 375
    font_size = 80
    label2_text_shift_right = 590
    font_type = 'Raleway'
    print(f'barcode png = {barcode_png}')
    if label == 2:
        text_spacing_x = text_spacing_x + label2_text_shift_right
        barcode_x = barcode_x + barcode2_shift
        img2 = ImageTk.PhotoImage(Image.open(f'QRCodes/{barcode_png}.png'))
        canvas.create_image(barcode_x, barcode_y, image=img2, anchor='w')
    else:
        img1 = ImageTk.PhotoImage(Image.open(f'QRCodes/{barcode_png}.png'))
        print(barcode_png)
        print(img1)
        canvas.create_image(barcode_x, barcode_y, image=img1, anchor='w')

    canvas.create_text(text_spacing_x, (text_spacing_y * 1 + text_shift_down), anchor='nw',
                       text=aisle_text, font=(font_type, font_size), fill='red')
    canvas.create_text(text_spacing_x, (text_spacing_y * 2 + text_shift_down), anchor='nw',
                       text=section_text, font=(font_type, font_size), fill='blue')
    canvas.create_text(text_spacing_x, (text_spacing_y * 3 + text_shift_down), anchor='nw',
                       text=bin_text, font=(font_type, font_size), fill='green')
    canvas.create_text(text_spacing_x, (text_spacing_y * 4 + text_shift_down), anchor='nw',
                       text=position_text, font=(font_type, font_size), fill='orange')


def jtk_label(barcode1='BLANK', barcode2='BLANK'):
    # global canvas
    root = tk.Tk()
    canvas_height = 800
    canvas_width = 1200
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
    canvas.grid(columnspan=2, rowspan=2, column=0, row=0, sticky='nw')
    canvas.pack()

    # Break down Barcode data

    add_labels_to_canvas(canvas, barcode1)
    if barcode2 != 'BLANK':
        add_labels_to_canvas(canvas, barcode2, label=2)

    # update changes to canvas

    canvas.update()

    # Create canvas .ps
    ps = canvas.postscript(colormode='color')

    # convert canvas.ps to .png readable
    img = Image.open(io.BytesIO(ps.encode('utf-8')))

    # destroy window
    root.destroy()

    # save .png
    img.save(f'labels/{barcode1}_{barcode2}.png')

    root.mainloop()


def make_a_set_of_labels():
    bin_index = 0
    qr1 = ''
    bin_list = Anag.get_bin_list()
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
            jtk_label(barcode1=qr1, barcode2=qr2)
    # If binlist length is odd create a PNG with only 1 label
    if len(bin_list) % 2 == 1:
        # Create a Label as .PNG
        jtk_label(barcode1=qr1)


# Create QR codes and save as PNGs
def generate_qr(name):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=18,
        border=1,
    )
    qr.add_data(name)
    img = qr.make_image(fill_color="black", back_color="white")
    filename = f'QRCodes/{name}.png'
    img.save(filename)


