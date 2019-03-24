from SteamSpy_API_Calls import SteamSpy_API_Caller
import requests

steam_api = SteamSpy_API_Caller(appFile="SteamSpy_App_Cache.txt", tagFile="SteamSpy_Tags_Cache.txt")


result = requests.get("https://steamspy.com/api.php?request=top100in2weeks").json()
top100 = list(result.keys())
tag_pile = []
for t in top100:
    print(t)
    t_tags = steam_api.get_tags(t)
    tag_pile += t_tags

check = steam_api.save_game_data_to_cache()
print(check) #Saved to cache successfully.

frequency_list = {}
for item in tag_pile:
    frequency_list[item] = frequency_list.get(item, 0) + 1

all_tags = list(frequency_list.keys())
print(len(all_tags))

for t in all_tags:
    flag = steam_api.load_tagged_games(t)
    print(t + " : " + str(flag))

check = steam_api.save_game_data_to_cache()
print(check) #Saved to cache successfully.
