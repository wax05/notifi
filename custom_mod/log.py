from SQL import *

def notifi_log(userid:str,title:str,content:str)->bool:
    """log적어주는 sql함수"""
    try:
        input_data = """insert into log(user_id, notifi_title, notifi_content, upload_time) values(%s,%s,%s,NOW())"""
        curs.execute(input_data, (f'{userid}',f'{title}',f'{content}'))
        conn.commit()
        return True
    except:
        return False