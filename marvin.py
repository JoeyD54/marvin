import time
from slackclient import SlackClient
import cleverbot
import requests

#---------------------------#
#Programmer: Joey Domino    #
#Date: 7/2/18               #
#Program:marvin for Slack   #
#Basic chatbot for now      #
#---------------------------#

SLACK_TOKEN = 'xoxb-8483522179-392696063798-IItvotS2Kd5pMiszkQarYeMx'
CLEVERBOT_TOKEN = 'CC8lzaIMoM8kVAcwNw36CJHfGDg'
#Must append URL with ?input=input&key=CLEVERBOT_TOKEN to function
CLEVERBOT_URL = 'https://www.cleverbot.com/getreply'
marvin_id = None
READ_WEB_DELAY = 1   #1 second delay between each RTM read

#------------------------------------------------------#
#Function: call_clever_bot
#Use: calls cleverbot API to receive and return messages to main
#Arguments: message (user's inputted message)
#Returns: response (API's response to user message)
#------------------------------------------------------#
def call_clever_bot(message):
    url_payload = {'input' : message, 'key' : CLEVERBOT_TOKEN}
    return_data = requests.get(CLEVERBOT_URL, url_payload)
    #data received correctly. Get response to print now.
    
    return

#------------------------------------------------------#
#Function: parse_command
#Use: checks for if marvin was called (!m or marvin)
#Arguments: slack_events
#Returns: command, channel
#------------------------------------------------------#
def parse_command(slack_events):
    for event in slack_events:
        print(event)
        #Check event type, then check if user is in it.
        if event["type"] == "message":
            if "user" in event:
                if event["user"] != "UBJLG1VPG":
                    event_text = event["text"].lower()
                    if event["type"] == "message" and not "subtype" in event:
                        if event_text.startswith("!m") or "marvin" in event_text:
                            if event_text.startswith("!m"):
                                event_text = event_text[3:]
                            return event_text, event["channel"]
        #Idea: have bot respond snarkily if used is in "typing" state for a minute.
        #if event["type"] == "typing":

        #Idea: make another check for if marvin is @'ed
        #if event["type"] == 'desktop_notification':
    return None, None

#------------------------------------------------------#
#Function: handle_command
#Use: processes command from user
#Arguments: command, channel
#Returns: none
#------------------------------------------------------#
def handle_command(command, channel):
    #if 
    print(command)
    call_clever_bot(command)
    #print(clever_bot_response)
    #slack_client.api_call(
    #    "chat.postMessage",
    #    channel = channel,
    #    text = command,
    #    as_user = True)

#main gatta be on the bottom. Code runs top to bottom. Functions need to be init'd first. For future notice (because Joey forgets things).
#------------------------------------------------------#
#Function: main
#Use: main processing of script
#Arguments: none
#Return: none
#------------------------------------------------------#
if __name__ == '__main__':
    slack_client = SlackClient(SLACK_TOKEN)
    if(slack_client.rtm_connect()):
        print("Marvin has connected sir. As if it matters.")
        marvin_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_command(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(READ_WEB_DELAY)
    else:
        print("RTM connection failure. Check Token dingleberry. DO IT AGAIN!")
