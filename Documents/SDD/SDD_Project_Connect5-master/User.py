import requests
import json


class SteamUser:
    
    def __init__(self, steamID="00000", token='7C8A11057FBAB292E6E6B0AF1F6E9D19',userFile="",ITAD_key="d8afa81cf7dc8b756e919d557ce68ccadf5405eb"):
        self.steamID = steamID
        self.steam_token = token
        self.ITAD_Key = ITAD_key
        self.userFileName = userFile
        self.user_data_cache = dict()
        
        if userFile !="":
            try:
                userCache = open(self.userFileName)
                self.user_data_cache = json.load(userCache)
                userCache.close()
            except:
                pass

        if self.steamID != "":
            self.loginSteamID(self.steamID)
        
    def save_user_data_to_cache(self):
            try:
                userCache = open(self.userFileName, 'w')
                json.dump(self.user_data_cache, userCache)
                userCache.close()

                return True
            except:
                return False

    def getAllUsers(self):
        all_ids = list(self.user_data_cache.keys())
        results = [ [u_id, self.user_data_cache[u_id]['name']] for u_id in all_ids]
        return results
        
    def getSteamID(self):
        return self.steamID
    
    def loginSteamID(self,ID):
        self.steamID = ID
        if self.steamID not in self.user_data_cache:
            self.user_data_cache[self.steamID] = {'name':"", 'desiredGames':[], 'playedGames':[], 'recommendGames':[], 'banList':[], 'hoursPlayed':0, 'accountWorth':0}
            check = self.loadName()
            check = self.loadPlayedGames()
            check = self.loadSteamWorth()
            self.save_user_data_to_cache()

    def loadName(self):
        try:
            summary_url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key="+self.steam_token+"&steamids="+self.steamID
            player = requests.get(summary_url).json()
            player = player['response']
            player = player['players'][0]
            player = player['personaname']
            self.user_data_cache[self.steamID]['name'] = player
            return True
        except:
            self.user_data_cache[self.steamID]['name'] = "NO LOGIN"
            return False

    def loadPlayedGames(self, playMinutesThreshold=10): 
        try:
            recent_games_url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="+self.steam_token+"&steamid="+self.steamID+"&format=json"
            games = requests.get(recent_games_url).json()
            totalHours = 0
            games = games['response']
            games = games['games']
            games_list = []
            for game in games:
                game_id = game['appid']
                play_time = game['playtime_forever']
                game_info = game_id,play_time
                totalHours += play_time/float(60)
                if play_time >= playMinutesThreshold:
                    games_list.append(game_info)
            self.user_data_cache[self.steamID]['playedGames'] = games_list
            self.user_data_cache[self.steamID]['hoursPlayed'] = totalHours
            return True
        except:
            return False
    
    def get_plain(self, steam_game_id):
        try:
            api_call_url = "https://api.isthereanydeal.com/v02/game/plain/?key=" + self.ITAD_Key + "&shop=steam&game_id=app%2F" + str(steam_game_id)
            parsed_result = requests.get(api_call_url).json()
            if parsed_result['.meta']['match'] == False:
                return ""
            return parsed_result['data']['plain']
        except:
            return ""
        
    def loadSteamWorth(self):
        playedGames = self.user_data_cache[self.steamID]['playedGames']
        worthTotal = 0
        try:
            for game in playedGames:
                app_plain = self.get_plain(game[0])
                if app_plain == "":
                    continue
                else:
                    api_call_url = "https://api.isthereanydeal.com/v01/game/prices/?key=" + self.ITAD_Key + "&plains=" + app_plain + "&country=US"
                    parsed_result = requests.get(api_call_url).json()
                    price_list = parsed_result['data'][app_plain]['list']
                    return_list =[]
                    for p in price_list:
                        if p['shop']['id'] == "steam":
                            worthTotal+=p['price_new']
                            break
            self.user_data_cache[self.steamID]['accountWorth'] = worthTotal
            return True
        except:
            self.user_data_cache[self.steamID]['accountWorth'] = -1
            return False

    def getName(self):
        return self.user_data_cache[self.steamID]['name']
    
    def getPlayedGames(self):
        return self.user_data_cache[self.steamID]['playedGames']

    def getTotalHours(self):
        return self.user_data_cache[self.steamID]['hoursPlayed']

    def getSteamWorth(self):
        return self.user_data_cache[self.steamID]['accountWorth']
    
    def getDesiredGames(self):
        return self.user_data_cache[self.steamID]['desiredGames']
    
    def addDesiredGame(self,game):
        desiredGames = self.user_data_cache[self.steamID]['desiredGames']
        if game not in desiredGames:
            desiredGames.append(game)
        
    def deleteDesiredGame(self, game):
        desiredGames = self.user_data_cache[self.steamID]['desiredGames']
        if(game in desiredGames):
            g = desiredGames.index(game)
            del desiredGames[g]

    def getRecommendGames(self):
        return self.user_data_cache[self.steamID]['recommendGames']
    
    def addRecommendGame(self,game):
        recommendGames = self.user_data_cache[self.steamID]['recommendGames']
        if game not in recommendGames:
            recommendGames.append(game)
        
    def deleteRecommendGame(self, game):
        recommendGames = self.user_data_cache[self.steamID]['recommendGames']
        if(game in recommendGames):
            g = recommendGames.index(game)
            del recommendGames[g]

    def getBanList(self):
        return self.user_data_cache[self.steamID]['banList']
    
    def addBanList(self,game):
        banList = self.user_data_cache[self.steamID]['banList']
        if game not in banList:
            banList.append(game)
        
    def deleteBanList(self, game):
        banList = self.user_data_cache[self.steamID]['banList']
        if(game in banList):
            g = banList.index(game)
            del banList[g]

