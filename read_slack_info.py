from dotenv import load_dotenv

import os
from slack_bolt.app import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

slack_app_token = os.getenv("SLACK_APP_TOKEN")
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")

app = App(token=slack_bot_token)

@app.event('message')
def message(args):
    print(args.__dict__)

    data = args.__dict__

    print("channel_id =", data["context"]["channel_id"])
    print("text =", data.get("body").get('event').get("text"))


handler = SocketModeHandler(app, slack_app_token)
handler.start()