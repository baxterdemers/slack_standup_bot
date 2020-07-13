import smtplib
import ssl
from email.mime.text import MIMEText
from datetime import date

import config

today = date.today()
today_str = today.strftime("%B %d, %Y")
msg = MIMEText("""
Hi Team, 

Here's your weekly email: 

1. What are your main goals for this week, and what OKR's do they fit under (or not).
2. Are there any problem solvings you would like to have this week to push you forward? Any blockers?
3. Are there any big (or small) accomplishments you want to celebrate with the group? Any recent developments or decisions made?
4. What is something you thought didn't go well last week, and what can we do to be more prepared/do better next time?
""")
msg['Subject'] = "Weekly email for {}".format(today_str)
sender = config.gmail_username
recipient_lst = [config.gmail_username] if config.debug else config.weekly_to_emails
recipients =  ", ".join(recipient_lst)
msg['From'] = sender
msg['To'] = recipients
port = 465
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(config.gmail_username, config.gmail_password)
    server.sendmail(sender, recipient_lst, msg.as_string())