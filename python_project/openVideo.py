import cv2

cropped_cap = cv2.VideoCapture("F:\python_project\data_xe_may_vi_pham\cropped_video_4.mp4")

while True:
    # Đọc frame từ video đã cắt
    ret, frame = cropped_cap.read()

    # Kiểm tra nếu không thể đọc frame
    if not ret:
        break

    # Hiển thị frame đã cắt
    cv2.imshow('Cropped Video Playback', frame)

    # Nhấn phím 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên của VideoCapture của video đã cắt
cropped_cap.release()
# import cv2
# import os
#
# def cut_and_display_video(input_path, output_folder, output_filename, x, y, width, height):
#     # Tạo đường dẫn đến video đích
#     output_path = os.path.join(output_folder, output_filename)
#
#     # Khởi tạo VideoWriter
#     fps = 30.0  # Số khung hình trên giây (frame per second)
#     frame_size = (width, height)  # Kích thước khung hình (chiều rộng, chiều cao)
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Định dạng video (ở đây là MP4)
#     video_writer = cv2.VideoWriter(output_path, fourcc, fps, frame_size)
#
#     # Đọc video nguồn
#     cap = cv2.VideoCapture(input_path)
#
#     while True:
#         # Đọc frame từ video nguồn
#         ret, frame = cap.read()
#
#         # Kiểm tra nếu không thể đọc frame
#         if not ret:
#             break
#
#         # Cắt vùng cắt từ frame
#         cropped_frame = frame[y:y+height, x:x+width]
#
#         # Ghi frame đã cắt vào video đích
#         video_writer.write(cropped_frame)
#
#         # Hiển thị frame đã cắt (tuỳ chọn)
#         cv2.imshow('Cropped Video', cropped_frame)
#
#         # Nhấn phím 'q' để thoát
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     # Giải phóng các tài nguyên của VideoWriter
#     video_writer.release()
#
#     # Đóng VideoCapture của video nguồn
#     cap.release()
#
#     # Mở và hiển thị video đã cắt
#     cropped_cap = cv2.VideoCapture(output_path)
#
#     while True:
#         # Đọc frame từ video đã cắt
#         ret, frame = cropped_cap.read()
#
#         # Kiểm tra nếu không thể đọc frame
#         if not ret:
#             break
#
#         # Hiển thị frame đã cắt
#         cv2.imshow('Cropped Video Playback', frame)
#
#         # Nhấn phím 'q' để thoát
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     # Giải phóng tài nguyên của VideoCapture của video đã cắt
#     cropped_cap.release()
#
#     # Đóng tất cả các cửa sổ hiển thị
#     cv2.destroyAllWindows()
#
#
# # Sử dụng hàm cut_and_display_video
# input_path = 'F:/python_project/Videos/lane.mp4'
# output_folder = 'F:\python_project\data_xe_may_vi_pham'
# output_filename = 'cropped_video_4.mp4'
# x = 100
# y = 100
# width = 200
# height = 200
# cut_and_display_video(input_path, output_folder, output_filename, x, y, width, height)
#
