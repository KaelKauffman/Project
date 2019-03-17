import simplejson as json
import requests
import urllib

steam_id = '76561197960434622'
steam_token = '7C8A11057FBAB292E6E6B0AF1F6E9D19'

class User:
    def __init__(self, steamID):
        self.steamID = steamID
        self.name = ''
        self.desiredGames = []
        self.gameTags = []
    def getPlayerName(steamID):
        summary_url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key="+steam_token+"&steamids="+steamID
        steam_data = urllib.urlopen(summary_url)
        player = json.loads(steam_data.read())
        player = player['response']
        player = player['players'][0]
        player = player['personaname']
        return player
    def getPlayedGames(steamID):
        recent_games_url = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key="+steam_token+"&steamid="+steamID+"&format=json"
        steam_data = urllib.urlopen(recent_games_url)
        games = json.loads(steam_data.read())
        games = games['response']
        games = games['games']
        games_list = []
        for game in games:
            game_id = game['appid']
            game_name = game['name']
            play_time = game['playtime_2weeks']
            game_info = game_id,game_name,play_time
            games_list.append(game_info)
        return games_list    
    
def getPlayerName(steamID):
    summary_url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key="+steam_token+"&steamids="+steamID
    steam_data = urllib.urlopen(summary_url)
    player = json.loads(steam_data.read())
    player = player['response']
    player = player['players'][0]
    player = player['personaname']
    print player


def getPlayedGames(steamID):
    recent_games_url = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key="+steam_token+"&steamid="+steamID+"&format=json"
    steam_data = urllib.urlopen(recent_games_url)
    games = json.loads(steam_data.read())
    games = games['response']
    games = games['games']
    games_list = []
    for game in games:
        game_id = game['appid']
        game_name = game['name']
        play_time = game['playtime_2weeks']
        game_info = game_id,game_name,play_time
        games_list.append(game_info)
    return games_list

def getGenres(gameID):
    genre_url = "https://steamspy.com/api.php?request=appdetails&appid="+str(gameID)
    check = requests.get(genre_url)
    if(check.status_code!=200):
        return None
    steam_data = urllib.urlopen(genre_url)
    genre = json.loads(steam_data.read())
    genre = genre ['genre']
    genre_list = [x.strip() for x in genre.split(',')]
    return map(str,genre_list)

def getRelatedGames(genreList):
    related_list = []
    bad_list = []
    apps_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    steam_data = urllib.urlopen(apps_url)
    apps = json.loads(steam_data.read())
    apps = apps['applist']
    apps = apps['apps']
    for app in apps:
        genres = getGenres(app['appid'])
        if genres == None:
            bad_list.append(app['appid'])
            continue
        intersection = list(set(genreList) & set(genres))
        if(len(intersection)>0): 
            app_id = app['appid']
            app_name = app['name']
            app_info = app_id,app_name,intersection
            related_list.append(app_info)
    print related_list
    print
    print bad_list
    
    
a = getGenres("7730") 
print getRelatedGames(a)

