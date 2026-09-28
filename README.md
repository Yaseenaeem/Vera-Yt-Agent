# Vera-Yt-Agent
Evidence-based YouTube market intelligence engine built with FastAPI and Streamlit to analyze public video metadata, view baselines, and title hooks.

# 🎬 VERA — Video Evidence & Resonance Analytics

## What is VERA?

VERA (Video Evidence & Resonance Analytics) is a YouTube research agent I built to analyze public video search metadata. 

When people plan YouTube content, they usually just look at whatever viral video popped up on their feed and try to copy it. The problem is that viral hits are usually outliers. If you only look at the top 0.1% of videos, you aren't seeing what actually works consistently across a whole topic.

I wanted to build a tool that looks at a full sample of public search results for any niche, calculates a realistic baseline for views, breaks down what top-performing titles have in common compared to low-performing ones, and gives you actual data-backed video ideas.

---

## Why I Built It & The Approach

Most advice for creators is really vague or relies on gut feeling. When I looked into how YouTube search results behave, a couple of things stood out:

* **Averages lie:** If you take 25 videos and one of them has 10 million views while the rest have 10k, the average view count looks huge. That gives a false picture. Using the **median** view count gives a much more accurate view of what an average video in that niche gets.
* **Title patterns actually matter:** By splitting a sample into top 25% and bottom 25% performance quartiles, you start seeing clear patterns. Things like adding specific location tags, using clear "How to" phrasing, or keeping titles short show up repeatedly in top performers.
* **Broad inputs break analysis:** Searching for something massive like "Coding" or "Fitness" gives messy data because the topics are too wide. I added a check in the backend so if a prompt is too broad, it stops and asks you to pick a specific sub-niche first.

---

## Tech Stack & Architecture

I decided to split the project into two separate parts: a **FastAPI backend** for fetching data and processing logic, and a **Streamlit frontend** for the dashboard UI.

```
VERA-Yt-Agent/
├── app/                  # Backend Code
│   ├── main.py           # FastAPI routes & endpoints
│   ├── tools.py          # YouTube API calls & data fetching
│   ├── analytics.py      # Calculations & pattern logic
│   └── __init__.py
├── UI/                   # Frontend code
│   └── Ui.py             # Streamlit dashboard & custom CSS
├── .env                  # API keys (kept local)
├── .gitignore            # Files ignored by Git
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

---

## Stack Used:
Backend: Python, FastAPI, Uvicorn, Pydantic
Frontend: Streamlit (with custom CSS for dark mode)
Data & APIs: YouTube Data API v3, Groq API (openai/gpt-oss-120b), Pandas, Requests

---


## Decisions & Trade-Offs
Here are a few choices I made while building this and why:

1. Public Metadata vs Private Analytics
I chose to use only public search metadata from the YouTube Data API instead of asking users to log in with their channel's Google account.

Trade-off: I can't see private stuff like click-through rates (CTR) or audience retention graphs.
Why: You don't need to log in or own a channel to use it. You can research any niche or competitor instantly.


2. Streamlit with Custom CSS vs React
I wanted a quick way to build an interactive dashboard without having to set up a full React frontend from scratch.

Trade-off: Streamlit can be rigid with layouts, so I had to write custom CSS overrides to get the dark YouTube theme and clean padding working right.
Why: It allowed me to focus heavily on the backend logic and Python data flow while still getting a good-looking interface.


3. Median Over Mean
As mentioned earlier, I used median views across sample sets instead of the mean average.

Why: YouTube view distributions are super skewed by big viral hits. The median shows what a normal video actually gets.

---

## How to Set Up and Run Locally
If you want to test VERA on your own machine, follow these steps.

# Prerequisites: 
- Python 3.10 or higher
- A YouTube Data API v3 Key
- A Groq API Key

1. Clone the Repo
```
git clone [https://github.com/Yaseenaeem/Vera-Yt-Agent.git](https://github.com/Yaseenaeem/Vera-Yt-Agent.git)
cd Vera-Yt-Agent
```

2. Set Up Virtual Environment
```
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install Requirements
```
pip install -r requirements.txt
```

4. Create .env File
Create a .env file in the main folder and add your API keys:
```
YOUTUBE_API_KEY=your_youtube_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

5. Start the Project
```
VERA needs both the FastAPI server and the Streamlit UI running at the same time. Open two terminal windows:
```

# Terminal 1 (Backend):
```
python -m uvicorn app.main:app --reload --port 8000
```

# Terminal 2 (Frontend):
```
streamlit run UI/Ui.py
```
Streamlit will open automatically in your browser at http://localhost:8501.


# Testing It Out
Try a broad query: Type something vague like Jewellery or Python. The system will trigger the NEEDS_NICHE state and show you a list of sub-niches to pick from.

Try a specific niche: Enter Lab-Grown Diamonds or Handmade Silver Jewellery.

Check the outputs: You should see the sample size, the median views baseline, the top vs bottom title patterns, and 3 testable video launch ideas.

---

## Privacy
VERA only uses public YouTube search data. It doesn't request, store, or access any personal account data or private channel analytics.

---

## Author
Muhammad Yaseen Naeem
