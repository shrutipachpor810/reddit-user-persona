# Reddit User Persona Generator

This script takes a Reddit user profile URL, scrapes their posts & comments, and generates a detailed user persona using OpenAI GPT-4.

---
## Project Structure

reddit-user-persona/
reddit_persona.py       # Main script
test_praw.py            # Test script to check Reddit API connectivity
output/                 # Output folder
  └── [username].txt    # Persona reports
.env                    # Environment variables
.env.example            # Example template for .env
requirements.txt        # Dependencies list
README.md               # Setup & usage guide

---

## ⚙️ Setup Instructions

1. **Clone this repository**  
   ```bash
   git clone <your-repo-link>
   cd reddit-user-persona
Create and activate a virtual environment (recommended)

2. **Create and activate a virtual environment**
python -m venv venv
# For Windows (PowerShell)
.\venv\Scripts\activate
# For macOS/Linux
source venv/bin/activate

3. **Install dependencies**
pip install -r requirements.txt

4. **Create your .env file**
Copy .env.example to .env and add your keys:
OPENAI_API_KEY=your_openai_api_key_here
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here

## How to test Reddit API
Use the provided test_praw.py script to verify your Reddit API works:
python test_praw.py
You should see output showing test user's post and comments

## How to Run
Run the main reddit_persona.py with url
python reddit_persona.py https://www.reddit.com/user/kojied/
The generated persona file will be saved in the output/ folder.

## Output
The generated persona file will be saved in the output/ folder.
User Persona Report
Username: [username]

[Persona content...]
