import json

class MediaPlayer:
    def load(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)