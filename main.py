import Track_Display
import Face_Recognition
try:
    print("Track_Display开启")
    Track_Display.Track_Display()
    print("Track_Display结束")

    print("Face_Recognition开启")
    print("请输入您的姓名：")
    mainname = input()
    Face_Recognition.main(mainname)
    print("Face_Recognition结束")
    
except KeyboardInterrupt:
    exit()
