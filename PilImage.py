from PIL import Image, ImageDraw, ImageFont
import Label_specs


def resize_images(image, new_size):
    image = image.resize(new_size)
    return image


class PI:
    def __init__(self, label_type='1 8X10'):
        self.label_type = label_type
        self.form = Label_specs.label_formats_pil[self.label_type]
        self.qrs = []
        self.qr_size = self.form['qr_size']
        self.logos = []
        self.image = None
        self.page_size = (self.form['canvas_width'], self.form['canvas_height'])

    def create_canvas(self):
        self.qrs = []
        self.logos = []
        self.image = Image.new('RGB', self.page_size, color='white')

    def load_qr(self, path):
        self.qrs.append(Image.open(path))
        for index, each in enumerate(self.qrs):
            self.qrs[index] = resize_images(each, (self.form['qr_size']*33, self.form['qr_size']*33))

    def load_logo(self):
        self.logos.append(Image.open(Label_specs.logo_path))
        for index, each in enumerate(self.logos):
            self.logos[index] = resize_images(each, (self.form['logo'], self.form['logo']))

    def position_adjust(self, x, y, num):
        x = x
        y = y
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
        myFont = ImageFont.truetype('arial.ttf', self.form['font_size'])
        draw.text((self.position_adjust(x, y, num)), label_id, fill="black", anchor="mm", font=myFont)

