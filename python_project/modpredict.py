# import cv2
# from ultralytics import YOLO
#
# model = YOLO('YoloWeights/yolov8n.pt')
# results = model.track(source="Videos/test4.mp4", show=True, stream=True)
# for result, im0, image_detect in results:
#     boxes = result[0].boxes.numpy()
#     print("name ", result.names)
#     for box in boxes:
#         print("xyxy", box.xyxy)
#         print("boxID", box.id)
#     cv2.imshow("jhk", image_detect)
#     cv2.waitKey(1)  # 1 millisecond
