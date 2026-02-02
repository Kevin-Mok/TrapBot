# TrapBot

A Reddit bot that automatically finds and links SoundCloud tracks mentioned in music discussion threads.

![Python](https://img.shields.io/badge/Python-3-blue)
![Reddit](https://img.shields.io/badge/Reddit-PRAW-orange)
![SoundCloud](https://img.shields.io/badge/SoundCloud-API-red)

> **Note**: This project is on hiatus due to SoundCloud API returning incorrect search results.

## Overview

[TrapBot](https://www.reddit.com/user/TrapSCBot) monitors music subreddits for comments listing songs and automatically replies with SoundCloud links. Inspired by r/trap discussion threads where users post song lists without accompanying links.

## Features

- **Automatic Song Detection** - Parses comments for "Artist - Song" format
- **SoundCloud Search** - Finds matching tracks via API
- **Multi-Subreddit Support** - Configurable subreddit monitoring
- **Formatted Replies** - Clean Reddit comment formatting with links

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3 |
| **Reddit API** | PRAW (Python Reddit API Wrapper) |
| **Music API** | SoundCloud Python SDK |
| **Deployment** | Virtual environment |

## Project Structure

```
TrapBot/
├── main.py               # Bot entry point
├── subreddits.txt        # Monitored subreddits list
├── praw.ini              # Reddit API credentials
├── soundcloud-api.ini    # SoundCloud API key
└── requirements.txt      # Python dependencies
```

## Usage

Type each song on a separate line with artist and song name separated by a dash:

```
* Helix - Flume
* Core - RL Grime
* U Already Know - Keys N Krates
```

The bot monitors subreddits listed in [`subreddits.txt`](https://github.com/Kevin-Mok/TrapBot/blob/master/subreddits.txt).

## Installation

### Prerequisites
- Python 3
- `virtualenv`
- Reddit app credentials
- SoundCloud API key

### Setup

```bash
# Create virtual environment
python -m venv trapbot
cd trapbot
source bin/activate

# Clone and install
git clone https://github.com/Kevin-Mok/TrapBot src
cd src
pip install -r requirements.txt

# Configure credentials
# 1. Create Reddit app at https://www.reddit.com/prefs/apps
#    (redirect uri: https://127.0.0.1/)

# 2. Create praw.ini:
cat > praw.ini << EOF
[trapbot]
client_id=     # below app name
client_secret=
password=
username=
user_agent=TrapBot user agent
EOF

# 3. Create soundcloud-api.ini with your API key

# Run the bot
python main.py
```

## Why This Project is Interesting

### Technical Highlights

1. **API Integration**
   - Reddit API via PRAW for comment monitoring
   - SoundCloud API for track searching
   - Multi-API orchestration

2. **Text Parsing**
   - Pattern matching for song/artist format
   - Handling various input formats
   - Error-tolerant parsing

3. **Bot Architecture**
   - Continuous subreddit monitoring
   - Rate limiting compliance
   - Formatted response generation

4. **Community Automation**
   - Solves real user pain point
   - Enhances music discussion threads
   - Non-intrusive, helpful automation

### Skills Demonstrated

- **Python Development**: API wrappers, text processing
- **Bot Development**: Reddit automation, rate limiting
- **API Integration**: OAuth, search APIs
- **DevOps**: Virtual environments, configuration management

## Built With

- [PRAW](https://github.com/praw-dev/praw) - Python Reddit API Wrapper
- [SoundCloud Python](https://github.com/soundcloud/soundcloud-python) - SoundCloud API SDK

## Author

[Kevin Mok](https://github.com/Kevin-Mok)
