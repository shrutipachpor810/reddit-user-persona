import os
import argparse
import praw
from openai import OpenAI
from dotenv import load_dotenv

#env
load_dotenv()

client = OpenAI()


def extract_username(profile_url):
    """
    Extracts the username from URL.
    """
    parts = profile_url.strip("/").split("/")
    if "user" in parts:
        idx = parts.index("user")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    raise ValueError("Invalid Reddit profile URL format.")


def fetch_user_data(reddit, username, max_posts=10, max_comments=10):
    """
    Fetches posts and comments 
    """
    redditor = reddit.redditor(username)
    posts = []
    comments = []

    for submission in redditor.submissions.new(limit=max_posts):
        posts.append({
            "title": submission.title,
            "text": submission.selftext,
            "url": f"https://www.reddit.com{submission.permalink}"
        })

    for comment in redditor.comments.new(limit=max_comments):
        comments.append({
            "body": comment.body,
            "url": f"https://www.reddit.com{comment.permalink}"
        })

    return posts, comments


def create_prompt(posts, comments):
    """
    Builds the prompt text to send to gpt-4o-mini.
    """
    prompt = (
        "Analyze this Reddit user's posts and comments.\n"
        "Create a detailed user persona including:\n"
        "Name:[if possible]\n"
        "Age:[if inferred]\n"
        "Occupation:[if inferred]\n"
        "Location:[if inferred]\n"
        "Behaviour and Habits:\n"
        "- ...\n"
        "\n"
        "Frustations:\n"
        "- ..\n"
        "\n"
        "Motivations:\n"
        "- ..\n "
        "\n"
        "Goals and Needs:\n"
        "- ..\n"
        "\n"
        "Personality Traits:\n"
        "-..\n"
        "\n"
        "For each point, cite exactly which post or comment (and its URL) you used.\n\n"
        "POSTS:\n"
    )

    for post in posts:
        prompt += f"Title: {post['title']}\n"
        prompt += f"Text: {post['text']}\n"
        prompt += f"URL: {post['url']}\n\n"

    prompt += "COMMENTS:\n"
    for comment in comments:
        prompt += f"Body: {comment['body']}\n"
        prompt += f"URL: {comment['url']}\n\n"

    return prompt


def generate_persona(prompt):
    """
    Calls the OpenAI API to generate persona.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert at writing clear, factual user personas. "
                    "Avoid using markdown symbols, fancy headings, or emojis. "
                    "Format the output as plain text with numbered or bulleted points."
                    "Use sructure: Name, Age, Occupation,Location,Behavious and Habits, Frustation, Motivations, Personality Traits. Include citations for each point."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content


def save_persona(username, persona_text):
    """
    Saves the persona to a .txt file which is in output folder.
    """
    os.makedirs("output", exist_ok=True)
    file_path = os.path.join("output", f"{username}.txt")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("User Persona Report\n")
        file.write(f"Username: {username}\n\n")

        # every new line is written on separate line in txt file
        for line in persona_text.splitlines():
            if line.strip():
                file.write(line.strip() + "\n")

    print(f"Persona saved to {file_path}")


def main():
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="reddit-persona-script"
    )

    parser = argparse.ArgumentParser(description="Generate a Reddit user persona.")
    parser.add_argument("profile_url", help="Reddit profile URL (e.g., https://www.reddit.com/user/username/)")
    args = parser.parse_args()

    username = extract_username(args.profile_url)
    print(f"Collecting data for user: {username}")

    posts, comments = fetch_user_data(reddit, username)

    print(f"Collected {len(posts)} posts and {len(comments)} comments.")

    prompt = create_prompt(posts, comments)

    print("Generating user persona.")

    persona = generate_persona(prompt)

    save_persona(username, persona)

if __name__ == "__main__":
    main()
