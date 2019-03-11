import requests
import json
import sqlite3
import urllib2
import shutil
from pathlib import Path

Index = range(1,747) # 746 moves in total

for index in Index:
    response = requests.get("https://pokeapi.co/api/v2/move/%s/"%index)
    content = json.loads(response.content)