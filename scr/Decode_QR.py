from pyzbar import pyzbar
import cv2
from preprocessing import *
import time
from title_web import *

def pyzbar_decode(img):
    """
    Decode QR code with framework Pyzbar
    """
    content = ""
    barcodes = pyzbar.decode(img, symbols=[pyzbar.ZBarSymbol.QRCODE])
    for barcode in barcodes:
        barcodeData = barcode.data.decode("utf-8")
        content = "{}".format(barcodeData)
        if content != "":
            if "http" in content:
                content = content + "\t Title website: " + title(content)
            return content
    return content

def cv2_decode(img):
    """
    Decode QR code with framework Opencv-python QRCodeDetector
    """
    detector = cv2.QRCodeDetector()
    data, vertices_array, _ = detector.detectAndDecode(img)
    if vertices_array is not None:
        return data
    else: return ""

def decode_image(newImage):
    """
    The function is decode QR code in Image
    """
    items = []
    img = cv2.cvtColor(newImage, 1)
    imgs = preprocessing_image_input(img)
    #YOLOv5
    # result_yolov5 = grpc_client_request_YOLOv5(imgs)
    # boxes, confidences = convert_bbox_yolov5(result_yolov5, img)
    #YOLOv3, YOLOv4
    result = grpc_client_request_image(imgs)
    boxes, confidences = convert_bbox_yolov3_and_yolov4(result, img)

    score_threshold = 0.7
    nms_threshold = 0.6
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold, nms_threshold)
    img_2 = img.copy()
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            if x<0: x=1
            if y<0: y=1
            if w<0: w=1
            if h<0: h=1
            crop_img = img_2[y:y+h, x:x+w]
            # Detection QR code
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # Decode QR code by pyzbar
            content = pyzbar_decode(crop_img)
            # Decode QR code by opencv-python
            # content = cv2_decode(crop_img)
            if content != "" and content not in items:
                items.append(content)
    return img, items

def decode_camera(newImage):
    """
    The function is decode QR code in Camera
    """
    start_time = time.time()
    items = []
    img = cv2.cvtColor(newImage, 1)
    imgs = preprocessing_image_input(img)
    #YOLOv5
    # result_yolov5 = grpc_client_request_YOLOv5(imgs)
    # boxes, confidences = convert_bbox_yolov5(result_yolov5, img)
    #YOLOv3, YOLOv4
    result = grpc_client_request_camera(imgs)
    boxes, confidences = convert_bbox_yolov3_and_yolov4(result, img)
    score_threshold = 0.7
    nms_threshold = 0.6
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold, nms_threshold)
    img_2 = img.copy()
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            if x<0: x=1
            if y<0: y=1
            if w<0: w=1
            if h<0: h=1
            crop_img = img_2[y:y+h, x:x+w]
            # Detection QR code
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # Decode QR code by pyzbar
            content = pyzbar_decode(crop_img)
            # Decode QR code by opencv-python
            #content = cv2_decode(crop_img)
            if content != "" and content not in items:
                items.append(content)
    end_time = time.time()
    FPS = 1/(end_time-start_time)
    fps = "FPS: " + str(round(FPS))
    cv2.putText(img, fps, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return img, items