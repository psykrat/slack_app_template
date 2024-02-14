from flask import Flask, request, jsonify
import json
import os
import hmac
import hashlib
import handlers
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from modals import main_menu_modal, home_view
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

def verify_slack_request(request):
    slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
    request_body = request.get_data().decode('utf-8')
    timestamp = request.headers['X-Slack-Request-Timestamp']
    sig_basestring = f"v0:{timestamp}:{request_body}"
    my_signature = 'v0=' + hmac.new(
        bytes(slack_signing_secret, 'utf-8'),
        msg=bytes(sig_basestring, 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()
    
    slack_signature = request.headers['X-Slack-Signature']
    return hmac.compare_digest(my_signature, slack_signature)

@app.route('/slack/command', methods=['POST'])
def handle_slack_command():
    if not verify_slack_request(request):
        return "Request verification failed", 401
    
    modal_payload = main_menu_modal()
    
    return jsonify(modal_payload)

@app.route('/slack/events', methods=['POST'])
def slack_events():
    if not verify_slack_request(request):
        return "Request verification failed", 401

    event_data = request.get_json()

    if 'challenge' in event_data:
        return jsonify({'challenge': event_data['challenge']})

    if event_data['event']['type'] == 'app_home_opened':
        user_id = event_data['event']['user']
        try:
            client.views_publish(
                user_id=user_id,
                view=home_view()
            )
        except SlackApiError as e:
            print(f"Error publishing to App Home: {e}")

    return "", 200

@app.route('/slack/interactive', methods=['POST'])
def handle_interactive():
    payload = json.loads(request.form["payload"])
    action_id = payload['actions'][0]['action_id']

    if action_id == 'action1':
        response = handlers.handle_action1()
    elif action_id == 'action2':
        response = handlers.handle_action2()
    # Additional actions here
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
