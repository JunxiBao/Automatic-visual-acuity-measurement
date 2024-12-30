import Track_Display
import MyFaceRecognation
try:
    print("Track_Display开启")
    Track_Display.Track_Display()
    print("Track_Display结束")
    MyFaceRecognation.main()

except KeyboardInterrupt:
    exit()
