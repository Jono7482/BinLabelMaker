from PIL import Image, ImageDraw, ImageFont
import qrcode
import Anag
import Label_specs
#
#
# # Generate_Qr
# # Takes in a string creates a QR code
# # Then saves the QR code to QRCodes folder as .png file
# def generate_qr(name):
#     _bin = name
#     if _bin[-1] == '^':
#         _bin = _bin.rstrip('-^')
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_H,  # Error correction H for 30% error correction
#         box_size=10,
#         border=1,
#     )
#     # Add Prefix For BINS
#     _bin = '%B%' + _bin
#     qr.add_data(_bin)
#     img = qr.make_image(fill_color="black", back_color="white")
#     filename = f'QRCodes/{name}.png'
#     img.save(filename)
#
#
# # Labels
# # Takes in a Label type and Label string
# # using the label type and string requests a bin list from Anag
# # then breaks down the bin list to requests for labels and pages of labels from Label Image
# # sample string (MC-1...2-A...B)
# # Label_type must be a key from Label_specs file
# class Labels:
#     def __init__(self, label_type, label_string):
#         self.label_type = label_type
#         self.variables = Label_specs.LABELS[self.label_type]
#         self.binlist, self.total = Anag.create_bins_from_string(label_string)
#         self.logo_image = None
#         self.prepare_labels()
#
#     def prepare_labels(self):
#         lpp = self.variables['lpp'][0] * self.variables['lpp'][1]
#         label_id = None
#         self.logo_image = LabelImage(label_type=self.label_type)
#         self.logo_image.create_canvas()
#         for count, label_id in enumerate(self.binlist):
#             generate_qr(label_id)
#             self.create_label_canvas(label_id, label_num=count % lpp)
#             if count % lpp == lpp - 1:
#                 self.logo_image.save_image(label_id, self.label_type)
#                 self.logo_image.create_canvas()
#         if len(self.binlist) % lpp != 0:
#             self.logo_image.save_image(label_id, self.label_type)
#             self.logo_image.create_canvas()
#
#     def create_label_canvas(self, label_id, label_num=0):
#         self.logo_image.load(f'QRCodes/{label_id}.png')
#         self.logo_image.paste(label_id, label_num)
#
#
# # LabelImage
# # This is where the actual labels are drawn onto an image and saved
# # opens logos and qr codes resizes them and positions and pastes them to the page
# # then saves the finished page to Labels folder as .png
# # label component positions are pulled from Label_specs file and
# # fitted to the page depending on label type and specifications from Label_specs file
# class LabelImage:
#     def __init__(self, label_type):
#         self.variables = Label_specs.LABELS[label_type]
#         logo = Image.open(Label_specs.LOGO)
#         new_size = self.variables['logo'], self.variables['logo']
#         self.logo = logo.resize(new_size)
#         self.qrs = []
#         self.logos = []
#         self.image = None
#
#     # Create_Canvas
#     # Creates a blank page and resents the qr and logo storage variables back to empty
#     def create_canvas(self):
#         self.qrs = []
#         self.logos = []
#         self.image = Image.new('RGB', (self.variables['canvas']), color='white')
#
#     # Load
#     # opens the required images and loads them into the qr and logo variables
#     def load(self, path):
#         qr = Image.open(path)
#         new_size = self.variables['qr_size'], self.variables['qr_size']
#         qr = qr.resize(new_size)
#         self.qrs.append(qr)
#         self.logos.append(self.logo)
#
#     # Label_Position
#     # offsets the position of additional labels on the page depending on the label
#     # number and the layout for that label type in LPP(labels per page) in (x, Y) format
#     # num % lpp_x for the x multiplier
#     # num floor lpp_x for the y multiplier
#     def label_position(self, x, y, num):
#         lpp_x = self.variables["lpp"][0]
#         lpp_y = self.variables["lpp"][1]
#         mod_x = num % lpp_x
#         floor_y = num // lpp_x
#         x = int(mod_x * (self.image.width / lpp_x) + x)
#         y = int(floor_y * (self.image.height / lpp_y) + y)
#         return x, y
#
#     # Paste
#     # places the images and text onto the page
#     def paste(self, label_id, num):
#         logo_x, logo_y = self.variables['logo_x'], self.variables['logo_y']
#         qr_x, qr_y = self.variables['qr_x'], self.variables['qr_y']
#         text_x, text_y = self.variables['text_x'], self.variables['text_y']
#         draw = ImageDraw.Draw(self.image)
#
#         if label_id[-1] == '^':
#             label_id = label_id.rstrip('-^')
#             logo_x -= 100
#             font = ImageFont.truetype(Label_specs.FONT, 200)
#             if label_id[-1] == 'A':
#                 draw.text((self.label_position(635, 230, num)), '▼', fill="black", anchor="mm", font=font)
#             else:
#                 draw.text((self.label_position(635, 230, num)), '▲', fill="black", anchor="mm", font=font)
#
#         self.image.paste(self.qrs[num], (self.label_position(qr_x, qr_y, num)))
#         self.image.paste(self.logos[num], (self.label_position(logo_x, logo_y, num)))
#         font = ImageFont.truetype(Label_specs.FONT, self.variables['font_size'])
#         draw.text((self.label_position(text_x, text_y, num)), label_id, fill="black", anchor="mm", font=font)
#
#     def save_image(self, barcode1, barcode2):
#         self.image.save(f'labels/{barcode1}_{barcode2}.png')
#


