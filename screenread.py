import ImageGrab, ImageEnhance, Image
from pytesser import image_to_string
import win32gui
import os

from main import Countdown

class Screenread:
    iteration = 0

    def ocr(self):
        self.iteration += 1

        bbox = win32gui.GetWindowRect(win32gui.FindWindow(None, "Nexus 5"))
        bbox = (bbox[0] + 45, bbox[1] + 325, bbox[2] - 70, bbox[3] - 200)

        grab = ImageGrab.grab(bbox)


        # test
        data = grab.getdata()

        new_data = []

        for item in data:
            if item != (255, 255, 255):
                new_data.append((0, 0, 0))
            else:
                new_data.append((255, 255, 255))

        grab.putdata(new_data)

        grab.save('test.png', quality=100)

        text = image_to_string(grab).strip().lower()

        os.remove('test.png')

        if len(text) == 9:
            Countdown(text)
        else:
            print 'Bad length, was {}. Detected {}'.format(len(text), text)
            if self.iteration < 5:
                self.ocr()

if __name__ == '__main__':
    reader = Screenread()
    reader.ocr()
