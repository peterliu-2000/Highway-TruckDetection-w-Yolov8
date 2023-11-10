## Overview ##

This simple program utilizes the advanced object recognition algorithm Yolov8 and was developed as a individual project during my research internship at Shanxi Intelligence Transport research institute at Shanxi, China in July - August 2023. The program's functions entail the following:

* Able to recognize small and large(six-wheel) tarpaulin-covered trucks, big container trucks and oil tankers in live feed or uploaded videos
* Able to _roughly_ count the number of each type of truck passed
* Store every frame where a vehicle of said type is detected, and stored the frame with timestamp
* Presented through a easily-guided user interface 

This Github and README.md file were created to both document what I accomplished, as well as serve as a reference for people who are using YOLO algorithm for similar purposes.

## Files ##

The project was programmed in Python 3.10 environment The main program is contained in _main.py_, and the rest of the Python files contain supporting functions and should be downloaded in the same pathway with main if one should use it. 

best.pt contains the neural network trained specifically for identifying large trucks/oil tanks in Shanxi highway.

## Methods ##

The main object recognition algorithm used is YOLOV-8 (You Only Look Once ver-8), developed as the newest in the Yolov series by Ultralytics team, and made public in Jan 2023. It is a one-stage (passing the frame only once) algorithm using end-to-end convolutional neural network, and it is known for its speed and accuracy in detecting and identifying object. More info on their original repo here: https://github.com/ultralytics/ultralytics

#### Training Data ####

The training image set was manually scraped from a series of surveillance video camera on a few highways in Shanxi Province; weather conditions are generally sunny and video is of high quality, with no visual obstructions. Some examples (contact peterzehan@gmail.com if you need the entire dataset)

<img src="https://github.com/peterliu-2000/Highway-TruckDetection-w-Yolov8/assets/136511104/0db72494-d395-4760-b148-83b8e2f56b5d" width="490" alt="Example 1">
<img src="https://github.com/peterliu-2000/Highway-TruckDetection-w-Yolov8/assets/136511104/138f4f54-57c8-4ceb-bace-1881299ddff6" width="432" alt="Example 2">

#### Image Annotation ####

The training image was annotated through Roboflow (https://roboflow.com/), which is nice as it's compatible with yolov8 algorithm, and very easy to import the annotated results in Python. The training image was split 7:2:1 into training, validation and testing. After annotation, I add two image-processing setps, which add random blockouts and range in exposures (-35% to +35%), to hopefully obtain a more robust neural network in the end. Eventually, the training set contains 1302 (434+868) frames, validation 124 frames, testing 62 frames

#### Model Training & Results ####

 Both Roboflow and YOLOV8 can be implemented easily in Python environment; the best.pt neural network is trained by the following code:

 <pre>
```python
  from ultralytics import YOLO
  from roboflow import Roboflow
  rf = Roboflow(api_key="your_api_key")
  project = rf.workspace("yolov7-dataset").project("-ddarz")
  dataset = project.version(1).download("yolov8")
  
  #Train the model from data
  !yolo task=detect mode=train model=yolov8s.pt data={dataset.location}/data.yaml epochs=25 imgsz=800 plots=True
  ![image](https://github.com/peterliu-2000/Highway-TruckDetection-w-Yolov8/assets/136511104/d3d190fe-448c-45a4-98ee-d889a36addc6)
```
</pre>

 Training with a GPU is much faster than using CPU. I used Google Colab where a free GPU was provided (~30 minutes for my training sets). I've set the training epochs to be 25, and it can be seen below that prediction errors (_box_loss_ and _class_loss_), as well as mAP50 stabilize after ~20 epochs:
 
<p align="center">
  <img width="700" alt="image" src="https://github.com/peterliu-2000/Highway-TruckDetection-w-Yolov8/assets/136511104/44d24521-c148-4692-bde9-7da31c5f5445">
</p>

 Precision-Recall curve and the confusion matrix both show good results; the only obvious shortcoming is the misclassification of background cars/trucks into one of the target truck class:

<p align="center">
  <img width="430" alt="image" src="https://github.com/peterliu-2000/Highway-TruckDetection-w-Yolov8/assets/136511104/4f00db21-f2ad-4b86-b327-323a02af4f2f">
  <img width="372" alt="image" src="https://github.com/peterliu-2000/Highway-TruckDetection-w-Yolov8/assets/136511104/d88f3bf9-60ea-45a7-9276-87fa4dff449f">
</p>

#### By-Frame Recognition & Vehicle Counting

Frame-by-frame recognition by YOLOV8 is faciliated by the OpenCV package in Python. The main program is contained in _main.py_; the file _frameprocess.py_ contains function that extracts the output information and annotate the bounding box and probability on the frame

In terms of counting, I developed a crude way of counting vehicles passed by specifying a rectangular region in the middle of the screen, with 1/75 of the full frame length, such that if a frame contains the mid-point of a predicted bounding box, that type of vehicle count is upped by one. However this is not an accurate way of accounting, since at times the same vehicle midpoint can be in more than one frames, or just happens to miss the frames; the 1/75 ratio was obtained through trial and error, and it can be tweaked for videos when camera angles, vehicles speed etc. are different.

<p align="center">
  <img width="650" alt="image" src="https://github.com/peterliu-2000/Highway-TruckDetection-w-Yolov8/assets/136511104/72415ba6-30c9-42d7-8c4a-ab7c47755b1d">
</p>

#### User Interface ####

Finally, PySimpleGUI package was used to create a easy-to-use user-interface, which allows user to specify the confidence threshold they want for the object detection among others.

#### Thoughts & Future Directions ####

* Currently most of the training images were scraped from surveillance cams with high resolution, and generally under very good weather conditions and with good visibility. The robustness of the neural network can potentially be improved by simply expanding the training set to include vehicles shot at various angles, and under different levels of visibility
* Currently the counting method is a rough one. Perhaps a better, more accurate method can be developed which is suitable for any scenario?
* I'm not sure if adding more vehicle categories would decrease the overall accuracy of YOLOV8 algorithm; can be explored in the future
* Currently YOLOV8 would scan the entire frame for designated vehicles. However for highway surveillance cams (which is what this project intended to be applied in), technically we can only focus on the bottom half area, as vehicles are closer to the area and have high predictive accuracy here. By eliminating the scanning of top half, we can potentially half the algorithm runtime as well








