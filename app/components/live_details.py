import os
import time
import warnings

import cv2

from header_agents import GetLiveAgents
from health import GetHealth
from loadouts import GetLoadouts
from score import GetScore
from scoreboard_agents import GetScoreBoardAgents
from scoreboard_detector import ScoreBoardDetector
from shields import GetShields
from spike import GetSpike
from ultimates import GetUltimates

warnings.filterwarnings("ignore")


class LiveDetails():
    def __init__(self):
        # get score from in-game api- discard ocr below
        # self.score_helper = GetScore()
        self.spike_helper = GetSpike()
        self.shield_helper = GetShields()
        self.loadout_helper = GetLoadouts()
        self.header_agent_helper = GetLiveAgents()
        self.scoreboard_agents_helper = GetScoreBoardAgents()
        self.scoreboard_detector_helper = ScoreBoardDetector()
        self.health_helper = GetHealth()
        self.ultimate_helper = GetUltimates()
        self.old_score = [0, 0]
        self.match_details = {}

    def get_live_details(self, frame):
        # get score from in-game api- discard ocr below
        # score = self.score_helper.get_score(frame)

        agents_health = self.health_helper.get_health(frame)
        agents_health["blue"] = agents_health["left"]
        agents_health["red"] = agents_health["right"]
        spike_status = self.spike_helper.get_spike_status(frame)
        header_agents = self.header_agent_helper.get_agents(
            frame)
        header_agents["blue"] = header_agents["left"]
        header_agents["red"] = header_agents["right"]
        scoreboard_present = self.scoreboard_detector_helper.detect_scoreboard(
            frame)
        print("ScoreBoardDetector", scoreboard_present)
        if scoreboard_present:
            agents_ultimate_points = self.ultimate_helper.get_ultimate_points(
                frame)
            shields = self.shield_helper.get_shields(frame)
            loadouts = self.loadout_helper.get_loadouts(frame)
            scoreboard_agents = self.scoreboard_agents_helper.get_agents(frame)
            agents_with_loadouts_shields = list(
                zip(scoreboard_agents["top"], loadouts["top"], shields["top"], agents_ultimate_points["top"]))

            return({"score": "score", "spike_status": spike_status,
                    "agents_with_loadouts_shields": agents_with_loadouts_shields,
                    "alive_agents": header_agents, "health_values": agents_health})
        return({"score": "score", "spike_status": spike_status,
                "alive_agents": header_agents, "health_values": agents_health})


if __name__ == "__main__":
    live_details_handler = LiveDetails()
    tab_images_directory = os.path.abspath(
        os.path.join(__file__, "../../test_images/Tab Images/"))
    for i in range(1, 10):
        start = time.time()
        image = cv2.imread('{}/{}.png'.format(tab_images_directory, i))
        print("===================Image No. {}===================".format(i))
        live_details = live_details_handler.get_live_details(image)
        print("Live Details", live_details)
        end = time.time()
        print("Time elapsed", end - start)
