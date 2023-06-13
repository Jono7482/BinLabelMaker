import tkinter as tk
from tkinter import ttk
import os
import subprocess
import File_Handler
import Anag
import Make_Labels


# App
# Main application
# All labels and buttons that make up the GUI are here
class App(tk.Tk):

    def __init__(self):
        # setting the window
        super().__init__()
        self.settings = File_Handler.get_settings()
        self.labels_settings = File_Handler.get_labels()
        size = (800, 510)
        self.tk.call('tk', 'scaling', 2.0)
        self.geometry(f'{size[0]}x{size[1]}')
        self.maxsize(size[0], size[1])
        self.iconbitmap('data/jonoico.ico')
        self.title('Jono Label Maker')
        self.grid()

        # Entry string variable holds the user input used to make bin lists
        self.entry_string_var = tk.StringVar()
        self.entry_string_var.set(self.settings['DEFAULT'])

        # Label for drop down box
        label_top = ttk.Label(text='Label Size:', justify='center', font='bold')
        label_top.grid(row=0, columnspan=4, column=0, pady=5)

        # text window with scroll bar by default takes in entry from entry string
        # and generates a bin list
        self.text_widget = tk.Text(self, height=20, width=20)
        scroll_bar = tk.Scrollbar(self, orient='vertical', command=self.text_widget.yview)
        self.text_widget.config(yscrollcommand=scroll_bar.set)
        scroll_bar.grid(rowspan=12, row=1, column=6, sticky='ns')
        self.text_widget.grid(rowspan=12, row=1, column=5, sticky='nw')
        self.text_widget.insert(tk.END, Anag.get_bin_list_text(self.entry_string_var.get(), 0, 0, 0))

        # Combo box to hold the different label types
        # selection is used when creating labels
        # values are populated from the Label_Specs file
        self.combo_box_var = tk.StringVar()
        combo_box = ttk.Combobox(self, textvariable=self.combo_box_var)
        combo_box['values'] = list(self.labels_settings.keys())
        combo_box.set(list(self.labels_settings.keys())[0])
        combo_box.grid(row=1, columnspan=4, column=0)

        # Event detects a change in the combo box selection
        def c_box_changed():
            combo_box.bind('<<ComboboxSelected>>', c_box_changed)

        # labels and entry window for bin string
        label_string = ttk.Label(text='Enter Bin String:', justify='center', font='bold')
        label_string.grid(row=2, columnspan=4, column=0, pady=0)
        label_string_box = ttk.Label(text='String:', justify='center')
        label_string_box.grid(row=3, column=0, padx=8)
        entry_string = ttk.Entry(self, textvariable=self.entry_string_var)
        entry_string.grid(row=3, column=1, columnspan=1, ipadx=85)
        label_string = ttk.Label(text='Use "-" to separate groups', justify='center')
        label_string.grid(row=4, columnspan=4, column=0, pady=0)
        label_string = ttk.Label(text='Use "..." to denote a range', justify='center')
        label_string.grid(row=5, columnspan=4, column=0, pady=0)
        label_string = ttk.Label(text='Ranges can be numbers OR letters', justify='center')
        label_string.grid(row=6, columnspan=4, column=0, pady=0)
        label_string = ttk.Label(text="Jono 2023  v2.0", justify='center', font=('Arial', 6))
        label_string.grid(row=13, columnspan=2, column=4, pady=0)

        # buttons
        button1 = ttk.Button(text='Create Labels', command=self.generate_labels)
        button1.grid(row=9, columnspan=4, column=0, pady=4)
        button2 = ttk.Button(text='Create Bin List', command=lambda: self.fill_text_widget())
        button2.grid(row=10, columnspan=4,  column=0, pady=4)
        button3 = ttk.Button(text='Exit', command=self.exit)
        button3.grid(row=12, columnspan=4,  column=0, pady=4)
        button4 = ttk.Button(text='Delete Labels', command=self.delete_labels)
        button4.grid(row=11, columnspan=4,  column=0, pady=4)

        # Checkboxes
        self.dash_variable = tk.IntVar()
        self.arrow_variable = tk.IntVar()
        self.arrow_variable_up = tk.IntVar()
        self.bin_variable = tk.IntVar()
        self.location_variable = tk.IntVar()
        dash_checkbox = tk.Checkbutton(text='Omit Dashes', variable=self.dash_variable, onvalue=1, offvalue=0, )
        dash_checkbox.grid(row=9, column=0)
        arrow_checkbox = tk.Checkbutton(text='Arrows Mix ', variable=self.arrow_variable, onvalue=1, offvalue=0, )
        arrow_checkbox.grid(row=10, column=0)
        arrow_checkbox = tk.Checkbutton(text='Arrows Up  ', variable=self.arrow_variable_up, onvalue=1, offvalue=0, )
        arrow_checkbox.grid(row=11, column=0)
        bin_checkbox = tk.Checkbutton(text='Bin Prefix  ', variable=self.bin_variable, onvalue=1, offvalue=0, )
        self.bin_variable.set(1)
        bin_checkbox.grid(row=12, column=0)
        location_checkbox = tk.Checkbutton(text='Loc Prefix  ',
                                           variable=self.location_variable, onvalue=1, offvalue=0, )
        location_checkbox.grid(row=13, column=0)

        # vertical seperator for visual effect
        vertical_seperator = ttk.Separator(orient='vertical')
        vertical_seperator.grid(rowspan=12, row=1, column=4, sticky='nsew', padx=10)

        # logo = ImageTk.PhotoImage(Image.open("data/jonologo.png"))
        #
        # label_logo = ttk.Label(image=logo)
        # label_logo.grid(row=13, columnspan=2, column=4, pady=0)
    # Generate_Labels
    # Creates Label and Qr folders if needed
    # then sends combobox drop down selection and entry string information to the Make labels file to create Labels
    # then opens the labels file to view created labels
    def generate_labels(self):
        if not os.path.exists('Labels'):
            os.makedirs('Labels')
        if not os.path.exists('QRCodes'):
            os.makedirs('QRCodes')
        Make_Labels.Labels(label_type=self.combo_box_var.get(),
                           label_string=self.entry_string_var.get(),
                           dash=self.dash_variable.get(),
                           arrow=self.arrow_variable.get(),
                           arrow_up=self.arrow_variable_up.get(),
                           prefix_b=self.bin_variable.get(),
                           prefix_l=self.location_variable.get()
                           )
        subprocess.Popen('explorer "labels"')

    # Fill_Text_Widget
    # Clears current text from text window
    # Then retrieves a new list of bins with the string variable from Anag file and populates the text window
    def fill_text_widget(self):
        self.text_widget.delete('1.0', 'end')
        self.text_widget.insert('end', Anag.get_bin_list_text(
            self.entry_string_var.get(),
            self.dash_variable.get(),
            self.arrow_variable.get(),
            self.arrow_variable_up.get()))

    # Exit
    # Deletes the content of the QRCodes folder and closes the program
    def exit(self):
        if os.path.exists('QRCodes'):
            for file in os.scandir('QRCodes'):
                os.remove(file.path)
        self.destroy()

    # Delete_Labels
    # Deletes the contents of the Labels folder
    def delete_labels(self):
        if os.path.exists('Labels'):
            for file in os.scandir('Labels'):
                os.remove(file.path)
