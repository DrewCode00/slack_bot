from dotenv import load_dotenv

import os
from slack_bolt.app import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

slack_app_token = os.getenv("SLACK_APP_TOKEN")
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")

history = {}

app = App(token=slack_bot_token)

@app.event({"type": "message", "subtype": None})
def message(args, say):
    data = args.__dict__

    user_input = data.get('event').get('text')
    event_ts = data.get('event').get('ts')
    channel_id = data.get('event').get("channel")

    if "hello" in user_input:
        if channel_id == "C06BUQNKFC1":
            message = 'This is channel 1'
            emoji = "one"
            bot_name = "Channel 1"
        elif channel_id == "C06C4FGCYCU":
            message = 'This is channel 2'
            emoji = "two"
            bot_name = "Channel 2"
        else:
            return
        thread_ts = say(channel=channel_id, text=message, thread_ts=event_ts, icon_emoji=emoji, username=bot_name)
        thread_ts = thread_ts.get("ts")
        history[event_ts] = thread_ts


handler = SocketModeHandler(app, slack_app_token)
handler.start()