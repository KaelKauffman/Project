from lxml import html
import requests
import json
import math
from time import sleep



class SteamSpy_API_Caller:

    def __init__(self, appFile="", tagFile=""):

        self.appFileName = appFile
        self.tagFileName = tagFile
        self.requiredGenres = []
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

    def setRequiredGenres(self, genres):
        self.requiredGenres = genres

    def getRequiredGenres(self):
        return self.requiredGenres 

    # Performs web scraping on steam store to search for the given game's app ID
    # Argument: search_string ; A string containing the name of the game; example: "Dota 2"
    # Returns: A list containing [id: string, image_link: string], with a string containing the steam app ID if the search contained a game that matched
    #          the search string, or a string of "999999999" (an invalid ID) if no matches were found
    def get_game_id_from_steam(self, search_string):
        try:
            steam_lookup_url = "https://store.steampowered.com/search/?term=" + search_string.replace(" ", "+")
            steam_page = requests.get(steam_lookup_url)
            html_tree = html.fromstring(steam_page.content)
            #xpath based on inspecting page source
            steam_store_urls = html_tree.xpath('//*[@id="search_result_container"]/div/a/@href')
            image_urls = html_tree.xpath('//*[@id="search_result_container"]/div/a/div/img/@src')
            results = []
            #Remove punctiation and capitals from search string, steam urls will never have these in the names
            search_string_formatted = search_string.replace(":", "").replace("!", "").replace("?", "").replace(",", "").replace("-", "").replace("  ", " ").lower()
            for i in range(len(steam_store_urls)):
                fields = steam_store_urls[i].split("/")
                name = fields[5].replace("_", " ").replace("  ", " ").lower()
                if search_string_formatted == name:
                    image_scrape = requests.get(image_urls[i])
                    return [fields[4], image_scrape.content]
            return ["999999999", ""]
        except:
            return ["999999999", ""]

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

    def get_ranked_by_rating(self, cut, with_conf=True):
        ranked = []
        if with_conf:
            ranked = sorted(self.app_data_cache.items(), key=lambda x: (0.5 + ((x[1]['positive'] / float(x[1]['positive']+x[1]['negative']))-0.5)*(1-1/float(math.log((x[1]['positive']+x[1]['negative']), 10)))), reverse=True)
        else:
            ranked = sorted(self.app_data_cache.items(), key=lambda x: (x[1]['positive'] / float(x[1]['positive']+x[1]['negative'])), reverse=True)
        result = []
        for i in range(0, cut):
            result.append([ranked[i][0], ranked[i][1]['name'], self.get_rating(ranked[i][0])])
        return result

    def get_ranked_by_hours(self, cut):
       
        ranked = sorted(self.app_data_cache.items(), key=lambda x: x[1]['median_2weeks'], reverse=True)
        result = []
        for i in range(0, cut):
            result.append([ranked[i][0], ranked[i][1]['name'], ranked[i][1]['median_2weeks']])
        return result
    
    
    def recommend_from_single_game(self, gameID, matchRate=0.5, cutoff=10, ratePower=1, confPower=1):
        if not str(gameID).isdigit():
            return []

        tags = self.get_tags_and_values(gameID)
        #tags = sorted(tags, key=lambda x: x[1], reverse=True)
        #Normalize the scores given to each tag
        tagSum = sum([t[1] for t in tags])
        tagWeights = [(tags[i][0], (len(tags)-i)*tags[i][1]/float(tagSum)) for i in range(len(tags))]

        frequency_list = {}
        for tag in tagWeights:
            #Take all tags of given game, add all games with those tags into a list
            gameList = list(self.get_games_with_tag(tag[0]).keys())
            #Make a set of pairs of game ID's and the tag similarity score with the given game
            for game in gameList:
                frequency_list[game] = frequency_list.get(game, 0) + 1
                    

        #Sort list by greatest number of tags in common and cut off at only the top items. 
        pre_final = sorted(frequency_list.items(), key=lambda x: x[1], reverse=True)
        original = pre_final[0]
        catch = len(pre_final)
        for i in range(len(pre_final)):
            if pre_final[i][1]/float(pre_final[0][1]) < matchRate:
                catch = i
                break
        pre_final = pre_final[0:catch]

        #Take the pre-final results and score them based on the difference between their weighted tag profiles
        #and the given game's. Lower difference scores indicate a closer match. 
        score_list = {}
        for game in pre_final:
            g_tags = self.get_tags_and_values(game[0])
            g_tagSum = sum([t[1] for t in g_tags])
            g_tagWeights = {g_tags[i][0]:((len(g_tags)-i)*g_tags[i][1]/float(g_tagSum)) for i in range(len(g_tags))}
            diff = sum([abs(t[1]-g_tagWeights.get(t[0],0)) for t in tagWeights])
            score_list[game[0]] = diff

        final = sorted(score_list.items(), key=lambda x: x[1])
        
        
        #Get the id, and name for each game in the cutoff
        #Compute a score using the number of tags in common and the player rating
        results = []
        for game in final:
            g_id = game[0]
            similarity = game[1]#/float(original[1])
            g_name = self.get_name(g_id)
            rate = self.get_rating(g_id)
            conf = (1-1/float(math.log(rate[1], 10)))
            revisedRate = 0.5 + (rate[0]-0.5)*math.pow(conf, confPower)
            #print([g_name, similarity, rate, conf, revisedRate])
            score = similarity*(1/math.pow(revisedRate, ratePower))
            results.append([g_id, g_name, score])
            
        #Sort final results by score 
        results = sorted(results, key=lambda x: x[2])

        if len(results) > cutoff:
            results = results[0:cutoff]
        
        return [ [r[0], r[1]] for r in results ]


    def recommend_multi_input(self, gameIDs=[], required_genres=[], banned_genres=[], banned_games=[], showTop=5, cross_thresh=0.5, matchRate=0.5, cutoff=10, ratePower=1, confPower=1):
        all_results = []
        for gameID in gameIDs:
            all_results.append( self.recommend_from_single_game(gameID, matchRate=matchRate, cutoff=cutoff, ratePower=ratePower, confPower=confPower) )
            
        for result in all_results:
            remove_list = []
            for r in result:
                r_genres = self.get_genres(r[0])
                found = False
                banned = False
                for g in r_genres:
                    if g in required_genres:
                        found = True
                        break
                    if g in banned_genres:
                        banned = True
                        break
        
                if r[0] in gameIDs or r[0] in banned_games or (found == False and len(required_genres) > 0) or banned:
                    remove_list.append(r)

            for r in remove_list:
                result.remove(r)

        
        frequency_list = {}
        for result in all_results:
            for r in result:
                frequency_list[r[0]] = frequency_list.get(r[0], 0) + 1

        cross_results = sorted(frequency_list.items(), key=lambda x: x[1], reverse=True)
        catch = len(cross_results)
        for i in range(len(cross_results)):
            if cross_results[i][1] < cross_thresh:
                catch = i
                break

        cross_results = cross_results[0:catch]

        final_cross = [ [c[0], self.get_name(c[0])] for c in cross_results ]

        final_single = [ [gameIDs[i], self.get_name(gameIDs[i]), all_results[i][0:showTop]] if len(all_results[i]) >= showTop else [gameIDs[i], self.get_name(gameIDs[i]), all_results[i]] for i in range(len(gameIDs)) ]

        return [final_cross, final_single]





        
            
        
