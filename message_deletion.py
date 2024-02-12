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

def is_deleted_message(data):
    if data.get("message", {}).get("message", {}).get("subtype", "") == "tombstone":
        return True
    else:
        return False

    @app.event({"type": "message", "subtype": None})
    def message(args, say):
        data = args.__dict__



    user_input =data.get('event').get('text')
    event_ts = data.get('event').get('ts')
    channel_id = data.get('event').get("channel")
    sub_type = data.get('event').get('message').get('subtype')

    if sub_type == 'bot_message' : #To prevent Bot from responding to it's own message.
        return

    if is_deleted_message(data)
        thread_ts = hsitory.get(event_ts)
        try:
            client.chat_delete(channel_id, ts=thread_ts)
            del hsitory[event_ts]
        except:
            pass
        return



    if "hello world" in user_input:
       thread_ts = say(channel=channel_id, text='Hello Python!', thread_ts=event_ts)
       thread_ts =thread_ts.get("ts")
       history[event_ts] = thread_ts
       return


for keyword in message_dict.keys():
    if keyword in user_input:
        if previous_message ! = user_input:
            if history.get(event_ts) is not None:
                thread_ts = history.get(event_ts)
                client.chat_update(channel=channel_id, text=message_dict[keyword], ts=thread_ts)

                return
            else:
                thread_ts = say(channel=chnanel_id, text=message_dict[keyword], thread_ts= event_ts)
    @app.event({"type": "message", "subtype": "message_deleted"})
    def message_deleted(args, client):
        data = args.__dict__

        event_ts =data.get('event').get('previous_message').get('tx')
        channel_id =data.get('event').get("channel")

        if event_ts in history.keys():
            thread_ts = history.get(event_ts)
            try:
                client.chat_delete(channel=channel_id, ts= thread_ts)
                del history[event_ts]
            except:
                pass

            handler = SocketModeHandler(app, slack_app_token)
            handler.start()