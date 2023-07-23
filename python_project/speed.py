# import time
#
# import cv2
# import pandas as pd
# from ultralytics import YOLO
#
# from tracker import *
#
# model = YOLO('YoloWeights/best.pt')
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
# cap = cv2.VideoCapture('Videos/test4.mp4')
#
# my_file = open("coco.txt", "r")
# data = my_file.read()
# class_list_car = data.split("\n")
# class_list_motorcycle = data.split("\n")
# class_list_truck = data.split("\n")
# class_list_bus = data.split("\n")
# print("List car : ")
# print(data)
# print("---------------------")
#
# count = 0
#
# tracker = Tracker()
#
# cy1 = 300
# cy2 = 430
#
# offset = 6
#
# vh_down = {}
# counter = []
#
# vh_up = {}
# counter1 = []
#
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
#     count += 1
#     if count % 3 != 0:
#         continue
#     frame = cv2.resize(frame, (1020, 500))
#
#     results = model.predict(frame)
#     #   print(results)
#     a = results[0].boxes.boxes
#     px = pd.DataFrame(a).astype("float")
#     #    print(px)
#     list_car = []
#     list_motor = []
#     list_truck = []
#     list_bus = []
#
#     for index, row in px.iterrows():
#         #        print(row)
#         x1 = int(row[0])
#         y1 = int(row[1])
#         x2 = int(row[2])
#         y2 = int(row[3])
#         d = int(row[5])
#         c = class_list_car[d]
#         print(c)
#         m = class_list_motorcycle[d]
#         tr = class_list_truck[d]
#         b = class_list_bus[d]
#         if 'car' in c:
#             list_car.append([x1, y1, x2, y2])
#         if "motorcycle" in m:
#             list_motor.append([x1, y1, x2, y2])
#         if "truck" in c:
#             list_truck.append([x1, y1, x2, y2])
#         if "bus" in c:
#             list_bus.append([x1, y1, x2, y2])
#     bbox_id = tracker.update(list_motor)
#     print("-------------")
#     print(bbox_id)
#     print("-------------")
#     for bbox in bbox_id:
#         x3, y3, x4, y4, id = bbox
#         cx = int(x3 + x4) // 2
#         cy = int(y3 + y4) // 2
#
#         cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)
#
#         if cy1 < (cy + offset) and cy1 > (cy - offset):
#             vh_down[id] = time.time()
#         if id in vh_down:
#
#             if cy2 < (cy + offset) and cy2 > (cy - offset):
#                 elapsed_time = time.time() - vh_down[id]
#                 if counter.count(id) == 0:
#                     counter.append(id)
#                     distance = 10  # meters
#                     a_speed_ms = distance / elapsed_time
#                     a_speed_kh = a_speed_ms * 3.6
#                     cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
#                     cv2.putText(frame, str(id), (x3, y3), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)
#                     cv2.putText(frame, str(int(a_speed_kh)) + 'Km/h', (x4, y4), cv2.FONT_HERSHEY_COMPLEX, 0.8,
#                                 (0, 255, 255), 2)
#
#         #####going UP#####
#         if cy2 < (cy + offset) and cy2 > (cy - offset):
#             vh_up[id] = time.time()
#         if id in vh_up:
#
#             if cy1 < (cy + offset) and cy1 > (cy - offset):
#                 elapsed1_time = time.time() - vh_up[id]
#
#                 if counter1.count(id) == 0:
#                     counter1.append(id)
#                     distance1 = 10  # meters
#                     a_speed_ms1 = distance1 / elapsed1_time
#                     a_speed_kh1 = a_speed_ms1 * 3.6
#                     cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
#                     cv2.putText(frame, str(id), (x3, y3), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)
#                     cv2.putText(frame, str(int(a_speed_kh1)) + 'Km/h', (x4, y4), cv2.FONT_HERSHEY_COMPLEX, 0.8,
#                                 (0, 255, 255), 2)
#
#     cv2.line(frame, (0, cy1), (950, cy1), (255, 255, 255), 1)
#
#     cv2.putText(frame, ('L1'), (600, 320), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
#
#     cv2.line(frame, (0, cy2), (927, cy2), (255, 255, 255), 1)
#
#     cv2.putText(frame, ('L2'), (182, 367), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
#     d = (len(counter))
#     u = (len(counter1))
#     cv2.putText(frame, ('goingdown:-') + str(d), (60, 90), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
#
#     cv2.putText(frame, ('goingup:-') + str(u), (60, 130), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
#     cv2.imshow("RGB", frame)
#     if cv2.waitKey(1) & 0xFF == 27:
#         break
# cap.release()
# cv2.destroyAllWindows()
# if __name__ == '__main__':
#     data = {"id_name": str(1),
#             "date_violate": str(56)}
#     print(data['id_name'], data['date_violate'])
