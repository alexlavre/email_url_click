from config import SLACK_TOKEN
from slack import WebClient
from slack.errors import SlackApiError


def send_slack_alert(text, data):
    try:
        client = WebClient(SLACK_TOKEN)
        response = client.chat_postMessage(
            channel=data['channel'],
            text=text,
            thread_ts=data['ts']
        )
        return response
    except SlackApiError as e:
        print(e)
