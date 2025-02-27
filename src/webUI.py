from flask import Flask, render_template

app = Flask(__name__)

# 首页路由，返回完整的 HTML 页面
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
