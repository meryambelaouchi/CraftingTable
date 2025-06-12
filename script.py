import cv2
import cv2.aruco as aruco
import requests
import time
from collections import Counter

marker_to_item = {
    3: "Stick",
    4: "Coal",
    42: "Iron Ingot",
    17: "Cobblestone"
}

# recipes and columns in resolume 
recipes = {
    (3, 4): 1,             
    (3, 17): 2,            
    (42, 42, 42): 4        
}

ordered_recipes = [
    (3, 4),
    (3, 17),
    (42, 42, 42)
]

RESOLUME_HOST = "http://localhost:8080"
CLIP_TRIGGER_PATH = "/api/v1/composition/columns/{column}/connect"
OVERLAY_TRIGGER_PATH = "/api/v1/composition/layers/{layer}/clips/{clip_index}/connect"

# hint columns for each recipe step (clip indices for layer 3)
hint_clips = {
    0: [12, 13, 14],  # Torch
    1: [15, 16, 17],  # Lever
    2: [18, 19, 20]   # Cart
}

# open webcam
cap = cv2.VideoCapture(0)

# set up aruco dictionary and detector
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)

current_step = 0
last_activity_time = time.time()
hint_level = 0

def trigger_column(column):
    url = f"{RESOLUME_HOST}{CLIP_TRIGGER_PATH.format(column=column)}"
    try:
        response = requests.post(url)
        if response.status_code == 200:
            print(f"Triggered Resolume column {column}")
        else:
            print("Trigger failed:", response.status_code, response.text)
    except Exception as e:
        print(" Error triggering Resolume:", e)

def trigger_hint_clip(layer, clip_index):
    url = f"{RESOLUME_HOST}{OVERLAY_TRIGGER_PATH.format(layer=layer, clip_index=clip_index)}"
    try:
        response = requests.post(url)
        if response.status_code == 200:
            print(f"Triggered hint: Layer {layer}, Clip {clip_index}")
        else:
            print("Hint trigger failed:", response.status_code, response.text)
    except Exception as e:
        print("Error triggering hint:", e)

def print_detected_items(ids):
    items = [marker_to_item.get(i, f"Unknown({i})") for i in ids]
    print("Detected items:", ", ".join(items))

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # convert to grayscale (needed to detect the markers)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect aruco markers
    corners, ids, _ = detector.detectMarkers(gray)

    if ids is not None:
        ids_list = sorted(ids.flatten().tolist())
        aruco.drawDetectedMarkers(frame, corners, ids)
        print_detected_items(ids_list)

        # get current recipe
        if current_step < len(ordered_recipes):
            required_recipe = ordered_recipes[current_step]

            if Counter(ids_list) == Counter(required_recipe):
                column_index = recipes[required_recipe]
                print(f"🎉 Crafted: {required_recipe} → triggering clip {column_index}")
                trigger_column(column=column_index)
                current_step += 1
                last_activity_time = time.time()
                hint_level = 0

    # show webcam
    cv2.imshow("Crafting Table Camera", frame)

    # hint logic
    if current_step < len(ordered_recipes):
        if time.time() - last_activity_time > 60 and hint_level < 3:
            clip_index = hint_clips[current_step][hint_level]
            print(f"Triggering hint level {hint_level+1} → clip {clip_index} on layer 3")
            trigger_hint_clip(layer=3, clip_index=clip_index)
            hint_level += 1
            last_activity_time = time.time()

    # exit with q
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
