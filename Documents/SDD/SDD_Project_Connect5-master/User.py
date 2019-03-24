import requests

steam_id = '76561197960434622'

class User:
    
    def __init__(self, steamID, token='7C8A11057FBAB292E6E6B0AF1F6E9D19'):
        self.steamID = steamID
        self.steam_token = token
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
    
    def loadName(self):
        summary_url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key="+self.steam_token+"&steamids="+self.steamID
        player = requests.get(summary_url).json()
        try:
            player = player['response']
            player = player['players'][0]
            player = player['personaname']
            self.name = player
            return True
        except:
            return False

    def getPlayedGames(self):
        return self.playedGames
     
    def loadPlayedGames(self, playMinutesThreshold=0):
        recent_games_url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="+self.steam_token+"&steamid="+self.steamID+"&format=json"
        games = requests.get(recent_games_url).json()
        try:
            games = games['response']
            games = games['games']
            games_list = []
            for game in games:
                game_id = game['appid']
                play_time = game['playtime_forever']
                game_info = game_id,play_time
                if play_time >= playMinutesThreshold:
                    games_list.append(game_info)
            self.playedGames = games_list
            return True
        except:
            return False
    
    def getTags(self):
        return gameTags
    
    def addTag(self,tag):
        self.gameTags.append(tag)
    
    def deleteTag(self, tag):
        if(tag in gameTags):
            t = gameTags.index(tag)
            del desiredGames[t]

       
