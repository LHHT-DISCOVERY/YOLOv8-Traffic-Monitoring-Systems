import math

import numpy as np

from sort import Sort
from testLane import *

cap = cv2.VideoCapture("F:/python_project/Videos/main.mp4")  # For video

model = YOLO(r"F:\python_project\best_new\best.pt")  # large model works better with the GPU

# tracking
tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

name_class = ["car", "motorcycle", "xe dap", "truck", "bus"]
stt_m = 0
stt_ctb = 0
examBB = createBB.infoObject()
dataBienBan_M = 'F:/python_project/BienBanNopPhatXeMay/ '
dataBienBan_CTB = 'F:/python_project/BienBanNopPhatXeOTo/ '
array_car_filter = []

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

            # if cls == 3:
            #     currentArray2 = np.array([x1, y1, x2, y2, conf, cls])
            #     detections = np.vstack((detections, currentArray2))
            #
            # if cls == 1:
            #     currentArray3 = np.array([x1, y1, x2, y2, conf, cls])
            #     detections = np.vstack((detections, currentArray3))
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
    for result in resultsTracker:
        x, y, w, h, id, cls = result
        x, y, w, h, id, cls = int(x), int(y), int(w), int(h), int(id), int(cls)
        # x = int(box.xyxy[0][0])
        # y = int(y)
        # w = int(box.xyxy[0][2])
        # h = int(box.xyxy[0][3])

        text = name_class[cls] + str(id)

        #####################################################################
        # Xe OTO vi pham lane XE MAY
        start_line_motor = (0 * int(frame.shape[1] / 10), int((2 * frame.shape[0] / 10)))
        # 11/20 = 5.5 / 10
        end_line_motor = (11 * int(frame.shape[1] / 20), int(8 * frame.shape[0] / 10))
        canh_bao_vi_pham_lane_xe_may = start_line_motor[0] < x < end_line_motor[0] and \
                                       start_line_motor[1] < y < end_line_motor[1]
        #####################################################################

        # ##################################################################
        # Xe máy vi pham lane OTO
        # lane xe ô tô (trục y phải khớp với vùng roi)
        # trục x lấy 6/10 , trục y lấy 3/10
        start_line_car = (6 * int(frame.shape[1] / 10), int((2 * frame.shape[0] / 10)))

        # lấy từ 6/10 đến hết trục X , trục y lấy 8/10
        end_line_car = (int(frame.shape[1]), int(8 * frame.shape[0] / 10))

        canh_bao_vi_pham_lane_oto = start_line_car[0] < x < end_line_car[0] and \
                                    start_line_car[1] < y < end_line_car[1]
        # filterDataViolate(frame, (0, int(5 * frame.shape[0] / 10)),
        #                   (int(frame.shape[1]), int(55 * frame.shape[0] / 10)))
        center_x = (x + w) // 2
        center_y = (y + h) // 2
        filterData = 0 <= center_x <= (int(frame.shape[1])) and int(
            5 * frame.shape[0] / 10) <= center_y <= int(
            52 * frame.shape[0] / 100)
        #####################################################################

        # vẽ ra vùng lane xe máy và oto
        # image = cv2.rectangle(frame, start_line_car, end_line_car
        #                       , (0, 0, 255), 2)
        image = cv2.rectangle(frame, start_line_motor, end_line_motor
                              , (255, 0, 255), 2)

        # xét vùng roi theo trục Y
        if int((2 * frame.shape[0]) / 10) < int(y) < int((8 * frame.shape[0]) / 10):
            cv2.rectangle(frame, (x, y), (w, h), (36, 255, 12), 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
            if cls == 1:
                if canh_bao_vi_pham_lane_oto:
                    draw_text(frame, text + " warning", font_scale=0.5,
                              pos=(int(box.xyxy[0][0]), int(y)),
                              text_color_bg=(0, 0, 0))
                    print("tọa độ xe máy vi phạm : ", box.xyxy[0])
                    # cắt hình ảnh xe máy
                    # cropped_frame = frame[round(y, 1) - 100:round(y + h, 2) + 100,
                    #                 round(x, 1) - 100: round(x + w, 1) + 100]

                    # Cắt hình làn ô tô
                    # cropped_frame = frame[int((3 * frame.shape[0]) / 10):int((8 * frame.shape[0]) / 10),
                    #                 6 * int(frame.shape[1] / 10):int(frame.shape[1])]
                    if filterData:
                        stt_m += 1
                        imageMotorViolate(frame, int((2 * frame.shape[0]) / 10),
                                          int((8 * frame.shape[0]) / 10), 2 * int(frame.shape[1] / 10),
                                          int(frame.shape[1]), stt_m)
                        stt_BB_m = dataBienBan_M + str(stt_m) + '.pdf'
                        frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                        # Tạo tệp tạm thời và lưu ảnh PIL vào đó
                        temp_image = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
                        frame_pil.save(temp_image.name)
                        # create(cls)
                        createBB.bienBanNopPhat(examBB,
                                                temp_image.name,
                                                "F:/python_project/data_xe_may_vi_pham/ " + str(
                                                    stt_m) + '.jpg',
                                                stt_BB_m)
                        temp_image.close()

                        # cv2.imwrite("F:\python_project\data_xe_may_vi_pham\ " + str(count) + ".xe_may_lan_lan.jpg",
                        #             cropped_frame)
                        # frame = cv2.putText(frame, cls + " warning", org, font, fontScale, (0, 0, 255),
                        #                     2, cv2.LINE_AA)
                else:
                    draw_text(frame, text, font_scale=0.5,
                              pos=(int(x), int(y)),
                              text_color=(255, 255, 255), text_color_bg=(78, 235, 133))
                    # frame = cv2.putText(frame, text, org, font, fontScale,
                    #                     generate_random_color(int(cls)), 2,
                    #                     cv2.LINE_AA)
            if cls == 0 or cls == 3 or cls == 4:
                if canh_bao_vi_pham_lane_xe_may:
                    draw_text(frame, text + " warning", font_scale=0.5,
                              pos=(int(x), int(y)),
                              text_color_bg=(0, 0, 0))
                    # Cắt hình làn ô tô
                    if filterData and id not in array_car_filter:
                        array_car_filter.append(id)
                        stt_ctb += 1
                        cropped_frame = frame[
                                        int((3 * frame.shape[0]) / 10):int((8 * frame.shape[0]) / 10),
                                        6 * int(frame.shape[1] / 10):int(frame.shape[1])]
                        imageCTBViolate(frame, int((2 * frame.shape[0]) / 10),
                                        int((8 * frame.shape[0]) / 10), 0 * int(frame.shape[1] / 10),
                                        6 *
                                        int(frame.shape[1] / 10), stt_ctb)

                        stt_BB_CTB = dataBienBan_CTB + str(stt_ctb) + '.pdf'
                        frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                        # Tạo tệp tạm thời và lưu ảnh PIL vào đó
                        temp_image = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
                        frame_pil.save(temp_image.name)
                        # create(cls)
                        createBB.bienBanNopPhat(examBB,
                                                temp_image.name,
                                                "F:/python_project/data_oto_vi_pham/ " + str(
                                                    stt_ctb) + '.jpg',
                                                stt_BB_CTB)
                        temp_image.close()
                else:
                    draw_text(frame, text, font_scale=0.5,
                              pos=(int(x), int(y)),
                              text_color=(255, 255, 255), text_color_bg=(77, 229, 26))

        # muốn lấy 5/10 phần của height tính từ trên xuống
        start_point = (0, int((2 * frame.shape[0]) / 10))
        # vẽ hết chiều rộng và chiểu cao lấy 9/10
        end_point = (int(frame.shape[1]), int((8 * frame.shape[0]) / 10))
        color = (255, 0, 0)

        # vẽ ra cái ROI
        image = cv2.rectangle(frame, start_point, end_point, color, 2)

        # scale_percent = 30
        # width = int(image.shape[1] * scale_percent / 100)
        # height = int(image.shape[0] * scale_percent / 100)
        # dim = (width, height)

        # resize Image
        # resize = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow("Roi ", frame)
        cv2.waitKey(1)
        # yield image
