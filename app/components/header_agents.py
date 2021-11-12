import glob
import os
import time

import cv2
import numpy as np


class GetLiveAgents():
    def __init__(self):
        self.agent_templates = self.generate_agent_templates()

    def generate_agent_templates(self):
        generated_agent_templates = []
        template_directory = os.path.abspath(os.path.join(
            __file__, "../../templates/agent_templates"))
        all_templates = [image for image in glob.glob(
            template_directory+"/*_resized.png")]
        for template in all_templates:
            agent = (template.split(r"\agent_templates"))[
                1].split("_icon")[0][1:]
            original = cv2.resize(cv2.imread(
                template, cv2.IMREAD_UNCHANGED), (44, 44))
            gray = cv2.resize(cv2.imread(template, 0), (44, 44))
            o_ret, original_mask = cv2.threshold(
                original[:, :, 3], 0, 255, cv2.THRESH_BINARY)
            f_ret, original_flipped_mask = cv2.threshold(
                cv2.flip(original[:, :, 3], 1), 0, 255, cv2.THRESH_BINARY)
            flipped_gray = cv2.flip(gray, 1)
            generated_agent_templates.append({
                "agent": agent,
                "original": original,
                "gray": gray,
                "original_mask": original_mask,
                "original_flipped_mask": original_flipped_mask,
                "flipped_gray": flipped_gray
            })
        return generated_agent_templates

    def identify_agent(self, resized_frame, side):
        identified_agent = None
        for template in self.agent_templates:
            if side == "right":
                result = cv2.matchTemplate(
                    resized_frame, template["flipped_gray"], cv2.TM_CCOEFF_NORMED, None, template["original_flipped_mask"])
            else:
                result = cv2.matchTemplate(
                    resized_frame, template["gray"], cv2.TM_CCOEFF_NORMED, None, template["original_mask"])
            max_location = cv2.minMaxLoc(result)[1]
            if max_location > 0.7:
                identified_agent = template["agent"]
        return identified_agent

    def process_frame(self, screen_frame, side):
        all_agents = []
        if side == "left":
            x_start = 389
        else:
            x_start = 1192
        x_end = x_start + 48
        for agent_place in range(0, 5):
            cropped_agent_image = screen_frame[33:77, x_start:x_end]
            identified_agent = self.identify_agent(cropped_agent_image, side)
            # if identified_agent:
            #     all_agents.append(identified_agent)
            all_agents.append(identified_agent)
            x_start = x_start + 73
            x_end = x_start + 48
        return all_agents

    def get_agents(self, main_frame):
        agents_alive = {"left": [], "right": []}
        main_frame_gray = cv2.cvtColor(main_frame, cv2.COLOR_BGR2GRAY)
        agents_alive["left"] = self.process_frame(main_frame_gray, "left")
        agents_alive["right"] = self.process_frame(main_frame_gray, "right")
        return agents_alive


if __name__ == "__main__":

    get_live_agents = GetLiveAgents()
    feed_images_directory = os.path.abspath(
        os.path.join(__file__, "../../test_images/Feed Images/"))
    for i in range(1, 54):
        print("=======================")
        print("FILE: ", i)
        start = time.time()
        img = cv2.imread('{}/feed{}.png'.format(feed_images_directory, i))
        # cv2.imshow("img",img)
        agents_alive = get_live_agents.get_agents(img)
        print(agents_alive)
        end = time.time()
        print("Time elapsed", end - start)