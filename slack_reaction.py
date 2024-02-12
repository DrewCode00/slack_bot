import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()


slack_app_token = os.getenv("SLACK_APP_TOKEN")
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")

app = App(token=slack_bot_token)

@app.event('message')
def message(args, say):
    data = args.__dict__

    user_input =data.get('event').get('text')
    event_ts = data.get('event').get('ts')
    channel_id = data.get('event').get("channel")
