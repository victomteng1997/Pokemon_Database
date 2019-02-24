import sqlite3
import random
conn = sqlite3.connect('pokemon.db')
c = conn.cursor()

# xingge
nature_attack_plus = ['Hardy',	'Lonely',	'Adamant',	'Naughty',	'Brave']
nature_defense_plus = ['Bold',	'Docile',	'Impish',	'Lax',	'Relaxed']
nature_sp_plus =  ['Modest',	'Mild',	'Bashful',	'Rash',	'Quiet']
nature_spdef_plus = ['Calm',	'Gentle',	'Careful',	'Quirky',	'Sassy']
speed_plus = ['Timid',	'Hasty',	'Jolly',	'Naive',	'Serious']
nature_list = [nature_attack_plus,nature_defense_plus,nature_sp_plus,nature_spdef_plus,speed_plus]
pokemon_name = 'blissey'


c.execute("SELECT * FROM Pokemon_basic_data WHERE name = '%s'" % pokemon_name)
id, name, height, weight, base_exp, species, url, type = c.fetchone()
print id, name, height, weight, base_exp, species, url, type

c.execute("SELECT * FROM Pokemon_combat_data WHERE name = '%s'" % pokemon_name)
id, name, move, hp_base, attack_base, defense_base, special_attack_base, special_deffense_base, speed_base, hp_effort, attack_effort, defense_effort, special_attack_effort, special_defense_effort, speed_effort = c.fetchone()

individual = {'hp':0,'attack':0,'defense':0,'special_attack':0,'special_defense':0,'speed':0}

# try to build one pokemon
stat_lvl = [0, 0, 0, 0, 0, 0]
star = 5
for key in individual:
    individual[key] = random.randint(0,31)
lvl = 100
nature_count = (random.randint(0,4),random.randint(0,4))
print nature_count
nature = nature_list[nature_count[0]][nature_count[1]]

hp = (2*hp_base+individual['hp']+hp_effort/4)*lvl/100.0+lvl+10
attack = (2*attack_base+individual['attack']+attack_effort/4)*lvl/100+5
defense = (2*defense_base+individual['defense']+defense_effort/4)*lvl/100+5
special_attack = (2*special_attack_base+individual['special_attack']+special_attack_effort/4)*lvl/100+5
special_defense = (2*special_deffense_base+individual['special_defense']+special_defense_effort/4)*lvl/100+5
speed = (2*speed_base+individual['speed']+speed_effort/4)*lvl/100+5

# nature modification
modified_stat = [attack, defense, special_attack, special_defense,speed]
modified_stat[nature_count[0]]=modified_stat[nature_count[0]]*1.1
modified_stat[nature_count[1]]=modified_stat[nature_count[1]]*0.9
stats = [hp]
for stat in modified_stat:
    stats.append(stat)

# star modification
for i in range(0,6):
    stats[i] = int(stats[i]*1.2)^star

# stat lvl
for i in range(0,6):
    if i == 0:
        stats[i] += stats[i]*0.01*stat_lvl[i] + stat_lvl[i]*2
    else:
        stats[i] += stats[i]*0.01*stat_lvl[i] + + stat_lvl[i]*1

print stats
