# 导入Flask类
from flask import Flask
from datetime import timedelta
from flask import render_template
from flask import request
import os
import re
from pyecharts import options as opts
from pyecharts.charts import Graph, Page
import xlrd
from create_echarts import CreateEcharts
from main import ChatBotGraph

# 实例化，可视为固定格式
app = Flask(__name__,template_folder=".")#将默认路径转化为当前文件所在路径


# 配置路由，当请求get.html时交由get_html()处理
@app.route('/index.html')
def get_html():
    # 使用render_template()方法重定向到templates文件夹下查找get.html文件
    return render_template('templates/index.html')

@app.route('/index1.html')
def get_html1():
    # 使用render_template()方法重定向到templates文件夹下查找get.html文件
    return render_template('templates/index1.html')

@app.route('/index2.html')
def get_html2():
    # 使用render_template()方法重定向到templates文件夹下查找get.html文件
    return render_template('templates/index2.html')


# 配置路由，当请求deal_request时交由deal_request()处理
# 默认处理get请求，我们通过methods参数指明也处理post请求
# 当然还可以直接指定methods = ['POST']只处理post请求, 这样下面就不需要if了
class JsCode:
    def __init__(self, js_code: str):
        self.js_code = "--x_x--0_0--" + js_code + "--x_x--0_0--"

    def replace(self, pattern: str, repl: str):
        self.js_code = re.sub(pattern, repl, self.js_code)
        return self
@app.route('/deal_question', methods = ['GET', 'POST'])
def deal_question():
    get_q = request.args.get("q", "")
    handler = ChatBotGraph()
    answer=handler.chat_main(get_q)
    return render_template("templates/index2.html", question=get_q,result=answer)
    #return answer


@app.route('/deal_request', methods = ['GET', 'POST'])
def deal_request():
    key_name = request.args.get("name", "")
    id= int(request.args.get("id", ""))
    url="templates//echarts//render"+str(id)+".html"
    searcher = CreateEcharts()
    if id>=1 and id<=111:
        searcher.create_disease(key_name,url)
    if id>=112 and id<=216:
        searcher.create_drug(key_name,url)
    if id>=217 and id<=589:
        searcher.create_symptom(key_name,url)

    return render_template(url)


if __name__ == '__main__':
    #app.run("0.0.0.0","5000")
    # 默认值：host=127.0.0.1, port=5000, debug=false
    app.run()