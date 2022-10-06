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
def Db_Export_Data(TableName:str)->tuple:
    """`TableName`에 있는 정보 다 빼옴"""
    try:
        sql = f"select * from {TableName}"
        curs.execute(sql)
        rows = curs.fetchall()
        return rows
    except:
        return 'error'

def Db_Export_Data_YouWant(TableName:str,Column:str,Value:str)->tuple:
    """`TableName`테이블내 `Column`에서 `Value`와 맞는것을 모두 가져옴"""
    try:
        sql = f"select * from {TableName} where {Column}='{Value}'"
        curs.execute(sql)
        rows = curs.fetchall()
        return rows
    except:
        return 'error'

def Db_Export_Data_DICT(TableName:str)->dict:
    """`TableName`내에서 있는 정보를 모두 Dict형태로 가져옴"""
    try:
        sql = f"select * from {TableName}"
        curs1.execute(sql)
        rows = curs1.fetchall()
        return rows
    except:
        return 'error'

def Db_Export_Data_YouWant_DICT(TableName:str,Column:str,Value:str,key_name:str,key_val:str)->dict:
    """`TableName`테이블내 `Column`에서 `Value`와 맞는것을 모두 Dict형태로 가져옴
    \n가져온 값을 `key_val`에 맞는 값을 `result`딕셔너리에 `key_name`으로 담아서 딕셔너리 리턴 """
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

def Db_Input_UserData(UserName:str,UserId:str,PwHash:str,Class_:str,Permision:str,)->str:
    """`UserName`,`UserId`,`PwHash`,`Class_`,`Permision`
    \n\t db-user_data 데이터 추가"""
    try:
        input_data = """insert into user_data(user_name, user_id, pw_hash, class, permision,auto_login) values(%s,%s,%s,%s,%s,0)"""
        curs.execute(input_data, (f'{UserName}',f'{UserId}',f'{PwHash}',f'{Class_}',f'{Permision}'))
        conn.commit()
        return 'done'
    except:
        return 'error'

def Delete_Data(TableName:str,Column:str,Value:str)->str:
    """`TableName`내에있는 `Column`에서 `Value`인 값만 삭제하는 함수"""
    try:
        sql = 'delete from {} where {} = {}'.format(TableName,Column,Value)
        curs.execute(sql)
        conn.commit()
        return 'done'
    except:
        return 'error'

def MakeAdminAccount(username:str, password:str)->dict:
    """어드민용 계정 생성"""
    try:
        pw_hash = pw_to_hash(password)
        Db_Input_UserData(username, username, pw_hash, 'admin', 'admin')
        return_dict = {'id':username, 'password':password}
        return return_dict
    except:
        return 'error'

def DeleteUserAccount(userid):
    """userid를 이용해 데이터를 삭제"""
    try:
        Delete_Data('user_data','user_id',f'{userid}')
        return 'done'
    except:
        return 'error'


def check_password(id:str,password:str)->bool:
    """`id`와`password`의 해쉬를 이용해 db에서 유저 정보를 체크하는 함수\n
    에러나면 `str`타입으로 에러라고 반환함"""
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
        

def url_gen(len:int)->str:
    """url `len` 자리만들어줌"""
    url = secrets.token_urlsafe(len)
    return url

def password_gen(len:int)->str:
    """16진수 무작위수로 `len` 자리 비밀번호 리턴"""
    pw = secrets.token_hex(len)
    return pw

def pw_to_hash(input_pw:str)->str:
    """`input_pw`를 64자리 해쉬로 변환"""
    password = str(input_pw)
    password_input = password.encode()
    m= sha256(password_input)
    return m.hexdigest()

def logging (userid:str,title:str,content:str)->bool:
    """유저가 공지 등록하면 sql에 로그 써주는 함수"""
    try:
        input_data = """insert into log(user_id, notifi_title, notifi_content, upload_time) values(%s,%s,%s,NOW())"""
        curs.execute(input_data, (f'{userid}',f'{title}',f'{content}'))
        conn.commit()
        return True
    except:
        return 'error'

def make_code(len: int) -> str:
    try:
        return secrets.token_urlsafe(len)
    except:
        return 'error'

def code_check(code:str)->bool:
    code_output = Db_Export_Data_YouWant('code','code',code)
    if code_output == 'error':
        return 'error'
    else:
        for i in code_output:
            used = i[1]
        if used == 0:
            return True
        elif used == 1:
            return False
        else:
            print(f'DB Code Table, Column code Value {code}')
            return 'error'

def email(userid:str,email:str)->bool:
    try:
        input_data = """insert into user_email(user_id, user_email) values(%s,%s)"""
        curs.execute(input_data, (f'{userid}',f'{email}'))
        conn.commit()
        return True
    except:
        return 'error'

def email_confim(userid:str)->bool:
    edit_data = """UPDATE user_email SET confirm=%s, confirm_date=NOW() WHERE user_id=%s"""
    curs.execute(edit_data, (1,userid))
    conn.commit()
    return True
#----------------------------------------------------------------function end
#----------------------------------------------------------------flask
app = Flask(__name__)

app.secret_key = secret_key

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

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
        print('Login\n\'ip\':{},\'id\': {}'.format(request.remote_addr,user_id))#로그인로그
        if login_TF == True:
            session['id'] = user_id
            return jsonify(login = True , id = True)
        elif login_TF == False:
            return jsonify(login = False, id = True)
        elif login_TF == "error":
            return jsonify(login = False, id = False)
    else:
        return render_template('login.html')

@app.route('/logout')#logout\
def logout():
    session.pop('id', None)
    return redirect('/')

@app.route('/account', methods=['GET','POST'])#계정생성
def account():
    if request.method == 'POST':
        input_data = request.get_json()#ajax로 들어온 데이터
        code = input_data['code']
        if code_check(code) == True:
            name = input_data['name']
            id = input_data['id']
            pw = pw_to_hash(input_data['pw'])
            input_email = input_data['email']
            Db_Input_UserData(name,id,pw,'user','user')
            email(id,input_email)
            return jsonify(sta=True)
        else:
            return jsonify(sta=False)

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
        print(request.form['time'])
        return f'Hello, Post!'
    else:
        return render_template('test.html')

@app.route('/admin')#admin_page
def admin_page():
    return render_template('admin.html')

@app.route('/user', methods=['GET','POST'])#유저페이지
def userpage():
    if request.method == 'POST':
        return 0
    else:
        if 'id' in session:
            return render_template('user_page.html',user_id = session['id'])
        else:
            return redirect('/login')

@app.route('/user/notifi', methods=['GET','POST'])#유저공지페이지
def user_notifi():
    if request.method == 'POST':
        input_json = request.get_json()#ajax input json data
        input_title = input_json['title']
        input_content = input_json['content']
        user_id = input_json['id']
        print(input_title,input_content,user_id)
        return jsonify(res = True)
    else:
        if 'id' in session:
            return render_template('user_notifi.html')
        else:
            return redirect('/login')

@app.route('/user/setting', methods=['GET','POST'])#유저세팅페이지
def user_setting():
    if request.method == 'POST':
        return 0
    else:
        if 'id' in session:
            return 'user_setting_page'
        else:
            return redirect('/login')

@app.errorhandler(404)
def error_404(error):
    return render_template('error.html'), 404