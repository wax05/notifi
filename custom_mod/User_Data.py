from SQL import *

def email(userid:str,email:str,code:str)->bool:
    try:
        input_data = """insert into user_email(user_id, user_email, code) values(%s,%s,%s)"""
        curs.execute(input_data, (f'{userid}',f'{email}',f'{code}'))
        conn.commit()
        return True
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

def DeleteUserAccount(userid):
    """userid를 이용해 데이터를 삭제"""
    try:
        Delete_Data('user_data','user_id',f'{userid}')
        return 'done'
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

