import json
import os
import sys
from datetime import date

import requests
from requests.exceptions import HTTPError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# Set WWCODE_API_WORKSHOP_PAT in you .env

token = os.getenv("WWCODE_API_WORKSHOP_PAT")
headers = {
    'Content-Type': "application/json",
    'Authorization': token
}
work_id = " "
base_url = "https://api.devrev.ai"

# Fetch the trancript of the youtube video, when the id
# of the video is provided.
# Reference: https://pypi.org/project/youtube-transcript-api/

def textlen(s):
    return len(s.encode('utf-8'))

def fetch_transcription(id):
    transcript = YouTubeTranscriptApi.get_transcript(
        id, preserve_formatting=True)
    tformatter = TextFormatter()
    finalText = tformatter.format_transcript(transcript)
    return finalText

# Lists the Devrev parts in order to pick a part to assign the issue to.
# Return Value: JSON response received from parts.list
# Corresponding API definition:
#       https://devrev.ai/docs/apis/methods#/operations/parts-list


def list_parts():
    url = base_url + "/parts.list?name=\"Learning Logs\"&type=capability"
    payload = {}
    try:
        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()
        part_list = response.json()["parts"]
        if part_list:
            return part_list[0]["display_id"]
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

# Lists the Devrev works.
# Return Value: The work-id corresponding to the query.
# Corresponding API definition:
#       https://devrev.ai/docs/apis/methods#/operations/works-list


def list_works(part_id):
    url = base_url + "/works.list?applies_to_part=" + part_id
    payload = {}
    try:
        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()
        works_list = response.json()["works"]
        if works_list:
            return works_list[0]["id"]
        else:
            return ""
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

# Fetch your user ID.
# Return Value: Your user ID
# Corresponding API definition:
#      https://devrev.ai/docs/apis/methods#/operations/dev-users-self


def dev_user_self():
    url = base_url + "/dev-users.self"
    payload = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()
        json_resp = response.json()
        return json_resp["dev_user"]["id"]
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def create_works():
    url = base_url + "/works.create"
    id_list = [dev_user_self()]
    part_id = list_parts()
    # Pick the first part to assign the issue to.
    if part_id != "":
        payload = {"owned_by": id_list,
                   "title": "Ashwini's LLM TIL Log",
                   "applies_to_part": part_id,
                   "type": "issue", }
        try:
            response = requests.request("POST", url, headers=headers, json=payload)
            response.raise_for_status()
            json_resp = response.json()
            return json_resp["work"]["id"]
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
    return ""


def create_comment(work_id, til):
    url = base_url + "/timeline-entries.create"
    payload = json.dumps({
        "object": work_id,
        "type": "timeline_comment",
        "body": til,
        "body_type": "text"
    })
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def main():
    if len(sys.argv) > 2:
        print("Too many ids. Please provide one at a time")
        return
    elif len(sys.argv) != 2:
        print("video id not provided")
        return
    vid_list = str(sys.argv[1])
    vid_link = "https://www.youtube.com/watch?v=" + vid_list
    part_id = list_parts()
    if not part_id:
        print(" Cannot find Part[Learning Logs]")
        return
    work_id = list_works(part_id)
    print("The work item updated is: " + work_id)
    if work_id == "":
        work_id = create_works()
        print("created " + work_id)
    today = date.today()
    datestr = today.strftime("%m/%d/%y")
    til = datestr + "\n" + " Original Video: " + vid_link + "\n" + fetch_transcription(vid_list)
    til_len = textlen(til)
    # Devrev limits posts to 16 KB
    if til_len > 16383:
        print("Size of text in bytes ", til_len)
        print("Truncating string, since Devrev limits posts to 16KB")
        til = til.encode('utf-8')[:16383].decode('utf-8', 'ignore')
    create_comment(work_id, til)

16384
if __name__ == "__main__":
    main()
