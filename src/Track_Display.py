import cv2
from picamera2 import Picamera2
import libcamera
from adafruit_servokit import ServoKit
import time

def track_display(dispW=640, dispH=480, step=1, model_path='../models/haarcascade_frontalface_default.xml', output_path='./static/image/output.jpeg'):
    """摄像头视频采集与人脸检测"""
    # 初始化伺服电机控制
    kit = ServoKit(channels=16)
    pan, tilt = 90, 90
    kit.servo[0].angle = pan
    kit.servo[1].angle = tilt
    
    temp, temp1, temp2, temp3, temp4 = 0, 0, 0, 0, 0
    
    # 人脸检测模型加载
    face_cascade = cv2.CascadeClassifier(model_path)
    
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
        while True:
            frame = picamera.capture_array()
            frame[..., [0, 2]] = frame[..., [2, 0]]  # B 和 R 通道交换
            
            # 转换为灰度图
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 15)
            
            # 人脸检测与伺服控制
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                Xcent, Ycent = x + w / 2, y + h / 2
                
                pan = max(0, min(180, pan))
                tilt = max(0, min(180, tilt))
                
                if (Xcent - dispW / 2) >= 35:
                    pan -= step
                else:
                    temp1 = 1
                
                if (Xcent - dispW / 2) <= -35:
                    pan += step
                else:
                    temp2 = 1
                
                if (Ycent - dispH / 2) >= 35:
                    tilt += step
                else:
                    temp3 = 1
                
                if (Ycent - dispH / 2) <= -35:
                    tilt -= step
                else:
                    temp4 = 1
                
                if temp1 == 1 and temp2 == 1 and temp3 == 1 and temp4 == 1:
                    temp = 1
                
                if temp == 1:
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    print("拍摄中～")
                    cv2.imwrite(output_path, frame)
                    print("图片拍摄完成！")
                    break
                
                kit.servo[0].angle = pan
                kit.servo[1].angle = tilt
                
            if temp == 1:
                time.sleep(0.5)
                break
            else:
                temp1, temp2, temp3, temp4 = 0, 0, 0, 0
                
            # 显示图像
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.imwrite("./static/image/temp.jpeg", frame)
            
            # 按 'q' 退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        # 释放资源
        picamera.stop()
        cv2.destroyAllWindows()

# 调用函数
if __name__ == "__main__":
    track_display()
