#!/usr/bin/env python3

import logging
import tkinter as tk
import subprocess
from tkinter import filedialog
from tkinter import font

goldtree_file = "./Goldtree.py"
logo = "resources/switch.gif"
literal_search_nsp = "Search for a NSP file"
error_list = ['Device not found', 'Input magic mismatch']

class GraphicInterface:

    def __init__(self):
        # Main window
        self.window = tk.Tk()
        self.window.title("GoldtreePy Gui")
        self.window.geometry('420x500')

        #Load image
        render = tk.PhotoImage(file=logo)
        self.img = tk.Label(self.window, image=render)
        self.img.image = render

        # Create labels
        self.file_label = tk.Label(self.window, text = "Choose a NSP file (be sure Goldleaf is open)", anchor=tk.W, justify=tk.CENTER, fg="grey", font=("Helvetica", 16, "italic"))
        self.title = tk.Label(self.window, text="GoldtreePy GUI", fg="salmon", font=("Helvetica", 24, "bold"))
        self.subtitle = tk.Label(self.window, text="by insalada", fg="light salmon", font=("Helvetica", 10, "italic"))
        self.info_message = tk.Label(self.window, text=literal_search_nsp, bg="light salmon")
        
        # Create buttons
        self.choose_button = tk.Button(self.window, text = "Search", command = self.open_dialog)
        self.install_button = tk.Button(self.window, text = "Install", command = self.install, state = tk.DISABLED)
        self.nsp_path = ""

    def packObjects(self):
        self.title.pack(padx=20, pady=20, fill=tk.X)
        self.img.pack()
        self.subtitle.pack(pady=10, fill=tk.X)
        self.file_label.pack(padx=5, pady=5)
        self.choose_button.pack()
        self.install_button.pack()
        self.info_message.pack(padx=10, pady=10, fill=tk.X, side=tk.BOTTOM)

    def printMessage(self, message):
        self.info_message['text'] = message
        self.info_message.update()
        logging.info(message)

    def open_dialog(self):
        self.nsp_path = filedialog.askopenfilename(title = "Select file",filetypes = (("nsp files","*.nsp"),("all files","*.*")))
        self.file_label['text'] = self.nsp_path[0:40] + '...'
        if(self.nsp_path != ""):
            self.install_button['state'] = tk.NORMAL
            self.printMessage("Click on Install")
        else:
            self.install_button['state'] = tk.DISABLED
            
    def handleError(self, output):
        for error in error_list:
            if(error in output):
                self.printMessage("ERROR: {}".format(error))
                self.install_button['state'] = tk.NORMAL
                return True
        
        return False

    def install(self):
        self.install_button['state'] = tk.DISABLED
        self.printMessage("Open Explore content -> Remote PC (via USB) in Goldleaf")
       
        p = subprocess.Popen([goldtree_file, self.nsp_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output, errors = p.communicate()
        logging.info(output)
        logging.error(errors)
        failed = self.handleError(errors)
        if not failed:
            self.printMessage("SUCCESS: Installation complete")
            self.file_label['text'] = 'Choose a NSP file (be sure Goldleaf is open)'
            self.nsp_path = ""
            self.install_button['state'] = tk.NORMAL   
        
def main():
    gui = GraphicInterface()
    gui.packObjects()
    gui.window.mainloop()

if __name__ == "__main__":
    main()