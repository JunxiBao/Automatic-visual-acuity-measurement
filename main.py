import cv2
from picamera2 import Picamera2
import libcamera
from adafruit_servokit import ServoKit
import threading
import time

step = 1
# 初始化伺服电机控制
kit = ServoKit(channels=16)

# 初始伺服角度
pan = 90
tilt = 90
kit.servo[0].angle = pan
kit.servo[1].angle = tilt

# 摄像头分辨率
dispW, dispH = 640, 480

# 人脸检测模型加载
face_cascade = cv2.CascadeClassifier('./source/haarcascade_frontalface_default.xml')
#//eye_cascade = cv2.CascadeClassifier('./source/haarcascade_eye.xml')

# 标志位用于控制线程退出
running = True

def Video_display():
    """摄像头视频采集与人脸检测"""
    global pan, tilt, running

    # 初始化摄像头
    picamera = Picamera2()
    config = picamera.create_preview_configuration(
        main={"format": 'RGB888', "size": (dispW, dispH)},
        raw={"format": "SRGGB12", "size": (1920, 1080)}
    )
    config["transform"] = libcamera.Transform(hflip=1, vflip=1)
    picamera.configure(config)
    picamera.start()

    try:
        while running:
            # 捕获帧
            frame = picamera.capture_array()
            frame[..., [0, 2]] = frame[..., [2, 0]]  # B 和 R 通道交换

            # 转换为灰度图
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 10)

            # 人脸检测与伺服控制
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                Xcent = x + w / 2
                Ycent = y + h / 2
                

                # 限制伺服角度范围
                pan = max(0, min(180, pan))
                tilt = max(0, min(180, tilt))

                if (Xcent - dispW / 2) >=35:
                   pan -=  step

                if (Xcent - dispW / 2) <=-35:
                   pan +=  step

                if (Ycent - dispH / 2) >= 35:
                   tilt +=  step

                if (Ycent - dispH / 2) <= -35:
                   tilt -=  step

                # 设置伺服角度
                kit.servo[0].angle = pan
                kit.servo[1].angle = tilt


            # 显示图像
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.imshow("Camera Output", frame)

            # 按 'q' 退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                running = False
                break
    finally:
        # 释放资源
        picamera.stop()
        cv2.destroyAllWindows()

# 启动线程运行视频显示
t = threading.Thread(target=Video_display)
t.start()

# 主程序运行，等待线程退出
try:
    while running:
        time.sleep(0.1)
except KeyboardInterrupt:
    running = False
    t.join()
