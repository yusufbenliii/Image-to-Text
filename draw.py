from tkinter import *
from PIL import Image, ImageGrab
import pytesseract as tess
import clipboard
import pyautogui


class ScreenShootDisplay:
    def __init__(self):
        self.root = Tk()
        self.root.title("Ss")
        path = "cut.ico"
        try:
        	self.root.iconbitmap(r'cut.ico')
        except Exception as e:
        	print(e)
        self.root.attributes('-alpha', 0.2)
        self.root.attributes('-fullscreen', True)
        w , h = self.root.winfo_screenwidth(),self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}")
        self.canvas = Canvas(
            self.root, width=w, height=h, highlightbackground="black", bg= 'black'  )
        self.canvas.pack()

        self.is_packed = False

        self.is_released = True
        self.is_clicked = False

        self.root.bind("<Button-1>", self.click)
        self.root.bind("<ButtonRelease-1>", self.release)
        self.root.bind("<Motion>", self.motion)
        self.root.bind("<Key>", self.key_events)
        self.root.bind("<Escape>", self.exit)
        tess.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        self.root.mainloop()

    def exit(self, event):
        self.root.quit()

    def clear(self):
        self.canvas.delete("all")
        self.canvas.pack()
        self.root.attributes('-alpha', 0)

    def key_events(self, event):
        if event.char == "s":
            self.is_packed = True
        if event.char == "m":
            self.root.iconify()

    def motion(self, event):
        if self.is_clicked and not self.is_released and self.is_packed:
            self.draw_rect(self.start_x, self.start_y, event.x, event.y)

    def release(self, event):
        self.canvas.delete("all")
        if self.is_packed:
            #self.clear()
            self.root.iconify()
            self.screenshot(self.start_x, self.start_y, event.x, event.y)
            self.is_packed = False
        self.is_released = True
        self.is_clicked = False

    def click(self, event):
        self.is_released = False
        self.is_clicked = True
        self.start_x = event.x
        self.start_y = event.y

    def draw_rect(self, x1, y1, x2, y2):
        self.canvas.delete("all")
        self.canvas.create_rectangle((x1, y1, x2, y2),fill="ghostwhite") # gray99
        self.canvas.pack()

    def screenshot(self, x1, y1, x2, y2):

        try:
            box = self.create_box(x1, y1, x2, y2)
            img = ImageGrab.grab(bbox=box, all_screens=True)
            basewidth = 1920
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            img.save("images/image.PNG")
            text = tess.image_to_string(img)
            self.write_to_file(text)
        except Exception as e:
            print(e, "error occured while reading image")
            pass


    def create_box(self, x1, y1, x2, y2):
        x_lst = [x1, x2]
        y_lst = [y1, y2]
        x_lst.sort()
        y_lst.sort()
        box = (x_lst[0], y_lst[0], x_lst[1], y_lst[1])
        return box

    def write_to_file(self, text):
        text = text[:-2]

        text = text.translate({8221: '"'})
        text = text.translate({ord('“'): '"'})
        text = text.translate({ord('‘'): "'"})
        text = text.translate({ord('’'): "'"})
        clipboard.copy(text)
        with open("output.txt", "w") as f:
            f.write(text)
        f.close()


if __name__ == '__main__':
    app = ScreenShootDisplay()
