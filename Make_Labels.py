import qrcode
from PIL import Image, ImageDraw, ImageFont
import Anag
import Label_specs


def resize_images(image, new_size):
    image = image.resize(new_size)
    return image


def generate_qr(name, size):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=size,
        border=1,
    )
    qr.add_data(name)
    img = qr.make_image(fill_color="black", back_color="white")
    filename = f'QRCodes/{name}.png'
    img.save(filename)


class Labels:
    def __init__(self, label_type, label_string):
        self.label_string = label_string
        self.label_type = label_type
        self.form = Label_specs.LABELS[self.label_type]
        self.lpp = self.form['lpp'][0] * self.form['lpp'][1]
        self.qr_size = self.form['qr_size']
        self.binlist, self.total = Anag.create_bins_from_string(self.label_string)
        self.prepare_labels()
        self.logo_image = None

    def prepare_labels(self):
        each = None
        self.logo_image = LabelImage(label_type=self.label_type)
        self.logo_image.create_canvas()
        for count, each in enumerate(self.binlist):
            generate_qr(each, self.form['qr_size'])
            self.create_label_canvas(each, label_num=count % self.lpp)
            if count % self.lpp == self.lpp - 1:
                self.logo_image.save_image(each, self.label_type)
                self.logo_image.create_canvas()
        if len(self.binlist) % self.lpp != 0:
            self.logo_image.save_image(each, self.label_type)
            self.logo_image.create_canvas()

    def create_label_canvas(self, label_id, label_num=0):
        self.logo_image.load_qr(f'QRCodes/{label_id}.png')
        self.logo_image.paste_qr(label_num)
        self.logo_image.load_logo()
        self.logo_image.paste_logo(label_num)
        self.logo_image.create_text(label_id, label_num)


class LabelImage:
    def __init__(self, label_type='1 8X10'):
        self.label_type = label_type
        self.form = Label_specs.LABELS[self.label_type]
        self.qrs = []
        self.qr_size = self.form['qr_size']
        self.logos = []
        self.image = None
        self.page_size = (self.form['canvas'])

    def create_canvas(self):
        self.qrs = []
        self.logos = []
        self.image = Image.new('RGB', self.page_size, color='white')

    def load_qr(self, path):
        self.qrs.append(Image.open(path))
        for index, each in enumerate(self.qrs):
            self.qrs[index] = resize_images(each, (self.form['qr_size']*33, self.form['qr_size']*33))

    def load_logo(self):
        self.logos.append(Image.open(Label_specs.LOGO))
        for index, each in enumerate(self.logos):
            self.logos[index] = resize_images(each, (self.form['logo'], self.form['logo']))

    def position_adjust(self, x, y, num):
        if self.form['lpp'][0] > 1:
            x = int(num * (self.image.width / self.form['lpp'][0]) + x)
        if self.form['lpp'][1] > 1:
            y = int(num * (self.image.height / self.form['lpp'][1]) + y)
        return x, y

    def paste_qr(self, num):
        x, y = self.form['qr_x'], self.form['qr_y']
        self.image.paste(self.qrs[num], (self.position_adjust(x, y, num)))

    def paste_logo(self, num):
        x, y = self.form['logo_x'], self.form['logo_y']
        self.image.paste(self.logos[num], (self.position_adjust(x, y, num)))

    def save_image(self, barcode1, barcode2):
        self.image.save(f'labels/{barcode1}_{barcode2}.png')

    def create_text(self, label_id, num):
        x, y = self.form['text_x'], self.form['text_y']
        draw = ImageDraw.Draw(self.image)
        myfont = ImageFont.truetype(Label_specs.FONT, self.form['font_size'])
        draw.text((self.position_adjust(x, y, num)), label_id, fill="black", anchor="mm", font=myfont)
