"""
install pillow, facebook_scraper, demoji, emoji
"""

import sys
if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
    import Tkinter.font as tkFont
else:
    from tkinter import *
    import tkinter.font as tkFont

from PIL import ImageTk, Image
import os

import facebook_scraping as fs

PAGE_NAME = "electroLAB.FPMs"
PHONE_NBR = "Tél. : NUMÉRO DE TÉLÉPHONE DE VINCENT" #emoji.emojize(":telephone_receiver:")

class Fullscreen_Window:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("electroLAB - Horaire")
        self.tk.wm_iconbitmap('electroLAB.ico')
        self.font = tkFont.Font(family="Helvetica", size=40)
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        # self.tk.wm_state('zoomed')  # This just maximizes it so we can see the window. It's nothing to do with fullscreen.

        # Get variable
        self.screen_width = self.tk.winfo_screenwidth()
        self.screen_height = self.tk.winfo_screenheight()
        self.post_text = ""
        self.post = StringVar()
        self.time = StringVar()
        self.previous_date = ""
        self.img = ImageTk.PhotoImage(Image.open('electroLAB-LOGO.png').resize((int(self.screen_height/10),int(self.screen_height/10)), Image.ANTIALIAS))
        
        # Frame and labels
        self.frame = Frame(self.tk)
        self.lbl_list = []
        self.lbl_list.append(Label(self.frame, image = self.img, background="#%02x%02x%02x" % (44,167,106), anchor=CENTER, height=int(self.screen_height/4.5), width=self.screen_width, relief=None, compound="center").grid(row=0, sticky="nsew"))
        self.lbl_list.append(Label(self.frame, textvariable=self.post, background='white', anchor='center', font=self.font, relief=None, compound="center", height=9).grid(row=1,sticky="nsew"))
        self.lbl_list.append(Label(self.frame, textvariable=self.time, background='white', anchor='center', font=self.font, relief=None, compound="center", height=3).grid(row=2,sticky="nsew"))
        self.lbl_list.append(Label(self.frame, image = self.img, background="#%02x%02x%02x" % (44,167,106), anchor=CENTER, height=int(self.screen_height/4.5), width=self.screen_width, relief=None, compound="center").grid(row=3, sticky="nsew"))
        
        #self.frame.grid_propagate(False)
        self.frame.grid_rowconfigure(0,weight=1)
        self.frame.grid_rowconfigure(1,weight=1)
        self.frame.grid_rowconfigure(2,weight=1)
        self.frame.grid_rowconfigure(3,weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.pack()

        # Init update
        self.updatePost()
        self.update()

        # Set as fullscreen
        self.state = True
        self.tk.attributes("-fullscreen", self.state)

    # Toggle fullscreen mode
    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    # Exit fullscreen mode
    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    # Update 
    def updatePost(self, page_name=PAGE_NAME, key=b'\xf0\x9f\x95\x93'.decode('utf8')):
        try:
            temp = fs.getPost(page_name=page_name, key=key)
            if temp != self.post_text:
                self.post_text = fs.getPost(page_name=page_name, key=key)
                self.post.set(self.post_text + "\n\n" + telephone)
        except:
            if "(Pas de connexion)\n" not in self.post_text:
                self.post_text = "(Pas de connexion)\n" + self.post_text
        self.tk.after(5000, self.updatePost)

    def update(self):
        from datetime import timezone, datetime
        from time import sleep

        # from time import strftime
        utc_datetime = datetime.now() # datetime.utcnow()
        while(self.previous_date==utc_datetime):
            sleep(0.01)
            utc_datetime = datetime.now()

        self.previous_date = utc_datetime
        self.time.set(self.previous_date.strftime("%d/%m/%Y %H:%M:%S"))

        self.tk.update()
        self.tk.after(10, self.update)

def main():
    import time
    w = Fullscreen_Window()
    w.tk.mainloop()

def test():
    schedule = fs.remove_emoji(fs.getPost(page_name='electroLAB.FPMs', key=b'\xf0\x9f\x95\x93'.decode('utf8')))

    if schedule:
        print(fs.remove_emoji(schedule))
    else:
        print("Pas d'horaire de disponible.")

if __name__ == "__main__":
    main()
