import base64
import json
import os
import time

import requests
import urllib3
from prettytable import PrettyTable

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BLACK = RED = GREEN = BROWN = BLUE = PURPLE = CYAN = LIGHT_GRAY = DARK_GRAY = LIGHT_RED = LIGHT_GREEN = YELLOW = ''
LIGHT_BLUE = LIGHT_PURPLE = LIGHT_CYAN = LIGHT_WHITE = BOLD = FAINT = ITALIC = UNDERLINE = ''
BLINK = NEGATIVE = CROSSED = end_tag = ''

number_to_ranks = {
    0: LIGHT_GRAY + "Unrated" + end_tag,
    1: LIGHT_GRAY + "Unrated" + end_tag,
    2: LIGHT_GRAY + "Unrated" + end_tag,
    3: LIGHT_GRAY + "Iron 1" + end_tag,
    4: LIGHT_GRAY + "Iron 2" + end_tag,
    5: LIGHT_GRAY + "Iron 3" + end_tag,
    6: BROWN + "Bronze 1" + end_tag,
    7: BROWN + "Bronze 2" + end_tag,
    8: BROWN + "Bronze 3" + end_tag,
    9: LIGHT_WHITE + "Silver 1" + end_tag,
    10: LIGHT_WHITE + "Silver 2" + end_tag,
    11: LIGHT_WHITE + "Silver 3" + end_tag,
    12: BOLD + YELLOW + "Gold 1" + end_tag,
    13: BOLD + YELLOW + "Gold 2" + end_tag,
    14: BOLD + YELLOW + "Gold 3" + end_tag,
    15: LIGHT_CYAN + "Platinum 1" + end_tag,
    16: LIGHT_CYAN + "Platinum 2" + end_tag,
    17: LIGHT_CYAN + "Platinum 3" + end_tag,
    18: LIGHT_PURPLE + "Diamond 1" + end_tag,
    19: LIGHT_PURPLE + "Diamond 2" + end_tag,
    20: LIGHT_PURPLE + "Diamond 3" + end_tag,
    21: LIGHT_RED + "Immortal" + end_tag,
    22: LIGHT_RED + "Immortal 2" + end_tag,
    23: LIGHT_RED + "Immortal 3" + end_tag,
    24: BOLD + "Radiant" + end_tag
}

headers = {}

class GetCoreMatch():
    def __init__(self):
        self.region = self.get_region()
        print("Region",self.region)
        self.pd_url = f"https://pd.{ self.region[0]}.a.pvp.net"
        self.glz_url = f"https://glz-{ self.region[1][0]}.{self.region[1][1]}.a.pvp.net"
        self.region = self.region[0]
        self.lockfile = self.get_lockfile()
        self.current_version = self.get_current_version()
        self.headers= self.get_headers()
        self.content = self.get_content()
        self.agent_dict = self.get_all_agents()
        self.seasonID = self.get_latest_season_id()
        self.table = PrettyTable()
    
    def get_region(self):
        path = os.path.join(os.getenv('LOCALAPPDATA'), R'VALORANT\Saved\Logs\ShooterGame.log')
        with open(path, "r", encoding="utf8") as file:
            while True:
                line = file.readline()
                if '.a.pvp.net/account-xp/v1/' in line:
                    pd_url = line.split('.a.pvp.net/account-xp/v1/')[0].split('.')[-1]
                elif 'https://glz' in line:
                    glz_url = [(line.split('https://glz-')[1].split(".")[0]), (line.split('https://glz-')[1].split(".")[1])]
                if "pd_url" in locals() and "glz_url" in locals():
                    return [pd_url, glz_url]

    def get_current_version(self):
        # version = f"{data['branch']}-shipping-{data['buildVersion']}-{data['version'].split('.')[3]}"
        # release-03.02-shipping-9-587972
        path = os.path.join(os.getenv('LOCALAPPDATA'), R'VALORANT\Saved\Logs\ShooterGame.log')
        with open(path, "r", encoding="utf8") as file:
            while True:
                line = file.readline()
                if 'CI server version:' in line:
                    version_without_shipping = line.split('CI server version: ')[1].strip()
                    version = version_without_shipping.split("-")
                    version.insert(2, "shipping")
                    return "-".join(version)
                    # return version


    def fetch(self,url_type, endpoint, method):
        # global response
        try:
            if url_type == "glz":
                response = requests.request(method, self.glz_url + endpoint, headers=self.headers, verify=False)
                return response.json()
            elif url_type == "pd":
                response = requests.request(method, self.pd_url + endpoint, headers=self.headers, verify=False)
                return response
            elif url_type == "local":
                local_headers = {}
                local_headers['Authorization'] = 'Basic ' + base64.b64encode(
                    ('riot:' + self.lockfile['password']).encode()).decode()
                response = requests.request(method, f"https://127.0.0.1:{self.lockfile['port']}{endpoint}",
                                            headers=local_headers,
                                            verify=False)
                return response.json()
            elif url_type == "custom":
                response = requests.request(method, f"{endpoint}", headers=self.headers,
                                            verify=False)
                return response.json()
        except json.decoder.JSONDecodeError:
            print(response)
            print(response.text)


    def get_lockfile(self):
        try:
            with open(os.path.join(os.getenv('LOCALAPPDATA'), R'Riot Games\Riot Client\Config\lockfile')) as lockfile:
                data = lockfile.read().split(':')
                keys = ['name', 'PID', 'port', 'password', 'protocol']
                return dict(zip(keys, data))
        except:
            raise Exception("Lockfile not found, you're not in a game!")

    def get_headers(self):
        local_headers = {}
        local_headers['Authorization'] = 'Basic ' + base64.b64encode(
            ('riot:' + self.lockfile['password']).encode()).decode()
        response = requests.get(f"https://127.0.0.1:{self.lockfile['port']}/entitlements/v1/token", headers=local_headers,
                                verify=False)
        entitlements = response.json()
        self.puuid = entitlements['subject']
        headers = {
            'Authorization': f"Bearer {entitlements['accessToken']}",
            'X-Riot-Entitlements-JWT': entitlements['token'],
            'X-Riot-ClientPlatform': "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Z"
                                    "m9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0I"
                                    "jogIlVua25vd24iDQp9",
            'X-Riot-ClientVersion': self.current_version
        }
        return headers


    def get_puuid(self):
        return self.puuid


    def get_coregame_match_id(self):
        try:
            response = self.fetch(url_type="glz", endpoint=f"/core-game/v1/players/{self.puuid}", method="get")
            match_id = response['MatchID']
            return match_id
        except KeyError:
            return 0
        except TypeError:
            return 0


    def get_pregame_match_id(self):
        try:
            response = self.fetch(url_type="glz", endpoint=f"/pregame/v1/players/{self.puuid}", method="get")
            match_id = response['MatchID']
            return match_id
        except KeyError:
            return 0
        except TypeError:
            return 0


    def get_coregame_stats(self):
        response = self.fetch("glz", f"/core-game/v1/matches/{self.get_coregame_match_id()}", "get")
        return response


    def get_pregame_stats(self):
        response = self.fetch("glz", f"/pregame/v1/matches/{self.get_pregame_match_id()}", "get")
        return response


    def getRank(self,puuid, seasonID):
        response = self.fetch('pd', f"/mmr/v1/players/{puuid}", "get")
        try:
            r = response.json()
            rankTIER = r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonID]["CompetitiveTier"]
            if int(rankTIER) >= 21:
                rank = [rankTIER,
                        r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonID]["RankedRating"],
                        r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonID]["LeaderboardRank"]]
            elif int(rankTIER) not in (0, 1, 2, 3):
                rank = [rankTIER,
                        r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonID]["RankedRating"],
                        0]
            else:
                rank = [0, 0, 0]
        except TypeError:
            rank = [0, 0, 0]
        except KeyError:
            rank = [0, 0, 0]
        return [rank, response.ok]


    def get_name_from_puuid(self,puuid):
        response = requests.put(self.pd_url + f"/name-service/v2/players", headers=self.headers, json=[puuid], verify=False)
        return response.json()[0]["GameName"] + "#" + response.json()[0]["TagLine"]


    def get_multiple_names_from_puuid(self,puuids):
        response = requests.put(self.pd_url + "/name-service/v2/players", headers=self.headers, json=puuids,
                                verify=False)
        name_dict = {}
        for player in response.json():
            name_dict.update({player["Subject"]: player["GameName"] + "#" + player["TagLine"]})
        return name_dict


    def get_content(self):
        content = self.fetch("custom", f"https://shared.{self.region}.a.pvp.net/content-service/v3/content", "get")
        return content


    def get_latest_season_id(self):
        for season in self.content["Seasons"]:
            if season["IsActive"]:
                return season["ID"]

    def get_all_agents(self):
        all_agents = requests.get("https://valorant-api.com/v1/agents?isPlayableCharacter=true").json()
        agent_dict = {}
        agent_dict.update({None: None})
        for agent in all_agents["data"]:
            agent_dict.update({agent['uuid'].lower(): agent['displayName']})
        return agent_dict
    def presence(self):
        presences = self.fetch(url_type="local", endpoint="/chat/v4/presences", method="get")
        # print("Response from presence",response)
        return presences['presences']


    def get_game_state(self):
        for presence in self.presence():
            if presence['puuid'] == self.puuid:
                return json.loads(base64.b64decode(presence['private']))["sessionLoopState"]


    def decode_presence(self,private):
        return json.loads(base64.b64decode(private))

    def level_to_color(self,level):
        PLcolor = ''
        if level >= 400:
            PLcolor = CYAN  # PL = Player Level
            pass
        elif level >= 300:
            PLcolor = YELLOW
            pass
        elif level >= 200:
            PLcolor = BLUE
            pass
        elif level >= 100:
            PLcolor = BROWN
            pass
        elif level < 100:
            PLcolor = LIGHT_GRAY
        return PLcolor


    def get_names_from_puuids(self,players):
        players_puuid = []
        for player in players:
            players_puuid.append(player["Subject"])
        return self.get_multiple_names_from_puuid(players_puuid)


    def get_color_from_team(self,team):
        if team == 'Red':
            color = LIGHT_RED
        elif team == 'Blue':
            color = LIGHT_BLUE
        else:
            color = ''
        return color


    def get_PlayersPuuid(self,Players):
        res = []
        for player in Players:
            res.append(player["Subject"])
        return res

    def addRowTable(self,table, args):
        # for arg in args:
        table.add_rows([args])

    def fetch_match_details(self):
        try:
            presence = self.presence()
            game_state = self.get_game_state()
        except TypeError:
            raise Exception("Game has not started yet!")
        game_state_dict = {
            "INGAME": LIGHT_RED + "In-Game" + end_tag,
            "PREGAME": LIGHT_GREEN + "Agent Select" + end_tag,
            "MENUS": BOLD + YELLOW + "In-Menus" + end_tag
        }
        teams={"blue":{},"red":{}}
        if game_state == "INGAME":
            initiated_player_team="blue"
            Players = self.get_coregame_stats()["Players"]
            Players= [player for player in Players if player["TeamID"] in ["Blue","Red"]]
            # print("Players INGAME",Players)
            # partyOBJ = get_party_json(get_PlayersPuuid(Players), presence)
            names = self.get_names_from_puuids(Players)
            # print("names INGAME",names)
            Players.sort(key=lambda Players: Players["PlayerIdentity"].get("AccountLevel"), reverse=True)
            Players.sort(key=lambda Players: Players["TeamID"], reverse=True)
            partyCount = 0
            partyIcons = {}
            for player in Players:
                if player["Subject"] == self.puuid:
                    initiated_player_team = player["TeamID"].lower()
                rank = self.getRank(player["Subject"], self.seasonID)
                rankStatus = rank[1]
                rank = rank[0]
                player_level = player["PlayerIdentity"].get("AccountLevel")
                color = self.get_color_from_team(player['TeamID'])
                PLcolor = self.level_to_color(player_level)

                # AGENT
                agent = BOLD + str(self.agent_dict.get(player["CharacterID"].lower())) + end_tag
                if agent.lower() == "kay/o":
                    agent = "kayo"

                # NAME
                # name = color + names[player["Subject"]] + end_tag
                name = color + names[player["Subject"]]
                try:
                    split_name = (name.split("#"))[0]
                    name = split_name
                except Exception as exception:
                    pass
                #rank
                rankName = number_to_ranks[rank[0]]

                #rr
                rr = rank[1]

                #leaderboard
                leaderboard = rank[2]


                #level
                level = PLcolor + str(player_level) + end_tag
                teams[player["TeamID"].lower()][agent.lower()]={"agent":agent.lower(),
                                "name":name,
                                "rankName":rankName,
                                "rr":rr,
                                "leaderboard":leaderboard,
                                "level":level,
                                "team":player["TeamID"].lower(),
                                "alive":True,
                                "health":100,
                                }
                self.addRowTable(self.table, [player['TeamID'],
                                agent,
                                name,
                                rankName,
                                rr,
                                leaderboard,
                                level
                                ])
                # table.add_rows([])
                if not rankStatus:
                    print("You got rate limited 😞 waiting 3 seconds!")
                    time.sleep(3)
        self.table.title = "s"
        self.table.field_names = ["Team","Agent", "Name", "Rank", "RR", "Leaderboard Position", "Level"]
        print(self.table)
        print("MAIN RESULTS",teams)
        teams["initiated_player_team"] = initiated_player_team
        return teams
if __name__ == "__main__":
    match=GetCoreMatch()
    match.fetch_match_details()
