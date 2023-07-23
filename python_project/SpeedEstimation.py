# import os
#
# import cv2
# from ultralytics import YOLO
#
#
# def draw_text(img, text,
#               font=cv2.FONT_HERSHEY_SIMPLEX,
#               pos=(0, 0),
#               font_scale=1.5,
#               font_thickness=1,
#               text_color=(0, 0, 255),
#               text_color_bg=(0, 0, 0)
#               ):
#     x, y = pos
#     text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
#     text_w, text_h = text_size
#     cv2.rectangle(img, pos, (x + text_w, y + text_h), text_color_bg, -1)
#     cv2.putText(img, text, (x, y + text_h), font, font_scale, text_color, font_thickness)
#
#     return text_size
#
#
# def generate_random_color(a):
#     if a == 1:
#         return (0, 255, 0)
#     else:
#         return (255, 50, 0)
#
#
# def color_violate():
#     return (0, 0, 255)
#
#
# def draw_roi(frame, xyxy, name, cls, conf):
#     output_folder = 'F:\python_project\data_xe_may_vi_pham'
#     os.makedirs(output_folder, exist_ok=True)
#     output_filename = 'cropped_video.mp4'
#     output_path = os.path.join(output_folder, output_filename)
#
#     # Khởi tạo VideoWriter
#     fps = 30.0  # Số khung hình trên giây (frame per second)
#     frame_size = (frame.shape[1], frame.shape[0])  # Kích thước khung hình (chiều rộng, chiều cao)
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Định dạng video (ở đây là MP4)
#     video_writer = cv2.VideoWriter(output_path, fourcc, fps, frame_size)
#     print("shape", frame.shape)  # (height, width, channels)
#
#     # font
#     font = cv2.FONT_HERSHEY_SIMPLEX
#
#     # xyxy trả về ma trận 2 chiều dạng [[x0, y0 , x1 ,y1]]
#     # đó là tọa độ bounding box
#     print("xyxy", xyxy)
#     # org (Tọa độ cần vẽ lên bounding box (x,y) )
#     # thêm int để lấy số nguyên (nghĩa là lấy x0 , y0 để vẽ lên bounding box)
#     org = (int(xyxy[0][0]), int(xyxy[0][1]))
#
#     # fontScale (Độ lớn của chữ)
#     fontScale = 0.5
#
#     # Blue color in RGB (Màu sắc của chữ)
#     color = ()
#
#     # Line thickness of 2px (Độ dày của chữ )
#     thickness = 1
#
#     # Lấy tọa độ bounding box
#     x = int(xyxy[0][0])
#     y = int(xyxy[0][1])
#     w = int(xyxy[0][2])
#     h = int(xyxy[0][3])
#     count = 0
#
#     # xét vùng roi theo trục Y
#     if int(xyxy[0][1]) > int((3 * frame.shape[0]) / 10) and int(xyxy[0][1]) < int((8 * frame.shape[0]) / 10):
#         text = str(name[cls[0]] + " ") + str(round(conf[0], 2))
#         # lane xe ô tô (trục y phải khớp với vùng roi)
#         # trục x lấy 6/10 , trục y lấy 3/10
#         start_line_car = (6 * int(frame.shape[1] / 10), int((3 * frame.shape[0] / 10)))
#
#         # lấy hết trục X , trục y lấy 8/10
#         end_line_car = (int(frame.shape[1]), int(8 * frame.shape[0] / 10))
#
#         # vẽ ra vùng lane
#         # image = cv2.rectangle(frame, start_line_car, end_line_car
#         #                       , (0, 0, 255), thickness)
#         canh_bao_vi_pham_lane_oto = start_line_car[0] < xyxy[0][0] < end_line_car[0] and start_line_car[1] < xyxy[0][
#             1] < end_line_car[1]
#
#         if cls[0] == 1:
#             if canh_bao_vi_pham_lane_oto:
#                 draw_text(frame, name[cls[0]] + " warning", font_scale=0.5, pos=(int(xyxy[0][0]), int(xyxy[0][1])),
#                           text_color_bg=(0, 0, 0))
#                 print("tọa độ xe máy vi phạm : ", xyxy[0])
#                 # cắt hình ảnh xe máy
#                 # cropped_frame = frame[round(y, 1) - 100:round(y + h, 2) + 100,
#                 #                 round(x, 1) - 100: round(x + w, 1) + 100]
#
#                 # Cắt hình làn ô tô
#                 cropped_frame = frame[int((3 * frame.shape[0]) / 10):int((8 * frame.shape[0]) / 10),
#                                 6 * int(frame.shape[1] / 10):int(frame.shape[1])]
#                 video_writer.write(cropped_frame)
#
#                 # cv2.imwrite("F:\python_project\data_xe_may_vi_pham\ " + str(count) + ".xe_may_lan_lan.jpg",
#                 #             cropped_frame)
#                 count += 1
#                 # frame = cv2.putText(frame, name[cls[0]] + " warning", org, font, fontScale, (0, 0, 255),
#                 #                     thickness, cv2.LINE_AA)
#             else:
#                 draw_text(frame, text, font_scale=0.5, pos=(int(xyxy[0][0]), int(xyxy[0][1])),
#                           text_color=(255, 255, 255), text_color_bg=(255, 0, 255))
#                 # frame = cv2.putText(frame, text, org, font, fontScale,
#                 #                     generate_random_color(int(cls[0])), thickness,
#                 #                     cv2.LINE_AA)
#         # using cv2.putText(frame) method
#         else:
#             draw_text(frame, text, font_scale=0.5, pos=(int(xyxy[0][0]), int(xyxy[0][1])),
#                       text_color=(255, 255, 255), text_color_bg=(100, 200, 0))
#             # frame = cv2.putText(frame, text, org, font, fontScale,
#             #                     generate_random_color(int(cls[0])), thickness,
#             #                     cv2.LINE_AA)
#             # cv2.rectangle(frame, (X0, Y0, X1, Y1), (0, 255, 0), 2)
#
#     # muốn lấy 5/10 phần của height tính từ trên xuống
#     start_point = (0, int((3 * frame.shape[0]) / 10))
#     # vẽ hết chiều rộng và chiểu cao lấy 9/10
#     end_point = (int(frame.shape[1]), int((8 * frame.shape[0]) / 10))
#     color = (255, 0, 0)
#     thickness = 2
#
#     # vẽ ra cái ROI
#     image = cv2.rectangle(frame, start_point, end_point, color, thickness)
#
#     # scale_percent = 30
#     # width = int(image.shape[1] * scale_percent / 100)
#     # height = int(image.shape[0] * scale_percent / 100)
#     # dim = (width, height)
#
#     # resize Image
#     # resize = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
#     video_writer.release()
#     cv2.imshow("Roi ", image)
#
#
# if __name__ == '__main__':
#     output_folder = 'F:\python_project\data_xe_may_vi_pham'
#     os.makedirs(output_folder, exist_ok=True)
#     output_filename = 'cropped_video_2.mp4'
#     output_path = os.path.join(output_folder, output_filename)
#
#     # Khởi tạo VideoWriter
#     fps = 30.0  # Số khung hình trên giây (frame per second)
#     frame_size = (300, 300)  # Kích thước khung hình (chiều rộng, chiều cao)
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Định dạng video (ở đây là MP4)
#     video_writer = cv2.VideoWriter(output_path, fourcc, fps, frame_size)
#     cap = cv2.VideoCapture("F:/python_project/Videos/lane.mp4")
#     model = YOLO('YoloWeights/best.pt')
#     # results = model.track(source="Videos/test4.mp4", show=True, stream=True)
#     while cap.isOpened():
#         success, frame = cap.read()
#         if success:
#             #  Dự đoán
#             results = model(frame)
#
#             # lấy ra frame sau khi đc gắn nhãn
#             annotated_frame = results[0].plot()
#
#             # lấy kích thước (height , width , _ )
#             # print("kích thước frame : ", annotated_frame.shape)
#
#             # Hiển thị lên
#             # cv2.imshow("Display ", annotated_frame)
#
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#             # results = model.track(source="Videos/test4.mp4", show=True, tracker="bytetrack.yaml", stream=True)
#             for result in results:
#                 boxes = result.boxes.numpy()
#
#                 # Lấy tên class
#                 name = result.names
#
#                 # lấy tất cả các thông số trong một list tọa độ các đối tượng (x0 ,y0, x1, y1, )
#                 # print("list 1 ", boxes.xyxy)
#                 list_2 = []
#
#                 # Lấy tất các các thông số của nhiều đối tượng (x0, y0 , x1 , y1 , id ,độ chính xác , loại class)
#                 # print("Boxes ", boxes)
#
#                 for box in boxes:
#                     # lấy tên class tương ứng bounding box trong model đã custom
#                     # print("Class : ", box.cls)
#
#                     # lấy tọa độ của bounding box đối tượng (x0y0 , x1y1)
#                     print("xyxy : ", box.xyxy[0])
#
#                     # Lấy độ chính xác của bounding box đối tượng
#                     # print("Độ chính xác : ", box.conf)
#
#                     print("ID------------------- ", box.id)
#                     font = cv2.FONT_HERSHEY_SIMPLEX
#
#                     # box.xyxy trả về ma trận 2 chiều dạng [[x0, y0 , x1 ,y1]]
#                     # đó là tọa độ bounding box
#                     print("box.xyxy", box.xyxy)
#                     # org (Tọa độ cần vẽ lên bounding box (x,y) )
#                     # thêm int để lấy số nguyên (nghĩa là lấy x0 , y0 để vẽ lên bounding box)
#                     org = (int(box.xyxy[0][0]), int(box.xyxy[0][1]))
#
#                     # fontScale (Độ lớn của chữ)
#                     fontScale = 0.5
#
#                     # Blue color in RGB (Màu sắc của chữ)
#                     color = ()
#
#                     # Line thickness of 2px (Độ dày của chữ )
#                     thickness = 1
#
#                     # Lấy tọa độ bounding box
#                     x = int(box.xyxy[0][0])
#                     y = int(box.xyxy[0][1])
#                     w = int(box.xyxy[0][2])
#                     h = int(box.xyxy[0][3])
#                     count = 0
#
#                     # xét vùng roi theo trục Y
#                     if int(box.xyxy[0][1]) > int((3 * frame.shape[0]) / 10) and int(box.xyxy[0][1]) < int(
#                             (8 * frame.shape[0]) / 10):
#                         text = str(name[box.cls[0]] + " ") + str(round(box.conf[0], 2))
#                         # lane xe ô tô (trục y phải khớp với vùng roi)
#                         # trục x lấy 6/10 , trục y lấy 3/10
#                         start_line_car = (6 * int(frame.shape[1] / 10), int((3 * frame.shape[0] / 10)))
#
#                         # lấy hết trục X , trục y lấy 8/10
#                         end_line_car = (int(frame.shape[1]), int(8 * frame.shape[0] / 10))
#
#                         # vẽ ra vùng lane
#                         # image = cv2.rectangle(frame, start_line_car, end_line_car
#                         #                       , (0, 0, 255), thickness)
#                         canh_bao_vi_pham_lane_oto = start_line_car[0] < box.xyxy[0][0] < end_line_car[0] and \
#                                                     start_line_car[1] < box.xyxy[0][
#                                                         1] < end_line_car[1]
#
#                         if box.cls[0] == 1:
#                             if canh_bao_vi_pham_lane_oto:
#                                 draw_text(frame, name[box.cls[0]] + " warning", font_scale=0.5,
#                                           pos=(int(box.xyxy[0][0]), int(box.xyxy[0][1])),
#                                           text_color_bg=(0, 0, 0))
#                                 print("tọa độ xe máy vi phạm : ", box.xyxy[0])
#                                 # cắt hình ảnh xe máy
#                                 # cropped_frame = frame[round(y, 1) - 100:round(y + h, 2) + 100,
#                                 #                 round(x, 1) - 100: round(x + w, 1) + 100]
#
#                                 # Cắt hình làn ô tô
#                                 cropped_frame = frame[int((3 * frame.shape[0]) / 10):int((8 * frame.shape[0]) / 10),
#                                                 6 * int(frame.shape[1] / 10):int(frame.shape[1])]
#                                 video_writer.write(cropped_frame)
#
#                                 # cv2.imwrite("F:\python_project\data_xe_may_vi_pham\ " + str(count) + ".xe_may_lan_lan.jpg",
#                                 #             cropped_frame)
#                                 count += 1
#                                 # frame = cv2.putText(frame, name[box.cls[0]] + " warning", org, font, fontScale, (0, 0, 255),
#                                 #                     thickness, cv2.LINE_AA)
#                             else:
#                                 draw_text(frame, text, font_scale=0.5, pos=(int(box.xyxy[0][0]), int(box.xyxy[0][1])),
#                                           text_color=(255, 255, 255), text_color_bg=(255, 0, 255))
#                                 # frame = cv2.putText(frame, text, org, font, fontScale,
#                                 #                     generate_random_color(int(box.cls[0])), thickness,
#                                 #                     cv2.LINE_AA)
#                         # using cv2.putText(frame) method
#                         else:
#                             draw_text(frame, text, font_scale=0.5, pos=(int(box.xyxy[0][0]), int(box.xyxy[0][1])),
#                                       text_color=(255, 255, 255), text_color_bg=(100, 200, 0))
#                             # frame = cv2.putText(frame, text, org, font, fontScale,
#                             #                     generate_random_color(int(box.cls[0])), thickness,
#                             #                     cv2.LINE_AA)
#                             # cv2.rectangle(frame, (X0, Y0, X1, Y1), (0, 255, 0), 2)
#
#                     # muốn lấy 5/10 phần của height tính từ trên xuống
#                     start_point = (0, int((3 * frame.shape[0]) / 10))
#                     # vẽ hết chiều rộng và chiểu cao lấy 9/10
#                     end_point = (int(frame.shape[1]), int((8 * frame.shape[0]) / 10))
#                     color = (255, 0, 0)
#                     thickness = 2
#
#                     # vẽ ra cái ROI
#                     image = cv2.rectangle(frame, start_point, end_point, color, thickness)
#
#                     # scale_percent = 30
#                     # width = int(image.shape[1] * scale_percent / 100)
#                     # height = int(image.shape[0] * scale_percent / 100)
#                     # dim = (width, height)
#
#                     # resize Image
#                     # resize = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
#                     video_writer.release()
#                     cv2.imshow("Roi ", image)
#                     # draw_roi(frame, box.xyxy, name, box.cls, box.conf)
#         else:
#             break
#
# cap.release()
# cv2.destroyAllWindows()
