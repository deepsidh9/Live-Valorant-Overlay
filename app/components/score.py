import cv2
import numpy as np
from easyocr import Reader


class GetScore():
    def __init__(self):
        self.reader = Reader(["en"])

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
        return frame

    def get_score(self, screen_frame):
        left_score = self.reader.readtext(self.clean_frame(
            screen_frame[43:68, 790:830]), allowlist='0123456789')
        right_score = self.reader.readtext(self.clean_frame(
            screen_frame[43:68, 1095:1140]), allowlist='0123456789')
        if left_score == [] or right_score == []:
            return None
        else:
            return [left_score[0][1], right_score[0][1]]

# if __name__ == '__main__':
#     score_helper = GetScore()
#     image = cv2.imread("Tab Images/3.png")
#     print(score_helper.get_score(image))
