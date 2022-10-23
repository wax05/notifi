#로컬함수
from key import json_parser

db_setting = json_parser('sql_key')#sql 설정
db_host=db_setting['host']
db_user=db_setting['user']
db_pw=db_setting['password']
db_name=db_setting['db_name']
db_charset=db_setting['charset']

mail_setting = json_parser('gmail_key')#gmail 키&계정
gmail_key = mail_setting['key']
gmail_address= mail_setting['email']