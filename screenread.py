import ImageGrab, ImageEnhance, Image
from pytesser import image_to_string
import win32gui
import os

from main import Countdown


class Screenread:
    iteration = 0

    def ocr(self):
        # We can use this to stop ourselves getting into an infinite loop.
        self.iteration += 1

        # Get the co-ordinates for the "Nexus 5" window and the crop to just
        # the letters of the app.
        bbox = win32gui.GetWindowRect(win32gui.FindWindow(None, "Nexus 5"))
        bbox = (bbox[0] + 45, bbox[1] + 325, bbox[2] - 70, bbox[3] - 200)

        grab = ImageGrab.grab(bbox)


        # Convert all non-white pixels to black, this greatly improves the
        # effectiveness of the OCR library.
        data = grab.getdata()

        new_data = []

        for item in data:
            if item != (255, 255, 255):
                new_data.append((0, 0, 0))
            else:
                new_data.append((255, 255, 255))

        grab.putdata(new_data)

        text = image_to_string(grab).strip().lower()

        # Only try and solve if we have 9 letters, otherwise try to OCR again.
        if len(text) == 9:
            Countdown(text)
        else:
            print 'Bad length, was {}. Detected {}'.format(len(text), text)
            if self.iteration < 5:
                self.ocr()

if __name__ == '__main__':
    reader = Screenread()
    reader.ocr()
