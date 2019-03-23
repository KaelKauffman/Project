import requests

steam_id = '76561197960434622'
steam_token = '7C8A11057FBAB292E6E6B0AF1F6E9D19'

class User:
    
    def __init__(self, steamID):
        self.steamID = steamID
        self.name = ''
        self.desiredGames = []
        self.playedGames = []
        self.gameTags = []
        
    def getSteamID(self):
        return self.steamID
    
    def setSteamID(self,ID):
        self.steamID = ID
    
    def getDesiredGames(self):
        return self.desiredGames
    
    def addDesiredGame(self,game):
        self.desiredGames.append(game)
        
    def deleteDesiredGame(self, game):
        if(game in desiredGames):
            g = desiredGames.index(game)
            del desiredGames[g]
    
    def getName(self):
        return self.name
    
    def setName(self):
        summary_url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key="+steam_token+"&steamids="+steamID
        player = requests.get(summary_url).json()
        try:
            player = player['response']
            player = player['players'][0]
            player = player['personaname']
            self.name = player
        except:
            return "Error: Player Name No Response"
     
    def getPlayedGames(steamID):
        recent_games_url = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key="+steam_token+"&steamid="+steamID+"&format=json"
        games = requests.get(recent_games_url).json()
        try:
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
        except:
            return []
    
    def getTags(self):
        return gameTags
    
    def addTag(self,tag):
        self.gameTags.append(tag)
    
    def deleteTag(self, tag):
        if(tag in gameTags):
            t = gameTags.index(tag)
            del desiredGames[t]    
    
    def getGenre(gameID):
        genre_url = "https://steamspy.com/api.php?request=appdetails&appid="+str(gameID)
        genre = requests.get(genre_url).json()
        try:
            genre = genre['genre']
            genre_list = [x.strip() for x in genre.split(',')]
            return genre_list            
        except:
            return []        

def getPlayedGames(steamID):
    recent_games_url = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key="+steam_token+"&steamid="+steamID+"&format=json"
    games = requests.get(recent_games_url).json()
    try:
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
    except:
        return []
    
def getGenre(gameID):
    genre_url = "https://steamspy.com/api.php?request=appdetails&appid="+str(gameID)
    genre = requests.get(genre_url).json()
    try:
        genre = genre['genre']
        genre_list = [x.strip() for x in genre.split(',')]
        genre_list = map(str,genre_list)
        return genre_list            
    except:
        return []

print (getGenre(730))
print (getPlayedGames(steam_id))
       