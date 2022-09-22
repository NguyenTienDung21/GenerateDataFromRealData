from processing.url_processing import extract_uri
import json

class TrafficData:
    def __init__(self, row):
        if row is not None:
            (
                self.session,
                self.url,
                self.created_at,
                self.action_target,
                self.action_data,
                self.action,
                self.timestamp
            ) = row
        self.url = extract_uri(self.url)


    def __repr__(self, seperator=","):
        return json.dumps({
            "url":self.url,
            "action": self.action,
            "action_data": self.action_data
        })