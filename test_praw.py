import os
from dotenv import load_dotenv
import praw

# Load keys from .env
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="test-script"
)

# Try to fetch your own user info (or any public user)
username = "spez"  # Reddit co-founder, always public

try:
    user = reddit.redditor(username)
    print(f"Redditor name: {user.name}")
    print(f"Redditor ID: {user.id}")

    # Fetch a few posts:
    print("Recent posts:")
    for submission in user.submissions.new(limit=2):
        print(f"Title: {submission.title}")

    # Fetch a few comments:
    print("Recent comments:")
    for comment in user.comments.new(limit=2):
        print(f"Comment: {comment.body}")

    print("PRAW test successful!")

except Exception as e:
    print(f"Something went wrong: {e}")
