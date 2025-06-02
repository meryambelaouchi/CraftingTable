import cv2
import cv2.aruco as aruco

# open webcam
cap = cv2.VideoCapture(0)

# set up aruco dictionary and detector
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # convert to grayscale (needed to detect the markers)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect aruco markers
    corners, ids, _ = detector.detectMarkers(gray)

    if ids is not None:
        ids_list = ids.flatten().tolist()
        aruco.drawDetectedMarkers(frame, corners, ids)
        print("👁 Detected marker IDs:", ids_list)

    # show webcam
    cv2.imshow("ArUco Marker Detection", frame)

    # exit with q
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
