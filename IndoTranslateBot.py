import praw
import config
import time
import datetime
import os
from googletrans import Translator 
import preconfig
from praw.models import Message
from praw.models import Comment

#List of languages that the bot translates. Language codes from https://cloud.google.com/translate/docs/languages
languages = ["hi", "ml", "ta", "te", "ur", "gu", "bn", "kn", "mr", "ne", "pa"]

#Checks if language is on the languages list
def is_indo_lang(language):
    global languages
    if language in languages:
        return True
    else:
        return False

#Creates the formatted reply for a translation
def get_formatted_text(translation):
    formatted_text = ">(" + translation + ")" + preconfig.comment_subtext
    return formatted_text

def log_activity(log_text):
    ts = time.time()
    print(log_text)
    timestamp = str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
    with open("activity_log.txt", "a") as writer:
        writer.write(timestamp + " -- " + log_text + "\n")

#Logs into reddit with the details in config.py
def login():
    print("Trying to log in...")
    reddit = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = config.user_agent)
    print("Logged in!")
    return reddit

#Translates comments if they are in certain language and replies with english translation
def translate_comments(reddit, replied_comments, translator, my_limit):
    print("Running bot...")
    for comment in reddit.subreddit('india').comments(limit=my_limit):
        try:
            if comment.id not in replied_comments:
                mytext = str(comment.body)
                detection = translator.detect(mytext)
                if is_indo_lang(detection.lang) and comment.author != reddit.user.me():
                    log_activity("Replied to: " + comment.author.name + ", comment was in: " + detection.lang + ", confidence of: " + str(float(detection.confidence)))
                    translation = translator.translate(mytext).text
                    #print("Translation was: " + translation)
                    reply_text = get_formatted_text(translation)
                    comment.reply(reply_text)

                    replied_comments.append(comment.id)

                    with open("replied_comments.txt", "a") as writer:
                        writer.write(comment.id + "\n")
        except Exception as e:
            print("ERROR - " + str(e))

            replied_comments.append(comment.id)

            with open("replied_comments.txt", "a") as writer:
                writer.write(comment.id + "\n")

#Reply to any Private Messages
def reply_to_pm(reddit):
    unread_messages = []
    for pm in reddit.inbox.unread():
        if isinstance(pm, Message) or isinstance(pm, Comment):
            pm.author.message("I am just a bot!", preconfig.pm_message)
            log_activity("Replied to a PM from: " + pm.author.name)
            unread_messages.append(pm)
    reddit.inbox.mark_read(unread_messages)

#Get the list of comments the bot has replied to
def get_replied_comments():
    print("Loading replied comments list...")
    if not os.path.isfile("replied_comments.txt"):
        replied_comments = []
    else:
        with open("replied_comments.txt", "r") as myfile:
            replied_comments = myfile.read()
            replied_comments = replied_comments.split("\n")
            replied_comments = list(filter(None, replied_comments))
    
    return replied_comments

#Delete comment if it has score of less than -1
def delete_downvoted_comment(reddit):
    user = reddit.user.me()
    for comment in user.comments.controversial(limit=50):
        if comment.score < -1:
            log_activity("Deleting comment due karma threshold: " + comment.id)
            comment.delete()

#START
print(config.user_agent)
reddit = login()
replied_comments = get_replied_comments()
translator = Translator()

while True:
    translate_comments(reddit, replied_comments, translator, 10)
    reply_to_pm(reddit)
    delete_downvoted_comment(reddit)
    print("Sleeping...")
    time.sleep(5)
