import math

import numpy as np

from sort import Sort
from testLane import *

cap = cv2.VideoCapture("Videos/test11.mp4")  # For video

model2 = YOLO("model_helmet/best_helmet_end.pt")  # large model works better with the GPU
model = YOLO("best_new/best.pt")  # large model works better with the GPU

# tracking
tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
name_class = ["without Helmet", "helmet"]
array_car_filter = []
count = 0

while True:
    success, frame = cap.read()
    results = model(frame, stream=True)
    detections = np.empty((0, 6))
    for r in results:
        boxes = r.boxes
        name = r.names
        for box in boxes:
            # BBOX
            print(box)
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
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

            if cls == 1:
                currentArray = np.array([x1, y1, x2, y2, conf, cls])
                detections = np.vstack((detections, currentArray))
                # cv2.putText(img=frame, text=str(name_class[1]),
                #             org=(int(x1), int(y1)), fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                #             fontScale=1, color=(255, 255, 0), thickness=1)
    classes_array = detections[:, -1:]
    print("class_array", classes_array)
    resultsTracker = tracker.update(detections)
    try:
        resultsTracker = np.hstack((resultsTracker, classes_array))
    except ValueError:
        classes_array = classes_array[:resultsTracker.shape[0], :]
        resultsTracker = np.hstack((resultsTracker, classes_array))
    cv2.line(frame, (0, int(frame.shape[0] / 3)), (int(frame.shape[1]), int(frame.shape[0] / 3)), (255, 255, 0), 4)
    for result in resultsTracker:
        x, y, w, h, id, cls = result
        x, y, w, h, id, cls = int(x), int(y), int(w), int(h), int(id), int(cls)
        text = name_class[cls] + str(id)

        center_x = (x + w) // 2
        center_y = (y + h) // 2
        # xét vùng roi theo trục Y
        if (center_y < (int(frame.shape[0] / 3) + 6)) and (center_y > (int(frame.shape[0] / 3) - 6)) and (
                center_x >= 0) and (center_x <= (int(frame.shape[1]))) and cls == 0:
            count += 1
            cv2.putText(img=frame, text=str(name_class[cls]) + str(count),
                        org=(int(x), int(y)), fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                        fontScale=1, color=(255, 255, 0), thickness=1)
        cv2.putText(img=frame, text=str(count),
                    org=((int(frame.shape[0] / 3)), (int(frame.shape[0] / 3))),
                    fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                    fontScale=1, color=(255, 255, 0), thickness=1)
        cv2.imshow("Roi ", frame)
        cv2.waitKey(1)
        # yield image
