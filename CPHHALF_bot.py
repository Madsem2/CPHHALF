#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests
import os

def send_slack_notification(webhook_url, message):
    payload = {
        "text": message
    }
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            print("Slack notification sent successfully")
        else:
            print(f"Failed to send Slack notification: {response.text}")
    except Exception as e:
        print(f"Failed to send Slack notification: {e}")

def check_availability(webhook_url):
    url = "https://secure.onreg.com/onreg2/bibexchange/?eventid=6277"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            unavailable_text = "II"  # Update this to match the text when tickets are unavailable
            if unavailable_text not in soup.text:
                send_slack_notification(webhook_url, "Ticket Available! Check the website: " + url)
            else:
                print("Tickets are not available at the moment.")
    except Exception as e:
        print(f"Code encountered an error: {e}")

if __name__ == "__main__":
    webhook_url = os.environ.get('https://hooks.slack.com/services/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')  # Retrieve the Slack webhook URL from environment variables

    print("Running script")
    check_availability(webhook_url)