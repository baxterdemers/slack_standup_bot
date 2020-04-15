import json
import traceback
import time
import smtplib
import ssl
import pickle

import slack
import requests

import config

def getUsername(user_id):
    print('user: ', user_id)
    r = requests.get('https://slack.com/api/users.info', params={'token': config.slack_token, 'user': user_id})
    print("reponse: ", r)
    body = json.loads(r.text)
    username = body['user']['name']
    real_name = body['user']['real_name']   
    return username, real_name

@slack.RTMClient.run_on(event='message')
def record_msg(**payload):
    data = payload['data']
    print("got message")
    try:
        if data['message']['subtype'] == 'bot_message':
            return
    except:
        pass
    try:
        if data['subtype'] == 'bot_message':
            return
    except:
        pass
    try:
        with open('thread_ts_pickle', 'rb') as f:
            thread_ts = pickle.load(f)
        print("Thread_TS = ", thread_ts)
    except:
        pass
    print(data.get('text', []))
    if "subtype" in data:
        if data["subtype"] == "message_changed":
            print("reply: ", data['message']['text'])
            data = data['message']
    if 'thread_ts' in data and data['thread_ts'] == thread_ts:
        real_name = data['user']
        user_standup = data.get('text', [])
        with open('msg_lst', 'rb') as f:
            member_ID_to_standup = pickle.load(f)
        member_ID_to_standup[real_name] = user_standup
        with open('msg_lst', 'wb') as f:
            pickle.dump(member_ID_to_standup, f)

def run():
    print("running proc")
    with open('msg_lst', 'wb') as f:
        var = {}
        pickle.dump(var, f)
    rtm_client = slack.RTMClient(token=config.slack_token)
    print("starting lister... ")
    rtm_client.start()

if __name__ == "__main__":
    run()
