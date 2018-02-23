# [TrapBot](https://www.reddit.com/user/TrapSCBot)

A reddit bot that looks for comments with song names and responds with their
respective SoundCloud links.

## Usage

Type each song on a separate line with the song name and artist (order is
irrelevant) separated by a dash. This bot will only scan the comments posted in
the subreddits listed in [`subreddits.txt`](https://github.com/Kevin-Mok/TrapBot/blob/master/subreddits.txt).

Example:
```
* Helix - Flume
* Core - RL Grime
* U Already Know - Keys N Krates
```
**Note:** The bot is still being tested, and all responses are currently being
manually approved before submission.

## Motivation

This bot was inspired by various music discussion threads (namely
in [r/trap](https://www.reddit.com/r/trap/)) where lists of songs would be
posted with no accompanying SoundCloud links.

## Built With
- Python API Wrappers:
  - [SoundCloud](https://github.com/soundcloud/soundcloud-python)
  - [reddit](https://github.com/praw-dev/praw)
