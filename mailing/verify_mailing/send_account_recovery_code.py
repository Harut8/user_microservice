import smtplib
from amqp_service.celery_app.celery_app import celery_decor


@celery_decor.task()
def send_account_recovery_code(*, receiver_email: str, message: str):
    """ FUNCTION FOR SENDING EMAIL"""
    try:
        from service.parser import ParseEnv
        sender_email = ParseEnv.EMAIL_
        password = ParseEnv.EMAIL_PASS
        receiver_add = receiver_email
        smtp_server = smtplib.SMTP("mail.pcassa.ru", 587)
        smtp_server.starttls()
        smtp_server.login(sender_email, password) #logging into out email id
        smtp_server.sendmail(sender_email, receiver_add, message)
        smtp_server.quit()
        print('SUCCESS EMAIL Sent')
        return message
    except Exception as e:
        print(e)
        return None


