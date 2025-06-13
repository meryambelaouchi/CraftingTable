# CraftingTable


## Table of Contents
1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Installation Instructions](#installation-instructions)
4. [Usage](#usage)
5. [Marker & Recipe Reference](marker-&-recipe-reference)
6. [Sources](#sources)

## Features

- Detect and identify Aruco markers in real time via webcam
- Match combinations of markers to recipes
- Trigger Resolume clips when recipes are crafted
- Play hint animations if no activity occurs
- Auto-reset the system after 3 minutes of inactivity


## Technologies Used

- Python 3.7+
- OpenCV (cv2, aruco)
- REST API calls
- Resolume Arena 

## Installation Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/aruco-crafting-resolume.git
cd aruco-crafting-resolume
Install dependencies:
```
2. Install dependencies:
```bash
pip install opencv-python requests
```

## Usage

- Start Resolume Arena
- Ensure the Web Server is enabled
- Go to Preferences → Web Server → Enable
- Run the app:
```bash
python main.py
```
- Place ArUco markers in front of your webcam according to the recipes.


## Marker & Recipe Reference

- Marker ID + Item

3 => Stick
4 => Coal
17 => Cobblestone
42 => Iron Ingot

- Recipe => Result => Resolume Column

Stick + Coal => Torch => 1
Stick + Cobblestone => Lever => 2
5x Iron Ingot => Cart => 4



## Sources

- https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce
- https://chev.me/arucogen/
- https://www.youtube.com/watch?v=AQXLC2Btag4&t=937s
- https://www.geeksforgeeks.org/computer-vision/detecting-aruco-markers-with-opencv-and-python-1/ 

