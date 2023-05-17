from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import smtplib 

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025
SENDER_ADDRESS='prashant@gmail.com'
SENDER_PASSWORD=''

def send_email(to_address,subject,message,content="text",attachment=None):
    msg = MIMEMultipart()
    msg['To']=to_address
    msg['From']=SENDER_ADDRESS
    msg['Subject']=subject
    if content == "html":
        msg.attach(MIMEText(message,'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))

    if attachment:
        with open(attachment,"rb") as a:
            cnt = MIMEBase("application", "octet-stream")
            cnt.set_payload(a.read())
        cnt.add_header("Content-Disposition", f"attachment: filename={attachment}")
        msg.attach(cnt)          

    s = smtplib.SMTP(host=SERVER_SMTP_HOST, port=SERVER_SMTP_PORT )
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True




# import smtplib
# from email.mime import multipart
# from email.mime import text
# import email

# SMTP_SERVER_HOST = "localhost"
# SMTP_SERVER_PORT = 1025
# SENDER_ADDRESS = "soumyag27402@gmail.com"
# SENDER_PASSWORD = ""


# def send_email(to_address, subject, message, attachment=None):
#     msg = multipart.MIMEMultipart()
#     msg["From"] = SENDER_ADDRESS
#     msg["To"] = to_address
#     msg["Subject"] = subject

#     msg.attach(text.MIMEText(message, "html"))
#     if attachment is not None:
#         with open(attachment, "rb") as attach:
#             stream = email.mime.base.MIMEBase("application", "octet-stream")
#             stream.set_payload(attach.read())
#         email.encoders.encode_base64(stream)
#         stream.add_header("Content-Disposition", f"attachment;filename={attachment}")
#         msg.attach(stream)
#     s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
#     s.login(SENDER_ADDRESS, SENDER_PASSWORD)
#     s.send_message(msg)
#     s.quit()
