from SQL import *
from sec import *
def check_password(id:str,password:str)->bool:
    """`id`와`password`의 해쉬를 이용해 db에서 유저 정보를 체크하는 함수\n
    에러나면 `str`타입으로 에러라고 반환함"""
    try:
        export = Db_Export_Data_YouWant_DICT('user_data','user_id',id)
        if len(export) == 1:
            for export_data in export:
                for i in export_data:
                    output_pw = i['pw_hash']
                if output_pw == pw_to_hash(password):
                    return True
                else:
                    return False
        else:
            print('UserId에 중복값이 있습니다')
            return 'error'
    except:
        return 'error'
        
def code_check(code:str)->bool:
    """db에 있는 코드를 체크합니다 \n Boolean형식으로 뱉어줍니다"""
    try:
        code_output = Db_Export_Data_YouWant_DICT('code','code',code)
        if code_output == 'error':
            return 'error'
        else:
            if len(code_output) == 1:
                for code_data in code_output:
                    used = ''
                    for i in code_data:
                        used = i['used']
                        limit = i['limit']
                    if used - limit == 0:
                        return False
                    else:
                        return True
            else:
                print('CODE에 중복값이 있습니다')
                return 'error'
    except:
        return 'error'

def email_confirm(userid:str)->bool:
    edit_data = """UPDATE user_email SET confirm=%s, confirm_date=NOW() WHERE user_id=%s"""
    curs2.execute(edit_data, (1,userid))
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
        curs2.execute(edit_data, (used, code))
        conn.commit()
        return True
    else:
        return False