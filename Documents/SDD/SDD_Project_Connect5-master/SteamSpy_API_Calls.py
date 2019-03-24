from lxml import html
import requests
import json
import math
from time import sleep

class SteamSpy_API_Caller:

    def __init__(self, appFile="", tagFile=""):

        self.appFileName = appFile
        self.tagFileName = tagFile
        self.app_data_cache = dict()
        self.tag_data_cache = dict()
        
        if appFile != "":
            try:
                appCache = open(self.appFileName)
                self.app_data_cache = json.load(appCache)
                appCache.close()
            except:
                pass

        if tagFile != "":
            try:
                tagCache = open(self.tagFileName)
                self.tag_data_cache = json.load(tagCache)
                tagCache.close()
            except:
                pass

    def save_game_data_to_cache(self):
        try:
            appCache = open(self.appFileName, 'w')
            json.dump(self.app_data_cache, appCache)
            appCache.close()

            tagCache = open(self.tagFileName, 'w')
            json.dump(self.tag_data_cache, tagCache)
            tagCache.close()
            return True
        except:
            return False

    # Performs web scraping on steam store to search for the given game's app ID
    # Argument: search_string ; A string containing the name of the game; example: "Dota 2"
    # Returns: A string containing the steam app ID if the search contained a game that matched
    #          the search string, or a string of "999999999" (an invalid ID) if no matches were found
    def get_game_id_from_steam(self, search_string):
        steam_lookup_url = "https://store.steampowered.com/search/?term=" + search_string.replace(" ", "+")
        steam_page = requests.get(steam_lookup_url)
        html_tree = html.fromstring(steam_page.content)
        #xpath based on inspecting page source
        steam_store_urls = html_tree.xpath('//*[@id="search_result_container"]/div/a/@href')
        results = []
        #Remove punctiation and capitals from search string, steam urls will never have these in the names
        search_string_formatted = search_string.replace(":", "").replace("!", "").replace("?", "").replace(",", "").replace("-", "").replace("  ", " ").lower()
        for url in steam_store_urls:
            fields = url.split("/")
            name = fields[5].replace("_", " ").replace("  ", " ").lower()
            if search_string_formatted == name:
                return fields[4]
        return "999999999"

    def load_game_data(self, gameID):
        if not str(gameID).isdigit() or str(gameID) == "999999999":
            return False
        api_call_url = "https://steamspy.com/api.php?request=appdetails&appid=" + str(gameID)
        sleep(0.2)
        parsed_result = requests.get(api_call_url).json()
        if parsed_result["name"] == None:
            return False
        self.app_data_cache[str(gameID)] = parsed_result
        return True

    def load_tagged_games(self, tag_name):
        api_call_url = "https://steamspy.com/api.php?request=tag&tag=" + tag_name.replace(" ", "+")
        sleep(0.2)
        parsed_result = requests.get(api_call_url).json()
        if len(parsed_result) == 0:
            return False
        tag_entry = dict()
        for game in parsed_result:
            owned = parsed_result[game]['owners']
            owned = [int(x.strip().replace(",", "")) for x in owned.split("..")]
            if len(owned) > 0 and owned[0] >= 200000:
                tag_entry[game] = True
        self.tag_data_cache[tag_name] = tag_entry
        return True

    def get_games_with_tag(self, tag_name):
        if tag_name not in self.tag_data_cache:
            isRealID = self.load_tagged_games(tag_name)
            if not isRealID:
                return []
        return self.tag_data_cache[tag_name]

    def get_genres(self, gameID):
        if str(gameID) not in self.app_data_cache:
            isRealID = self.load_game_data(gameID)
            if not isRealID:
                return []
            
        genre = self.app_data_cache[str(gameID)]['genre']
        genre_list = [x.strip() for x in genre.split(',')]
        return genre_list

    def get_tags(self, gameID):
        if str(gameID) not in self.app_data_cache:
            isRealID = self.load_game_data(gameID)
            if not isRealID:
                return []
            
        tags = self.app_data_cache[str(gameID)]['tags']
        tag_list = list(tags.keys())
        return tag_list

    def get_tags_and_values(self, gameID):
        if str(gameID) not in self.app_data_cache:
            isRealID = self.load_game_data(gameID)
            if not isRealID:
                return []
            
        tags = self.app_data_cache[str(gameID)]['tags']
        tag_list = list(tags.items())
        return tag_list
    

    def get_rating(self, gameID):
        if str(gameID) not in self.app_data_cache:
            isRealID = self.load_game_data(gameID)
            if not isRealID:
                return []

        pos = self.app_data_cache[str(gameID)]['positive']
        neg = self.app_data_cache[str(gameID)]['negative']

        # Returns [ (pos / total) , total ]
        return [ pos/float(pos+neg), pos+neg ]

    def get_playtime(self, gameID):
        if str(gameID) not in self.app_data_cache:
            isRealID = self.load_game_data(gameID)
            if not isRealID:
                return []
            
        avg = self.app_data_cache[str(gameID)]['average_forever']
        med = self.app_data_cache[str(gameID)]['median_forever']
        
        #Calls are in minutes, but return is in hours
        return [avg/float(60), med/float(60)]

    def get_name(self, gameID):
        if str(gameID) not in self.app_data_cache:
            isRealID = self.load_game_data(gameID)
            if not isRealID:
                return ""

        return self.app_data_cache[str(gameID)]['name']

    def get_steam_price(self, gameID):
        if str(gameID) not in self.app_data_cache:
            isRealID = self.load_game_data(gameID)
            if not isRealID:
                return []
            
        currentPrice = self.app_data_cache[str(gameID)]['price']
        normalPrice = self.app_data_cache[str(gameID)]['initialprice']
        currentDiscount = self.app_data_cache[str(gameID)]['discount']

        return [currentPrice, normalPrice, currentDiscount]
    
    def recommend_similar_games(self, gameID, matchRate=0.7, cutoff=10, ratePower=2, confPower=2):
        if not str(gameID).isdigit():
            return []

        tags = self.get_tags(gameID)
        refRate = self.get_rating(gameID)
        refConf = (1-1/float(math.log(refRate[1], 10)))
        
        #Take all tags of given game, add all games with those tags into a list
        total_combined_tag_lists = []
        for tag in tags:
            gameList = self.get_games_with_tag(tag)
            total_combined_tag_lists += list(gameList.keys())

        #Make a set of pairs of game ID's and how many tags they share with given game
        frequency_list = {}
        for item in total_combined_tag_lists:
            frequency_list[item] = frequency_list.get(item, 0) + 1

        #Sort list by greatest number of tags in common and cut off at only the top items. 
        final = sorted(frequency_list.items(), key=lambda x: x[1], reverse=True)
        catch = 0
        for i in range(len(final)):
            if final[i][1]/float(len(tags)) < matchRate:
                catch = i
                break
            
        final = final[0:catch]

        #Get the id, and name for each game in the cutoff
        #Compute a score using the number of tags in common and the player rating
        results = []
        for game in final:
            g_id = game[0]
            similarity = game[1]/float(len(tags))
            g_name = self.get_name(g_id)
            rate = self.get_rating(g_id)
            conf = (1-1/float(math.log(rate[1], 10)))
            conf = conf/float(refConf)
            revisedRate = 0.5 + (rate[0]-0.5)*math.pow(conf, confPower)
            print([g_name, similarity, rate, conf, revisedRate])
            score = similarity*math.pow(revisedRate, ratePower)
            results.append([g_id, g_name, score])
            
        #Sort final results by score 
        results = sorted(results, key=lambda x: x[2], reverse=True)

        if len(results) > cutoff:
            results = results[0:cutoff]
        
        return results
            
        
