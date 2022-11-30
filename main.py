from tkinter import *
import cv2 as cv
import numpy
import matplotlib.pyplot as plt
from PIL import ImageTk, Image

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


def resize_img(img, scale_percent=60):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)
    return resized


class CartoonifyApp:
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def get_checkboxes(self):
        print("blur: %d,\n contour: %d" % (self.var1.get(), self.var2.get()))
        return self.var1.get(), self.var2.get()

    def show_image(self):
        blur, contours = self.get_checkboxes()
        originalmage = cv.imread("lena.png", cv.IMREAD_COLOR)
        img = cv.cvtColor(originalmage, cv.COLOR_BGR2GRAY)
        if blur:
            img = cv.medianBlur(img, 5)

        colorImage = cv.bilateralFilter(originalmage, 9, 300, 300)
        if contours:
            getEdge = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 9, 9)
            cartoonImage = cv.bitwise_and(colorImage, colorImage, mask=getEdge)
        else:
            cartoonImage = cv.bitwise_and(colorImage, colorImage)
        resized = cv.resize(cartoonImage, (960, 540))

        cv.imwrite("lena2.png",resized)


        image1 = Image.open("lena2.png")
        test = ImageTk.PhotoImage(image1)

        label1 = Label(self.main_label,image=test)
        label1.image = test

        label1.place(x= 100, y = 30)


    def run(self):
        self.window.mainloop()


    def _setup_main_window(self):
        self.window.title("Cartoonify")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=1000, height=700, bg=BG_COLOR)

        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        #tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # main label
        self.main_label = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=5, pady=5)

        self.main_label.place(relheight=0.745, relwidth=1, rely=0.08)
        self.main_label.configure(cursor="arrow", state=DISABLED)
        self.var1 = IntVar()
        Checkbutton(self.main_label, text="blur", variable=self.var1).grid(row=0, sticky=W)
        self.var2 = IntVar()
        Checkbutton(self.main_label, text="contours", variable=self.var2).grid(row=1, sticky=W)
        Button(self.main_label, text='Show', command=self.show_image).grid(row=4, sticky=W, pady=4)

        mainloop()

        #bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)



if __name__ == "__main__":
    app=CartoonifyApp()
    app.run()
