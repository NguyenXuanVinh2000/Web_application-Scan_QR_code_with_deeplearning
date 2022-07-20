from server_detection import *
import cv2
from keras.preprocessing.image import img_to_array
import numpy as np

def preprocessing_image_input(image):
    """
    Process input image in YOLO
    """
    data = cv2.resize(image, (416, 416))
    im_arr = img_to_array(data, )
    im_arr = data / 255.0
    im_arr = np.expand_dims(im_arr, axis=0)
    return im_arr

def convert_bbox_yolov3_and_yolov4(boxes, image):
    """
    The function convert bounding box with YOLOv3 and YOLOv4
    """
    Width = image.shape[1]
    Height = image.shape[0]
    i = 1
    lst = []
    confi=[]
    for i in range(int(len(boxes) / 5)):
        ymin = (boxes[i * 5 + 0] * Height) 
        xmin = (boxes[i * 5 + 1] * Width) 
        ymax = (boxes[i * 5 + 2] * Height)
        xmax = (boxes[i * 5 + 3] * Width)
        score = boxes[i * 5 + 4]
        x = int(xmin)
        y = int(ymin)
        w = int(xmax - x)
        h = int(ymax - y)
        ls = [x, y, w, h]
        lst.append(ls)
        confi.append(score)
    return lst, confi

def convert_bbox_yolov5(boxes, image):
    """
    The function convert bounding box with YOLOv5
    """
    W = image.shape[1]
    H = image.shape[0]
    i = 1
    lst = []
    confi=[]
    for i in range(int(len(boxes) / 6)):
        x = boxes[i * 6 + 0] 
        y = boxes[i * 6 + 1] 
        w = boxes[i * 6 + 2]
        h = boxes[i * 6 + 3]
        score = boxes[i * 6 + 4]
        xyxy = [x - w / 2, y - h / 2, x + w / 2, y + h / 2]
        xmin = int(max(1,(xyxy[0] * W)))
        ymin = int(max(1,(xyxy[1] * H)))
        xmax = int(min(H,(xyxy[2] * W)))
        ymax = int(min(W,(xyxy[3] * H)))
        x = int(xmin)
        y = int(ymin)
        w = int(xmax - x)
        h = int(ymax - y)
        ls = [x, y, w, h]
        lst.append(ls)
        confi.append(score)
    return lst, confi
