
# Valorant Live Overlay

  

  

An Overlay proof-of-concept Application for Valorant giving information in real-time about current match, spike and player status(dead/alive, weapons, ultimate points, shields etc.)

  

  

### Important Caveat:

  

- Currently works only with the following configuration :

  

- "Fullscreen Windowed"

  

-  [1920x1080](https://github.com/deepsidh9/Live-Valorant-Overlay/tree/1920x1080) **OR**  [1920x1200](https://github.com/deepsidh9/Live-Valorant-Overlay/)

  

- "Fill" Mode

  
  
  

## Disclaimer

  

  

This is a fan-made project. Riot Games does not endorse, sponsor or affiliate with this project. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.

  

## Description

  

This project is a proof-of-concept that gets you live details of a match and populates a HTML file which can be used as an overlay in streaming apps such as OBS, Streamlabs OBS, Twitch Studio and XSplit which support "BrowserSource".

  

#### A small demo

  

  

![](demo.gif)

  

  

#### Features

  

  

The following features are currently available:

  

1. A Player's name, agent and **alive/dead status**

  

2. A Player's bought **shield** (only none/half/full values)

  

3. Both team's bought **weapons** (as seen from a spectator's perspective)

  

4. Both teams' agents' current **ultimate points** (as seen from a spectator's perspective).

5. Current Score

- It is ready to use but has to be incorporated in the main live details aggregator component (app/components/live_details.py). The reason for exclusion is because there exists a better way of obtaining the score - through the in-game API (yet to be implemented). See Possible Future Updates below for more information.

6. Current Spike Status (True/False)

- It is ready to use but has to be incorporated in the main live details aggregator component (app/components/live_details.py). The reason for exclusion is the occasional inaccurate result.

  

## Installation

  

  

#### Prerequisites

  

- Python3.x

  

- Run the following command in the project's root directory (assuming you have cloned this repository) to install all other dependencies

  

  

```sh

  

pip install -r requirements.txt

  

```

  

You also need to install the latest build of [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) if you intend to use that instead of easyocr. It's totally up to you. You would need to make changes in the code as necessary, however OCR is only a small part of the app.

  

## Usage

  

  

1. Run Python Server

  

  

Change the working directory to ```app``` and run the following command to start the python server which will serve requests such as starting/stopping match processing and facilitate communication using Socket IO between different components (both the backend and the frontend).

  

```

  

python app.py

  

```

  

2. Open Overlay

  

##### Using the Overlay in streaming apps

  

For using the overlay with OBS, add a "BrowserSource" and navigate to the ```overlay``` directly and open ```index.html``` . Set the width and height to 1920 and 1080/1200 (whichever resolution you are using) respectively (currently supported for this resolution only, explained further below) It should show dummy data for two teams.

  

  

3. Instruct server to start match processing

  

When your match has just started, send a GET/POST request to ```http://127.0.0.1:4445/start_match``` or just open this link in the browser. It will start processing the match and the details will be reflected in the overlay.

  

4. Stop Match Processing

  

When your match has ended, send a GET/POST request to ```http://127.0.0.1:4445/stop_match``` or just open this link in the browser. It will stop processing the match.

  

#### Get Match Details from the Server directly

  

  

You can make POST requests to ```http://127.0.0.1:4445/get_match_details``` to get the current match details.

  

  

To receive match details the moment they are updated, connect to Socket IO at ```http://127.0.0.1:4445/``` (see app/components/get_live_frames.py to see how to connect) and listen on "new_event" event.

  

## How does it work?

  

  

### Match Processing Techniques

  

This app uses Image Processing using OpenCV and largely Template Matching to get information from a screenshot of the game.

  

  

#### Starting the match processing

  

- When you send the "start_match" request to the server, it fetches all the players' information such as their name, rank, team etc.

  

- It then starts another process of taking screenshots (see app/components/get_live_frames.py) of the game every 1 second and passes this screenshot to the relevant module for processing.

  

  

#### What happens in the match processing

  

  

- The agent icons' present in the header bar are matched with all of the existing player icon templates (see app/components/header_agents.py) and the one that matches the most (a confidence of greater than 70%) is then determined to be alive.

  

- All of the other data is grabbed from the scoreboard (when it is present) using a combination of Template Matching and OCR. You can inspect all the respective modules to see how they work.

  

### Populating the Overlay

  

  

The Overlay files (overlay/index.html+overlay/app.js) connect to the Python server via SocketIO.

  

  

The provided overlay files are a crude proof of concept of a working overlay.

  

  

#### Developing your own overlay

  

  

Feel free to develop your own overlay using the data received from the server.

  

  

## How can I make it work for other resolutions?

  

  

For now the values for [1920x1080](https://github.com/deepsidh9/Live-Valorant-Overlay/tree/1920x1080) or [1920x1200](https://github.com/deepsidh9/Live-Valorant-Overlay/) are hardcoded.

  

  

- The template images are also applied directed using template matching **BUT** can be resized using relative measurements to the desired resolution.

  

- The template images should be easy, accurate enough to scale down but I cannot account for the results when they are scaled up.

  

- You can make your own templates too for a specific resolution if you wish.

  

You can compare both the branches to see what changes have to be made in order to make it work for other resolutions.

  

## How can I make it work for getting the other team's information?

  

**This is only relevant for the [1920x1200](https://github.com/deepsidh9/Live-Valorant-Overlay/) resolution as the modules only process the top part of the scoreboard for that resolution. This functionality has been completed for the [1920x1080](https://github.com/deepsidh9/Live-Valorant-Overlay/tree/1920x1080) resolution.**

  

- The scoreboard can be divided into two parts - top (your team) and the bottom part (enemy team).

  

- The modules as of this moment only process the top part as seen in the code. You can pinpoint the pixels from where you need to start processing the bottom part.

  

- The current configuration of all the modules returns the bottom part as an empty array or a null object. Once you specify the pixels and it starts working, you don't need to do much work to aggregate the bottom results with the top.

  

  

## Possible Future Updates

  

- CREDS through OCR

  

- Score through in-game API

  

- UI for application:

  

- Inputting team's names, logos etc.

  

- Automatic match processing start/end using presence data

  

- Getting information from all modules parallelly to speed up information retrieval.

  

- Write resizing logic to support different resolutions.

  

  

## Credits

  

  

The players' information retrieval method is inspired by the wonderful work done by [isaacKenyon's VRY](https://github.com/isaacKenyon/VALORANT-rank-yoinker) and [colinhartigan's fork](https://github.com/colinhartigan/valorant-live-match-rank-grabber).

  

  

## Contact

  

If you'd like to contact me regarding this application (for removal or any other purpose), feel free to [email me](mailto:deepsidh912@gmail.com) or reach out on Discord - (Deep#8700).
