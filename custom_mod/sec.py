import random
import secrets
from hashlib import sha256

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
