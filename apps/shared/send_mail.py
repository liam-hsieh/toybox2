
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from shared.utils import parse_db_access

db_access = parse_db_access("/opt/ssl/db.ini","kerberos")

SENDER = 'DoNotReply <sys_e2esol@intel.com>'
CONFIG = {
    'sender': db_access.get("email"),
    'sender_password' :db_access.get("password"),
    'receivers': [
        "liam.hsieh@intel.com",
        "sys-e2esol@intel.com"
        #"rajbir.k.girn@intel.com",
        # "marissa.mena@intel.com",
        # "laura.n.sannes@intel.com",
        # "lexey.sbriglia@intel.com",
        # "amy.loomis@intel.com",
        # "jeffrey.maclaren@intel.com"
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
        subject = "Visitor on E2E Solutions Station left a message"#st.text_input("Subject")
        smtp_auth_user=CONFIG["sender"]
        smtp_auth_password=CONFIG["sender_password"]

        subject = "Visitor on E2E Solutions Station left a message"
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


        server = smtplib.SMTP('smtpauth.intel.com', 587)
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



