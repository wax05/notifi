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
import requests
from flask import Flask, render_template, request, redirect, session, url_for, jsonify, make_response
from flask_cors import CORS
from flask_socketio import SocketIO
from markupsafe import escape
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

with open('config/key.json') as f:
    json_file = json.load(f)
api_key = f"KEY={json_file['api-key']}"

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

def Db_Input_UserData(UserName:str,UserId:str,PwHash:str,Class_:str,Permision:str,Email:str)->bool:
    """`UserName`,`UserId`,`PwHash`,`Class_`,`Permision`
    \n\t db-user_data 데이터 추가"""
    try:
        input_data = """insert into user_data(user_name, user_id, pw_hash, class, permision, email,auto_login) values(%s,%s,%s,%s,%s,%s,0)"""
        curs.execute(input_data, (f'{UserName}',f'{UserId}',f'{PwHash}',f'{Class_}',f'{Permision}',f'{Email}'))
        conn.commit()
        return True
    except:
        return False

def Delete_Data(TableName:str,Column:str,Value:str)->str:
    """`TableName`내에있는 `Column`에서 `Value`인 값만 삭제하는 함수"""
    try:
        sql = 'delete from {} where {} = {}'.format(TableName,Column,Value)
        curs.execute(sql)
        conn.commit()
        return 'done'
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

def id_overlap_check(user_id:str)->bool:#id 중복체크
    try:
        data = Db_Export_Data_DICT('user_data')
        if data != 'error':
            for i in data:
                if user_id == (i['user_id']):
                    return True
        else:
            return 'error'
        return False
    except:
        return 'error'

def db_pw_update(user_id:str,pw:str)->bool:
    try:
        edit_data = """UPDATE user_data SET pw_hash=%s WHERE user_id=%s"""
        curs.execute(edit_data,(pw_to_hash(pw),user_id))
        curs.commit()
        return True
    except:
        return False

def reset_pw(user_id:str,code:str)->bool:
    try:
        db_data = Db_Export_Data_DICT('reset_pw')
        user_db_id = []
        user_db_code = []
        for i in db_data:
            user_db_id.append(i['user_id'])
            user_db_id.append(i['code'])
        if user_id in user_db_id:
            if code in user_db_code:
                
        return True
    except:
        return 'error'

def id_check(user_id:str)->bool:
    try:    
        data = Db_Export_Data_DICT('user_data')
        user_id_db = []
        for i in data:
            user_id_db.append(i['user_id'])
        if user_id in user_id_db:
            return True
        else:
            return False
        return False
    except:
        return 'error'


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
        content = f"""<html><head></head><body><h1>인증코드는 {code} 입니다</h1><a href="wax05.xyz/email/notme">만약 당신이 요청한것이 아니라면 클릭해주세요</a></body></html>"""
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

def send_reset_email(email_to:str)->bool:
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
        content = f"""<html><head></head><body><h1>인증코드는 {make_code(5)} 입니다</h1><a href="wax05.xyz/notme">만약 당신이 요청한것이 아니라면 클릭해주세요</a></body></html>"""
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

#----------------------------------------------------------------gov api

def get_geb_info(date:int)->dict:
    url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?{api_key}&Type=json&ATPT_OFCDC_SC_CODE=J10&SD_SCHUL_CODE=7531374&MLSV_YMD={date}"
    res = requests.get(url)
    json_res = res.json()
    data1 = json_res['mealServiceDietInfo']
    data2 = data1[1]
    data3 = data2['row']
    data4 = data3[0]
    data5 = data4['DDISH_NM'].split('<br/>')
    return_list = []
    for i in data5:
        try:
            start = i.index('(')
            end = i.rindex(')')
            cut_val = i[start:end+1]
            menu = (i.rstrip(cut_val))
            return_list.append(menu.strip())
        except ValueError:
            menu = (i)
            return_list.append(menu.strip())
    return return_list

def get_school_info(school_name:str)->dict:
    """
    https://open.neis.go.kr/portal/data/service/selectServicePage.do?page=1&rows=10&sortColumn=&sortDirection=&infId=OPEN17020190531110010104913&infSeq=2
    명세서 대로 값을 반환함
    """
    SCH_INFO_url = 'schoolInfo'
    url = f"https://open.neis.go.kr/hub/{SCH_INFO_url}?{api_key}&Type=json&SCHUL_NM={school_name}"
    res = requests.get(url)
    json_res = res.json()
    data1 = json_res['schoolInfo']
    data2 = data1[1]
    data3 = data2['row']
    data3 = data3[0]
    return data3

def get_school_time(ATPT_OFCDC_SC_CODE:str,school_code:int,grade:int,class_:int,date:int):
    url = f"https://open.neis.go.kr/hub/hisTimetable?{api_key}&Type=json&ATPT_OFCDC_SC_CODE={ATPT_OFCDC_SC_CODE}&SD_SCHUL_CODE={school_code}&GRADE={grade}&CLASS_NM={class_}&TI_FROM_YMD={date}&TI_TO_YMD={date}"
    res = requests.get(url)
    json_data = res.json()
    data1 = json_data['hisTimetable']
    data2 = data1[1]
    data3 = data2['row']
    return_list = []
    for i in data3:
        return_list.append(i['ITRT_CNTNT'])
    return return_list

#----------------------------------------------------------------function end
#----------------------------------------------------------------flask
app = Flask(__name__)#메인
cors_accept = app#cors 허용
CORS(cors_accept)
app.secret_key = secret_key

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

@app.route('/')
def main():
    return render_template('portfolio.html')

@app.route('/api/docs')
def docs_page():
    return render_template('docs.html')

@cors_accept.route('/api/geb/<date>')
def geb_api(date:int):
    data = get_geb_info(date)
    return jsonify(data)
    
@cors_accept.route('/api/schinfo/<name>')
def schoolinfo_api(name:str):
    data = get_school_info(name)
    return jsonify(data)

@cors_accept.route('/api/time/<grade>/<class_>/<date>')
def time_api(grade:int, class_:int, date:int):
    data = get_school_time('J10',7531374,grade,class_,date)
    return jsonify(data)

@app.route('/notifi')#main page
def notifi_main():
    return render_template('mainpage.html')

@app.route('/notifi/login', methods=['GET', 'POST'])#login page
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

@app.route('/notifi/logout')#logout\
def logout():
    session.pop('id', None)
    return redirect('/')

@app.route('/notifi/account', methods=['GET','POST'])#계정생성
def account():
    if request.method == 'POST':
        input_data = request.get_json()#ajax로 들어온 데이터
        print(input_data)
        code = input_data['code']
        if code_check(code) == True:
            name = input_data['name']
            id = input_data['id']
            pw = pw_to_hash(input_data['pw'])
            input_email = input_data['email']
            if id_overlap_check(id) == False:
                if code_update(code) == True:
                    if Db_Input_UserData(name,id,pw,'user','user',input_email) == True:
                        return jsonify(sta=True)
                    else:
                        return jsonify(sta=False, why='SQL ERROR')
                else:
                    return jsonify(sta=False, why='code not match')
            else:
                return jsonify(sta=False, why='id_overlap')
        else:
            return jsonify(sta=False)
    else:
        return render_template('account.html')

@app.route('/notifi/search', methods=['GET'])
def search_account():
    return render_template('search.html')

@app.route('/notifi/search/id', methods=['GET','POST'])
def find_id():
    if request.method == 'GET':
        return render_template('id_find.html')
    else:
        return jsonify(send=True)

@app.route('/notifi/search/pw', methods=['GET','POST'])
def find_pw():
    if request.method == 'GET':
        return render_template('pw_find.html')
    else:
        data = request.get_json()
        print(data)
        id = data['id']
        if id_check(id) == True:
            db_exp = Db_Export_Data_YouWant_DICT('user_data','user_id',id)
            for i in db_exp:
                global user_email
                user_email = i['email']
            send_reset_email(user_email)
        return jsonify(send=True)

@app.route('/notifi/account/email', methods=['GET','POST'])#이메일 확인 !!안씀!!
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

@app.route('/notifi/invite/<invite_code>', methods=['GET','POST'])#초대페이지
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

@app.route('/notifi/admin/account/create', methods=['POST'])#어드민용 계정생성
def create_account():
    id = request.form['id']
    pw = request.form['pw']
    MakeAdminAccount(id, pw)
    return 'done'

@app.route('/test')#테스트용
def post():
    return render_template('test.html')

@app.route('/notifi/admin')#admin_page
def admin_page():
    if 'id' in session:
        return render_template('admin.html')
    else:
        return redirect('/login')

@app.route('/notifi/user', methods=['GET','POST'])#유저페이지
def userpage():
    if request.method == 'POST':
        return 0
    else:
        return render_template('user_page.html')

@app.route('/notifi/user/notifi', methods=['GET','POST'])#유저공지페이지
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

@app.route('/notifi/user/setting', methods=['GET','POST'])#유저세팅페이지
def user_setting():
    if request.method == 'POST':
        return 0
    else:
        return render_template('user_setting.html')

@app.route('/notifi/log/login', methods=['POST'])#로그인 로깅
def login_log():
    return 0

@app.errorhandler(404)#404에러페이지
def error_404(error):
    return render_template('error_404.html'), 404

@app.errorhandler(405)#405에러페이지
def error(error):
    return render_template('error.html',error = error), 405

if __name__ == '__main__':#서버 시작
      app.run(host='127.0.0.1', port=5000, debug=True)

if __name__ == '__main__':#socketIO 시작
    SocketIO.run(app, debug=True)