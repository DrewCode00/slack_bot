from dotenv import load_dotenv


import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()


slack_app_token = os.getenv("SLACK_APP_TOKEN")
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")

history = {}_# Save timestamp history, but unstable

message_dict = {"hello world": "Hello python!", "nice to meet you too"}

app = App(token=slack_bot_token)




@app.event({"type": "message", "subtype": None})
def message(args, say):
    data = args.__dict__

    user_input =data.get('event').get('text')
    event_ts = data.get('event').get('ts')
    channel_id = data.get('event').get("channel")

    if "hello world" in user_input:
       thread_ts = say(channel=channel_id, text='Hello Python!', thread_ts=event_ts)
       thread_ts =thread_ts.get("ts")
       history[event_ts] = thread_ts


@app.event({"type": "message", "subtype": "message_changed"})
def message_edit(args, say, client):
    data = args.__dict__

    user_input = data.get('event').get('message').get('text')
    event_ts = data.get('event').get('previous_message').get('ts')
    channel_id = data.get('event').get("channel")
    subtype = data.get('event').get('message').get('subtype')

    if sub_type == 'bot_message': # To prevent the bot from responding to it's own message
        return

    for keyword in message_dict.keys():
        if keyword in user_input:
            if history.get(event_ts) is not None: # If bot message is already existed
                thread_ts = history.get(event_ts)
                client.chat_update(channel=channel_id, text=message_dict[keyword], ts=thread_ts)
                return
            else: # if bot message is not existed
                thread_ts =say(channel=channel_id, text=message_dict[keyword], thread_ts= event_ts)
                thread_ts =thread_ts.get("ts")
                history[event_ts] = thread_ts
                return


  handler = SocketModeHandler(app, slack_app_token)
    handler.start()