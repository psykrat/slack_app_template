# slack_app_template
A template for building Slack apps in Python using Flash and Slack SDK.

---

## Introduction

This Flask application template is designed to kick-start your Slack app development, providing a foundational structure for handling Slack commands, events, and interactive components. By leveraging the Slack SDK for Python, it simplifies the process of integrating your application with Slack, enabling you to focus on developing unique features for your Slack app.

## Prerequisites

To make the most of this template, ensure you have:

- Python 3.8 or newer installed on your machine.
- pip for installing Python packages.
- A Slack account and a new Slack app created at [api.slack.com/apps](https://api.slack.com/apps).

## Utilizing the Template for Slack App Development

### Environmental Variables

Set `SLACK_BOT_TOKEN` and `SLACK_SIGNING_SECRET` in your `.env` file to authenticate requests and communicate securely with Slack's API.

### Handling Slack Commands and Events

- **Commands**: Define new slash commands in Slack and handle them in `@app.route('/slack/command', methods=['POST'])`.
- **Events**: Subscribe to events in your Slack app settings. Use `@app.route('/slack/events', methods=['POST'])` to process these events, such as welcoming users when they first open the app home.

### Interactive Components

For handling interactive actions (buttons, select menus, date pickers, etc.), implement your logic within `@app.route('/slack/interactive', methods=['POST'])`. Decode the incoming payload to identify the action and respond accordingly.

### Extending the Template

- **Handlers**: Add new functions in `handlers.py` to manage custom logic for commands and interactive actions.
- **Views**: Use `modals.py` to define the JSON structures of modals and message blocks. Customize or extend this to create dynamic and engaging UI components for your app.

### Running in Production

Before deploying, switch Flask's debug mode off by setting `debug=False` in `app.py`. For production environments, consider using a WSGI server like Gunicorn for better performance and reliability.
