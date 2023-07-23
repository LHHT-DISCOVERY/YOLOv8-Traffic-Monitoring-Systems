import math

import cvzone
import numpy as np

from sort import Sort
from testLane import *

cap = cv2.VideoCapture("F:/python_project/Videos/main.mp4")  # For video

model = YOLO(r"F:\python_project\best_new\best.pt")  # large model works better with the GPU

mask = cv2.imread("static/mask.png")

mainCounter = cv2.imread("static/main_counter.png", cv2.IMREAD_UNCHANGED)
# mainCounter = cv2.resize(mainCounter, (700, 250))
outCounter = cv2.imread("static/out.png", cv2.IMREAD_UNCHANGED)
inCounter = cv2.imread("static/in.png", cv2.IMREAD_UNCHANGED)

# tracking
tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

limitsUp = [210, 450, 600, 450]
limitsDown = [650, 450, 1000, 450]

totalCountUp = []
totalCountDown = []

clsCounterUp = {'car': 0, 'truck': 0, 'motorbike': 0}
clsCounterDown = {'car': 0, 'truck': 0, 'motorbike': 0}

name_class = ["car", "motorcycle", "xe dap", "truck", "bus"]

while True:
    success, img = cap.read()
    results = model(img, stream=True)
    detections = np.empty((0, 6))
    for r in results:
        boxes = r.boxes
        name = r.names
        for box in boxes:
            # BBOX
            print(box)
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            w, h = x2 - x1, y2 - y1
            bbox = (x1, y1, w, h)
            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100

            # Class Name
            cls = int(box.cls[0])
            currentClass = model.names[cls]
            print(currentClass)
            if cls == 0:
                currentArray = np.array([x1, y1, x2, y2, conf, cls])
                detections = np.vstack((detections, currentArray))

            if cls == 3:
                currentArray2 = np.array([x1, y1, x2, y2, conf, cls])
                detections = np.vstack((detections, currentArray2))

            if cls == 1:
                currentArray3 = np.array([x1, y1, x2, y2, conf, cls])
                detections = np.vstack((detections, currentArray3))

    # print("printing directions")
    # print(detections)
    classes_array = detections[:, -1:]
    print("class_array", classes_array)
    resultsTracker = tracker.update(detections)
    # print("printing result tracker")
    # print(resultsTracker)
    # print(resultsTracker.shape, classes_array.shape)
    try:
        resultsTracker = np.hstack((resultsTracker, classes_array))
        print("result tracker -----------------------------------", resultsTracker)
    except ValueError:
        classes_array = classes_array[:resultsTracker.shape[0], :]
        resultsTracker = np.hstack((resultsTracker, classes_array))
        print("result tracker ex ------------------------------------", resultsTracker)
    # print(resultsTracker)
    # cv2.line(img, (limitsUp[0], limitsUp[1]), (limitsUp[2], limitsUp[3]), (0, 0, 255), thickness=5)
    # cv2.line(img, (limitsDown[0], limitsDown[1]), (limitsDown[2], limitsDown[3]), (0, 0, 255), thickness=5)

    for result in resultsTracker:
        x1, y1, x2, y2, id, cls = result
        print(
            "frame _ id --------------------------------------------------------------------------------------------------------------------------",
            cls)
        x1, y1, x2, y2, id, cls = int(x1), int(y1), int(x2), int(y2), int(id), int(cls)
        w, h = x2 - x1, y2 - y1
        cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))
        cvzone.putTextRect(img, text=f"{model.names[cls]} {id}", pos=(max(0, x1), max(35, y1)),
                           scale=2,
                           thickness=3,
                           offset=10)
        cx, cy = x1 + w // 2, y1 + h // 2
        cv2.circle(img, (cx, cy), radius=5, color=(255, 0, 255), thickness=cv2.FILLED)
    cv2.imshow('Image', img)
    cv2.waitKey(1)
