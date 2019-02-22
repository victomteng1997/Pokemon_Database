import requests
import json
import sqlite3
import urllib2
import shutil
from pathlib import Path



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
    '''
    :param json_content:
    :return: held item in dictioanry, {item_name: item rarity, item_name: item rarity}
    '''
    output = {}
    items = json_content['held_items']
    for item in items:
        version_detials = item['version_details']
        for versions in version_detials:
            if versions['version']['name'] == 'heartgold':
                rarity = versions['rarity']
                output[item['item']['name']] = rarity
    return output


def get_sprites(json_content):
    output = {}
    contents = json_content['sprites']
    for key in contents:
        if contents[key]:
            output[key] = contents[key]
    return output



#########################################################################################
# Main Function Below
#########################################################################################

# Assume that we are doing 493 at first
Index = range(1,494)

conn = sqlite3.connect('pokemon.db')
c = conn.cursor()
for index in Index:
    response = requests.get("https://pokeapi.co/api/v2/pokemon/%s/"%index)
    content = json.loads(response.content)

    # basic information
    id, name, height, weight, base_exp, species, species_url, type = get_basics(content)
    ability = get_ability(content)
    item = get_item(content)
    move = get_move_info(content)
    stats = get_stats(content)
    sprites = get_sprites(content)

    json_type = json.dumps(type)
    json_ability = json.dumps(ability)
    json_item = json.dumps(item)
    json_move = json.dumps(move)
    special_attack = stats['special-attack']['base']
    hp = stats['hp']['base']
    attack = stats['attack']['base']
    defense = stats['defense']['base']
    speed = stats['speed']['base']
    special_defense = stats['special-defense']['base']
    special_attack_effort = stats['special-attack']['effort']
    hp_effort = stats['hp']['effort']
    attack_effort = stats['attack']['effort']
    defense_effort = stats['defense']['effort']
    speed_effort = stats['speed']['effort']
    special_defense_effort = stats['special-defense']['effort']



    # Download Sprites
    for key in sprites:
        url = sprites[key]
        response = requests.get(url, stream=True)
        pic_name = '.\sprites\\'+ name + '_' + key + '.png'
        print pic_name
        with open(pic_name, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

    # Do SQLITE magic

    table_name = 'Pokemon_basic_data'

    c.execute('''CREATE TABLE if not exists %s
                                 (id real, name text, height real, weight real, base_exp real, species text, species_url text, type text)''' % table_name)
    basic_data = [(int(id), str(name), float(height), float(weight), float(base_exp), str(species), str(species_url), str(json_type)),]
    c.executemany('INSERT INTO Pokemon_basic_data VALUES (?,?,?,?,?,?,?,?)', basic_data)

    table_name = 'Pokemon_combat_data'
    c.execute('''CREATE TABLE if not exists %s
                                     (id real, name text, move text, hp real, attack real, defense real, special_attack real, special_defense real, speed real,  hp_effort real, attack_effort real, defense_effort real, special_attack_effort real, special_defense_effort real, speed_effort real)''' % table_name)
    combat_data = [(id, name, json_move, hp, attack, defense, special_attack, special_defense, speed, hp_effort, attack_effort, defense_effort, special_attack_effort, special_defense_effort, speed_effort),]
    c.executemany('INSERT INTO Pokemon_combat_data VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', combat_data)
    conn.commit()

conn.close()
