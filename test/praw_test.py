import praw
import config
import time
import os

def login():
    print("Trying to log in...")
    reddit = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = config.user_agent)
    print("Logged in!")
    return reddit

def run(reddit, replied_comments):
    print("Running bot...")
    for comment in reddit.subreddit('test').comments(limit=25):
        if "randomword" in comment.body and comment.id not in replied_comments and comment.author != reddit.user.me():
            print("Replied to " + comment.author.name)
            #comment.reply("OK")

            replied_comments.append(comment.id)

            with open("replied_comments.txt", "a") as writer:
                writer.write(comment.id + "\n")

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

while True:
    run(reddit, replied_comments)
    print("Sleeping...")
    time.sleep(5)
