import cv2
import os
import shutil

"""
def draw_frame(model,frame,conf, class_list, vehicles_counter, show_counter):

    frame_height, frame_width, num_channels = frame.shape
    result = model.track(frame, conf=conf, iou=0.5, persist=True, tracker="bytetrack.yaml")
    boxes = result[0].boxes.xyxy.cpu().numpy()
    conf = result[0].boxes.conf.cpu().numpy()
    counts = result[0].boxes.id
    classes = result[0].boxes.cls.cpu().numpy().astype(int)
    labels = [class_list[i] for i in classes]
    result_list = list(zip(classes, labels, conf, boxes))

    if counts is not None:
        counts = counts.cpu().numpy().astype(int)
        for i in range(len(counts)):
            vehicles_counter[classes[i]] = counts[i]

    box_thickness = 2
    text_color = (255, 255, 255)

    #TODO: Update box_colors if new classes are added (currently 2)
    box_colors = [(123, 45, 234), (99, 3, 39)]
    box_color_dict = {}
    for id in range(0,len(class_list)):
        box_color_dict[id] = box_colors[id]

    for run_result in result_list:
        id, label, conf, box = run_result
        box_color = box_color_dict[id]
        xmin = int(box[0])
        ymin = int(box[1])
        xmax = int(box[2])
        ymax = int(box[3])

        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), box_color, box_thickness)

        count = vehicles_counter[id]
        text_print = '{count} {label} {con:.2f}'.format(count=count, label=label, con=conf)
        text_location = (xmin, ymin - 10)
        labelSize, baseLine = cv2.getTextSize(text_print, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        cv2.rectangle(frame
                      , (xmin, ymin - labelSize[1] - 10)
                      , (xmin + labelSize[0], ymin + baseLine - 10)
                      , box_color, cv2.FILLED)
        cv2.putText(frame, text_print, text_location
                    , cv2.FONT_HERSHEY_SIMPLEX, 1
                    , text_color, 2, cv2.LINE_AA)

    if show_counter:
        cv2.putText(frame, 'Monitored Vehicles', (int(frame_width * 0.7), 30), fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                    fontScale=1, color=(255, 0, 0), thickness=1)

        counter_txt = [f'{class_list[class_id]}:{class_label}' for class_id, class_label in
                       vehicles_counter.items()]
        pos = 40
        for txt in range(len(counter_txt)):
            pos += 30
            cv2.putText(frame, counter_txt[txt], (int(frame_width * 0.7), pos), fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                        fontScale=1, color=(255, 0, 0), thickness=1)

    return frame
"""



def draw_frame(model,frame,conf, class_list, vehicles_counter,show_counter,frame_num,frame_folder_path):



    result = model.predict(frame, conf=conf, iou=0.6)
    frame_height, frame_width, num_channels = frame.shape
    boxes = result[0].boxes.xyxy.cpu().numpy()
    conf = result[0].boxes.conf.cpu().numpy()
    classes = result[0].boxes.cls.cpu().numpy().astype(int)
    labels = [class_list[i] for i in classes]
    result_list = list(zip(classes, labels, conf, boxes))
    to_store = False

    line_color = (255, 0, 0)
    line_thickness = 2
    box_thickness = 2
    text_color = (255, 255, 255)

    #TODO: Line position & offset value might be adjusted depending on different camera angles
    line_left = (0, int(frame_height * 0.6))
    line_right = (int(frame_width), int(frame_height * 0.6))
    offset = int(frame_height/120)

    #TODO: Update box_colors if new classes are added (currently 2)
    box_colors = [(123, 45, 234), (99, 3, 39)]
    box_color_dict = {}
    for id in range(0,len(class_list)):
        box_color_dict[id] = box_colors[id]

    for run_result in result_list:
        id, label, conf, box = run_result
        box_color = box_color_dict[id]
        xmin = int(box[0])
        ymin = int(box[1])
        xmax = int(box[2])
        ymax = int(box[3])

        #TODO: adjusted_y value can be tweaked
        adjusted_y = int((ymax + ymin) / 2)
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), box_color, box_thickness)

        text_print = '{label} {con:.2f}'.format(label=label, con=conf)
        text_location = (xmin, ymin - 10)
        labelSize, baseLine = cv2.getTextSize(text_print, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        cv2.rectangle(frame
                      , (xmin, ymin - labelSize[1] - 10)
                      , (xmin + labelSize[0], ymin + baseLine - 10)
                      , box_color, cv2.FILLED)
        cv2.putText(frame, text_print, text_location
                    , cv2.FONT_HERSHEY_SIMPLEX, 1
                    , text_color, 2, cv2.LINE_AA)

        if (adjusted_y < (offset + line_left[1])) and (adjusted_y > (line_left[1] - offset)):
            vehicles_counter[id] += 1
            to_store = True

    if show_counter:
        draw_counter(frame,line_left,line_right,line_color,line_thickness,frame_width, class_list,vehicles_counter)

    if to_store:
        store_frame(frame, frame_num, frame_folder_path)

    return frame

def draw_counter(frame,line_left,line_right,line_color,line_thickness, frame_width, class_list, vehicles_counter):
    cv2.line(frame, line_left, line_right, line_color, line_thickness)
    cv2.putText(frame, 'Monitored Vehicles', (int(frame_width * 0.7), 30), fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                fontScale=1, color=(255, 0, 0), thickness=1)

    counter_txt = [f'{class_list[class_id]}:{class_label}' for class_id, class_label in
                   vehicles_counter.items()]
    pos = 40
    for txt in range(len(counter_txt)):
        pos += 30
        cv2.putText(frame, counter_txt[txt], (int(frame_width * 0.7), pos), fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                    fontScale=1, color=(255, 0, 0), thickness=1)

    return None

def make_store_frame_folder():
    folder = 'detected_frames'
    directory = os.getcwd()
    folder_path = os.path.join(directory, folder)

    if os.path.exists(folder_path):
        print(folder_path)
        shutil.rmtree(folder_path)

    os.mkdir(folder_path)
    print(f'Folder {folder} created at {folder_path}')
    return folder_path

def store_frame(frame, frame_num, folder_path):

    frame_name = f'frame {frame_num}.png'
    print(frame_name)
    frame_path = os.path.join(folder_path, frame_name)
    cv2.imwrite(frame_path, frame)

    return None

def resize_frame(frame, scale_percent) :
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

    return resized
