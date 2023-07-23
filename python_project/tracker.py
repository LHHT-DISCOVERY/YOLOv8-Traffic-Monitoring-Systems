# import math
#
#
# class Tracker:
#     def __init__(self):
#         # Store the center positions of the objects
#         self.center_points = {}
#         # Keep the count of the IDs
#         # each time a new object id detected, the count will increase by one
#         self.id_count = 0
#
#     def update(self, objects_rect):
#         # Objects boxes and ids
#         objects_bbs_ids = []
#
#         # Get center point of new object
#         for rect in objects_rect:
#             x, y, w, h = rect
#             cx = (x  + w) // 2
#             cy = (y + h) // 2
#
#             # Find out if that object was detected already
#             same_object_detected = False
#             for id, pt in self.center_points.items():
#                 dist = math.hypot(cx - pt[0], cy - pt[1])
#
#                 if dist < 35:
#                     self.center_points[id] = (cx, cy)
#                     #                    print(self.center_points)
#                     objects_bbs_ids.append([x, y, w, h, id])
#                     same_object_detected = True
#                     break
#
#             # New object is detected we assign the ID to that object
#             if same_object_detected is False:
#                 self.center_points[self.id_count] = (cx, cy)
#                 objects_bbs_ids.append([x, y, w, h, self.id_count])
#                 self.id_count += 1
#
#         # Clean the dictionary by center points to remove IDS not used anymore
#         new_center_points = {}
#         for obj_bb_id in objects_bbs_ids:
#             _, _, _, _, object_id = obj_bb_id
#             center = self.center_points[object_id]
#             new_center_points[object_id] = center
#
#         # Update dictionary with IDs not used removed
#         self.center_points = new_center_points.copy()
#         return objects_bbs_ids

# async def ClearMemory():
#     while True:
#         gc.collect()
#         time.sleep(10)
#
# def main():
#     model = YOLO('best_new/best.pt')
#     ClearMemory()
#     for results in model.track(source="F:/python_project/Videos/main.mp4", imgsz=320, show=True, stream=True):
#         frame = results.orig_img
#
#         cv2.imshow('yolov8', frame)
#
#         if (cv2.waitKey(30)==27):
#             break
#
#
# if __name__ == '__main__':
#     main()
import math


class Tracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0

    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h, c = rect
            cx = (x + w) // 2
            cy = (y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 20:
                    self.center_points[id] = (cx, cy)
                    #                    print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, c, id])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, c, self.id_count])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids
