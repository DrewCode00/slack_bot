import json

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

message_dict = {"hello world": "Hello Python!", "nice to meet you too"}

json_path = './history.json'

def is_deleted_message(data):
    if data.get("message", {}).get("message", {}).get("subtype", "") == "tombstone":
        return True

    else:
        return False

    def add_timestamp(event_ts, thread_ts):
        with open(json_path, 'r ') as f:
            data = json.load(f)

        data[event_ts] = thread_ts

        with open(json_path, 'w') as f:
            json.dump(data, f)


    def delete_timestamp(event_ts):
        with open(json_path, 'r') as f:
            data = json.load(f)

            del data[event_ts]

            with open(json_path, 'w') as f:
                json.dump(data, f)


                @app.event({"type": "message", "subtype": None})
                def message(args, say):
                    data = args.__dict__

                    user_input = data.get('event').get('text')
                    event_ts = data.get('event').get('ts')
                    channel_id = data.get('event').get("channel")

                    if "hello world" in user_input:
                        thread_ts =say(channel=channel_id, text='hello python', thread_ts= event_ts)
                        thread_ts = thread_ts.get("ts")
                        add_timestamp(event_ts, thread_ts)

                        @app.event({"type": "message", "subtype": "message_changed"})
                        def message_edit(args, say, client):
                            data = args.__dict__

                            user_input = data.get('event').get('message').get('text')
                            previous_message = data.get('event').get('previous_message').get('text')
                            event_ts = data.get('event').get('previous_message').get('ts')
                            channel_id = data.get('event').get('channel')


                            if is_deleted_message(data):
                                thread_ts =load_timestamp(event_ts)
                                try:
                                    client.chat_delete(channel=channel_id, ts=thread_ts)
                                    delete_timestamp(event_ts)
                                except:
                                    pass
                                return

                            for keyword in user_input:
                                if keyword in user_input:





    def load_timestamp(event_ts):
        with open(json_path, 'r') as f:
            data = json.load(f)
            return data.get(event_ts)

