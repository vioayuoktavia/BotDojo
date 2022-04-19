import os
import logging, secrets
from flask import Flask, jsonify
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from bot_for_dojo import DojoBot
from flask_ngrok import run_with_ngrok
from random import randint


# Initialize a Flask app to host the events adapter
app = Flask(__name__)
run_with_ngrok(app)
# Create an events adapter and register it to an endpoint in the slack app for event injestion.
slack_events_adapter = SlackEventAdapter("b608ebfde2f137f19171e1b26df23c3e", "/slack/events", app)
# print(slack_events_adapter)

# Initialize a Web API client
#Bot Dojo
slack_web_client = WebClient("xoxb-3337749177426-3375191433860-f6klSfgXWP6gAZ33wXc7XUfn")
#Bot Food
# slack_web_client = WebClient("xoxb-3403362312805-3418880221297-O1P9WNXfFxzAQBHKKVzA9aKq")

def report(channel):
    """Craft the CoinBot, flip the coin and send the message to the channel
    """
    # Create a new CoinBot
    bot = DojoBot(channel)

    # Get the onboarding message payload
    message = bot.get_message_payload()

    # Post the onboarding message in Slack
    slack_web_client.chat_postMessage(**message)

@app.route('/slack/weather', methods=["POST"])
def weather():
    status = "failed"
    channel_id = "dojo-demo"
    # channel_id = "q2-budget"

    weather_slash = DojoBot(channel_id)

    message = weather_slash.weather_message_payload()
    sending_message = slack_web_client.chat_postMessage(**message)
    if sending_message:
        status = "success"

    return jsonify(status)

@app.route('/slack/kucing', methods=["POST"])
def kucing():
    status = "failed"
    channel_id = "dojo-demo"
    # channel_id = "q2-budget"

    sending_message = slack_web_client.files_upload(
                        channels=channel_id,
                        file="./images/kucing%i.jpeg" % randint(1, 6)
                    )
    if sending_message:
        status = "success"

    return jsonify(status)


# When a 'message' event is detected by the events adapter, forward that payload
# to this function.
@slack_events_adapter.on("message")
def message(payload):
    """Parse the message event, and if the activation string is in the text, 
    simulate a coin flip and send the result.
    """

    # Get the event data from the payload
    event = payload.get("event", {})

    # Get the text from the event that came through
    text = event.get("text")

    # Check and see if the activation phrase was in the text of the message.
    # If so, execute the code to flip a coin.
    if "report" in text.lower():
        # Since the activation phrase was met, get the channel ID that the event
        # was executed on
        channel_id = event.get("channel")

        return report(channel_id)

if __name__ == "__main__":
    # Create the logging object
    logger = logging.getLogger()

    # Set the log level to DEBUG. This will increase verbosity of logging messages
    logger.setLevel(logging.DEBUG)

    # Add the StreamHandler as a logging handler
    logger.addHandler(logging.StreamHandler())

    # Run our app on our externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run()