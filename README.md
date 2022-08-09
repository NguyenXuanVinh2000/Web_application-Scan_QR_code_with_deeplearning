# *The project scan QR code by YOLOvX and pyzbar*

# I. INSTRUCTION FOLDER 

## 1. SCAN_QR_CODE_WITH_DEEP_LEARNING
### 1.1 SETUP:
	- Folder and file settings for the application
### 1.2 SOURCE:
	- Code Preprocessing data
	- Code Training models
	- Code Evaluation models
## 2. BAOCAO:
### 2.1 ABS: Slide report and video demo
### 2.2 DOC: file .doc
### 2.3 PDF: file .pdf
## 3. SOFT:
	- Source demo app scan QR code with deep learning models
# II. APPLICATION
## 1. Install :
	install docker
	install nvidia-gpu
### In folder ../SCAN_QR_CODE_WITH_DEEP_LEARNING/SETUP/app
	pip install -r requirements.txt
## 2. Build Image by : 
### In folder ../SCAN_QR_CODE_WITH_DEEP_LEARNING/SETUP/app
	docker build -t qr_detection_gpu:1.15.0-gpu .
## 3. Run Server by :
### In folder ../SCAN_QR_CODE_WITH_DEEP_LEARNING/SETUP/app
	docker-compose up
## 4. Open app in browser
### In folder ../SOFT/app
	python3 streamlit app.py
# III. Note
	The application install in OS ubuntu
# IV. Information author:
	Name			: 	Nguyen Xuan Vinh
	Phone Number		: 	0965004314
	Email			: 	18521655@gm.uit.edu.vn
						vinhnx20@gmail.com
