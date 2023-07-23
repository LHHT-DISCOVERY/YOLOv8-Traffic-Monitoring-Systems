# Object Detecion

import math

import numpy as np

import createBB_helmet
from sort import Sort
from testLane import *


# basics
# Display image and videos


# plots

# %matplotlib inline
# Video  path for experiment

def risize_frame(frame, scale_percent):
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    return resized

    # --------------------------------------------------------------


def video_detect_helmet(path_x):
    cap = cv2.VideoCapture(path_x)  # For video
    examBB = createBB_helmet.infoObject()
    model = YOLO('model_helmet/helmet.pt')  # large model works better with the GPU

    # tracking
    tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
    dataBienBan_XEMAYVIPHAMBAOHIEM = 'F:/python_project/BienBanNopPhatXeMayViPhamMuBaoHiem/ '
    name_class = ["without helmet", "helmet"]
    array_helmet_filter = []
    count = 0
    while True:

        success, frame = cap.read()
        results = model(frame, stream=True)
        detections = np.empty((0, 6))
        # print("shape frame : ", frame.shape)
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
                if int(box.cls[0]) == 1:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (134, 255, 162), 2)
                    draw_text(frame, " Helmet", font_scale=0.5,
                              pos=(int(x1), int(y1)), text_color=(26, 93, 26),
                              text_color_bg=(208, 192, 79))
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
        # image = cv2.line(frame, (0, int(frame.shape[0] / 2)), (int(frame.shape[1]), int(frame.shape[0] / 2)), (0, 0, 255),
        #                  8)
        for result in resultsTracker:
            x, y, w, h, id, cls = result
            x, y, w, h, id, cls = int(x), int(y), int(w), int(h), int(id), int(cls)

            text = str(id) + ": " + name_class[cls]

            #####################################################################
            #####################################################################
            center_x = (x + w) // 2
            center_y = (y + h) // 2

            filterData = 0 <= center_x <= (int(frame.shape[1])) and int(
                3 * frame.shape[0] / 10) <= center_y <= int(
                4 * frame.shape[0] / 10)

            # xét vùng roi theo trục Y
            if 0 < center_x < int(frame.shape[1]) and int((2 * frame.shape[0]) / 10) < center_y < int(
                    (8 * frame.shape[0]) / 10):
                cv2.rectangle(frame, (x, y), (w, h), (36, 255, 12), 2)
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
                if filterData and id not in array_helmet_filter:
                    draw_text(frame, text + " warning", font_scale=0.5,
                              pos=(int(x), int(y)),
                              text_color_bg=(0, 0, 0))
                    count += 1
                    array_helmet_filter.append(id)
                    cropped_frame = frame[
                                    int((3 * frame.shape[0]) / 10):int((8 * frame.shape[0]) / 10),
                                    6 * int(frame.shape[1] / 10):int(frame.shape[1])]
                    imageViolateHelmet(frame, int((0 * frame.shape[0]) / 10),
                                       int((8 * frame.shape[0]) / 10), 0 * int(frame.shape[1] / 10),
                                       8 *
                                       int(frame.shape[1] / 10), id)

                    stt_BB_CTB = dataBienBan_XEMAYVIPHAMBAOHIEM + str(id) + '.pdf'
                    frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    # Tạo tệp tạm thời và lưu ảnh PIL vào đó
                    temp_image = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
                    frame_pil.save(temp_image.name)
                    # create(box.cls[0])
                    createBB_helmet.bienBanNopPhat(examBB,
                                                   temp_image.name,
                                                   "F:/python_project/data_xe_vp_bh/ " + str(
                                                       id) + '.jpg',
                                                   stt_BB_CTB)
                    temp_image.close()
                draw_text(frame, text + " warning", font_scale=0.5,
                          pos=(int(x), int(y)),
                          text_color_bg=(0, 0, 0))
                print("count : ", count)
        start_point = (0, int((2 * frame.shape[0]) / 10))
        # vẽ hết chiều rộng và chiểu cao lấy 9/10
        end_point = (int(frame.shape[1]), int((8 * frame.shape[0]) / 10))
        color = (255, 0, 0)
        image = draw_text(frame, "So luong vi pham : " + str(len(array_helmet_filter)), font_scale=1.5,
                          pos=(int(0), int(0)),
                          text_color_bg=(255, 255, 255))

        # vẽ ra cái ROI
        image = cv2.rectangle(frame, start_point, end_point, color, 2)
        # cv2.imshow("Roi ", image)
        # cv2.waitKey(1)
        yield image


if __name__ == '__main__':
    video_detect_helmet("Videos/test9.mp4")
