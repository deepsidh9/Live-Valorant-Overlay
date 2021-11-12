import glob
import os
import time

import cv2
import numpy as np


class GetLoadouts():
    def __init__(self):
        self.weapon_templates = self.generate_weapon_templates()

    def generate_weapon_templates(self):
        generated_weapon_templates = []
        template_directory = os.path.abspath(os.path.join(
            __file__, "../../templates/weapon_templates"))
        all_templates = [image for image in glob.glob(
            template_directory+"/*_template.png")]
        for template in all_templates:
            weapon = ((template.split("\weapon_templates"))
                      [1]).split("_template")[0][1:]
            generated_weapon_templates.append({
                "weapon": weapon,
                "gray": cv2.imread(template, 0)[0:100, 0:139]
            })
        return generated_weapon_templates

    def process_loadouts_frame(self, image):
        identified_weapon = None
        for template in self.weapon_templates:
            current_template = template["gray"]
            result = cv2.matchTemplate(
                image, current_template, cv2.TM_CCOEFF_NORMED)
            max_location = cv2.minMaxLoc(result)[1]
            if max_location > 0.75:
                identified_weapon = template["weapon"]

        return identified_weapon

    def identify_weapons(self, frame, side):
        all_identified_weapons = []
        if side == "top":
            y_start = 380
            y_end = 410
        else:
            y_start = 380  # fix this
            y_end = 410  # fix this
        for agent_loadout in range(0, 5):
            resized_frame = frame[y_start:y_end, 1065:1204]
            identified_weapon = self.process_loadouts_frame(resized_frame)
            all_identified_weapons.append(identified_weapon)
            y_start = y_start + 38
            y_end = y_end + 38
        return all_identified_weapons

    def get_loadouts(self, frame):
        all_identified_weapons = {}
        main_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        all_identified_weapons["top"] = self.identify_weapons(
            main_frame_gray, "top")
        return all_identified_weapons


if __name__ == "__main__":
    get_all_loadouts = GetLoadouts()
    tab_images_directory = os.path.abspath(
        os.path.join(__file__, "../../test_images/Tab Images/"))
    for i in range(2, 10):
        start = time.time()
        image = cv2.imread('{}/{}.png'.format(tab_images_directory, i))
        print("===================Image No. {}===================".format(i))
        identified_weapons = get_all_loadouts.get_loadouts(image)
        print("Identified Weapons", identified_weapons)
        end = time.time()
        print("Time elapsed", end - start)
