import glob
import os
import time

import cv2


class GetShields():
    def __init__(self):
        self.shield_templates = self.generate_shield_templates()

    def generate_shield_templates(self):
        generated_shield_templates = []
        template_directory = os.path.abspath(os.path.join(
            __file__, "../../templates/shield_templates"))
        all_templates = [image for image in glob.glob(
            template_directory+"/*.png")]
        for template in all_templates:
            shield = (template.split(r"\shield_templates"))[
                1].split(".png")[0][1:]
            generated_shield_templates.append({
                "shield": shield,
                "gray": cv2.imread(template, 0)[0:100, 0:139]
            })
        return generated_shield_templates

    def process_shields_frame(self, image):
        all_results = []
        for template in self.shield_templates:
            current_template = template["gray"]
            result = cv2.matchTemplate(
                image, current_template, cv2.TM_CCOEFF_NORMED)
            all_results.append((cv2.minMaxLoc(result)[1], template["shield"]))
        if max(all_results)[0] > 0.4:
            print("Result", max(all_results))
            return max(all_results)[1]
        else:
            return None

    def identify_shields(self, frame, side):
        all_identified_shields = []
        if side == "top":
            y_start = 382
            y_end = 413
        else:
            y_start = 380  # fix this
            y_end = 410  # fix this
        for agent_loadout in range(0, 5):
            resized_frame = frame[y_start:y_end, 1201:1230]
            identified_weapon = self.process_shields_frame(resized_frame)
            all_identified_shields.append(identified_weapon)
            y_start = y_start + 37
            y_end = y_start + 31
        return all_identified_shields

    def get_shields(self, frame):
        all_identified_shields = {}
        main_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        all_identified_shields["top"] = self.identify_shields(
            main_frame_gray, "top")
        # all_identified_shields["bottom"] = self.get_weapons(frame,"bottom")
        return all_identified_shields


if __name__ == "__main__":
    get_all_shields = GetShields()
    tab_images_directory = os.path.abspath(
        os.path.join(__file__, "../../test_images/Tab Images/"))
    for i in range(1, 12):
        start = time.time()
        image = cv2.imread('{}/{}.png'.format(tab_images_directory, i))
        print("===================Image No. {}===================".format(i))
        identified_weapons = get_all_shields.get_shields(image)
        print("Identified Weapons", identified_weapons)
        end = time.time()
        print("Time elapsed", end - start)


# for i in range(1,10):
#     frame = cv2.imread("Tab Images/{}.png".format(i),0)
#     y_start =382
#     y_end =413
#     for agent_row in range(0,5):
#         cropped_shield_image= frame[y_start:y_end,1201:1230]
#         print("image shape",cropped_shield_image.shape)
#         full_shield_template= cv2.imread(r'''C:\Users\deepb\Desktop\Development\Overlay-Live Valorant Stats\full_shield.png''',0)
#         print("full shield shape",full_shield_template.shape)
#         half_shield_template= cv2.imread(r'''C:\Users\deepb\Desktop\Development\Overlay-Live Valorant Stats\half_shield.png''',0)
#         print("half shield shape",half_shield_template.shape)
#         full_result= cv2.matchTemplate(cropped_shield_image,full_shield_template,cv2.TM_CCOEFF_NORMED)
#         half_result= cv2.matchTemplate(cropped_shield_image,half_shield_template,cv2.TM_CCOEFF_NORMED)
#         print("Full Shield",cv2.minMaxLoc(full_result))
#         print("Half Shield",cv2.minMaxLoc(half_result))
#         cv2.imshow("Image",cropped_shield_image)
#         cv2.waitKey()
#         # if agent_row==3:
#         #     cv2.imwrite("half_shield.png",cropped_shield_image)
#         y_start = y_start + 37
#         y_end = y_start + 31

# image = cv2.imread(r'''C:\Users\deepb\Desktop\Development\Overlay-Live Valorant Stats\All Inclusive OBS Overlay\Tab Images\12.png''',0)
# cropped_shield_image= image[554:577,1202:1226]
# cv2.imshow("Image",cropped_shield_image)
# cv2.imwrite("half_shield.png",cropped_shield_image)
# cv2.waitKey()
