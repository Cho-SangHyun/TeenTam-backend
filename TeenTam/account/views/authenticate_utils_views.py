from django.core.mail import EmailMessage
from email.mime.text import MIMEText
import string, random, smtplib


# 길이 12인 랜덤 비밀번호 생성
def TemporaryPassword():
    _LENGTH = 12
    string_pool = string.ascii_letters + string.digits
    result = ""
    for _ in range(_LENGTH):
        result += random.choice(string_pool)
    return result

def ChangePasswordEmail(title, message, email):
    email = EmailMessage(
        title,                # 제목
        message,       # 내용
        to=[email],  # 받는 이메일 리스트
    )
    email.send()
    
    return "email send success"


class GMailClient:

    def __init__(self, username: str, password: str) -> None:
        self.port = 587
        # ex. example@gmail.com
        self.username = username
        # 16digit app password
        self.password = password


    def send_email(self, email: str, subject: str, content: str) -> None:
        
        # login

        with smtplib.SMTP("smtp.gmail.com", self.port) as smtp:
            smtp.starttls()
            smtp.login(self.username, self.password)

            # send_email
            msg = MIMEText(content)
            msg['From'] = self.username
            msg['To'] = email
            msg['Subject'] = subject
            smtp.sendmail(self.username, email, msg.as_string())
            
