import praw
import config
import time

def login():
    print("Trying to log in...")
    reddit = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = config.user_agent)
    print("Logged in!")
    return reddit



def run(reddit):
    print("Running bot...")
    for comment in reddit.subreddit('test').comments(limit=25):
        if "randomword" in comment.body:
            print("Found Word!")
            comment.reply("OK")

reddit = login()
while True:
    run(reddit)
    print("Sleeping...")
    time.sleep(5)
