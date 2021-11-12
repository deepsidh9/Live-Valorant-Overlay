import time

import cv2
import numpy as np
import pytesseract
from easyocr import Reader


class GetCreds():
    def __init__(self):
        # self.reader = Reader(["en"])
        pass

    def cleanup_text(self, text):
        # strip out non-ASCII text
        return "".join([c if ord(c) < 128 else "" for c in text]).strip()

    def clean_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, None, fx=8, fy=8,
                           interpolation=cv2.INTER_CUBIC)
        frame = cv2.bilateralFilter(frame, 9, 75, 75)
        frame = cv2.threshold(
            frame, 240, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        kernel = np.ones((4, 4), np.uint8)
        frame = cv2.dilate(frame, kernel, iterations=1)
        frame = cv2.erode(frame, kernel, iterations=1)
        frame = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)
        # cv2.imshow("frame", frame)
        # cv2.waitKey()
        return frame

    def process_frame(self, frame, side):
        all_points = []
        if side == "top":
            y_start = 383
            y_end = 410
        else:
            y_start = 1192
            y_end = y_start + 40
        for agent_row in range(0, 5):
            cropped_cred_image = frame[y_start:y_end, 1239:1321]
            # cv2.imshow("Image", cropped_cred_image)
            # cv2.waitKey()
            pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
            points = pytesseract.image_to_string(
                cropped_cred_image, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
            print("points: ", points)
            # points = self.reader.readtext(self.clean_frame(cropped_cred_image),allowlist ='0123456789')
            # print(points)
            all_points.append(points)
            y_start = y_start + 73
            y_end = y_start + 40
        return all_points

    def get_creds(self, frame):
        all_ultimates = {"top": [], "bottom": []}
        all_ultimates["top"] = self.process_frame(frame, "top")
        print(all_ultimates)
        # all_ultimates["bottom"] = self.process_frame(frame,"bottom")


if __name__ == "__main__":
    gc = GetCreds()
    for i in range(2, 10):
        image = cv2.imread("Tab Images/{}.png".format(i))
        gc.get_creds(image)
        # cv2.imshow("Image",image[383:410,1239:1321])
        # cv2.waitKey()
