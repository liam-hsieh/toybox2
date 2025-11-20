
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
# from shared.utils import parse_db_access

load_dotenv()
# Load email credentials from a secure location

SENDER = os.getenv("SENDER", 'DoNotReply <sys@xxx.com>')
PSW = os.getenv("PSW", None)
USER = os.getenv("USER", None)
SERVER = os.getenv("SERVER", 'smtpauth.xxx.com')
PORT = os.getenv("PORT", 587)

CONFIG = {
    'sender': SENDER, #db_access.get("email"),
    'sender_password' : PSW,
    'receivers': [
        "liam.hsieh@xxx.com",
        "sys@xxx.com"
    ]
}

def getDefaultReceivers(): 
    # listPath = os.path.join(utils.getDeQPDirectory(), 'intel', 'MAIL_LIST.txt')
    # listFile = open(listPath, 'r')
    
    #ret = []
    # for line in listFile.readlines():
    #     ret.append(line.strip())

    ret = CONFIG["receivers"]

    return ret

def send_mail(cookies_info, user_message):      
        #user_message = "My daughter told Santa that she wants all the junk food from Trader Joe's"#st.text_area("Your Message")
        subject = "Visitor on Toybox left a message"#st.text_input("Subject")
        smtp_auth_user=USER
        smtp_auth_password=PSW
        smtp_server=SERVER
        smtp_port=PORT

        subject = "Visitor on Toybox left a message"
        # Email template
        body = f"""
        A visitor left a message for us.

        Here is the visitor info:
        {cookies_info}
        , 
        and the is the message from the visitor:
        {user_message}

        """
        
        # Construct the message string with headers and body
        message = f"Subject: {subject}\n\n{body}"


        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_auth_user, smtp_auth_password)        
        server.sendmail(SENDER, getDefaultReceivers(), message)
        server.quit() 

def getMailMessage(from_sender, receivers, subject, text, html = None):
    msg = MIMEMultipart('alternative')
    msg['From'] = from_sender
    # msg['To'] = ','.join(receivers)
    msg['Bcc'] = ','.join(receivers)
    msg['Subject'] = subject
    msg.attach(MIMEText(text, 'plain'))
    if html:
        msg.attach(MIMEText(html, 'html'))

    return msg.as_string()



