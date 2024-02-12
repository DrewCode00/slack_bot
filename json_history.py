from dotenv import load_dotenv

import os
import json
from slack_bolt.app import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

slack_app_token = os.getenv("SLACK_APP_TOKEN")
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")

app = App(token=slack_bot_token)

message_dict = {"hello world": "hello python!", "nice to meet you": "nice to meet you too!"}

json_path = './history.json'

def is_deleted_message(data):
    if data.get("message", {}).get("message", {}).get("subtype", "") == "tombstone":
        return True
    else:
        return False

def load_timestamp(event_ts):
    with open(json_path, 'r') as f:
        data = json.load(f)
        return data.get(event_ts)

def add_timestamp(event_ts, thread_ts):
    with open(json_path, 'r') as f:
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
        thread_ts = say(channel=channel_id, text='hello python!', thread_ts=event_ts)
        thread_ts = thread_ts.get("ts")
        add_timestamp(event_ts, thread_ts)

@app.event({"type": "message", "subtype": "message_changed"})
def message_edit(args, say, client):
    data = args.__dict__

    user_input = data.get('event').get('message').get('text')
    previous_message = data.get('event').get('previous_message').get('text')
    event_ts = data.get('event').get('previous_message').get('ts')
    channel_id = data.get('event').get("channel")

    if is_deleted_message(data):
        thread_ts = load_timestamp(event_ts)
        try:
            client.chat_delete(channel=channel_id, ts=thread_ts)
            delete_timestamp(event_ts)
        except:
            pass
        return

    for keyword in message_dict.keys():
        if keyword in user_input:
            if previous_message != user_input:  # "To prevent other messages within the thread from being modified together.
                thread_ts = load_timestamp(event_ts)
                if thread_ts is not None:  # if bot message is already existed
                    client.chat_update(channel=channel_id, text=message_dict[keyword], ts=thread_ts)
                    return
                else:  # if bot message is not existed
                    thread_ts = say(channel=channel_id, text=message_dict[keyword], thread_ts=event_ts)
                    thread_ts = thread_ts.get("ts")
                    add_timestamp(event_ts, thread_ts)
                    return

@app.event({"type": "message", "subtype": "message_deleted"})
def message_delete(args, client):
    data = args.__dict__

    event_ts = data.get('event').get('previous_message').get('ts')
    channel_id = data.get('event').get("channel")

    thread_ts = load_timestamp(event_ts)

    if thread_ts is not None:
        try:
            client.chat_delete(channel=channel_id, ts=thread_ts)
            delete_timestamp(event_ts)
        except:
            pass

@app.event({"type": "reaction_added"})
def add_emoji_message(args, say):
    data = args.__dict__

    message_ts = data.get('body').get('event').get('item').get('ts')
    channel_id = data.get('body').get('event').get('item').get('channel')
    reaction = data.get('body').get('event').get('reaction')

    if reaction == 'wave':
        thread_ts = say(channel=channel_id, text='hello!', thread_ts=message_ts)
        thread_ts = thread_ts.get("ts")
        add_timestamp(message_ts, thread_ts)

@app.event({"type": "reaction_removed"})
def del_emoji_message(args, client):
    data = args.__dict__

    message_ts = data.get('body').get('event').get('item').get('ts')
    channel_id = data.get('body').get('event').get('item').get('channel')
    reaction = data.get('body').get('event').get('reaction')

    thread_ts = load_timestamp(message_ts)

    if reaction == 'wave':
        if thread_ts is not None:
            try:
                client.chat_delete(channel=channel_id, ts=thread_ts)
                delete_timestamp(message_ts)
            except:
                pass


handler = SocketModeHandler(app, slack_app_token)
handler.start()