import requests
import json
import sqlite3

# the following code is just for testing to extract all the moves from a pokemon in the heartgold-soulsilver verison
def get_move_info(json_content):
    '''
    :param json_content:
    :return: The moves in a list, and each list element is [name, url, learn method, learn lvl]
    '''
    output = []
    moves = json_content['moves']
    number_of_moves = len(moves)
    for i in range(0,number_of_moves):
        move_name = moves[i]['move']['name']
        move_url = moves[i]['move']['url']
        version_details = moves[i]['version_group_details']
        move_learn_method = None
        lvl_learned_at = None
        for versions in version_details:
            if versions['version_group']['name'] == 'heartgold-soulsilver':
                lvl_learned_at = versions['level_learned_at']
                move_learn_method = versions['move_learn_method']['name']
            output.append([move_name, move_url, move_learn_method, lvl_learned_at])
    output.sort(key = lambda x:x[3])
    return output


def get_ability(json_content):
    '''
    :param json_content:
    :return: The abilities in a list, and each list element is [name, is_hidden, url]
    '''
    output = []
    abilities = json_content['abilities']
    abilitie_num = len(abilities)
    for ability in abilities:
        is_hidden = ability['is_hidden']
        name = ability['ability']['name']
        url = ability['ability']['url']
        output.append([name, is_hidden, url])
    return output


def get_basics(json_content):
    id = json_content['id']
    name = json_content['name']
    height = json_content['height']
    weight = json_content['weight']
    base_exp = json_content['base_experience']
    species = json_content['species']['name']
    species_url = json_content['species']['url']
    type = []
    types = json_content['types']
    for t in types:
        type.append(t['type']['name'])
    return id, name, height, weight, base_exp, species, species_url, type

def get_stats(json_content):
    '''
    :param json_content:
    :return: output dictionary, where keys are the name of the stats, and contents are the base and efforts of the corresponding stats
    '''
    output = {}
    stats = json_content['stats']
    for stat in stats:
        name = stat['stat']['name']
        base = stat['base_stat']
        effort = stat['effort']
        output[name] = {'base': base, 'effort':effort}
    return output

def get_item(json_content):
    


#########################################################################################
# Main Function Below
#########################################################################################

# Assume that we are doing 386 at first
# Index = range(1,494)
#
# for index in Index:
#     response = requests.get("https://pokeapi.co/api/v2/pokemon/%s/"%index)
#     print response.content

response = requests.get("https://pokeapi.co/api/v2/pokemon/123/")
content = json.loads(response.content)
print get_basics(content)