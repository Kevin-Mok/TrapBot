**Note**: *This project has been put on hiatus due to the SoundCloud API
returning incorrect search results.*

# [TrapBot](https://www.reddit.com/user/TrapSCBot)

A reddit bot that looks for comments with song names and responds with their
respective SoundCloud links.

## Usage <!---  {{{ -->

Type each song on a separate line with the song name and artist (order is
irrelevant) separated by spaces and a dash. This bot will only scan the comments
posted in the subreddits listed in
[`subreddits.txt`](https://github.com/Kevin-Mok/TrapBot/blob/master/subreddits.txt).

Example:
```
* Helix - Flume
* Core - RL Grime
* U Already Know - Keys N Krates
```
**Note:** This bot is still in beta. If you find any errors, please respond
to the bot's comment or PM it with the post and type of error. I will be sure to
edit the post and try to prevent those errors from reoccuring in the future.

<!---  }}} -->

## Installation <!---  {{{ -->

**Requirements**:
- Python 3
- `virtualenv`

1. Make a new working directory for the virtual environment.
    ```
    python -m venv trapbot
    ```
1. `cd` into the new directory, and activate the virtual environment.
    ```
    cd trapbot
    source bin/activate
    ```
1. Clone the repository.
    ```
    git clone https://github.com/Kevin-Mok/TrapBot src
    ```
1. Install the necessary packages.
    ```
    cd src
    pip install -r requirements.txt
    ```
1. [Create a reddit app](https://www.reddit.com/prefs/apps) with a redirect
   uri of `https://127.0.0.1/`. Then, create `praw.ini` with the following
   information:
    ```
    [trapbot]
    client_id=     # below app name
    client_secret=
    password=
    username=
    user_agent=TrapBot user agent
    ```
1. Create `soundcloud-api.ini` with your SoundCloud API key as the only
   line in the file.
1. Run `main.py`.

<!---  }}} -->

## Motivation <!--- {{{ -->

This bot was inspired by various music discussion threads (namely
in [r/trap](https://www.reddit.com/r/trap/)) where lists of songs would be
posted with no accompanying SoundCloud links.

## Built With
- Python API Wrappers:
  - [SoundCloud](https://github.com/soundcloud/soundcloud-python)
  - [reddit](https://github.com/praw-dev/praw)

<!---  }}} -->
