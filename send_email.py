import smtplib
from email.mime.text import MIMEText


def send_email(email, height, average_hight, people_count):
    from_email = "heightcollector@mail.ru"
    from_passw = "thisisawkward"

    subj = "Height data"
    message = f"Hello. Your height is <strong>{height}</strong>. The average height of <strong>{people_count}</strong> is <strong>{average_hight}cm</strong>."

    msg = MIMEText(message, "html")
    msg['Subject'] = subj
    msg['From'] = from_email
    msg['To'] = email

    mail = smtplib.SMTP('smtp.mail.ru', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(from_email, from_passw)

    # trying to send email if email exists
    try:
        mail.send_message(msg)
        return True
    except (smtplib.SMTPRecipientsRefused, smtplib.SMTPDataError):
        return False


if __name__ == '__main__':
    send_email("velidonimo@mail.ru", 111, 20, 5)
