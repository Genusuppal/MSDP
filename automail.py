import yagmail
import os
import datetime

def send_email():
    date = datetime.date.today().strftime("%B %d, %Y")
    sub = "Defaulter Report for " + str(date)
    # mail information
    yag = yagmail.SMTP(user = "sqera.theopengate@gmail.com", password = "Sqera!@#1")

    # sent the mail
    yag.send(
        to="navdeepuppal1609@gmail.com",
        subject=sub, # email subject
        contents="hi................................\n................................",  # email body
        attachments= "StudentDetails"+os.sep+"Defaulters.csv"  # file attached
    )
    print("Email Sent!")
