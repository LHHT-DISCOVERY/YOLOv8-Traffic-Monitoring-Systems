# import cv2
# import numpy as np
# import pandas as pd
# from ultralytics import YOLO
#
# from tracker import *
#
# model = YOLO('best_new/best.pt')
#
#
# def RGB(event, x, y, flags, param):
#     if event == cv2.EVENT_MOUSEMOVE:
#         colorsBGR = [x, y]
#         print(colorsBGR)
#
#
# cv2.namedWindow('RGB')
# cv2.setMouseCallback('RGB', RGB)
#
# cap = cv2.VideoCapture("F:/python_project/Videos/main.mp4")
#
# my_file = open("coco.txt", "r")
# data = my_file.read()
# class_list = data.split("\n")
# print(class_list)
# tracker = Tracker()
# area = [(0, 100), (480, 100), (480, 300), (0, 300)]
# while True:
#
#     ret, frame = cap.read()
#     if not ret:
#         break
#     # frame = cv2.resize(frame, (1020, 500))
#
#     results = model.predict(frame)
#     a = results[0].boxes.boxes
#     px = pd.DataFrame(a).astype("float")
#     list = []
#     for index, row in px.iterrows():
#         x1 = int(row[0])
#         y1 = int(row[1])
#         x2 = int(row[2])
#         y2 = int(row[3])
#         d = int(row[5])
#         c = class_list[d]
#         if "car" in c:
#             list.append([x1, y1, x2, y2])
#         box_id = tracker.update(list)
#         for bbox in box_id:
#             x3, y3, x4, y4, id = bbox;
#             cx = int(x3 + x4) // 2
#             cy = int(y3 + y4) // 2
#             results = cv2.pointPolygonTest(np.array(area, np.int32), ((cx, cy)), False)
#             if results >= 0:
#                 cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)
#                 cv2.putText(frame, str(id), (x3, y3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#     cv2.polylines(frame, [np.array(area, np.int32)], True, (255, 255, 0), 3)
#     # frame = cv2.rectangle(frame, (0, int((2 * frame.shape[0]) / 10)),
#     #                       (int(frame.shape[1]), int((8 * frame.shape[0]) / 10)), (0, 0, 255), 1)
#     cv2.imshow("RGB", frame)
#     if cv2.waitKey(1) & 0xFF == 27:
#         break
# cap.release()
# cv2.destroyAllWindows()

import pandas as pd

import createBB
from testLane import *
from tracker import *

model = YOLO("YolWeights/best.pt")

cap = cv2.VideoCapture("F:/python_project/Videos/main.mp4")

stt_m = 0
stt_ctb = 0

my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")
print("dđ", class_list)

examBB = createBB.infoObject()
dataBienBan_M = 'F:/python_project/BienBanNopPhatXeMay/ '
dataBienBan_CTB = 'F:/python_project/BienBanNopPhatXeOTo/ '

count = 0
tracker = Tracker()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    # frame = cv2.resize(frame, (1020, 500))
    # frame = cv2.flip(frame, 1)
    results = model(frame)
    font = cv2.FONT_HERSHEY_SIMPLEX
    # print("ht",results)
    a = results[0].boxes.boxes
    px = pd.DataFrame(a).astype("float")
    list = []

    for index, row in px.iterrows():
        print(row)
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]
        print("tọa độ trước cập nhật : ", x1, y1, x2, y2)
        if d == 0:
            list.append([x1, y1, x2, y2, c])
        elif d == 1:
            list.append([x1, y1, x2, y2, c])
        elif d == 2:
            list.append([x1, y1, x2, y2, c])
        elif d == 3:
            list.append([x1, y1, x2, y2, c])
        elif d == 4:
            list.append([x1, y1, x2, y2, c])

    bbox_id = tracker.update(list)

    for bbox in bbox_id:
        x4, y4, x5, y5, c, id = bbox
        print("tọa độ sau cập nhật : ", x4, y4, x5, y5)
        # cv2.rectangle(frame, (x4, y4), (x5, y5), (0, 255, 255), 2)
        # cv2.putText(frame, c + str(id), (x5, y5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        # lấy tên class tương ứng bounding box trong model đã custom
        # print("Class : ", box.cls)

        # lấy tọa độ của bounding box đối tượng (x0y0 , x1y1)
        # print("xyxy : ", box.xyxy[0])

        # Lấy độ chính xác của bounding box đối tượng
        # print("Độ chính xác : ", box.conf)

        # print("ID------------------- ", box.id)
        font = cv2.FONT_HERSHEY_SIMPLEX

        # box.xyxy trả về ma trận 2 chiều dạng [[x0, y0 , x1 ,y1]]
        # đó là tọa độ bounding box
        # print("box.xyxy", box.xyxy)
        # org (Tọa độ cần vẽ lên bounding box (x,y) )
        # thêm int để lấy số nguyên (nghĩa là lấy x0 , y0 để vẽ lên bounding box)
        org = (int(x4), int(y4))

        # fontScale (Độ lớn của chữ)
        fontScale = 0.5

        # Blue color in RGB (Màu sắc của chữ)
        color = ()

        # Line thickness of 2px (Độ dày của chữ )
        thickness = 2

        # Lấy tọa độ bounding box
        # x = int(box.xyxy[0][0])
        # y = int(box.xyxy[0][1])
        # w = int(box.xyxy[0][2])
        # h = int(box.xyxy[0][3])

        text = str(str(id) + ":" + c)

        #####################################################################
        # Xe OTO vi pham lane XE MAY
        start_line_motor = (0 * int(frame.shape[1] / 10), int((2 * frame.shape[0] / 10)))
        # 11/20 = 5.5 / 10
        end_line_motor = (11 * int(frame.shape[1] / 20), int(8 * frame.shape[0] / 10))
        canh_bao_vi_pham_lane_xe_may = start_line_motor[0] < x4 < end_line_motor[0] and \
                                       start_line_motor[1] < y4 < end_line_motor[1]
        #####################################################################

        # ##################################################################
        # Xe máy vi pham lane OTO
        # lane xe ô tô (trục y phải khớp với vùng roi)
        # trục x lấy 6/10 , trục y lấy 3/10
        start_line_car = (6 * int(frame.shape[1] / 10), int((2 * frame.shape[0] / 10)))

        # lấy từ 6/10 đến hết trục X , trục y lấy 8/10
        end_line_car = (int(frame.shape[1]), int(8 * frame.shape[0] / 10))

        canh_bao_vi_pham_lane_oto = start_line_car[0] < x4 < end_line_car[0] and \
                                    start_line_car[1] < y4 < end_line_car[1]
        # filterDataViolate(frame, (0, int(5 * frame.shape[0] / 10)),
        #                   (int(frame.shape[1]), int(55 * frame.shape[0] / 10)))
        center_x = (x4 + x5) // 2
        center_y = (y4 + y5) // 2
        filterData = 0 <= center_x <= (int(frame.shape[1])) and int(
            5 * frame.shape[0] / 10) <= center_y <= int(
            52 * frame.shape[0] / 100)
        #####################################################################

        # vẽ ra vùng lane xe máy và oto
        # image = cv2.rectangle(frame, start_line_car, end_line_car
        #                       , (0, 0, 255), thickness)
        image = cv2.rectangle(frame, start_line_motor, end_line_motor
                              , (255, 0, 255), thickness)

        # xét vùng roi theo trục Y
        if int((2 * frame.shape[0]) / 10) < int(y4) < int((8 * frame.shape[0]) / 10):
            cv2.rectangle(frame, (x4, y4), (x5, y5), (36, 255, 12), 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
            if d == 1:
                if canh_bao_vi_pham_lane_oto:
                    draw_text(frame, text + " warning", font_scale=0.5,
                              pos=(int(x4), int(y4)),
                              text_color_bg=(0, 0, 0))
                    # print("tọa độ xe máy vi phạm : ", box.xyxy[0])
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
                        # create(box.cls[0])
                        createBB.bienBanNopPhat(examBB,
                                                temp_image.name,
                                                "F:/python_project/data_xe_may_vi_pham/ " + str(
                                                    stt_m) + '.jpg',
                                                stt_BB_m)
                        temp_image.close()

                        # cv2.imwrite("F:\python_project\data_xe_may_vi_pham\ " + str(count) + ".xe_may_lan_lan.jpg",
                        #             cropped_frame)
                        # frame = cv2.putText(frame, name[box.cls[0]] + " warning", org, font, fontScale, (0, 0, 255),
                        #                     thickness, cv2.LINE_AA)
                else:
                    draw_text(frame, text, font_scale=0.5,
                              pos=(int(x4), int(y4)),
                              text_color=(255, 255, 255), text_color_bg=(78, 235, 133))
                    # frame = cv2.putText(frame, text, org, font, fontScale,
                    #                     generate_random_color(int(box.cls[0])), thickness,
                    #                     cv2.LINE_AA)
            elif d == 0 or d == 3 or d == 4:
                if canh_bao_vi_pham_lane_xe_may:
                    draw_text(frame, text + " warning", font_scale=0.5,
                              pos=(int(x4), int(y4)),
                              text_color_bg=(0, 0, 0))
                    # Cắt hình làn ô tô
                    if filterData:
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
                        # create(box.cls[0])
                        createBB.bienBanNopPhat(examBB,
                                                temp_image.name,
                                                "F:/python_project/data_oto_vi_pham/ " + str(
                                                    stt_ctb) + '.jpg',
                                                stt_BB_CTB)
                        temp_image.close()
                else:
                    draw_text(frame, text, font_scale=0.5,
                              pos=(int(x4), int(y4)),
                              text_color=(255, 255, 255), text_color_bg=(77, 229, 26))

        # muốn lấy 5/10 phần của height tính từ trên xuống
        start_point = (0, int((2 * frame.shape[0]) / 10))
        # vẽ hết chiều rộng và chiểu cao lấy 9/10
        end_point = (int(frame.shape[1]), int((8 * frame.shape[0]) / 10))
        color = (255, 0, 0)
        thickness = 2

        # vẽ ra cái ROI
        image = cv2.rectangle(frame, start_point, end_point, color, thickness)

        # scale_percent = 30
        # width = int(image.shape[1] * scale_percent / 100)
        # height = int(image.shape[0] * scale_percent / 100)
        # dim = (width, height)

        # resize Image
        # resize = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow("Rois ", image)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
