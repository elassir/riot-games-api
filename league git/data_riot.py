from flask import Flask, render_template
import pandas as pd
import requests
from collections import defaultdict
import time
app = Flask(__name__)

def get_participant_team(match_data, summoner_name):
    for participant in match_data['info']['participants']:
        if participant['summonerName'].lower() == summoner_name.lower():
            return participant['teamId']
    return None

def get_team_bans(match_data, team_id):
    if 'teams' in match_data['info']:
        for team in match_data['info']['teams']:
            if team['teamId'] == team_id and 'bans' in team:
                return [ban['championId'] for ban in team['bans']]
    return []

def get_match_result(match_data, summoner_name):
    for participant in match_data['info']['participants']:
        if participant['summonerName'].lower() == summoner_name.lower():
            return participant['win']
    return None

def get_vision_wards_bought(match_data, summoner_name):
    for participant in match_data['info']['participants']:
        if participant['summonerName'].lower() == summoner_name.lower():
            return participant['visionWardsBoughtInGame']
    return None

def get_champion_id(match_data, summoner_name):
    for participant in match_data['info']['participants']:
        if participant['summonerName'].lower() == summoner_name.lower():
            return participant['championId']
    return None

def get_average_pings(match_data, summoner_name):
    for participant in match_data['info']['participants']:
        if participant['summonerName'].lower() == summoner_name.lower():
            ping_types = ["allInPings", "assistMePings", "baitPings", "basicPings", "commandPings", "dangerPings", "getBackPings","enemyMissingPings", "holdPings", "needVisionPings", "onMyWayPings","pushPings", "visionClearedPings"]
            total_pings = sum(participant[ping] for ping in ping_types if ping in participant)
            return total_pings 
    return None


@app.route("/")
def home():
    api_key = 'RGAPI-3d6c1cb4-3c9c-40a6-ba24-e13475cb2098'
    summoner_names = ['sampiklesyeux', 'Barkeagles', 'MisterJLB' ]  # 'Montépixou', 'Alfortville'
    region = 'euw1'

    # Fetch the champion data
    champion_response = requests.get('https://ddragon.leagueoflegends.com/cdn/14.23.1/data/en_US/champion.json')
    champion_data = champion_response.json()

    champion_dict = {}
    for champ, data in champion_data['data'].items():
        champion_dict[int(data['key'])] = {'name': champ, 'icon_url': f"http://ddragon.leagueoflegends.com/cdn/14.23.1/img/champion/{data['image']['full']}"}

    data_list = []
    for summoner_name in summoner_names:
        response = requests.get(f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}')
        data = response.json()

        
        
            
        if 'accountId' in data:
            account_id = data['puuid']
            listematches = requests.get(f'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{account_id}/ids?start=0&count=20&api_key={api_key}')
            match_ids = listematches.json()

            total_vision_wards_bought = 0
            match_count = 0
            win_count = 0
            total_average_pings = 0
            champion_win_count = {}
            ban_counts = defaultdict(int)

            for match_id in match_ids:
                match_response = requests.get(f'https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}')
                match_data = match_response.json()

                if 'info' not in match_data or 'participants' not in match_data['info']:
                    continue

                if match_data['info']['gameMode'] == 'ARAM':
                    continue

                team_id = get_participant_team(match_data, summoner_name)
                if team_id is not None:
                    bans = get_team_bans(match_data, team_id)
                    for ban in bans:
                        ban_counts[ban] += 1

                result = get_match_result(match_data, summoner_name)
                if result is not None:
                    win_count += result
                
                average_pings = get_average_pings(match_data, summoner_name)
                if average_pings is not None:
                    total_average_pings += average_pings

                vision_wards_bought = get_vision_wards_bought(match_data, summoner_name)
                if vision_wards_bought is not None:
                    total_vision_wards_bought += vision_wards_bought

                champion_id = get_champion_id(match_data, summoner_name)
                if champion_id is not None:
                    champion = champion_dict.get(champion_id, {'name': 'Unknown', 'icon_url': '#'})
                    if champion['name'] not in champion_win_count:
                        champion_win_count[champion['name']] = {'games': 0, 'wins': 0, 'icon_url': champion['icon_url']}
                    champion_win_count[champion['name']]['games'] += 1
                    if result:
                        champion_win_count[champion['name']]['wins'] += 1

                match_count += 1

            top_champions = sorted(champion_win_count.items(), key=lambda item: item[1]['games'], reverse=True)[:4]
            top_champions = [{'name': k, 'games': v['games'], 'wins': v['wins'], 'winrate': v['wins']*100/v['games'] if v['games'] > 0 else 0, 'icon_url': v['icon_url']} for k, v in top_champions]

            top_bans = sorted(ban_counts.items(), key=lambda item: item[1], reverse=True)[:3]
            top_bans = [{'name': champion_dict.get(ban_id, {'name': 'Unknown', 'icon_url': '#'})['name'], 'icon_url': champion_dict.get(ban_id, {'name': 'Unknown', 'icon_url': '#'})['icon_url']} for ban_id, _ in top_bans]

            if match_count > 0:
                average_vision_wards_bought = total_vision_wards_bought / match_count
                average_pings = total_average_pings / match_count
                data_list.append([summoner_name, win_count, match_count, average_vision_wards_bought,average_pings, top_champions, top_bans])

    return render_template('home.html', data_list=data_list)

if __name__ == "__main__":
    app.run(debug=True)
