import os
import json

import requests
import slack

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from databricks_langchain import ChatDatabricks

app = App(token=os.environ["BOT_TOKEN"])
client = slack.WebClient(token=os.environ['BOT_TOKEN'])
bot_id = client.api_call('auth.test')['user_id']

@app.event("app_mention")
def mention_handler(event, say, logger):
    # Extract message basic data
    user_id = event['user'] #channel_id = event['channel']
    text = event['text']

    # Create and send answer
    if bot_id != user_id:
        chat_model = ChatDatabricks(
            endpoint=os.environ['RAG_ENDPOINT_NAME'], 
            temperature=0.1,
            max_tokens=250,
        )

        reply = chat_model.invoke(text)
        say("Um momento...")
        say(reply.content)

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["APP_TOKEN"])
    handler.start()
