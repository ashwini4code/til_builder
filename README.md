# til_builder


## Goal

The goal of this project is to easily capture, organize and share learnings.

<img width="1358" alt="til" src="https://user-images.githubusercontent.com/86735914/233455665-da76df20-b07f-4e55-a4db-356c1ae5470a.png">


For groups, wanting to share and maintain learnings, [DevRev](https://devrev.ai/)
offers a mechanism, to create [Issues](https://devrev.ai/docs/product/build) using the [DevRev works API](https://devrev.ai/docs/apis/methods#/operations/works-create)
which you can post learnings to.
Often, we learn concepts through Youtube videos and want to transcribe and
maintain a log of our learnings for quick reference.
Youtube videos can be transcribed using the [YouTube Transcript API](https://pypi.org/project/youtube-transcript-api/).

## Setup


Join the WWCode Devorg on Devrev, by accepting the email invite.

Follow steps listed [here](https://devrev.ai/docs/apis/auth) to fetch the
Devrev Personal Access Token.

Set the env variable `WWCODE_API_WORKSHOP_PAT` to your token value using,
`export WWCODE_API_WORKSHOP_PAT=<Fetched PAT value>`

Please do not share your PAT with anyone else, as this prepresents you as a user ont he platform.


## Usage

```
python3 src/video_to_til.py <youtube_video_id> "DevRev Feature Name"

```
