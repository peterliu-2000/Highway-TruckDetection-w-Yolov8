import torch
from ultralytics import YOLO
import cv2

model = YOLO('best.pt')
model.track('long-test-vid.mp4', conf=0.6, iou=0.5, device='mps')