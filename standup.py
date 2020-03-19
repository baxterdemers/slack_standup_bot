# -*- coding: utf-8 -*-
import json
import time
import smtplib
import ssl
import pickle

import slack

import config

def conformToAscii(text):
    text = text.replace('•', '-')
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

def send_email(msg_lst):
    port = 465  # For SSL
    # Create a secure SSL context
    context = ssl.create_default_context()
    sender_email = config.gmail_username
    ascii_msg_lst = list(map(conformToAscii, msg_lst)) #necessary to use the SMTP_SSL mail server
    message = "Subject: PGP Daily Standup \n\nPGP Daily Standup: \n\n{}".format("\n\n".join(ascii_msg_lst))
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(config.gmail_username, config.gmail_password)
        if config.debug:
            server.sendmail(sender_email, sender_email, message)
        else:
            server.sendmail(sender_email, config.to_emails, message)

def slack_message(message, channel=config.slack_channel):
    response = sc.chat_postMessage(channel=channel,text=message, username='Standup Bot', icon_emoji=':robot_face:')
    thread_ts = response['ts']
    return thread_ts
    
if __name__ == "__main__":
    #reset the message file (to be used for persistent asynchronous communication with the listener.py proccess)
    with open('msg_lst', 'wb') as f:
        msg_lst = []
        pickle.dump(msg_lst, f)

    sc = slack.WebClient(config.slack_token)

    # thread time stamp serves as a way to identify messages which are replies to the standup request
    # replies will have a 'thread_ts' field equal to the ts of this request (ts = timestamp)
    thread_ts = slack_message("""Good morning <!channel>! Reply to this thread with
    • what you worked on yesterday
    • what you’re planning to working on today
    • a list of any blockers you have.""")

    # puts the thread_ts in persistent storage so that the listener.py can asynchronously access it
    with open('thread_ts_pickle', 'wb') as f:
        pickle.dump(thread_ts, f)

    time.sleep(54 if config.debug else 5400) # wait 1.5 hours
    slack_message("Reminder - only 30 minutes left to submit your standup report.")
    time.sleep(18 if config.debug else 1800) # wait .5 hours
    slack_message("Responses are closed for today - emailing Baxter the responses")

    # reads the list of standup reports collected by listener.py
    with open('msg_lst', 'rb') as f:
        msg_lst = pickle.load(f)
        print("msg_lst : ", msg_lst)

    send_email(msg_lst)

