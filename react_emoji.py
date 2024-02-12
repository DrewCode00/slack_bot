


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

def add_emoji_message(args, say):

   data = args.__dict__

   message_ts = data.get('body').get('event').get('item').get('ts')
   channel_id = data.get('body').get('event').get('item').get('channel')
   reaction = data.get('body').get('event').get('reaction')

   if reaction = 'wave':
       thread_ts = say(channel_id, text='hello', thread_ts=message_ts)
       thread_ts =thread_ts.get('ts')
       history[message_ts] = thread_ts


       @app.event({"type": "reaction_removed"})
    def del_emoji_message(args, client):
        data = args.__dict__

        message_ts = data.get('body').get('event').get('item').get('ts')
        channel_id = data.get('body').get('event').get('item').get('channel')
        reaction = data.get('body').get('event').get('reaction')


     if reaction == 'wave'
         if message_ts in history.key():
             thread_ts = hsitory.get(mmessage_ts)

             try:
                 client.chat_delete(channel=channel_id, ts=thread_ts
                                    del history(message_ts))
             except:
                 pass

