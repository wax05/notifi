#----------------------------------------------------------------module importa
from datetime import timedelta
import json
import pymysql
import secrets
import random
import smtplib
from email.mime.multipart import MIMEMultipart # 메일의 Data 영역의 메시지를 만드는 모듈 
from email.mime.text import MIMEText # 메일의 본문 내용을 만드는 모듈
from hashlib import sha256
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_socketio import SocketIO
from markupsafe import escape
from module import *
#----------------------------------------------------------------function
#----------------------------------------------------------------json_parser
with open('config/sql_key.json') as f:
    setting = json.load(f)
host=setting['host']
user=setting['user']
pw=setting['password']
db_name=setting['db_name']
charset=setting['charset']

with open('config/flask_key.json') as f:
    setting = json.load(f)
secret_key = setting['key']

with open('config/gmail_key.json') as f:
    key = json.load(f)
email_pw = key['key']
email_mail = key['email']

#----------------------------------------------------------------values make
def group_user(input:str)->list:
    """user_id를 다 뱉어줌"""
    output = []
    for i in input.split("/"):
        if i != "":
            output.append(str(i))
    return output
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

def Db_Export_Data_YouWant_DICT(TableName:str,Column:str,Value:str)->tuple:
    """`TableName`테이블내 `Column`에서 `Value`와 맞는것을 모두 Dict형태로 가져옴"""
    try:
        sql = f"select * from {TableName} where {Column}='{Value}'"
        curs1.execute(sql)
        rows = curs1.fetchall()
        return rows
    except:
        return 'error'

def Db_Export_Data_YouWant_DICT_indict(TableName:str,Column:str,Value:str,key_name:str,key_val:str)->dict:
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
        
def code_check(code:str)->bool:
    """db에 있는 코드를 체크합니다 \n Boolean형식으로 뱉어줍니다"""
    try:
        code_output = Db_Export_Data_YouWant('code','code',code)
        if code_output == 'error':
            return 'error'
        else:
            used = ''
            for i in code_output:
                used = i[1]
                limit = i[3]
            if used - limit == 0:
                return False
            else:
                return True
    except:
        return 'error'
        
def email(userid:str,email:str,code:str)->bool:
    try:
        input_data = """insert into user_email(user_id, user_email, code) values(%s,%s,%s)"""
        curs.execute(input_data, (f'{userid}',f'{email}',f'{code}'))
        conn.commit()
        return True
    except:
        return 'error'

def email_code(user_id:str,code:str)->bool:
    try:
        edit_data = """UPDATE user_email SET code=%s WHERE user_id=%s"""
        curs.execute(edit_data, (code, user_id))
        conn.commit()
        return True
    except:
        return False

def email_confirm(userid:str)->bool:
    edit_data = """UPDATE user_email SET confirm=%s, confirm_date=NOW() WHERE user_id=%s"""
    curs.execute(edit_data, (1,userid))
    conn.commit()
    return True

def code_update(code:str)->bool:
    edit_data = """UPDATE code SET used=%s WHERE code=%s"""
    data = Db_Export_Data_YouWant_DICT('code','code',code)
    for i in data:
        used = i['used']
        lim = i['limit']
    if used != lim:
        used += 1
        curs.execute(edit_data, (used, code))
        conn.commit()
        return True
    else:
        return False
    
def notifi_log(userid:str,title:str,content:str)->bool:
    """log적어주는 sql함수"""
    try:
        input_data = """insert into log(user_id, notifi_title, notifi_content, upload_time) values(%s,%s,%s,NOW())"""
        curs.execute(input_data, (f'{userid}',f'{title}',f'{content}'))
        conn.commit()
        return True
    except:
        return False
#----------------------------------------------------------------sql end,secrets start
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

def make_code(in_len: int) -> str:
    try:
        result = ""
        down_case = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        upper_case = ["A", "B", "C", "D", "E", "F", "G", "H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        numbers = [0,1,2,3,4,5,6,7,8,9]
        while len(result) <= in_len-1:
            big = random.randint(0,2)
            if big == 0:
                res = down_case[random.randint(0,len(down_case)-1)]
                result += res
            elif big == 1:
                res = upper_case[random.randint(0,len(upper_case)-1)]
                result += res
            else:
                res = numbers[random.randint(0,len(numbers)-1)]
                result += str(res)
        return result
    except:
        return 'error'

def group_member_check(group_name:str)->str:
    db_export = Db_Export_Data_YouWant_DICT('group','group_name',group_name)
    admin = db_export['admin']
    user = db_export['user']
    admin_many = admin.count('/')
    user_many = user.count('/')

def user_parsing(group:str,type:bool)->list:
    """`group`이름에서 있는 유저 정보 가져옴 \n `type`이 True이면 admin,아니면 일반user"""
    try:
        res = []
        if type == True:
            data = Db_Export_Data_YouWant_DICT('user_group','group_name',group)
            for i in data:
                admin_user = i['admin']
                for e in admin_user.split('/'):
                    if e != '':
                        res.append(e)
            return res
        elif type == False:
            data = Db_Export_Data_YouWant_DICT('user_group','group_name',group)
            for i in data:
                common_user = i['user']
                for e in common_user.split('/'):
                    if e != '':
                        res.append(e)
            return res
        else:
            print('type error: type is no boolean') 
    except:
        return 'error'

def many_group_member(group:str)->int:#그룹 인원 체크
    admin = user_parsing(group,True)
    user = user_parsing(group,False)
    return len(admin) + len(user)

def send_check_email(email_to:str,code:str)->bool:
    try:
        # smpt 서버와 연결
        gmail_smtp = "smtp.gmail.com"  #gmail smtp 주소
        gmail_port = 465  #gmail smtp 포트번호
        smpt = smtplib.SMTP_SSL(gmail_smtp, gmail_port)
        # 로그인
        smpt.login(email_mail,email_pw)
        # 메일 기본 정보 설정
        msg = MIMEMultipart()
        msg["Subject"] = "인증요청"
        msg["From"] = "saesol-api"
        msg["To"] = email_mail

        # 메일 내용 쓰기
        content = f"""<html><head></head><body><h1>인증코드는 {code} 입니다</h1><a href="wax05/email/notme">만약 당신이 요청한것이 아니라면 클릭해주세요</a></body></html>"""
        common = '만약 이 인증을 요청하신적이 없으시면 위 버튼을 눌러주시기 바랍니다'
        content_part = MIMEText(content, 'html')
        common_part = MIMEText(common, 'plain')
        msg.attach(content_part)
        msg.attach(common_part)
        # 메일 보내고 서버 끄기
        smpt.sendmail(email_mail, email_to, msg.as_string())  
        smpt.quit()
        return True
    except:
        return False

#----------------------------------------------------------------function end
#----------------------------------------------------------------flask
app = Flask(__name__)

app.secret_key = secret_key

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

def no_session():#세션없으면 돌려주는 함수 // 개발중
    return render_template('nosession.html')

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
        print('Login\n\'ip\':{},\'id\': {},login={}'.format(request.remote_addr,user_id,login_TF))#로그인로그
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
            if code_update(code) == True:
                code = make_code(5)
                Db_Input_UserData(name,id,pw,'user','user')
                email(id,input_email,code)
                session['email'] = input_email
                send_check_email(input_email,code)
                return jsonify(sta=True)
            else:
                return jsonify(sta=False)
        else:
            return jsonify(sta=False)
    else:
        return render_template('account.html')

@app.route('/account/email', methods=['GET','POST'])#이메일 확인
def email_check():
    if request.method == 'POST':
        db_exp_data = Db_Export_Data_YouWant_DICT('user_email','user_id',)
        for i in db_exp_data:
            user_id = i['user_id']
            db_code = i['code']
        input_data = request.get_json()#ajax로 들어온 데이터
        user_code = input_data['code']
        if db_code == user_code:
            email_confirm(user_id)
            session.pop('email', None)
            return jsonify(res = True)
    else:
        return render_template('email.html')

@app.route('/invite/<invite_code>', methods=['GET','POST'])
def group_code_invite(invite_code):
    if request.method == 'POST':
        return 0
    else:
        if 'id' in session:
            if code_check(invite_code) == True:
                #---------------------------------------------------------------누가 초대했는지 확인(id)
                db_output = Db_Export_Data_YouWant_DICT('code','code',invite_code)
                for i in db_output:
                    user_id = i['user_id']
                    school_code = i['group']#학교 코드
                #---------------------------------------------------------------누가 초대했는지 확인(이름)
                user_data_output = Db_Export_Data_YouWant_DICT('user_data','user_id',user_id)
                for i in user_data_output:
                    user_name = i['user_name']
                #----------------------------------------------------------------school_name
                school_db = Db_Export_Data_YouWant_DICT('user_group','group_name',school_code)
                for i in school_db:
                    school_name = i['school_name']
                #----------------------------------------------------------------group_member_check
                group_many = many_group_member(school_code)
                #----------------------------------------------------------------이미지
                db_img = Db_Export_Data_YouWant_DICT('img','group_name',school_code)
                for i in db_img:
                    img_file_name = i['img_file']
                return render_template('invite.html',invite_user = user_name, school_name1 = school_name, group_count = group_many, file_name=img_file_name)
            else:
                return render_template('error.html')
        else:
            return redirect('/login')

@app.route('/admin/account/create', methods=['POST'])#어드민용 계정생성
def create_account():
    id = request.form['id']
    pw = request.form['pw']
    MakeAdminAccount(id, pw)
    return 'done'

@app.route('/PostTest', methods=['GET','POST'])#post 테스트용
def post():
    if request.method == 'POST':
        input_data = request.get_json()
        print(input_data)
        return jsonify(sta = True)
    else:
        return render_template('test.html')

@app.route('/admin')#admin_page
def admin_page():
    if 'id' in session:
        return render_template('admin.html')
    else:
        return redirect('/login')

@app.route('/user', methods=['GET','POST'])#유저페이지
def userpage():
    if request.method == 'POST':
        return 0
    else:
        return render_template('user_page.html')

@app.route('/user/notifi', methods=['GET','POST'])#유저공지페이지
def user_notifi():
    if request.method == 'POST':
        input_json = request.get_json()#ajax input json data
        input_title = input_json['title']
        input_content = input_json['content']
        user_id = input_json['id']
        if user_id == '':
            return jsonify(res = False, why = 'login')
        else:
            return jsonify(res = True)
    else:
        # if 'id' in session:
            return render_template('user_notifi.html')
        # else:
            # return redirect(url_for('login'))

@app.route('/user/setting', methods=['GET','POST'])#유저세팅페이지
def user_setting():
    if request.method == 'POST':
        return 0
    else:
        return render_template('user_setting.html')

@app.route('/log/login', methods=['POST'])#로그인 로깅
def login_log():
    return 0

@app.errorhandler(404)
def error_404(error):
    return render_template('error_404.html'), 404

@app.errorhandler(405)
def error(error):
    return render_template('error.html',error = error), 405

if __name__ == '__main__':
      app.run(host='127.0.0.1', port=5000, debug=True)

if __name__ == '__main__':
    SocketIO.run(app, debug=True)