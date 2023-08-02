import os
import json
import logging
import time


from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

#local imports
#from my slack channel
#loads secrets created on operating system  (environmental variables)
load_dotenv()

#create logging object
logger = logging.getLogger(__name__)
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

#respond to /huh command
@app.command("/huh")
def open_modal(ack, body, client):
    #acknowledge received request
    ack()
    #logo
    logo = "LINK HERE"

    #call views_open with built-in client
    client.views_open(
        trigger_id = body["tigger_id"],
        view = {
            "type": "modal",
            "callback_id" : "task-menu",
            "title": {
                "type": "plain_text",
                "text": "Mihika's Slack Bot",
                "emoji": True,
            },
            "close": {"type": "plain_text", "text": "cancel", "emoji": True},
            "blocks" :[
                {
                    "type": "image",
                    "image_url" : logo,
                    "alt_text": "Mihika slack bot",
                },
                {"type": "divider"},
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Please select a task",
                        "emoji": True,
                    },
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text" : {
                        "type": "plain_text",
                        "text": "Retrieve address objects",
                        "emoji": True,
                    },
                    "accessory" : {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Click Here"},
                        "action_id": "address_objects",
                    },
                },
                {
                    "type": "section",
                    "text" : {
                        "type": "plain_text",
                        "text": "Run automated Reports",
                        "emoji": True,
                    },
                     "accessory" : {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Click Here"},
                        "action_id": "automated_reports",
                    },
                },
            ],
        },
    )

    @app.action("address_objects")
    def address_objects_view(ack, body, client):
        ack(response_action = "clear")
        client.views_update(
            view_id = body["view"]["id"],
            hash = body["view"]["hash"],
            view = {
                "type" = "modal",
                "callback_id" : "address_objects",
                "private_metadata": json.dumps(body),
                "title": {
                    "type" :"plain_text",
                    "text" : "MihikaBot",
                    "emoji": True,
                },
                "blocks" : [
                    {
                        "type": "header",
                        "text": {
                             "type" :"plain_text",
                             "text": ":bar_chart: Address Objects",
                             "emoji": True,
                        },
                    }, 
                    {
                        "type": "context",
                        "elements" : [
                            {
                            "text": "Retrieve address objects",
                            "type": "mrkdwn",
                            },
                        ],
                    },
                    {
                        "type": "divider",
                    },
                    {
                        "type":"section",
                        "text": {
                            "type" :"mrkdwn",
                            "text": " :spiral_note_pad: *List of addresses*",
                        },
                    },
                    {
                        "type": "input",
                        "block_id" : "folder",
                        "element": {
                            "type": "plain_text_input",
                            "initial_value" : "Shared",
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Name of folder",
                            "emoji": True,
                        },
                    },
                    {
                        "type": "divider",
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text" : ":pushpin: Do you have something that you would like to see automated?",
                            }
                        ],
                    },
                ],
                "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
                "close": {"type": "plain_text", "text": "close", "emoji": True},
            },
        )
        #when name of folder text inport is submitted in secondary view
        

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, "SLACK_BOT_TOKEN").start()
    #SocketModeHandler.start(port=int(os.environ.get("PORT", 3000)))
