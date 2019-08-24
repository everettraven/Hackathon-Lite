import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"

receiver_email = "jhaddixpymail1000@gmail.com"
message = """\
Subject: Canvas Alert!

Hello, World! This is a canvas alert!"""    
   
def sendEmail(receiver_email, message):
    sender_email = "jhaddixpymail1000@gmail.com"
    password = "xXwinrar69Xx"
   
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
