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
from utils import pyUtils

fb = Blueprint('fb',__name__)

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

@fb.route('/form',methods=['GET','POST'])
@login_required
def form():
    if request.method == 'GET':
        config = configparser.RawConfigParser()
        config.read("group-answer.ini", encoding="utf-8")
        return render_template("fb/form.html", groups=config.sections(), user=session.get('user'),active="fbForm")
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        mp = MysqlPool()
        try:
            for i,group_id in enumerate(json_data.get('group_id')):
                sql = "insert into tb_post(group_id,keyword,nums,share_num,done_num,done_share,content,user_id,status,add_time,accounts) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'')"
                param = [group_id, json_data.get("keyword"), json_data.get("nums"),json_data.get("share_num"),"0","0",
                         json_data.get('content'), session.get('user')['id'], 'working', datetime.now()]
                mp.insert(sql, param)
            res_json = {"code": "0000", "message": "已成功提交%s个任务" % (len(json_data.get('group_id')))}
        except IntegrityError as e:
            res_json = {"code":"1000","message":"%s"%e}
        return jsonify(res_json)

@fb.route('/fbList')
@login_required
def fbList():
    return render_template("fb/post-list.html", user=session.get('user'),active="fbList")

@fb.route('/getFbData',methods=['POST'])
def getFbDataByUser():
    data = request.get_data()
    json_data = []
    if data:
        json_data = json.loads(data.decode("utf-8"))
    mp = MysqlPool()
    sql = "select * from tb_post where user_id=%s "
    param = [session.get('user')['id']]
    try:
        if json_data.get('status'):
            sql += "and status=%s "
            param.append(json_data.get('status'))
    except:
        pass
    try:
        if json_data.get('keyword'):
            keyword = '%' + str(json_data.get('keyword')) + '%'
            sql += " and keyword like %s "
            param.append(keyword)
    except:
        pass
    try:
        if json_data.get('group_id'):
            group_id = '%' + str(json_data.get('group_id')) + '%'
            sql += " and group_id like %s "
            param.append(group_id)
    except:
        pass
    sql += "order by id desc"
    post_list = mp.fetch_all(sql,param)
    res_json = {"code":"0000","list":post_list}
    return jsonify(res_json)

@fb.route('/cpList')
@login_required
def cpList():
    return render_template("fb/comment-pool.html", user=session.get('user'),active="fbCpList")

@fb.route('/getCpData',methods=['POST'])
def getCpData():
    data = request.get_data()
    json_data = []
    if data:
        json_data = json.loads(data.decode("utf-8"))
    param = []
    mp = MysqlPool()
    sql = "select * from tb_comment "
    try:
        if json_data.get('content'):
            content = '%' + str(json_data.get('content')) + '%'
            sql += "where content like %s "
            param.append(content)
    except:
        pass
    sql += "order by id desc"
    cp_list = mp.fetch_all(sql,param)
    res_json = {"code":"0000","list":cp_list}
    return jsonify(res_json)

@fb.route('/addComment',methods=['POST'])
def addComment():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    mp = MysqlPool()
    sql = "insert into tb_comment(content,add_time) values(%s,%s)"
    mp.insert(sql,[json_data.get('content'),datetime.now()])
    res_json = {"code": "0000"}
    return jsonify(res_json)

@fb.route('/updateComment',methods=['POST'])
def updateComment():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    mp = MysqlPool()
    sql = "update tb_comment set content=%s where id=%s"
    mp.insert(sql,[json_data.get('content'),json_data.get('id')])
    res_json = {"code": "0000"}
    return jsonify(res_json)

@fb.route('/deleteComment',methods=['POST'])
def deleteComment():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    mp = MysqlPool()
    sql = "delete from tb_comment where id=%s"
    mp.update(sql,json_data.get('id'))
    res_json = {"code": "0000"}
    return jsonify(res_json)

@fb.route('/fileUpload',methods=['POST'])
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

@fb.route('/accountList')
@login_required
def accountList():
    return render_template("fb/account-list.html", user=session.get('user'),active="fbAccountList")

@fb.route('/getAccountData',methods=['POST'])
@login_required
def getAccountData():
    config = configparser.RawConfigParser()
    config.read("fb-user.ini", encoding="utf-8")
    res_json = {"code": "0000","list":pyUtils.parserToJson(config)}
    print(res_json)
    return res_json

@fb.route('/groupList')
@login_required
def groupList():
    return render_template("fb/group-list.html", user=session.get('user'),active="fbGroupList")

@fb.route('/getGroupData',methods=['POST'])
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