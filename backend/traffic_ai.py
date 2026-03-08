from ultralytics import YOLO
import cv2
import numpy as np


model = YOLO("models/yolov8m.pt")


def read_video_frame(video_path, frame_index):

    cap = cv2.VideoCapture(video_path)

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

    ret, frame = cap.read()

    cap.release()

    return frame, frame_index+5, 0


def analyze_frame(frame, conf=0.35):

    results = model.predict(frame, conf=conf, verbose=False)

    r = results[0]

    count = len(r.boxes)

    density = min(count/20,1)

    if density>0.7:
        label="HIGH"
    elif density>0.35:
        label="MEDIUM"
    else:
        label="LOW"

    return {
        "vehicle_count":count,
        "density_score":density,
        "density_label":label,
        "annotated_frame":r.plot()
    }