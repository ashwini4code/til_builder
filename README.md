# til_builder


The goal of this project is to easily capture, organize and share learnings.
For groups, wanting to share and maintain learnings, [DevRev](https://devrev.ai/)
offers a mechanism,to create features and work items which can maintain
TIL posts.
Often, we learn concepts through Youtube videos and there is value in
transacribing and maintaining a log for quick reference.
Youtube videos can be transcribed using the YouTube Transcript API.

## Setup

```
Join the WWCode Devorg on Devrev, by accepting the email invite.

Follow steps listed [here](https://devrev.ai/docs/apis/auth) to fetch the
Devrev Personal Access Token.

Set the env variable `WWCODE_API_WORKSHOP_PAT` to your token value using,
export WWCODE_API_WORKSHOP_PAT <Fetched PAT value>

Please do not share your PAT with anyone else, as this prepresents you as a user ont he platform.
```

## Usage

```

python3 src/video_to_til.py <youtube_video_id>


```
