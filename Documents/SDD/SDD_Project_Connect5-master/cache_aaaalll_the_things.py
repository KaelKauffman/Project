from SteamSpy_API_Calls import SteamSpy_API_Caller
import requests

steam_api = SteamSpy_API_Caller(appFile="SteamSpy_App_Cache.txt", tagFile="SteamSpy_Tags_Cache.txt")

super_cache = steam_api.tag_data_cache

frequency_list = {}
for tag in super_cache:
    gamesList = list(super_cache[tag].keys())
    for item in gamesList:
        frequency_list[item] = frequency_list.get(item, 0) + 1

all_games = list(frequency_list.keys())
print("Total: " + str(len(all_games)))
print(int(len(all_games)/20))
for i in range(len(all_games)):
    print(str(i+1) + " : " + steam_api.get_name(all_games[i]))
    if i%(int(len(all_games)/20)) == 0:
        check = steam_api.save_game_data_to_cache()
        print("Saving... " + str(check)) #Saved to cache successfully.

check = steam_api.save_game_data_to_cache()
print("Saving Final... " + str(check)) #Saved to cache successfully.

##result = steam_api.app_data_cache
##super_apps = list(result.keys())
##tag_pile = []
##for t in super_apps:
##    #print(t)
##    t_tags = steam_api.get_tags(t)
##    tag_pile += t_tags
##
##check = steam_api.save_game_data_to_cache()
##print(check) #Saved to cache successfully.
##
##frequency_list = {}
##for item in tag_pile:
##    frequency_list[item] = frequency_list.get(item, 0) + 1
##
##all_tags = list(frequency_list.keys())
##print(len(all_tags))
##
##for i in range(len(all_tags)):
##    junk = steam_api.get_games_with_tag(all_tags[i])
##    print(str(i+1) + " " + all_tags[i] + " : " + str(len(junk) > 0))
##    if i%(int(len(all_tags)/10)) == 0:
##        check = steam_api.save_game_data_to_cache()
##        print("Saving... " + str(check)) #Saved to cache successfully.
##
##check = steam_api.save_game_data_to_cache()
##print("Saving Final... " + str(check)) #Saved to cache successfully.
