from tkinter import *
from PIL import ImageTk, Image
from time import *

class Arrow():
    def __init__(self):
        self.root = Tk()
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+0" % (self.w, self.h))
        self.canvas = Canvas(self.root,width=self.w,height=self.h)
        self.canvas.pack()
        self.root.after(0, self.animation)
        self.root.mainloop()
    
    def animation(self):
        while True:
            sleep(1)
            self.img = ImageTk.PhotoImage(Image.open("imageToSave.png"))
            self.canvas.delete('all')
            self.canvas.create_image(int(self.w)/2,int(self.h)/2, image=self.img)
            self.canvas.update()
