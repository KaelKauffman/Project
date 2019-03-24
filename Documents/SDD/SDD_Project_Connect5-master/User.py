import requests
import json

steam_id = '76561197960434622'

class User:
    
    def __init__(self, steamID, token='7C8A11057FBAB292E6E6B0AF1F6E9D19',userFile="",ITAD_key="d8afa81cf7dc8b756e919d557ce68ccadf5405eb"):
        self.steamID = steamID
        self.steam_token = token
        self.ITAD_Key = itad_key
        self.name = ''
        self.desiredGames = []
        self.playedGames = []
        self.gameTags = []
        self.userFileName = userFile
        self.user_data_cache = dict()
        self.steamAccountWorth = 0
        if userFile !="":
            try:
                userCache = open(self.userFileName)
                self.user_data_cache = json.load(userCache)
                userCache.close()
            except:
                pass
        
    def save_user_data_to_cache(self):
            try:
                userCache = open(self.userFileName, 'w')
                json.dump(self.user_data_cache, userCache)
                userCache.close()

                return True
            except:
                return False
    '''
    def load_user_data(self):
        self.app
        
    '''
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
    
    def get_plain(steam_game_id):
        api_call_url = "https://api.isthereanydeal.com/v02/game/plain/?key=" + self.ITAD_Key + "&shop=steam&game_id=app%2F" + str(steam_game_id)
        parsed_result = requests.get(api_call_url).json()
        if parsed_result['.meta']['match'] == False:
            return ""
        return parsed_result['data']['plain']   
    
    def get_Steam_Worth(itad_game_plain):
        if itad_game_plain == "":
            return []
    
        api_call_url = "https://api.isthereanydeal.com/v01/game/prices/?key=" + self.ITAD_Key + "&plains=" + itad_game_plain + "&country=US"
        parsed_result = requests.get(api_call_url).json()
        price_list = parsed_result['data'][itad_game_plain]['list']
        return_list =[]
        for p in price_list:
            shop = p['shop']
            if shop['id'] == "steam":
                self.steamAccountWorth+=p['price_new']
        return accountWorth    
    
    


'''
print get_plain('954870')
x = get_plain('954870')
print get_prices(x,0)
'''