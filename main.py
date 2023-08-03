from ultralytics import YOLO
from frameprocessing import *
from createwindow import *
from storeoutput import *

window = create_window('GreenMono')

run_model = False
model = YOLO('myWeights.pt')
class_list = model.model.names
classes = class_list.keys()
vehicles_counter = dict.fromkeys(classes, 0)

while True:
    event, values = window.read(timeout=0)

    if event == "运行":
        if not run_model:
            scale_percent = int(values['scale_percent'])
            pathway = values['video']
            video = cv2.VideoCapture(pathway)
            output_video = initialize_output_video(video)
            frame_folder_path = make_store_frame_folder()
            frame_num = 0
            run_model = True

    elif event in ('停止','取消', sg.WIN_CLOSED):
        vehicles_counter = dict.fromkeys(classes, 0)
        if run_model:
            run_model = False
            video.release()
            output_video.release()
            if event != sg.WIN_CLOSED:
                window['display'].update(filename='')
        if event in (sg.WIN_CLOSED, '取消'): break

    if run_model:
        ret, frame = video.read()
        conf = values['confidence'] / 10
        frame_num += 1

        if ret:
            show_counter = values['counter']
            labeled_frame = draw_frame(model,frame,conf, class_list,vehicles_counter,show_counter,frame_num,frame_folder_path)
            output_video.write(labeled_frame)
            resized_frame = resize_frame(labeled_frame, scale_percent)
            imgbytes = cv2.imencode('.png', resized_frame)[1].tobytes()
            window['display'].update(data=imgbytes)

        else:
            video.release()
            output_video.release()
            run_model = False
            vehicles_counter = dict.fromkeys(classes, 0)

window.close()






