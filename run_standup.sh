cd /home/ubuntu/slack_standup_bot
source standup_ve/bin/activate
python3 listener.py &
python3 standup.py
pkill -9 -f listener.py
