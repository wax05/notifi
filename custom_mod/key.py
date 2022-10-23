import json
file_path = './config/'#상대경로 지정
def json_parser(file_name:str)->dict:
    """json파일 딕셔너리 형태로 파싱하는 모듈"""
    with open(f'{file_path}{file_name}.json') as json_file:
        json_dict = json.load(json_file)
    return json_dict

flask_sec_key_dict = json_parser('flask_key')#플라스크 비밀키
flask_sec_key = flask_sec_key_dict['key']

db_setting = json_parser('sql_key')#sql 설정
db_host=db_setting['host']
db_user=db_setting['user']
db_pw=db_setting['password']
db_name=db_setting['db_name']
db_charset=db_setting['charset']

mail_setting = json_parser('gmail_key')#gmail 키&계정
gmail_key = mail_setting['key']
gmail_address= mail_setting['email']