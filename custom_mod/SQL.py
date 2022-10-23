import pymysql
import key
from sec import *

start_up = False

class DB_config():
    def __init__(self,json_file_name):
        db_key = key.json_parser(json_file_name)
        self.host = db_key['host']
        self.user = db_key['user']
        self.password = db_key['password']
        self.db_name = db_key['db_name']
        self.charset = db_key['charset']
        self.port = db_key['port']

def db_startup():
    db_key = DB_config()
    global conn, dict_cursor, tuple_cursor
    conn = pymysql.connect(host = db_key.host , user = db_key.user , password = db_key.password , db = db_key.db_name , charset = db_key.charset)#db기본설정
    tuple_cursor = conn.cursor()#그냥 딕셔너리 커서 쓰셈 ㅇㅇ
    dict_cursor = conn.cursor(pymysql.cursors.DictCursor)#딕셔너리 커서
    start_up = True

def Db_Export_Data(TableName:str)->tuple:
    """`TableName`에 있는 정보 다 빼옴"""
    try:
        sql = f"select * from {TableName}"
        tuple_cursor.execute(sql)
        rows = tuple_cursor.fetchall()
        return rows
    except:
        return 'error'

def Db_Export_Data_DICT(TableName:str)->dict:
    """`TableName`내에서 있는 정보를 모두 Dict형태로 가져옴"""
    try:
        sql = f"select * from {TableName}"
        dict_cursor.execute(sql)
        rows = dict_cursor.fetchall()
        return rows
    except:
        return 'error'

def Db_Export_Data_YouWant_DICT(TableName:str,Column:str,Value:str)->tuple:
    """`TableName`테이블내 `Column`에서 `Value`와 맞는것을 모두 Dict형태로 가져옴"""
    try:
        sql = f"select * from {TableName} where {Column}='{Value}'"
        dict_cursor.execute(sql)
        rows = dict_cursor.fetchall()
        return rows
    except:
        return 'error'

def Delete_Data(TableName:str,Column:str,Value:str)->str:
    """`TableName`내에있는 `Column`에서 `Value`인 값만 삭제하는 함수"""
    try:
        sql = 'delete from {} where {} = {}'.format(TableName,Column,Value)
        tuple_cursor.execute(sql)
        conn.commit()
        return 'done'
    except:
        return 'error'


print(start_up)
db_startup('sql_key')
print(start_up)