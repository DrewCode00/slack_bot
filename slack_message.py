import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()


slack_app_token = os.getenv("SLACK_APP_TOKEN")
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")

app = App(token=slack_bot_token)

@app.event('message')
def message(args, client):
    data = args.__dict__

    user_input =data.get('event').get('text')
    event_ts = data.get('event').get('ts')
    channel_id = data.get('event').get("channel")

    if "good" in user_input:
        client.reactions_add(
            channel=channel_id,
            timestamp=event_ts,
            name="thumbsup"
        )

        time.sleep(5)

        client.reactions_remove(
            channel=channel_id,
            timestamp=event_ts,
            name="thumbsup"
        )

        handler =SocketModeHandler(app, slack_app_token)
        handler.start()
