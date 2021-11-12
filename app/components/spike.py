import os
import time

import cv2

class GetSpike():
    def __init__(self):
        # self.spike_template = cv2.imread(r'''C:\Users\deepb\Desktop\Development\Overlay-Live Valorant Stats\All Inclusive OBS Overlay\cropped_spike.png''',cv2.IMREAD_UNCHANGED)
        # o,self.mask = cv2.threshold(self.spike_template[:, :, 3], 0, 255, cv2.THRESH_BINARY)
        # self.gray_template = cv2.cvtColor(self.spike_template, cv2.COLOR_BGR2GRAY)
        # self.spike_template = cv2.imread(r'''red_spike_template.png''')
        pass

    def get_spike_status(self, frame):
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)[40:66,894:915]
        frame = frame[88:91, 957:962]
        average_color = cv2.mean(frame)
        # print( "average_color",average_color)
        # cv2.imshow("frame1",frame)
        # cv2.waitKey()
        # print("frame shape",frame.shape)
        # print("self.spike_template shape",self.spike_template.shape)
        # print("self.mask shape",self.mask.shape)
        # result =  cv2.matchTemplate(frame,self.spike_template,cv2.TM_CCOEFF_NORMED)
        # print("result",result)
        # print("result",cv2.minMaxLoc(result)[1])
        # if cv2.minMaxLoc(result)[1]>.9:
        #     return True
        if average_color[2] == 230.0 or average_color[2] == 169.0:
            return True
        return False


if __name__ == "__main__":
    spike_handler = GetSpike()
    feed_images_directory = os.path.abspath(
        os.path.join(__file__, "../../test_images/Feed Images/"))
    for i in range(1, 58):
        start = time.time()
        image = cv2.imread('{}/feed{}.png'.format(feed_images_directory, i))
        # copy= image.copy()
        # cv2.rectangle(copy, (957, 88), (962, 91), (255,0,0), 1)
        print("===================Image No. {}===================".format(i))
        spike_status = spike_handler.get_spike_status(image)
        print("spike_status", spike_status)
        end = time.time()
        print("Time elapsed", end - start)
