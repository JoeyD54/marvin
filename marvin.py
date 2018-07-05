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
#Function: parse_command
#Use: checks for if marvin was called (!m or marvin)
#   Ignores teambuilding channel
#Arguments: slack_events
#Returns: command, channel
#------------------------------------------------------#
def parse_command(slack_events):
    for event in slack_events:
        if "channel" in event:
            if event["channel"] == "C08E7RN72":
                return None, None
            else:
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
                if event["type"] == 'desktop_notification':
                    if "content" in event:
                        if "leave channel" in event["content"]:
                            channel = event["channel"]
                            slack_client.api_call(
                                "chat.postMessage",
                                channel = channel,
                                text = "Leaving channel: <!channel>",
                                as_user = True)
                            slack_client.api_call(
                                "channels.leave",
                                channel = channel)
    return None, None

#------------------------------------------------------#
#Function: handle_command
#Use: processes command from user
#Arguments: command, channel
#Returns: none
#------------------------------------------------------#
def handle_command(command, channel, convo_started):
    #if 
    #print(command)
    response = call_clever_bot(command, convo_started)
    #print(response)
    slack_client.api_call(
        "chat.postMessage",
        channel = channel,
        text = response,
        as_user = True)

#------------------------------------------------------#
#Function: call_clever_bot
#Use: calls cleverbot API to receive and return messages to main
#Arguments: message (user's inputted message)
#Returns: response (API's response to user message)
#------------------------------------------------------#
def call_clever_bot(message, convo_started):
    #url_params = {'input' : message, 'key' : CLEVERBOT_TOKEN}
    try:
        if convo_started is 0:
            cb = cleverbot.Cleverbot(CLEVERBOT_TOKEN, cs='76nxdxIJ02AAA', timeout=60, tweak1=0, tweak2=100, tweak3=100)
            convo = cb.conversation()
            print("\n\nNew conversation started\n\n")
            convo_started = 1
        reply = convo.say(message)
        return reply
    #data received correctly. Get response to print now.
        #return reply.get("output", None)
    except cleverbot.APIError as e:
        print(e.error, e.status)


#main gatta be on the bottom. Code runs top to bottom. Functions need to be init'd first. For future notice (because Joey forgets things).
#------------------------------------------------------#
#Function: main
#Use: main processing of script
#Arguments: none
#Return: none
#------------------------------------------------------#
if __name__ == '__main__':
    slack_client = SlackClient(SLACK_TOKEN)
    convo_started = 0
    if(slack_client.rtm_connect()):
        print("Marvin has connected sir. As if it matters.")
        marvin_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_command(slack_client.rtm_read())
            if command:
                handle_command(command, channel, convo_started)
            time.sleep(READ_WEB_DELAY)
    else:
        print("RTM connection failure. Check Token dingleberry. DO IT AGAIN!")
