from os import listdir
from os.path import isfile, join
from slippi.parse import parse, ParseEvent
from slippi import Game
#import pandas as pd
#import matplotlib.pyplot as plt
#from IPython.display import display
from datetime import date, datetime
import sqlite3
from slippifile import SlippiFile
from slippi.parse import ParseError

#conn = sqlite3.connect(':memory:')
conn = sqlite3.connect('slippi.db')
c = conn.cursor()

#c.execute("""CREATE TABLE slippi (
#           filename text,
#           lcancel real,
#           datetime datetime
#   )""")

def insert_slippi_file(slippi_file):
    with conn:
        c.execute("INSERT INTO slippi VALUES (:filename, :lcancel, :datetime)", {'filename':slippi_file.filename, 'lcancel':slippi_file.lcancel, 'datetime':slippi_file.datetime})

def get_slippi_file(filename):
    c.execute("SELECT * FROM slippi WHERE filename=:filename", {'filename':filename})
    return c.fetchall()

def get_slippi_files():
    c.execute("SELECT * FROM slippi")
    return c.fetchall()

def update_file(slippi_file, lcancel):
    with conn:
        c.execute("""UPDATE slippi SET lcancel = :lcancel
                    WHERE filename = :filename""",
                  {'filename': slippi_file.filename, 'lcancel': lcancel})

def remove_file(slippi_file):
    with conn:
        c.execute("DELETE from slippi WHERE filename = :filename",
                  {'filename': slippi_file.filename})

def did_i_win(player_ports, game_winner_ports, search_tag):
    winner_tags = []
    for port in game_winner_ports:
        winner_tags.append(player_ports[str(port)]['code'])
    if len(winner_tags) > 1:
        print("More than one winner, disregard")
        return -1
    return search_tag in winner_tags

def get_game_winner_ports(frames): 
    dead_port = -1
    winner_ports = []
    port_index = 0
    last_frame = len(frames) - 1
    for port in frames[last_frame].ports:
        if port:
            last_frame_state = str(port.leader.post.state)
            if not 'DEAD' in last_frame_state:
                winner_ports.append(port_index)
        port_index += 1
    return winner_ports

def get_player_ports(players):
    player_port = 0
    player_dict = {}
    for player in players:
        if player:
            player_dict[str(player_port)] = {'code':player.netplay.code, 'name':player.netplay.name}
            player_port += 1
    return player_dict

def get_slippi_files(folder):
    files = []
    for filename in listdir(folder):
        if not get_slippi_file(filename) and isfile(join(folder, filename)):
            files.append((join(folder, filename),filename))
    return files

def get_date_from_filename(filename):
    return filename[5:13]

def get_slippi_files_multi_folder(folder_list):
    files = []
    for folder in folder_list:
        files.extend(get_slippi_files(folder))
    return files

def get_player_port(players):
    port = -1
    index = 0
    for player in players:
        if player:
            if player.netplay:
                if code in player.netplay.code:
                    port = index
                index += 1
            else:
                break
    return port

def parse_files(files, game_limit):
    current_game_count=0
    games = []
    #Loop over all files
    for filename in files:
        if not get_slippi_file(filename[1]):
            try:
                current_game = Game(filename[0])
            except ParseError:
                print("Failed parsing on file: " + filename[1])
                continue
            if current_game.end: 
                if 'NO_CONTEST' in str(current_game.end.method):
                    continue
            port = get_player_port(current_game.metadata.players)
            if port == -1:
                print('Player not found in file: ' + filename[1])
                continue
            l_cancel_success = 0
            l_cancel_failure = 0
            l_cancel_total = 0
            action_list = []
            air_action_list = []
            attack_action_list = []
            for frame in current_game.frames:                
                try:
                    character_state = frame.ports[port].leader.post.state
                except:
                    print("No player on specified port")
                    break
                #opp_character_state = frame.ports[port].leader.post.state

                if not character_state in air_action_list and 'AIR' in str(character_state):
                    air_action_list.append(character_state)
                elif not character_state in attack_action_list and 'ATTACK' in str(character_state):
                    attack_action_list.append(character_state)
                elif not character_state in action_list:
                    action_list.append(character_state)

                l_cancel = frame.ports[port].leader.post.l_cancel
                if l_cancel:
                    l_cancel = str(l_cancel)
                    l_cancel_total += 1
                    if 'LCancel.SUCCESS' in l_cancel:
                        l_cancel_success += 1
                    elif 'LCancel.FAILURE' in l_cancel:
                        l_cancel_failure += 1
            if l_cancel_total > 0:
                l_cancel_success_rate = l_cancel_success/l_cancel_total
            else:
                #Skipping games with no L-Cancels
                continue
            slippi_datetime = filename[1][5:20]
            new_game = SlippiFile(filename[1], l_cancel_success_rate,slippi_datetime)
            games.append(new_game)
            insert_slippi_file(new_game)
            current_game_count+=1
            if game_limit > 0 and current_game_count > game_limit:
                print("Reached game limit")
                break
    return games

def add_games_to_slippi(slippi_files):
    for file in slippi_files:
        if get_slippi_file(file.filename):
            insert_slippi_file(file)
        else:
            insert_slippi_file(file)

if __name__ == "__main__":
    folders = ['C:\\Users\\cjsch\\Documents\\Slippi\\2022-11\\',
        'C:\\Users\\cjsch\\Documents\\Slippi\\2022-10\\',
        'C:\\Users\\cjsch\\Documents\\Slippi\\old\\']
    code = 'CATS#636' #Need to change this to be able to search for multiple codes

    files = get_slippi_files_multi_folder(folders)
    slippi_files = parse_files(files, -1)
    #print(slippi_files)

