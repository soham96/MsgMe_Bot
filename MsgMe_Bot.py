import praw
import datetime as dt
import random
import time
from multiprocessing import Process
import re

def publicize(comment_id):
    
    text=("Hi there! I see you used the remind me bot"
        "\n \n This is the MsgMe Bot!"
        "If you don't want a reminder, and just want to save a post, then this bot "
        "will help you send you a message with the post details"
        "\n \n How it works:"
        "\n \n Just type !MsgMe or !MessageMe (case insensitive) and you will get a message with the subject 'Saved Post'"
        "\n \n If you want a custom title then write !MsgMe (or !MessageMe) followed by the subject you want"
        "\n \n For example, !MessageMe Cool Post will send you a message with the subject 'Cool Post'")
    
    comment=reddit.comment(id=comment_id)
    try:
        comment.reply(text)
        print(f"Publicized on {comment_id} and url {comment.permalink}")
    except:
        time.sleep(600)
        comment.reply(text)
        print(f"Publicized on {comment_id} and url {comment.permalink}")


def get_remindme():
    print(f'Remind Me Start {time.time()}')
    for comment in reddit.subreddit('all').stream.comments():
        if comment.author == 'MsgMeBot' or comment.author == 'RemindMeBot':
            continue
        if '!remindme' in comment.body.lower():
            publicize(comment.id)
            print(time.time())

def get_comments():
    print(f'Comment Start {time.time()}')
    for comment in reddit.subreddit('all').stream.comments(skip_existing=True):
        if comment.author == 'MsgMeBot':
            continue
        if '!msgme' in comment.body.lower() or '!messageme' in comment.body.lower():
                send_msg(comment.id)
                print(time.time())

def send_msg(cmnt_id):
    # import ipdb; ipdb.set_trace()
    comment=reddit.comment(id=cmnt_id)
    redditor=comment.author
    
    try:
        subject=comment.body.split(' ')[1]
    except:
        subject='Saved Post'
    
    try:
        parent_comment=reddit.comment(id=comment.parent_id.split('_')[-1]).permalink
    except:
        parent_comment='NA'
    post_title=reddit.submission(id=comment.link_id.split('_')[-1]).title
    post_body=reddit.submission(id=comment.link_id.split('_')[-1]).selftext
    reply_text=(f"Thank You for using MsgMeBot {redditor.name}!!!"
                "I have sent you a message for this post"
                "\n \n How it works:"
                "\n \n Just type !MsgMe or !MessageMe (case insensitive) and you will get a message with the subject 'Saved Post'"
                "\n \n If you want a custom title then write !MsgMe (or !MessageMe) followed by the subject you want"
                "\n \n For example, !MessageMe Cool Post will send you a message with the subject 'Cool Post'")

    msg_text=(f"Thank You for using MsgMeBot {redditor.name}!!!"
                f"\n \n You asked me to remind you about the post:"
                f"\n \n_______\n \n {post_title}"
                f"\n \n {post_body}"
                "\n \n______\n \n"
                f"Link to your comment is: {parent_comment}")

    try:
        comment.reply(reply_text)
        redditor.message(subject, msg_text)
        print(f"Sent Msg to user {redditor.name} {cmnt_id} with url {comment.permalink}")
    except:
        time.sleep(600)
        comment.reply(reply_text)
        redditor.message(subject, msg_text)
        print(f"Sent Msg to user {redditor.name} {cmnt_id} with url {comment.permalink}")

def main(reddit):
    p1=Process(target=get_remindme)
    # p2=Process(target=get_comments)
    # p2.start()
    p1.start()

    get_comments()

if __name__ == "__main__":
    reddit=praw.Reddit(client_id='client_id',
                        client_secret='client_secret',
                        user_agent='Messaging Reminders by u/MsgMeBot',
                        username='MsgMeBot',
                        password='my password')
    
    main(reddit)
