from json_def import json_read
from pathlib import Path
import json
import requests
        
    
class Shortlink():
    def __init__(self):
        self.base_url: str = json_read(f'{str(Path.cwd())}/res/config.json')['short_link_url']
        self.token: str = json_read(f'{str(Path.cwd())}/res/config.json')['token_short_link']
    
    def create_link(self) -> dict:
        self.create_url: str = "create"
        payload: dict = {
            "url": "",
        }
        headers: dict = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url=self.base_url+self.create_url, headers=headers, data=json.dumps(payload))
        return response.json()
    