# -*- codeing = utf-8 -*-
# @Time : 2020/9/10 17:15
# @Author : Cj
# @File : autoFlask.py
# @Software : PyCharm

from flask import Flask, render_template, request, session, redirect,jsonify,url_for,json,flash
from functools import wraps
from db import MysqlPool
import os,logging,logging.handlers,threading
from blueprint_facebook import fb
from zzz import DownThread

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(fb,url_prefix='/fb')

dt = DownThread()
t = None

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

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html",user=session.get('user'),title="世纪营联")


@app.route('/login', methods=['GET', 'POST'])
def login():
    logging.error("-----login-----")
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        '''
        设置session过期时间，默认1个月
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=1)
        '''
        account = request.form.get("account")
        mp = MysqlPool()
        user = mp.fetch_one("select * from tb_user where account=%s",account)
        if user:
            if request.form.get("pwd") == user['password']:
                session['user'] = user
                mp = MysqlPool()
                sql = "update tb_user set login_time=now() where id=%s"
                mp.update(sql,user['id'])
                return redirect('/index')
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

@app.route('/stopThread',methods=['POST'])
def stopThread():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    global t,dt
    try:
        if json_data.get('stop'):
            print("stop")
            if t.is_alive():
                print("stopppppppppppp")
                dt.terminate()
                t.join()
    except:
        pass
    res_json = {"code": "0000"}
    return jsonify(res_json)

@app.route('/buyerList')
@login_required
def buyerList():
    return render_template("buyer-list.html", user=session.get('user'))

@app.route('/getBuyerData',methods=['POST'])
def getBuyerData():
    data = request.get_data()
    json_data = []
    if data:
        json_data = json.loads(data.decode("utf-8"))
    mp = MysqlPool()
    sql = "select * from tb_cbb_customer where 1=1 "
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
    group_list = mp.fetch_all(sql,param)
    res_json = {"code":"0000","list":group_list}
    return jsonify(res_json)

if __name__ == '__main__':
    app.run()
