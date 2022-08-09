import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import logging.handlers
import queue
from pathlib import Path
from typing import List, NamedTuple
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
import os
import av
from aiortc.contrib.media import MediaPlayer
from streamlit_webrtc import (
    AudioProcessorBase,
    ClientSettings,
    VideoProcessorBase,
    WebRtcMode,
    webrtc_streamer,
)
from Decode_QR import *

HERE = Path(__file__).parent

logger = logging.getLogger(__name__)

WEBRTC_CLIENT_SETTINGS = ClientSettings(
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={
        "video": True,
        "audio": False,
    },
)
def scan_image(my_img):
    """
    Show the display result scan QR code with Image
    """
    st.set_option('deprecation.showPyplotGlobalUse', False)
    column1, column2 = st.columns(2)
    column1.subheader("Input image")
    st.text("")
    plt.figure(figsize=(16, 16))
    plt.imshow(my_img)
    column1.pyplot(use_column_width=True)
    newImage = np.array(my_img.convert('RGB'))
    img, contents = decode_image(newImage)
    st.text("")
    column2.subheader("Output image")
    st.text("")
    plt.figure(figsize=(15, 15))
    plt.imshow(img)
    column2.pyplot(use_column_width=True)
    if st.checkbox("Show the result scan QR code", value=True):
        if contents == []:
            st.success("Unable to decode QR code")
        for content in contents:
            st.success(content)
    st.markdown(
            "DESIGN BY NGUYEN XUAN VINH - contact: vinhnx20@gmail.com"
    )


def scan_video(video):
    """
    Show the display result scan QR code with Video
    """
    vid = cv2.VideoCapture(video)
    ret = True
    frame = st.empty()
    result = st.empty()
    lst = []
    count = 0
    while ret:
        ret, frame_raw = vid.read()
        count = count + 1
        if ret and count%3==0:
            count = 0
            img, contents = decode_camera(frame_raw)
            frame.image(img, channels="BGR")
            if contents == []:
                result.success("Unable to decode QR code")
            for content in contents:
                result.success(content)
                if  content not in lst:
                    lst.append(content)
    st.subheader("Show all result scan QR code with video")
    for j in lst:
        st.success(j)
    st.markdown(
            "DESIGN BY NGUYEN XUAN VINH - contact: vinhnx20@gmail.com"
    )

def scan_camera():
    """
    Show the display result scan QR code with Camera
    """
    class yolov4(VideoProcessorBase):
        confidence_threshold: float
        result_queue: "queue.Queue"
        def __init__(self) -> None:
            self.result_queue = queue.Queue()   

        def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
            image = frame.to_ndarray(format="bgr24")
            annotated_image, results = decode_camera(image)
            content = []
            for result in results:
                if result not in content:
                    content.append(result)
            self.result_queue.put(content)
            return av.VideoFrame.from_ndarray(annotated_image, format="bgr24")

    webrtc_ctx = webrtc_streamer(
        key="object-detection",
        mode=WebRtcMode.SENDRECV,
        client_settings=WEBRTC_CLIENT_SETTINGS,
        video_processor_factory=yolov4,
        async_processing=True,
    )
    confidence_threshold = 0.5
    if webrtc_ctx.video_processor:
        webrtc_ctx.video_processor.confidence_threshold = confidence_threshold
    if st.checkbox("Show the result scan QR code", value=True):
        if webrtc_ctx.state.playing:
            labels_placeholder = st.empty()
            while True:
                if webrtc_ctx.video_processor:
                    try:
                        results = webrtc_ctx.video_processor.result_queue.get(
                            timeout=1.0
                        )
                    except queue.Empty:
                        results = None
                    labels_placeholder.table(results)
                else:
                    break
    st.markdown(
            "DESIGN BY NGUYEN XUAN VINH - contact: vinhnx20@gmail.com"
    )


def main():
    """
    It is a main function with 4 option for user
    """
    #st.set_page_config(layout="wide")
    st.image("https://tuyensinh.uit.edu.vn/sites/default/files/uploads/files/dai-hoc-uit-3.jpg",  use_column_width=True)
    st.markdown("<h1 style='text-align: center; color: red;'>DEMO SCAN QR CODE APP - UIT</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;' > Sinh vien: 18521655 - Nguyen Xuan Vinh </h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;' > GVHD: ThS. Pham The Son </h3>", unsafe_allow_html=True)    
    with st.sidebar:
        st.header(
            "Yon can scan QR code. Click option:")
        choice = st.radio("", ("See an illustration", "Scan QR code with Image", "Scan QR code with Video", "Scan QR code with Camera"))
        st.markdown(
            "contact: vinhnx20@gmail.com"
        )
    if choice == "Scan QR code with Image":
        image_file = st.file_uploader("Upload", type=['jpg', 'png', 'jpeg', 'svg', 'webp', 'jfif'])
        if image_file is not None:
            my_img = Image.open(image_file)
            scan_image(my_img)
    elif choice == "Scan QR code with Video":
        uploaded_video = st.file_uploader("Choose video", type=["mp4", "mov"])
        if uploaded_video is not None: 
            vid = uploaded_video.name
            with open(vid, mode='wb') as f:
                f.write(uploaded_video.read())
            scan_video(vid)
    elif choice == "Scan QR code with Camera":
        scan_camera()
    elif choice == "See an illustration":
        my_img = Image.open("images/qr.jpg")
        scan_image(my_img)

def app_media_constraints():
    """ A sample to configure MediaStreamConstraints object """
    frame_rate = 5
    WEBRTC_CLIENT_SETTINGS.update(
        ClientSettings(
            media_stream_constraints={
                "video": {"frameRate": {"ideal": frame_rate}},
            },
        )
    )
    webrtc_streamer(
        key="media-constraints",
        mode=WebRtcMode.SENDRECV,
        client_settings=WEBRTC_CLIENT_SETTINGS,
    )
    st.write(f"The frame rate is set as {frame_rate}")

if __name__ == '__main__':
    DEBUG = os.environ.get("DEBUG", "false").lower() not in ["false", "no", "0"]
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)7s from %(name)s in %(pathname)s:%(lineno)d: "
               "%(message)s",
        force=True,
    )
    logger.setLevel(level=logging.DEBUG if DEBUG else logging.INFO)
    st_webrtc_logger = logging.getLogger("streamlit_webrtc")
    st_webrtc_logger.setLevel(logging.DEBUG)
    fsevents_logger = logging.getLogger("fsevents")
    fsevents_logger.setLevel(logging.WARNING)

    main()