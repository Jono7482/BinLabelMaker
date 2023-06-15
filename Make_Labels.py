from PIL import Image, ImageDraw, ImageFont
import qrcode
import File_Handler


def strip_arrows(name):
    _bin = name
    if _bin[-1] == '▼' or _bin[-1] == '▲':
        _bin = _bin.strip('▼')
        _bin = _bin.strip('▲')
        _bin = _bin.rstrip('▼')
        _bin = _bin.rstrip('▲')
    return _bin


# Generate_Qr
# Takes in a string creates a QR code
# Then saves the QR code to QRCodes folder as .png file
def generate_qr(name, prefix_b=False, prefix_l=False):
    _name = strip_arrows(name)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Error correction H for 30% error correction
        box_size=10,
        border=1,
    )
    # Add Prefix For BINS
    settings = File_Handler.get_settings()
    _bin = _name
    if prefix_b:
        _bin = settings['PREFIX_B'] + _bin
    if prefix_l:
        _bin = settings['PREFIX_L'] + _bin
    qr.add_data(_bin)
    img = qr.make_image(fill_color="black", back_color="white")
    filename = f'QRCodes/{_name}.png'
    img.save(filename)
    return _bin


# Labels
# Takes in a Label type, label list, and Label string
# then breaks down the bin list to requests for labels and pages of labels from Label Image
# sample string (MC-1...2-A...B)
class Labels:
    def __init__(self, label_type, binlist, prefix_b, prefix_l):
        self.label_type = label_type
        self.variables = File_Handler.get_labels()[self.label_type]
        self.binlist = binlist
        self.logo_image = None
        self.prefix_b = prefix_b
        self.prefix_l = prefix_l
        self.qr_data = None
        self.prepare_labels()

    def prepare_labels(self):
        lpp = self.variables['lpp'][0] * self.variables['lpp'][1]
        label_id = None
        self.logo_image = LabelImage(label_type=self.label_type)
        self.logo_image.create_canvas()
        for count, label_id in enumerate(self.binlist):
            self.qr_data = generate_qr(label_id, self.prefix_b, self.prefix_l)
            self.create_label_canvas(label_id, label_num=count % lpp)
            if count % lpp == lpp - 1:
                self.logo_image.save_image(label_id, self.label_type)
                self.logo_image.create_canvas()
        if len(self.binlist) % lpp != 0:
            self.logo_image.save_image(label_id, self.label_type)
            self.logo_image.create_canvas()

    def create_label_canvas(self, label_id, label_num=0):
        stripped_label_id = strip_arrows(label_id)
        self.logo_image.load(f'QRCodes/{stripped_label_id}.png')
        self.logo_image.paste(label_id, label_num, self.qr_data)


# LabelImage
# This is where the actual labels are drawn onto an image and saved
# opens logos and qr codes resizes them and positions and pastes them to the page
# then saves the finished page to Labels folder as .png
# label component positions are pulled from data/settings.json file and
# fitted to the page depending on label type and specifications from settings file
class LabelImage:
    def __init__(self, label_type):
        self.settings = File_Handler.get_settings()
        self.variables = File_Handler.get_labels()[label_type]
        logo = Image.open(File_Handler.get_settings()['LOGO'])
        new_size = self.variables['logo'], self.variables['logo']
        self.logo = logo.resize(new_size)
        self.qrs = []
        self.logos = []
        self.image = None

    # Create_Canvas
    # Creates a blank page and resets the qr and logo storage variables back to empty
    def create_canvas(self):
        self.qrs = []
        self.logos = []
        self.image = Image.new('RGB', (self.variables['canvas']), color='white')

    # Load
    # opens the required images and loads them into the qr and logo variables
    def load(self, path):
        _path = strip_arrows(path)
        qr = Image.open(_path)
        new_size = self.variables['qr_size'], self.variables['qr_size']
        qr = qr.resize(new_size)
        self.qrs.append(qr)
        self.logos.append(self.logo)

    # Label_Position
    # offsets the position of additional labels on the page depending on the label
    # number and the layout for that label type in LPP(labels per page) in (x, Y) format
    # num % lpp_x for the x multiplier
    # num floor lpp_x for the y multiplier
    def label_position(self, x, y, num):
        page_offset_x = self.variables["page_offset"][0]
        page_offset_y = self.variables["page_offset"][1]
        canvas_usable_x = self.variables['canvas_usable'][0]
        canvas_usable_y = self.variables['canvas_usable'][1]
        lpp_x = self.variables["lpp"][0]
        lpp_y = self.variables["lpp"][1]
        mod_x = num % lpp_x
        floor_y = num // lpp_x
        x = int(mod_x * (canvas_usable_x / lpp_x) + x)
        y = int(floor_y * (canvas_usable_y / lpp_y) + y)
        x = x + page_offset_x
        y = y + page_offset_y
        return x, y

    # Paste
    # places the images and text onto the page
    def paste(self, label_id, num, qr_data):
        font_size = self.variables['font_size']
        logo_x, logo_y = self.variables['logo_x'], self.variables['logo_y']
        qr_x, qr_y = self.variables['qr_x'], self.variables['qr_y']
        text_x, text_y = self.variables['text_x'], self.variables['text_y']
        draw = ImageDraw.Draw(self.image)

        #  If Label ID ends with an arrow replace Logo with arrow
        if label_id[-1] == '▲':
            font = ImageFont.truetype(self.settings['FONT'], (font_size * 4))
            draw.text((self.label_position(logo_x, logo_y, num)), '▲', fill="black", anchor="lt", font=font)
        elif label_id[-1] == '▼':
            font = ImageFont.truetype(self.settings['FONT'], (font_size * 4))
            draw.text((self.label_position(logo_x, logo_y, num)), '▼', fill="black", anchor="lt", font=font)
        else:
            self.image.paste(self.logos[num], (self.label_position(logo_x, logo_y, num)))

        #  Add QR Code
        self.image.paste(self.qrs[num], (self.label_position(qr_x, qr_y, num)))

        #  Add Label Text
        font = ImageFont.truetype(self.settings['FONT'], font_size)
        draw.text((self.label_position(text_x, text_y, num)), label_id, fill="black", anchor="mm", font=font)

        #  Add QR Data above QR Code
        if self.settings['SHOW_QR_DATA']:
            font = ImageFont.truetype(self.settings['FONT'], int((font_size / self.settings['QR_DATA_SCALE'])))
            draw.text((self.label_position(qr_x, qr_y, num)), qr_data, fill="black", anchor="lb", font=font)

    def save_image(self, label1, label_type):
        label1 = strip_arrows(label1)
        label_type = strip_arrows(label_type)
        self.image.save(f'labels/{label1} {label_type}.png')
