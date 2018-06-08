import praw
import config
import time
import os
from googletrans import Translator 

languages = ["hi", "ml", "ta", "te", "ur", "gu", "bn", "kn", "mr", "ne", "pa"]

def is_indo_lang(language):
    global languages
    if language in languages:
        return True
    else:
        return False


def login():
    print("Trying to log in...")
    reddit = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = config.user_agent)
    print("Logged in!")
    return reddit

def run(reddit, replied_comments, translator):
    print("Running bot...")
    for comment in reddit.subreddit('test').comments(limit=10):
        try:
            mytext = str(comment.body)
            detection = translator.detect(mytext)
            if is_indo_lang(detection.lang) and comment.id not in replied_comments and comment.author != reddit.user.me():
                print("Replied to: " + comment.author.name + " ,comment was in: " + detection.lang)
                translation = translator.translate(mytext).text
                #print("Translation was: " + translation)
                comment.reply(translation)

                replied_comments.append(comment.id)

                with open("replied_comments.txt", "a") as writer:
                    writer.write(comment.id + "\n")
        except Exception as e:
            print("ERROR - " + str(e))

def get_replied_comments():
    if not os.path.isfile("replied_comments.txt"):
        replied_comments = []
    else:
        with open("replied_comments.txt", "r") as myfile:
            replied_comments = myfile.read()
            replied_comments = replied_comments.split("\n")
            replied_comments = list(filter(None, replied_comments))
    
    return replied_comments

reddit = login()
replied_comments = get_replied_comments()
translator = Translator()

while True:
    run(reddit, replied_comments, translator)
    print("Sleeping...")
    time.sleep(5)
