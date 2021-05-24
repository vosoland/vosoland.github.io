import pandas as pd
import sqlite3
import csv

# 文件地址
file_schedule = 'compare_data/16-17Schedule.csv'  # 处理后的比赛日程表
file_real_result = 'compare_data/16-17 Oct_realResult.csv'  # 在 NBA官网中下载
file_real_winner = 'compare_data/realWinner.csv'  # 处理后的真实胜负表
file_predicted = 'compare_data/16-17Result.csv'  # 经过预测生成的胜负表

# 数据库名称
db_chinaNews = 'china_news1.db'  # 新闻数据库


# 读取预测结果
def read_predicted(pre_file):
    # 读文件
    df_predicted = pd.read_csv(pre_file)
    # 读取每一列
    date = df_predicted['Date'].values.tolist()
    start_time = df_predicted['Start (ET)'].values.tolist()
    winner = df_predicted['win'].values.tolist()
    lose = df_predicted['lose'].values.tolist()

    # 转成字符串，保留三位
    win_probability = df_predicted['win_probability'].values.tolist()
    win_probability = [str(x)[:5] for x in win_probability]

    # 打包
    zipped = zip(date, start_time, winner, lose, win_probability)

    return zipped


# 查找某一预测结果
def find_result(pre_file, key_words):
    # 读文件
    df_predicted = pd.read_csv(pre_file)
    # 读取每一列
    result_date = df_predicted[df_predicted['Date'] == key_words]
    # 依次判断查询结果的 df是否为空
    if len(result_date.index) == 0:
        result_start_time = df_predicted[df_predicted['Start (ET)'] == key_words]
        if len(result_start_time) == 0:
            result_team = df_predicted[(df_predicted['win'] == key_words) | (df_predicted['lose'] == key_words)]
            if len(result_team.index) == 0:
                return []  # 没找到，必须返回一个空的可迭代对象，因为在 html中要进行迭代
            else:
                return result_team.values.tolist()  # 返回查找结果
        else:
            return result_start_time.values.tolist()  # 返回查找结果
    else:
        return result_date.values.tolist()  # 返回查找结果


# 连接数据库并读取所有数据
def db_read_all(db_name):
    # 连接数据库并查询
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    sql = 'select * from athlete_info'
    cursor_data = c.execute(sql)

    news_list = [list(x) for x in cursor_data]
    for i in news_list:
        i[3] = i[3][:196] + '......（点击标题查看更多）'

    # 关闭游标与连接
    c.close()
    conn.close()

    # 返回列表
    return news_list


# 连接 news数据库并查询数据
def find_news(db_name, index):
    # 连接数据库并查询
    datalist = []
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    sql = 'select * from athlete_info'
    cursor_data = c.execute(sql)
    # 将所有数据保存在列表中
    for item in cursor_data:
        title = str(item[1])  # 标题列
        time = str(item[2])  # 时间列
        if (index['index'] in title) or (index['index'] in time):
            datalist.append(item)

    datalist = [list(x) for x in datalist]
    for i in datalist:
        i[3] = i[3][:196] + '......（点击标题查看更多）'

    # 关闭游标与连接
    c.close()
    conn.close()

    # 返回列表
    return datalist









