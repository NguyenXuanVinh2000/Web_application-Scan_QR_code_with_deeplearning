## Install
	install docker
	install nvidia-gpu
	pip install -r requirements.txt
## Build Image by : 
	docker build -t qr_detection_gpu:1.15.0-gpu .
## Run Server by :
	docker-compose up