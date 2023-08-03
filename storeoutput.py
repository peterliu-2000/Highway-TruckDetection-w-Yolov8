import cv2
import os
import shutil

def initialize_output_video(video):
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = video.get(cv2.CAP_PROP_FPS)

    folder = 'results'
    directory = os.getcwd()
    folder_path = os.path.join(directory, folder)

    if os.path.exists(folder_path):
        print(folder_path)
        shutil.rmtree(folder_path)

    os.mkdir(folder_path)
    print(f'Folder {folder} created at {folder_path}')

    video_name = 'result.mp4'
    video_path = os.path.join(folder_path, video_name)
    video_codec = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(video_path, video_codec, fps, (frame_width,frame_height))

    return output_video



