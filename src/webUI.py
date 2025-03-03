from flask import Flask, render_template, request, redirect, url_for
import threading
import time
import Track_Display

app = Flask(__name__)
isStart = False

# 首页路由
@app.route('/')
def home():
    lang = request.args.get('lang', 'zh')  # 获取URL中的语言参数，默认为中文
    return render_template('home.html', lang=lang)



# 关于页面路由
@app.route('/about')
def about():
    lang = request.args.get('lang', 'zh')  # 获取URL中的语言参数，默认为中文
    return render_template('about.html', lang=lang)

@app.route('/introduction')
def introduction():
    lang = request.args.get('lang', 'zh')  # 获取URL中的语言参数，默认为中文
    return render_template('introduction.html', lang=lang)

@app.route('/face')
def face():
    global isStart
    lang = request.args.get('lang', 'zh')
    if isStart == False:
        tread = threading.Thread(target=Track_Display.track_display)
        tread.start()
        isStart = True
    
    return render_template('faceRecognition.html', lang=lang)

if __name__ == '__main__':
    # 启动Flask服务并监听所有可用的IP地址，这样在局域网中其他设备可以访问
    app.run(host='0.0.0.0', port=5000, debug=True)
