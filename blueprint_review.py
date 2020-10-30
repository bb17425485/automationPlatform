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

review = Blueprint('review',__name__)

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

@review.route('/buyerList')
@admin_required
def buyerList():
    return render_template("review/buyer-list.html", user=session.get('user'),active="reviewBuyerList")

@review.route('/getBuyerData',methods=['POST'])
@admin_required
def getBuyerData():
    data = request.get_data()
    json_data = []
    if data:
        json_data = json.loads(data.decode("utf-8"))
    mp = MysqlPool()
    sql = "select * from tb_buyer where 1=1 "
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

@review.route('/reviewForm',methods=['GET','POST'])
@login_required
def reviewForm():
    mp = MysqlPool()
    if request.method == 'GET':
        user = session.get('user')
        user_sql = "select * from tb_user where status=1"
        user_list = None
        if user['level'] == 1:
            user_list = mp.fetch_all(user_sql,None)
        return render_template("review/review-form.html", user=user,user_list=user_list,active="reviewForm")
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        sql = "insert into tb_review_task(user_id,asin,brand,country,img,keyword,kw_page,store," \
              "price,days_order,total_order,is_vp,note,add_time,name) values(%s,%s,%s,'us',%s,%s," \
              "%s,%s,%s,%s,%s,1,%s,now(),%s)"
        try:
            user_id = json_data.get("user_id")
        except:
            user_id = session.get('user')['id']
        if not user_id:
            user_id = session.get('user')['id']
        param = [user_id, json_data.get("asin"), json_data.get("brand"),json_data.get("img"),json_data.get("keyword"),
                 json_data.get("kw_page"),json_data.get("store"),json_data.get("price"),json_data.get("days_order"),
                 json_data.get("total_order"),json_data.get("note"),json_data.get("name")]
        try:
            task_id = mp.insert(sql, param)
            asin_sql = "insert into tb_task_asin(asin,task_id,status,is_put) values(%s,%s,%s,%s)"
            for asin in str(json_data.get("asin")).split("|"):
                asin_param = [asin,task_id,1,0]
                mp.insert(asin_sql,asin_param)
            res_json = {"code": "0000","message": "已成功提交刷单任务"}
        except Exception as e:
            res_json = {"code": "9999","message":"提交失败%s"%e}
        return jsonify(res_json)

@review.route('/reviewList')
@login_required
def reviewList():
    mp = MysqlPool()
    user = session.get('user')
    user_sql = "select * from tb_user"
    user_list = None
    if user['level'] == 1:
        user_list = mp.fetch_all(user_sql, None)
    return render_template("review/review-list.html", user=session.get('user'),active="reviewList",user_list=user_list)

@review.route('/getReviewData',methods=['POST'])
@login_required
def getReviewData():
    data = request.get_data()
    json_data = []
    if data:
        json_data = json.loads(data.decode("utf-8"))
    mp = MysqlPool()
    sql = "SELECT t.*,DATE_FORMAT(t.add_time,'%%Y-%%m-%%d') add_time_str,u.nickname," \
          "(select count(0) from tb_task_order t1 where t1.task_id=t.id) num," \
          "(select count(0) from tb_task_order t1 where t1.task_id=t.id and t1.status=1) done_num," \
          "REPLACE(t.asin,'|',' ') as asin_str" \
          " from tb_review_task t,tb_user u where t.user_id = u.id "
    param = []
    if session.get('user')['level'] != 1:
        sql += 'and t.user_id = %s'
        param.append(session.get('user')['id'])
    try:
        if json_data.get('keyword'):
            keyword = '%' + str(json_data.get('keyword')) + '%'
            sql += " and t.keyword like %s "
            param.append(keyword)
    except:
        pass
    try:
        if json_data.get('asin'):
            asin = '%' + str(json_data.get('asin')) + '%'
            sql += " and t.asin like %s "
            param.append(asin)
    except:
        pass
    try:
        if json_data.get('user_id'):
            sql += " and t.user_id = %s "
            param.append(json_data.get('user_id'))
    except:
        pass
    sql += " order by t.status desc,t.id desc"
    review_list = mp.fetch_all(sql,param)
    res_json = {"code":"0000","list":review_list}
    return jsonify(res_json)

@review.route('/getOrderData',methods=['POST'])
@login_required
def getOrderData():
    data = request.get_data()
    json_data = []
    if data:
        json_data = json.loads(data.decode("utf-8"))
    mp = MysqlPool()
    sql = "SELECT t.*,DATE_FORMAT(t.order_time,'%%Y-%%m-%%d') order_time_str,tb.profile " \
          "from tb_task_order t,tb_buyer tb where t.task_id = %s and t.buyer_id = tb.id"
    param = [json_data.get('task_id')]
    sql += " order by t.order_time desc"
    order_list = mp.fetch_all(sql,param)
    res_json = {"code":"0000","list":order_list}
    return jsonify(res_json)

@review.route('/updateTaskStatus',methods=['POST'])
@login_required
def updateTaskStatus():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    sql = "update tb_review_task set status=%s where id=%s"
    param = [json_data.get('status'),json_data.get('id')]
    mp = MysqlPool()
    mp.update(sql, param)
    res_json = {"code": "0000", "msg": "上架状态修改成功！"}
    return jsonify(res_json)

@review.route('/updateOrderStatus',methods=['POST'])
@admin_required
def updateOrderStatus():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    sql = "update tb_task_order set status=%s where id=%s"
    param = [json_data.get('status'),json_data.get('id')]
    mp = MysqlPool()
    mp.update(sql, param)
    res_json = {"code": "0000", "msg": "结算状态修改成功！"}
    return jsonify(res_json)

@review.route('/groundingList')
@admin_required
def groundingList():
    return render_template("review/grounding-list.html", user=session.get('user'),active="reviewGroundingList")

@review.route('/getGroundingData',methods=['POST'])
@admin_required
def getGroundingData():
    data = request.get_data()
    json_data = []
    if data:
        json_data = json.loads(data.decode("utf-8"))
    mp = MysqlPool()
    sql = "select t.*,t1.price,t1.status as task_status,u.nickname,t1.img," \
          "DATE_FORMAT(t.put_time,'%%Y-%%m-%%d %%H:%%i') put_time_str" \
          " from tb_task_asin t,tb_review_task t1,tb_user u where t1.id=t.task_id and t1.user_id=u.id "
    param = []
    try:
        if json_data.get('order_status'):
            sql += " and t.status = %s "
            param.append(json_data.get('order_status'))
    except:
        pass
    try:
        if json_data.get('asin'):
            sql += " and t.asin = %s "
            param.append(json_data.get('asin'))
    except:
        pass
    try:
        if json_data.get('task_id'):
            sql += " and t.task_id = %s "
            param.append(json_data.get('task_id'))
    except:
        pass
    try:
        if json_data.get('task_status'):
            sql += " and t1.status = %s "
            param.append(json_data.get('task_status'))
    except:
        pass
    sql += " order by t1.status desc,t1.user_id desc,t.id desc"
    asin_list = mp.fetch_all(sql,param)
    res_json = {"code":"0000","list":asin_list}
    return jsonify(res_json)

@review.route('/updateAsinStatus',methods=['POST'])
@admin_required
def updateAsinStatus():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    sql = "update tb_task_asin set status=%s where id=%s"
    param = [json_data.get('status'),json_data.get('id')]
    mp = MysqlPool()
    mp.update(sql, param)
    res_json = {"code": "0000", "msg": "上架状态修改成功！"}
    return jsonify(res_json)

@review.route('/updateTaskDiscount',methods=['POST'])
@admin_required
def updateTaskDiscount():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    sql = "update tb_review_task set discount=%s where id=%s"
    param = [json_data.get('discount'),json_data.get('id')]
    mp = MysqlPool()
    mp.update(sql, param)
    res_json = {"code": "0000", "msg": "折扣修改成功！"}
    return jsonify(res_json)