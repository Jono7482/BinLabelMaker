from PIL import Image
import Label_specs


class PI:
    def __init__(self, label_type='1 8X10'):
        self.label_type = label_type
        self.form = Label_specs.label_formats[self.label_type]
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
        print(f'path = {path}')
        self.qrs.append(Image.open(path))
        print(f'self.qrs = {self.qrs}')
        for index, each in enumerate(self.qrs):
            self.qrs[index] = self.resize_images(each, (self.form['qr_size']*33, self.form['qr_size']*33))

    def load_logo(self):
        self.logos.append(Image.open(Label_specs.logo_path))
        for index, each in enumerate(self.logos):
            self.logos[index] = self.resize_images(each, (self.form['logo'], self.form['logo']))

    def resize_images(self, image, new_size=(200, 200)):
        image = image.resize(new_size)
        return image

    def paste_images(self, x, y, num, l_type):
        if l_type == 'qr':
            print(f'num = {num}')
            self.image.paste(self.qrs[num], (int(x), int(y-275)))
        if l_type == 'logo':
            self.image.paste(self.logos[num], (x+140, y+200))

    def save_image(self, name):
        name = 'p' + name
        self.image.save(name)

    def create_text(self):
        pass

# if __name__ == "__main__":
    # pl = PI()
    # pl.create_canvas()
    # pl.load_images()
    # pl.paste_images()
    # pl.save_image()


