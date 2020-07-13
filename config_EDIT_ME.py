debug = False

slack_token = ''

slack_channel_prod = ''
slack_channel_debug = ''

slack_channel = slack_channel_debug if debug else slack_channel_prod
standup_member_IDs = {} if debug else {}


gmail_password = ''
gmail_username = ''

standup_to_emails = []
weekly_to_emails = []