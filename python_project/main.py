import gc
import os
import time
from datetime import timedelta
import os
import shutil
import cv2
import supervision as sv
from IPython import display
from ultralytics import YOLO


def get_video_info(video_path):
    # Extracting information about the video
    video_info = sv.VideoInfo.from_video_path(video_path)
    width, height, fps, total_frames = video_info.width, video_info.height, video_info.fps, video_info.total_frames

    # Calculating the length of the video by dividing the total number of frames by the frame rate and rounding to the nearest second
    video_length = timedelta(seconds=round(total_frames / fps))

    # Print out the video resolution, fps, and length u
    print(f"\033[1mVideo Resolution:\033[0m ({width}, {height})")
    print(f"\033[1mFPS:\033[0m {fps}")
    print(f"\033[1mLength:\033[0m {video_length}")


def vehicle_count(source_path, destination_path, line_start, line_end):
    # Load the pre-trained YOLO model
    model = YOLO('YoloWeights/best.pt')

    # Create two points from the line_start and line_end coordinates
    line_start = sv.Point(line_start[0], line_start[1])
    line_end = sv.Point(line_end[0], line_end[1])

    # Create a line zone object from the two points
    line_counter = sv.LineZone(line_start, line_end)

    # Create a line zone annotator object with specific thickness and text scale
    line_annotator = sv.LineZoneAnnotator(thickness=2,
                                          text_thickness=1,
                                          text_scale=0.5)

    # Create a box annotator object with specific thickness and text scale
    box_annotator = sv.BoxAnnotator(thickness=1,
                                    text_thickness=1,
                                    text_scale=0.5)

    # Extract information about the video from the given source path
    video_info = sv.VideoInfo.from_video_path(source_path)

    # Create a video out path by combining the destination path and the video name
    video_name = os.path.splitext(os.path.basename(source_path))[0] + ".mp4"
    video_out_path = os.path.join(destination_path, video_name)

    # Create a video writer object for the output video
    video_out = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(*'mp4v'), video_info.fps,
                                (video_info.width, video_info.height))

    # Loop over each frame of the video and perform object detection and tracking
    for result in model.track(source=source_path, tracker='bytetrack.yaml', show=True, stream=True, agnostic_nms=True):

        # Get the original frame from the detection result
        frame = result.orig_img

        # Convert the YOLO detection results to a Detections object
        detections = sv.Detections.from_yolov8(result)

        # If the detections have an associated ID, set the tracker ID in the Detections object
        if result.boxes.id is not None:
            detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)

        # Filter the detections to only include classes 2 (cars) and 7 (trucks)
        detections = detections[(detections.class_id == 2) | (detections.class_id == 7)]

        # Generate labels for the detections, including the tracker ID, class name, and confidence
        labels = [f"{tracker_id} {model.model.names[class_id]} {confidence:0.2f}"
                  for _, confidence, class_id, tracker_id
                  in detections]

        # Trigger the line counter to count any detections that intersect the line zone
        line_counter.trigger(detections)

        # Annotate the frame with the line zone and any intersecting detections
        line_annotator.annotate(frame, line_counter)

        # Annotate the frame with bounding boxes and labels for all detections
        frame = box_annotator.annotate(scene=frame,
                                       detections=detections,
                                       labels=labels)
        # Write the annotated frame to the output video
        video_out.write(frame)

    # Release the video writer and clear the Jupyter Notebook output
    video_out.release()
    display.clear_output()


async def ClearMemory():
    while True:
        gc.collect()
        time.sleep(10)


def main():
    model = YOLO('YoloWeights/best.pt')
    # ClearMemory()
    for results in model.track(source="Videos/test4.mp4", imgsz=320, show=True, stream=True):
        frame = results.orig_img

        cv2.imshow('yolov8', frame)

        if (cv2.waitKey(30) == 27):
            break


if __name__ == '__main__':

    # model = YOLO('YoloWeights/best.pt')
    # results = model.predict(source="F:\YOLOv8-Traffic-Monitoring-System\DATA_DATN\Validation", save=True)
    # for r, i in results:
    #     print("frame :" + i)
    #     print(" : " + r)
    main()
    # get_video_info("Videos/test4.mp4")
    # vehicle_count(source_path="Videos/test1.mp4", destination_path="Data/Example Results", line_start=(337, 391),
    #               line_end=(917, 387))
