from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

if __name__ == '__main__':
    # 启动Flask服务并监听所有可用的IP地址，这样在局域网中其他设备可以访问
    app.run(host='0.0.0.0', port=5000)
