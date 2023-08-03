from ultralytics import YOLO
import cv2
import pandas as pd
import tqdm
from frameprocessing import *

#Model&Video
path = 'test-vid.mp4'
model = YOLO('myWeights.pt')

#alterables
scale_percent = 100

#line_property
line_color = (255,0,0)
line_thickness = 2

#box_property
box_color = (1,1,1)
box_thickness = 2

text_color = (255,255,255)
video = cv2.VideoCapture(path)
class_list = model.model.names
classes = class_list.keys()
vehicles_counter = dict.fromkeys(classes, 0)
print(vehicles_counter)

while True:
    ret, frame = video.read()

    if ret:
        frame_height, frame_width, num_channels = frame.shape

        result = model.predict(frame, conf=0.6, iou=0.6)
        boxes = result[0].boxes.xyxy.cpu().numpy()
        conf = result[0].boxes.conf.cpu().numpy()
        classes = result[0].boxes.cls.cpu().numpy().astype(int)
        labels = [class_list[i] for i in classes]
        result_list = list(zip(classes, labels, conf, boxes))

        flag = 'marker'

        for run_result in result_list:
            print(flag)
            id, label, conf, box = run_result
            xmin = int(box[0])
            ymin = int(box[1])
            xmax = int(box[2])
            ymax = int(box[3])

            center_x, center_y = int((xmax + xmin)/2), int((ymax + ymin)/2)
            line_left = (0, int(frame_height*0.75))
            line_right = (int(frame_width), int(frame_height*0.75))
            offset = 8


            cv2.line(frame, line_left, line_right, line_color, line_thickness)
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), box_color, box_thickness)

            text_print = '{label} {con:.2f}'.format(label=label, con=conf)
            text_location = (xmin, ymin-10)
            labelSize, baseLine = cv2.getTextSize(text_print, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            #textbox
            cv2.rectangle(frame
                          , (xmin, ymin-labelSize[1]-10)
                          , (xmin+ labelSize[0], ymin+baseLine-10)
                          , box_color, cv2.FILLED)
            cv2.putText(frame, text_print, text_location
                        , cv2.FONT_HERSHEY_SIMPLEX, 1
                        , text_color, 2, cv2.LINE_AA)

            if (center_y < (offset+line_left[1])) and (center_y > (line_left[1]-offset)):
                vehicles_counter[id] += 1

            cv2.putText(frame, 'Monitored Vehicles', (int(frame_width*0.7),30), fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                fontScale=1, color=(255, 0, 0),thickness=1)

            counter_txt = [f'{class_list[id]}:{number}' for id, number in vehicles_counter.items()]
            pos = 40
            for txt in range(len(class_list)):
                pos += 30
                cv2.putText(frame, counter_txt[txt], (int(frame_width*0.7), pos), fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                fontScale=1, color=(255, 0, 0),thickness=1)

            frame = resize_frame(frame, scale_percent)

            cv2.imshow('rec',frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        break






