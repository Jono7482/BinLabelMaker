# Pyinstaller command
# pyinstaller main.py -F -n JonoLabelMaker -w

import Gui
import File_Handler

if __name__ == "__main__":
    File_Handler.generate_labels_json()
    File_Handler.generate_settings_json()
    app = Gui.App()
    app.mainloop()

