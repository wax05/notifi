#----------------------------------------------------------------module importa
from datetime import timedelta
import json
import pymysql
import secrets
from hashlib import sha256
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from markupsafe import escape
#----------------------------------------------------------------function
#----------------------------------------------------------------json_parser
with open('config/key.json') as f:
    setting = json.load(f)
host=setting['host']
user=setting['user']
pw=setting['password']
db_name=setting['db_name']
charset=setting['charset']

with open('config/flask_key.json') as f:
    setting = json.load(f)
secret_key = setting['key']
#----------------------------------------------------------------sql
conn = pymysql.connect(host = host, user = user, password = pw ,db = db_name,charset = charset)#db기본설정

curs = conn.cursor()#일반커서
curs1 = conn.cursor(pymysql.cursors.DictCursor)#딕셔너리 커서
def Db_Export_Data(TableName):
    """ Args:\n\t`TableName` : `string`\nReturn:\n\t`Type` : `Typle`"""
    try:
        sql = f"select * from {TableName}"
        curs.execute(sql)
        rows = curs.fetchall()
        return rows
    except:
        return 'error'

def Db_Export_Data_YouWant(TableName,Column,Value):
    """ Args:\n\t`TableName` : `string`\n\t`Column` : `string`\n\t`Value` : `string`\nReturn:\n\t`Type` : `Typle(List)`"""
    try:
        sql = f"select * from {TableName} where {Column}='{Value}'"
        curs.execute(sql)
        rows = curs.fetchall()
        return rows
    except:
        return 'error'

def Db_Export_Data_DICT(TableName):
    """ Args:\n\t`TableName` : `string`\n\t`Column` : `string`\n\t`Value` : `string`\nReturn:\n\t`Type` : `List(Dict)`"""
    try:
        sql = f"select * from {TableName}"
        curs1.execute(sql)
        rows = curs1.fetchall()
        return rows
    except:
        return 'error'

def Db_Export_Data_YouWant_DICT(TableName,Column,Value,key_name,key_val):
    """ Args:\n\t`TableName` : `string`\n\t`Column` : `string`\n\t`Value` : `string`\n\t`key_name` : `string`\n\t`key_val` : `string`\nReturn:\n\t`Type` : `List(in(Dict))`"""
    try:
        sql = f"select * from {TableName} where {Column}='{Value}'"
        curs1.execute(sql)
        rows = curs1.fetchall()
        result = {}
        for data in rows:
            dat = data[f'{key_val}']
            result[key_name] = dat
        return result
    except:
        return 'error'

def Db_Input_UserData(UserName,UserId,PwHash,Class_,Permision):
    """ Args:\n\t`UserName` : `string`\n\t`UserId` : `string`\n\t`PwHash` : `string`\n\t`Class_` : `string`\n\t`Permision` : `string`\nReturn:\n\t `none`\n\t db-user_data 데이터 추가"""
    input_data = """insert into user_data(user_name, user_id, pw_hash, class, permision, admin) values(%s,%s,%s,%s,%s)"""
    curs.execute(input_data, (f'{UserName}',f'{UserId}',f'{PwHash}',f'{Class_}',f'{Permision}'))
    conn.commit()
    return 'done'

def Delete_Data(TableName,Column,Value):
    """Args:\n\t`TableName` : `string`\n\t`Column` : `string`\n\t`Value` : `string`\nReturn:\n\t`none``"""
    sql = 'delete from {} where {} = {}'.format(TableName,Column,Value)
    curs.execute(sql)
    conn.commit()
    return 'done'

def MakeAdminAccount(username, password):
    """어드민용 계정 생성\n\nArgs:\n\t`username` : `string`\n\t`password` : `string`\nReturn\n\t`type` : `dict`"""
    pw_hash = pw_to_hash(password)
    Db_Input_UserData(username, username, pw_hash, 'admin', 'admin')
    return_dict = {'id':username, 'password':password}
    return return_dict

def DeleteUserAccount(userid):
    """userid를 이용해 데이터를 삭제\n\nArgs:\n\t`userid` : `string`\nReturn:\n\t`return` : `none`"""
    Delete_Data('user_data','user_id',f'{userid}')
    return 'done'


def check_password(id,password):
    """Args:\n\t`userid` , `password` : `String`\nReturn:\n\t`type` : `boolean`"""
    try:
        export = Db_Export_Data_YouWant('user_data','user_id',id)
        for i in export:
            output_pw = i[2]
        user_pw = pw_to_hash(password)
        if output_pw == user_pw:
            return True
        else:
            return False
    except:
        return 'error'
        

def url_gen ():#url 만들어줌
    """`return` : `string`\n`len` : `10`"""
    url = secrets.token_urlsafe(10)
    return url

def password_gen():#16진수 무작위수로 15자리 비밀번호 리턴
    """16진수로 15자리 비밀번호 리턴\n`return` : `string`\n`len` : `15`"""
    pw = secrets.token_hex(15)
    return pw

def pw_to_hash(input_pw):#password를 64자리 해쉬로 변환
    """ Args:\n\t`input_pw` : `string`\nReturn:\n\t`Type` : `string`\n\t`len` : `64`"""
    password = str(input_pw)
    password_input = password.encode()
    m= sha256(password_input)
    return m.hexdigest()

#----------------------------------------------------------------function end
#----------------------------------------------------------------flask
app = Flask(__name__)

app.secret_key = secret_key

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)

@app.route('/')#main page
def main():
    return render_template('mainpage.html')

@app.route('/login', methods=['GET', 'POST'])#login page
def login():
    if request.method == 'POST':
        input_data = request.get_json()#ajax로 들어온 데이터
        user_id = input_data['id']#데이터 파싱
        user_pw = input_data['password']
        login_TF = check_password(user_id,user_pw)#체크
        print(login_TF)
        if login_TF == True:
            session['id'] = user_id
            print(session['id'])
            return jsonify(login = True , id = True)
        elif login_TF == False:
            return jsonify(login = False, id = True)
        elif login_TF == "error":
            return jsonify(login = False, id = False)
    else:
        return render_template('login.html')

@app.route('/account', methods=['GET','POST'])#계정생성
def account():
    if request.method == 'POST':
        id = request.form['user_id']
        pw = request.form['pw']
        print(id,pw)
    else:
        return render_template('account.html')

@app.route('/admin/account/create', methods=['POST'])#어드민용 계정생성
def create_account():
    id = request.form['id']
    pw = request.form['pw']
    MakeAdminAccount(id, pw)
    return 'done'

@app.route('/PostTest', methods=['GET','POST'])#post 테스트용
def post():
    if request.method == 'POST':
        req = request.form['text']
        print(req)
        return f'Hello, Post!\n{req}'
    else:
        return render_template('test.html')

@app.route('/admin')#admin_page
def admin_page():
    return render_template('admin.html')

@app.route('/userpage', methods=['GET','POST'])#유저페이지
def userpage():
    if request.method == 'POST':
        return 0
    else:
        if 'id' in session:
            return render_template('user_page.html',user_id = session['id'])
        else:
            return redirect('/login')


