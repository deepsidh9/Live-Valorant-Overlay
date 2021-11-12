import os

import cv2


class ScoreBoardDetector():
    def __init__(self):
        template_directory = os.path.abspath(os.path.join(
            __file__, "../../templates/scoreboard_templates/scoreboard_template.png"))
        self.scoreboard_template = cv2.imread(template_directory, 0)

    def detect_scoreboard(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = frame[355:370, 610:656]
        result = cv2.matchTemplate(
            frame, self.scoreboard_template, cv2.TM_CCOEFF_NORMED)
        print("Scoreboard result", cv2.minMaxLoc(result))
        if cv2.minMaxLoc(result)[1] > .4:
            return True
        return False


if __name__ == '__main__':
    scoreboard_detector = ScoreBoardDetector()
    feed_images_directory = os.path.abspath(
        os.path.join(__file__, "../../test_images/Feed Images/"))
    for i in range(1, 58):
        image = cv2.imread('{}/feed{}.png'.format(feed_images_directory, i))
        print("===================Image No. {}===================".format(i))
        print(scoreboard_detector.detect_scoreboard(image))
