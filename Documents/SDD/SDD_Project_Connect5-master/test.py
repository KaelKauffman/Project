from SteamSpy_API_Calls import SteamSpy_API_Caller
from ITAD_API_Calls import ITAD_API_Caller

steam_api = SteamSpy_API_Caller(appFile="SteamSpy_App_Cache.txt", tagFile="SteamSpy_Tags_Cache.txt")
itad_api = ITAD_API_Caller()

game_title_to_search = "Dota 2"

#If the appID is already known, it can be entered here directly.
#appID = 000000
#Otherwise, this tries to find it by web-scraping a game title search on the Steam online store.
appID = steam_api.get_game_id_from_steam(game_title_to_search)

genres = steam_api.get_genres(appID)
tags = steam_api.get_tags(appID)
rate = steam_api.get_rating(appID)
play = steam_api.get_playtime(appID)
name = steam_api.get_name(appID)
prices = itad_api.get_prices(itad_api.get_plain(appID))

print(appID)
print(genres)
print(tags)
print(rate)
print(play)
print(name)

print("Lowest Price in History: " + str(prices[0]))
print("Current Prices: " + str(prices[1:]))
print()

print("Loading Recommender... May take 30 seconds or more if tags are not cached.")
recommend = steam_api.recommend_similar_games(appID, matchRate=0.5, cutoff=10, ratePower=1, confPower=5)
print("Done.")
print()

print("Recommendations:  [ id, name, score ]")
for r in recommend:
    print(r)


check = steam_api.save_game_data_to_cache()
print(check) #Saved to cache successfully.
