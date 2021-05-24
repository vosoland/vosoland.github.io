from flask import Flask, render_template, request
import data_read as dr
import sqlite3
import time

app = Flask(__name__)


# 连接数据库并读取所有数据
def conn_db(db_name, index):
    # 连接数据库并查询
    datalist = []
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    sql = 'select * from athlete_info'
    cursor_data = c.execute(sql)
    # 将所有数据保存在列表中
    for item in cursor_data:
        temp_item = str(item)
        if index['index'] in temp_item:
            datalist.append(item)

    # 关闭游标与连接
    c.close()
    conn.close()

    # 返回列表
    return datalist


# ==================== 主页 /index ====================
@app.route('/')
def home1():
    return render_template('index.html')


@app.route('/index')
def home2():
    return render_template('index.html')


# ==================== 主页 /index ====================


# ==================== 主页 /blog ====================
@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.method == 'POST':
        form_content = request.form  # 字典键名：index，键值：提交的内容
        datalist = conn_db('athlete.db', form_content)
        return render_template('blog.html', var_data=datalist, key=form_content['index'])
    else:
        return render_template('blog.html')


# ==================== 主页 /blog ====================

# ==================== 主页 /blog-sports ====================
@app.route('/blog-sports', methods=['POST', 'GET'])
def blog_sports():
    if request.method == 'POST':
        form_content = request.form  # 字典键名：index，键值：提交的内容
        datalist = conn_db('sports.db', form_content)
        return render_template('blog-sports.html', var_data=datalist, key=form_content['index'])
    else:
        return render_template('blog-sports.html')


# ==================== 主页 /blog-sports ====================

# ==================== 主页 /blog-olympic ====================
@app.route('/blog-olympic', methods=['POST', 'GET'])
def blog_olympic():
    if request.method == 'POST':
        form_content = request.form  # 字典键名：index，键值：提交的内容
        datalist = conn_db('olympics.db', form_content)
        return render_template('blog-olympic.html', var_data=datalist, key=form_content['index'])
    else:
        return render_template('blog-olympic.html')


# ==================== 主页 /blog-sports ====================

# ==================== 结果预测 /about ====================
@app.route('/about', methods=['POST', 'GET'])
def about():
    if request.method == 'POST':
        form_content = request.form  # 字典键名：index，键值：提交的内容
        find_result_list = dr.find_result(dr.file_predicted, form_content['index'])
        return render_template('prediction-post.html', var_result=find_result_list, key=form_content['index'])
    else:
        zipped = dr.read_predicted(dr.file_predicted)
        return render_template('prediction.html', var_allData=zipped)


# ==================== 结果预测 /about ====================


# ==================== 主页 /contact ====================
@app.route('/contact')
def contact():
    return render_template('contact.html')


# ==================== 主页 /contact ====================


# ==================== 主页 /team ====================
@app.route('/team')
def team():
    return render_template('team.html')


# ==================== 主页 /team ====================


# ==================== 主页 /news ====================
@app.route('/news', methods=['POST', 'GET'])
def news():
    if request.method == 'POST':
        form_content = request.form  # 字典键名：index，键值：提交的内容
        data_list = dr.find_news(dr.db_chinaNews, form_content)
        return render_template('news-post.html', var_news_list=data_list, key=form_content['index'])
    else:
        news_list = dr.db_read_all(dr.db_chinaNews)
        return render_template('news.html', var_news_list=news_list)


# ==================== 主页 /news ====================


if __name__ == '__main__':
    app.run()
