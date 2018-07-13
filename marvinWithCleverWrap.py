import time
import requests
from slackclient import SlackClient
from cleverwrap import CleverWrap
from yelpapi import YelpAPI

#---------------------------#
#Programmer: Joey Domino    #
#Date: 7/2/18               #
#Program:marvin for Slack   #
#Basic chatbot for now      #
#---------------------------#

SLACK_TOKEN = 'xoxb-8483522179-392696063798-IItvotS2Kd5pMiszkQarYeMx'
CLEVERBOT_TOKEN = 'CC8lzaIMoM8kVAcwNw36CJHfGDg'
YELP_TOKEN = 'nxnPpM0ToXtVZw7FholFve7bZQSLfxf_N3Zpq6zlJxAiBcaBugGNz-ddYGHCxzVnIQmfVFqMWum2POFmJDNXpQ2o9cWECukgLWkOhh7_uMujUA3cZBCtqHNvqck_W3Yx'
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
    clever_bot_called = 0
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

                #Another check for if marvin is @'ed
                if event["type"] == 'desktop_notification':
                    if "content" in event:
                        #Yelp food implementation
                        if "@marvin" and "lunch" in event["content"]:
                            slack_client.api_call(
                                "chat.postMessage",
                                channel = event["channel"],
                                text = "What're ya cravin?",
                                as_user = True)
                            lunch_check = True
                            while lunch_check:
                                for lunch_event in slack_client.rtm_read():
                                    if "text" in lunch_event:
                                        if lunch_event["text"] == "nevermind":
                                            slack_client.api_call(
                                                "chat.postMessage",
                                                channel = event["channel"],
                                                text = "Alright.",
                                                as_user = True)
                                            lunch_check = False
                                        #currently returns 3 headers "businesses, total, and region. Need to dip into businesses to get name and ratings.
                                        if lunch_event["text"] == "food":
                                            yelp_api = YelpAPI(YELP_TOKEN)
                                            print("\n\n")
                                            search_results = yelp_api.search_query(term = 'food', location = 'Detroit, MI', sort_by = 'rating', limit = 5)
                                            for header in search_results:
                                                for topic in header:
                                                    print(topic)
                                                    #slack_client.api_call(
                                                    #    "chat.postMessage",
                                                    #    channel = event["channel"],
                                                    #    text = topic + "\n\n",
                                                    #    as_user = True)
                                            #print(search_results + "\n\n")
                                            lunch_check = False
                                    
                            
                            
    return None, None

#------------------------------------------------------#
#Function: handle_command
#Use: processes command from user
#Arguments: command, channel
#Returns: none
#------------------------------------------------------#
def handle_command(command, channel, cb_convo): 
    print(command)
    
    response = call_clever_bot(command, cb_convo)
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
def call_clever_bot(message, clever_bot_convo):
    #url_params = {'input' : message, 'key' : CLEVERBOT_TOKEN}
    try:
        reply = clever_bot_convo.say(message)
        return reply
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
    cb = CleverWrap(CLEVERBOT_TOKEN)
    convo = cb.conversation()
    if(slack_client.rtm_connect()):
        print("Marvin has connected sir. As if it matters.")
        marvin_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_command(slack_client.rtm_read())
            if command:
                handle_command(command, channel, convo)
            time.sleep(READ_WEB_DELAY)
    else:
        print("RTM connection failure. Check Token dingleberry. DO IT AGAIN!")
