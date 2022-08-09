# Training model YOLOv3, YOLOv4, YOLOv4-tiny and YOLOv5s
## 1. YOLOv3, YOLOv4 and YOLOv4-tiny
### 1.1 Change file cfg
- YOLOv3: yolov3-custom.cfg
- YOLOv4: yolov4-custom.cfg
- YOLOv4-tiny: yolov4-tiny-custom.cfg
#### Edit parameters: 
- classes = 1
- fillter = 18
- max_batches = 6000
- steps = 4800, 5400
- width = height = 416
### 1.2 Change Makefile
- GPU = 1
- CUDNN = 1
- OPENCV = 1
### 1.3 Data 
Up load data and split train:test:validation file. 
### 1.4 Run file (.ipynb) YOLOv3_TRAIN, YOLOv4_TRAIN and YOLOV4tiny_TRAIN 
## 2. YOLOv5s
### 2.1 Create custom_model.yaml
- Clone yolov5 in pytorch
- pip install -r requirements.txt
#### Copy model yolov5s.yaml and change parameters: 
- nc : 1 
- names : ["QR"] 
### 2.2 Create custom_data.yaml
#### Copy yolov5/data/coco128.yaml and change parameters:
- change train: ../yolov5/data/train_data/images/train/ to my_train_data_path
- change val: ../yolov5/data/train_data/images/val/ to my_val_data_path
- nc : 1
- names : ["QR"]
### 2.3 RUN file (.ipynb) YOLOv5_TRAIN