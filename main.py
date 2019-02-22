import requests
import json

# Assume that we are doing 386 at first
Index = range(1,387)

# for index in Index:
#     response = requests.get("https://pokeapi.co/api/v2/pokemon/%s/"%index)
#     print response.content

response = requests.get("https://pokeapi.co/api/v2/pokemon/1/")
json_content = json.loads(response.content)
for dictionary in json_content['moves']:
    for key in dictionary:
        print dictionary[key]