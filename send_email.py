from email.mime.text import MIMEText
import smtplib

def send_email(email,height,average_height,count):
    from_email = ""
    from_password = ""
    to_email = email

    subject = "Height Data"
    message = "Hey there, your height is <strong>{}</strong>cm. Average height out of {} all participants {}cm. ".format(height,count,average_height)

    msg = MIMEText(message,"html") #this means that the message line will be read as html
    msg['Subject'] = subject
    msg["To"] = to_email
    msg["From"] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email,from_password)
    gmail.send_message(msg)


