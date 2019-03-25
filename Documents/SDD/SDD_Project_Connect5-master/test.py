from SteamSpy_API_Calls import SteamSpy_API_Caller
from ITAD_API_Calls import ITAD_API_Caller
from User import SteamUser
from time import sleep

kael_id = '76561198046994663'
wellsee_id = '76561198319742744'

steam_api = SteamSpy_API_Caller(appFile="SteamSpy_App_Cache.txt", tagFile="SteamSpy_Tags_Cache.txt")
itad_api = ITAD_API_Caller()
steam_user = SteamUser(kael_id, userFile="User_Data_Cache.txt")

game_name_list = [ "Factorio", "Subnautica", "Slay the Spire", "Terraria" ]
game_ids = []
for name in game_name_list:
    game_ids.append(steam_api.get_game_id_from_steam(name))
    sleep(0.25)
print(game_ids)


all_the_things = [ steam_user.getName(), steam_user.getPlayedGames(), steam_user.getTotalHours(), steam_user.getSteamWorth() ]
print(all_the_things)
print(steam_user.getDesiredGames())
for g in game_ids:
    steam_user.addDesiredGame(g)
print(steam_user.getDesiredGames())
print(steam_user.getRecommendGames())
for g in game_ids:
    steam_user.addRecommendGame(g)
print(steam_user.getRecommendGames())

print(steam_user.save_user_data_to_cache())



### Multi-game Recommendation Test ###

all_results = steam_api.recommend_multi_input(gameIDs=steam_user.getRecommendGames(), required_genres=[], banned_genres=[], banned_games=[], showTop=5, cross_thresh=3, matchRate=0.5, cutoff=10, ratePower=1, confPower=3)

print("Cross-Recommendation Results:")
for r in all_results[0]:
    print(r)

for results in all_results[1]:
    print("Recommendations from " + results[1] + " (" + results[0] + "):")
    for r in results[2]:
        print(r)

check = steam_api.save_game_data_to_cache()
print(check) #Saved to cache successfully.

for g in game_ids:
    p = itad_api.get_plain(g)
    print(g + " : " + p)
    prices = itad_api.get_prices(p)
    print(prices)


##game_title_to_search = "Slay the Spire"
##
###If the appID is already known, it can be entered here directly.
###appID = 000000
###Otherwise, this tries to find it by web-scraping a game title search on the Steam online store.
##appID = steam_api.get_game_id_from_steam(game_title_to_search)
##
##genres = steam_api.get_genres(appID)
##tags = steam_api.get_tags(appID)
##rate = steam_api.get_rating(appID)
##play = steam_api.get_playtime(appID)
##name = steam_api.get_name(appID)
##prices = itad_api.get_prices(itad_api.get_plain(appID))
##
##print(appID)
##print(genres)
##print(tags)
##print(rate)
##print(play)
##print(name)
##
##print("Lowest Price in History: " + str(prices[0]))
##print("Current Prices: " + str(prices[1:]))
##print()
##
##print("Loading Recommender... May take 30 seconds or more if tags are not cached.")
##recommend = steam_api.recommend_similar_games(appID, matchRate=0.5, cutoff=10, ratePower=2, confPower=5)
##print("Done.")
##print()
##
##print("Recommendations:  [ id, name, score ]")
##for r in recommend:
##    print(r)



