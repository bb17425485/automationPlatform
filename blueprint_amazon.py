# -*- codeing = utf-8 -*-
# @Time : 2020/9/10 17:15
# @Author : Cj
# @File : autoFlask.py
# @Software : PyCharm

from flask import render_template, request, session, redirect,jsonify,url_for,json,Blueprint
from functools import wraps
from datetime import datetime
from db import MysqlPool
from pymysql.err import IntegrityError
import configparser

amz = Blueprint('amz',__name__)

def login_required(func):
    @wraps(func) # 修饰内层函数，防止当前装饰器去修改被装饰函数的属性
    def inner(*args, **kwargs):
        # 从session获取用户信息，如果有，则用户已登录，否则没有登录
        user = session.get('user')
        if not user:
            return redirect(url_for("login"))
        else:
            return func(*args, **kwargs)
    return inner

def admin_required(func):
    @wraps(func) # 修饰内层函数，防止当前装饰器去修改被装饰函数的属性
    def inner(*args, **kwargs):
        # 从session获取用户信息，如果有，则用户已登录，否则没有登录
        user = session.get('user')
        if not user or user['level'] != 1:
            return redirect(url_for("login"))
        else:
            return func(*args, **kwargs)
    return inner

@amz.route('/form',methods=['GET','POST'])
@login_required
def form():
    if request.method == 'GET':
        config = configparser.RawConfigParser()
        config.read("group-answer.ini", encoding="utf-8")
        return render_template("amz/track-form.html", groups=config.sections(), user=session.get('user'),active="amzTrackForm")
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        mp = MysqlPool()
        sql = "insert into tb_amz_track_pro(user_id,keyword,asin,status,page_size,add_time) values(%s,%s,%s,%s,%s,now())"
        param = [session.get('user')['id'], json_data.get("keyword"), json_data.get("asin"), "1",json_data.get('page_size')]
        try:
            mp.insert(sql, param)
            res_json = {"code": "0000","message": "已成功提交追踪任务"}
        except IntegrityError as e:
            res_json = {"code": "1000","message":"%s"%e}
        return jsonify(res_json)

@amz.route('/trackList')
@login_required
def trackList():
    return render_template("amz/track-list.html", user=session.get('user'),active="amzTrackList")

@amz.route('/getTrackData',methods=['POST'])
def getTrackData():
    data = request.get_data()
    json_data = []
    if data:
        json_data = json.loads(data.decode("utf-8"))
    mp = MysqlPool()
    sql = "SELECT t.*,DATE_FORMAT(t.add_time,'%%Y-%%m-%%d %%H') update_time, tt.asin, tt.keyword, tt.page_size, tt.status FROM tb_amz_track_data t, tb_amz_track_pro tt " \
          "WHERE t.add_time IN ( SELECT MAX(t1.add_time) FROM tb_amz_track_data t1 GROUP BY t1.pro_id ) " \
          "AND t.pro_id = tt.id AND tt.user_id = %s"
    param = [session.get('user')['id']]
    try:
        if json_data.get('status'):
            sql += "and tt.status=%s "
            param.append(json_data.get('status'))
    except:
        pass
    try:
        if json_data.get('keyword'):
            keyword = '%' + str(json_data.get('keyword')) + '%'
            sql += " and tt.keyword like %s "
            param.append(keyword)
    except:
        pass
    try:
        if json_data.get('asin'):
            sql += " and tt.asin = %s "
            param.append(json_data.get('asin'))
    except:
        pass
    sql += " order by t.id desc"
    post_list = mp.fetch_all(sql,param)
    res_json = {"code":"0000","list":post_list}
    return jsonify(res_json)

@amz.route('/getDataByProId',methods=['POST'])
def getDataByProId():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    sql = "select *,DATE_FORMAT(t.add_time,'%%m月%%d日%%H时') update_time from tb_amz_track_data t where t.pro_id = %s order by t.id asc"
    param = [json_data.get('pro_id')]
    mp = MysqlPool()
    pro_list = mp.fetch_all(sql,param)
    res_json = {"code": "0000", "list": pro_list}
    return jsonify(res_json)

@amz.route('/updateTrackStatus',methods=['POST'])
def updateTrackStatus():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    status = json_data.get('status')
    sql = "update tb_amz_track_pro set status=%s where id=%s"
    if status == 1:update_status = 0
    else:update_status = 1
    param = [update_status,json_data.get('id')]
    mp = MysqlPool()
    mp.update(sql, param)
    res_json = {"code": "0000", "msg": "状态修改成功！"}
    return jsonify(res_json)

@amz.route('/addComment',methods=['POST'])
def addComment():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    mp = MysqlPool()
    sql = "insert into tb_comment(content,add_time) values(%s,%s)"
    mp.insert(sql,[json_data.get('content'),datetime.now()])
    res_json = {"code": "0000"}
    return jsonify(res_json)

@amz.route('/updateComment',methods=['POST'])
def updateComment():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    mp = MysqlPool()
    sql = "update tb_comment set content=%s where id=%s"
    mp.insert(sql,[json_data.get('content'),json_data.get('id')])
    res_json = {"code": "0000"}
    return jsonify(res_json)

@amz.route('/deleteComment',methods=['POST'])
def deleteComment():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    mp = MysqlPool()
    sql = "delete from tb_comment where id=%s"
    mp.update(sql,json_data.get('id'))
    res_json = {"code": "0000"}
    return jsonify(res_json)

@amz.route('/fileUpload',methods=['POST'])
def fileUpload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        mp = MysqlPool()
        sql = "insert into tb_comment(content,add_time) values(%s,now())"
        params = []
        while True:
            lines = file.readline()  # 整行读取数据
            if not lines:
                break
            params.append(lines)
        mp.insertMany(sql,params)
    res_json = {"code": "0000"}
    return jsonify(res_json)



@amz.route('/groupList')
@login_required
def groupList():
    return render_template("amz/group-list.html", user=session.get('user'))

@amz.route('/getGroupData',methods=['POST'])
def getGroupData():
    data = request.get_data()
    json_data = []
    if data:
        json_data = json.loads(data.decode("utf-8"))
    mp = MysqlPool()
    sql = "select * from tb_group where 1=1 "
    param = []
    try:
        if json_data.get('type'):
            sql += "and type=%s "
            param.append(json_data.get('type'))
    except:
        pass
    try:
        if json_data.get('name'):
            name = '%' + str(json_data.get('name')) + '%'
            sql += " and name like %s "
            param.append(name)
    except:
        pass
    try:
        if json_data.get('bigNum'):
            sql += " and nums < %s "
            param.append(json_data.get('bigNum'))
    except:
        pass
    try:
        if json_data.get('smallNum'):
            sql += " and nums > %s "
            param.append(json_data.get('smallNum'))
    except:
        pass
    sql += "order by nums desc"
    group_list = mp.fetch_all(sql,param)
    res_json = {"code":"0000","list":group_list}
    return jsonify(res_json)