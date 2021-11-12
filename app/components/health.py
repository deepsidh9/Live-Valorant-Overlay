import glob
import os
import time

import cv2
import numpy as np


class GetHealth():
    def __init__(self):
        pass

    def detect_health(self, frame):
        max_health_value = 250
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
        mask_white = cv2.inRange(frame, np.array(
            [240, 240, 240]), np.array([255, 255, 255]))
        mask_red = cv2.inRange(frame, np.array(
            [0, 0, 0]), np.array([250, 100, 110]))

        health_bar = cv2.bitwise_and(frame, frame, mask=mask_white)
        health_bar_red = cv2.bitwise_and(frame, frame, mask=mask_red)

        health_bar_red = cv2.cvtColor(health_bar_red, cv2.COLOR_BGR2GRAY)
        health_bar = cv2.cvtColor(health_bar, cv2.COLOR_BGR2GRAY)

        hb_pixels = health_bar.reshape(-1, 1)
        lhb_pixels = health_bar_red.reshape(-1, 1)

        hp = 0
        pixels_found = False

        for pixel in hb_pixels:
            if pixel[0] >= 240:
                hp += 1
                pixels_found = True

        for pixel in lhb_pixels:
            if not pixels_found:
                if pixel[0] >= 70:
                    hp += 1
        # print("hp",hp)
        health_percent = (hp / max_health_value) * 100
        # print("percent",health_percent)
        if health_percent > 100:
            health_percent = 100
        # cv2.imshow("Image",frame)
        # cv2.waitKey()
        return round(health_percent)

    def process_frame(self, frame, side):
        agents_health_points = []
        if side == "left":
            x_start = 389
        else:
            x_start = 1192  # fix this
        x_end = x_start + 45
        for agent_place in range(0, 5):
            cropped_health_bar = frame[85:92, x_start:x_end]
            detected_health = self.detect_health(cropped_health_bar)
            agents_health_points.append(detected_health)
            x_start = x_start+73
            x_end = x_start + 46
        return agents_health_points

    def get_health(self, frame):
        agents_health_points = {"left": [], "right": []}
        agents_health_points["left"] = self.process_frame(frame, "left")
        # agents_health_points["right"] = self.process_frame(frame,"right")
        return agents_health_points


if __name__ == "__main__":
    get_health_handler = GetHealth()
    feed_images_directory = os.path.abspath(
        os.path.join(__file__, "../../test_images/Feed Images/"))
    for i in range(1, 57):
        image = cv2.imread('{}/feed{}.png'.format(feed_images_directory, i))
        print("=====================Image No. {}===========================".format(i))
        print("Result", get_health_handler.get_health(image))
