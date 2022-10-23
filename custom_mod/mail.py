import smtplib
from email.mime.multipart import MIMEMultipart # 메일의 Data 영역의 메시지를 만드는 모듈 
from email.mime.text import MIMEText # 메일의 본문 내용을 만드는 모듈
import key
from SQL import *

def send_check_email(email_to:str,code:str)->bool:
    try:
        # smpt 서버와 연결
        gmail_smtp = "smtp.gmail.com"  #gmail smtp 주소
        gmail_port = 465  #gmail smtp 포트번호
        smpt = smtplib.SMTP_SSL(gmail_smtp, gmail_port)
        # 로그인
        smpt.login(key.gmail_address,key.gmail_key)
        # 메일 기본 정보 설정
        msg = MIMEMultipart()
        msg["Subject"] = "인증요청"
        msg["From"] = "saesol-api"
        msg["To"] = key.gmail_address

        # 메일 내용 쓰기
        content1 = """<html><head><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap" rel="stylesheet"></head><body style="margin:0;padding:0;text-align:center;position:relative;font-family:'Gowun Dodum',sans-serif"><div style="width:80%;height:70%;margin-left:10%;margin-right:10%;margin-top:5%;background-image:linear-gradient(to left,#fbc2eb 0,#a6c1ee 100%);border-radius:15px;position:absolute;border:solid 1px #000"><div style="width:30%;font-size:20px;background-color:#fff;margin:3% 34% 3% 34%;padding:1% 1% 1% 1%;border-radius:10px;border:solid 1px #000"><h1 style="margin:0;padding:0">인증코드</h1></div><div style="width:50%;height:40%;background-color:#fff;border:solid 1px #000;margin:0 25% 5% 25%;border-radius:15px"><p style="font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;font-size:50px;margin:13% 5% 13% 5%">"""
        content2 = """<p></p><a href="wax05.xyz/email/notme">인증을 요청하지 않았습니다</a></body></html>"""
        content = content1 + code + content2
        common = '만약 이 인증을 요청하신적이 없으시면 위 버튼을 눌러주시기 바랍니다'
        content_part = MIMEText(content, 'html')
        common_part = MIMEText(common, 'plain')
        msg.attach(content_part)
        msg.attach(common_part)
        # 메일 보내고 서버 끄기
        smpt.sendmail(key.gmail_address, email_to, msg.as_string())  
        smpt.quit()
        return True
    except:
        return False