import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from amqp_service.celery_app.celery_app import celery_decor


#@celery_decor.task()
def send_email_verify_link(receiver_email: str, message: str):
    """ FUNCTION FOR SENDING EMAIL"""
    try:
        print(message)
        from service.parser import ParseEnv
        sender_email = ParseEnv.EMAIL_
        password = ParseEnv.EMAIL_PASS
        receiver_add = receiver_email
        smtp_server = smtplib.SMTP("mail.pcassa.ru", 587)
        smtp_server.starttls()  # setting up to TLS connection
        #smtp_server.ehlo()
        ##############
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "VERIFY PCASSA ACCOUNT"
        msg['From'] = formataddr(("PCASSA MANAGER", sender_email))
        msg['To'] = receiver_email
        # smtp_server.starttls() #setting up to TLS connection
        smtp_server.login(sender_email, password)  # logging into out email id
        print('login')
        text = "ПОДТВЕРДИТЬ АККАУНТ PCASSA"
        link_for_verify = u'<a href="{mes}">НАЖМИТЕ, ЧТОБЫ ПОДТВЕРДИТЬ ВАШ АККАУНТ PCASSA </a>'.format(mes=message)
        html = f"""\
        <html>
          <head></head>
          <body>
                <h2 color='red'> PCASSA </h2>
                <p> ПОСЛЕ ПЕРЕХОДА ПО ЭТОЙ ССЫЛКЕ ВАШ АККАУНТ БУДЕТ ПОДТВЕРЖДЕН</p>
               {link_for_verify}
          </body>
        </html>
        """
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        smtp_server.sendmail(sender_email, receiver_add, msg.as_string())
        smtp_server.quit()
        print('SUCCESS EMAIL Sent')
        return True
    except Exception as e:
        print(e)
        return False
