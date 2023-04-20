import json
import os
import requests
from requests.exceptions import HTTPError

class DevrevAPI:
    def __init__(self, feature_name):
        self.base_url = "https://api.devrev.ai"
        token = os.getenv("WWCODE_API_WORKSHOP_PAT")
        self.headers = {
            'Content-Type': "application/json",
            'Authorization': token} 
        self.user_id = self.dev_user_self()["id"]
        self.user_name = self.dev_user_self()["full_name"]
        self.feature_name = feature_name
        self.part_id = self.list_parts()
        self.work_id = self.maybe_create_works()

    # Print the work_id which is initialized.
    def print_work_id(self):
        print(self.work_id)
        
    # Lists the Devrev parts in order to pick a part to assign the issue to.
    # Return Value: JSON response received from parts.list
    # Corresponding API definition:
    #       https://devrev.ai/docs/apis/methods#/operations/parts-list
    def list_parts(self):
        url = self.base_url + "/parts.list"
        payload = json.dumps({
            "name": [self.feature_name]
        })
        try:
            response = requests.post(url, headers=self.headers, data=payload)
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


    def list_works(self):
        owner_filter = "&owned_by=" + self.user_id
        url = self.base_url + "/works.list?applies_to_part=" + self.part_id + owner_filter
        payload = {}
        try:
            response = requests.get(url, headers=self.headers, data=payload)
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
        # Return Value: Your user information
        # Corresponding API definition:
        #      https://devrev.ai/docs/apis/methods#/operations/dev-users-self


    def dev_user_self(self):
        url = self.base_url + "/dev-users.self"
        payload = {}
        try:
            response = requests.request("GET", url, headers=self.headers, data=payload)
            response.raise_for_status()
            json_resp = response.json()
            return json_resp["dev_user"]
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
    def maybe_create_works(self):
        work_id = self.list_works()
        if work_id == "":
            url = self.base_url + "/works.create"
            issue_title = self.feature_name + " :TIL Log for - " + self.user_name
            if self.part_id != "":
                payload = {"owned_by": [self.user_id],
                        "title": issue_title,
                        "applies_to_part": self.part_id,
                        "type": "issue",}
                try:
                    response = requests.request("POST", url, headers=self.headers, json=payload)
                    response.raise_for_status()
                    json_resp = response.json()
                    work_id = json_resp["work"]["id"]
                except HTTPError as http_err:
                    print(f'HTTP error occurred: {http_err}')
                except Exception as err:
                    print(f'Other error occurred: {err}')
        return work_id
        
    def create_comment(self, til):
        url = self.base_url + "/timeline-entries.create"
        payload = json.dumps({
            "object": self.work_id,
            "type": "timeline_comment",
            "body": til,
            "body_type": "text"
        })
        try:
            response = requests.request("POST", url, headers=self.headers, data=payload)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
