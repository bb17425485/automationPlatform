# -*- codeing = utf-8 -*-
# @Time : 2020/9/10 17:15
# @Author : Cj
# @File : autoFlask.py
# @Software : PyCharm

from flask import Flask, render_template, request, session, redirect,jsonify,url_for,json,flash
from functools import wraps
from db import MysqlPool
import os,logging,logging.handlers,threading,hashlib,pymysql
from blueprint_facebook import fb
from blueprint_amazon import amz
from blueprint_review import review
from utils import pyUtils

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(fb,url_prefix='/fb')
app.register_blueprint(amz,url_prefix='/amz')
app.register_blueprint(review,url_prefix='/review')

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

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html",user=session.get('user'),title="世纪营联",active="index")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        '''
        设置session过期时间，默认1个月
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=1)
        '''
        account = request.form.get("account").lower()
        mp = MysqlPool()
        user = mp.fetch_one("select * from tb_user where account=%s",account)
        if user:
            if pyUtils.getMd5(request.form.get("pwd")) == user['password']:
                if user['status'] == 3:
                    flash("帐号已停用，请联系管理员")
                elif user['status'] == 2:
                    flash("帐号待审核，请联系管理员")
                else:
                    session['user'] = user
                    mp = MysqlPool()
                    sql = "update tb_user set login_time=now() where id=%s"
                    mp.update(sql,user['id'])
                    if user['level'] == 1:return redirect('/index')
                    elif user['level'] == 2:return redirect('/review/reviewList')
            else:flash("密码错误")
        else:flash("帐号未注册")
        return redirect(url_for("login"))

@app.route('/logout')
@login_required
def logout():
    session.pop("user")
    session.clear()
    return redirect(url_for('login'))

@app.route('/signup')
def signup():
    return render_template("sign-up.html")

@app.route('/doThread',methods=['POST'])
def doThreading():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    global t,dt
    try:
        if json_data.get('start'):
            print("start")
            t = threading.Thread(target=dt.run, args=(10,))
            t.start()
    except:
        pass
    res_json = {"code": "0000"}
    return jsonify(res_json)

@app.route('/userList')
@admin_required
def userList():
    return render_template("user-list.html", user=session.get('user'),active="userList")

@app.route('/getUserData',methods=['POST'])
@admin_required
def getUserData():
    data = request.get_data()
    json_data = []
    if data:
        json_data = json.loads(data.decode("utf-8"))
    mp = MysqlPool()
    sql = "select t.id,t.account,t.level,t.nickname,t.status,DATE_FORMAT(t.reg_time,'%%Y-%%m-%%d %%H:%%i:%%s') reg_time," \
          "DATE_FORMAT(t.login_time,'%%Y-%%m-%%d %%H:%%i:%%s') login_time from tb_user t where 1=1 "
    param = []
    try:
        if json_data.get('level'):
            sql += "and level=%s "
            param.append(json_data.get('level'))
    except:
        pass
    user_list = mp.fetch_all(sql,param)
    res_json = {"code":"0000","list":user_list}
    return jsonify(res_json)

@app.route('/updateUser',methods=['POST'])
@admin_required
def updateUser():
    data = request.get_data()
    json_data = []
    if data:
        json_data = json.loads(data.decode("utf-8"))
    mp = MysqlPool()
    sql = "update tb_user set status=%s where id=%s"
    param = [json_data.get('status'),json_data.get('id')]
    mp.update(sql,param)
    res_json = {"code":"0000","msg":"修改成功"}
    return jsonify(res_json)

@app.route('/addUser',methods=['POST'])
@admin_required
def addUser():
    data = request.get_data()
    json_data = []
    if data:
        json_data = json.loads(data.decode("utf-8"))
    mp = MysqlPool()
    sql = "insert into tb_user(account, password, nickname, level, status, reg_time) values (%s,%s,%s,%s,1,now())"
    param = [json_data.get('account'), pyUtils.getMd5(json_data.get("password")),json_data.get('nickname'),json_data.get('level')]
    msg = "用户添加成功"
    try:
        mp.update(sql, param)
    except pymysql.err.IntegrityError:
        msg = "添加失败,用户名已存在"
    except Exception as e:
        msg = "添加失败,%s"%e
    res_json = {"code": "0000", "msg": msg}
    return jsonify(res_json)

@app.route('/updatePassword',methods=['POST'])
@login_required
def updatePassword():
    data = request.get_data()
    json_data = []
    if data:
        json_data = json.loads(data.decode("utf-8"))
    mp = MysqlPool()
    find_sql = "select * from tb_user where password=%s and id=%s"
    find_param = [pyUtils.getMd5(json_data.get('old_psw')),session.get('user')['id']]
    find_req = mp.fetch_all(find_sql,find_param)
    if len(find_req) == 1:
        sql = "update tb_user set password=%s where id=%s"
        param = [pyUtils.getMd5(json_data.get('new_psw')),session.get('user')['id']]
        mp.update(sql,param)
        res_json = {"code":"0000","msg":"修改成功"}
    else:
        res_json = {"code": "9999", "msg": "修改失败,原密码错误"}
    return jsonify(res_json)

if __name__ == '__main__':
    app.run()
