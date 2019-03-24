from SteamSpy_API_Calls import SteamSpy_API_Caller
from ITAD_API_Calls import ITAD_API_Caller

steam_api = SteamSpy_API_Caller(appFile="SteamSpy_App_Cache.txt", tagFile="SteamSpy_Tags_Cache.txt")
itad_api = ITAD_API_Caller()

appID = steam_api.get_game_id_from_steam("Factorio")

genres = steam_api.get_genres(appID)
tags = steam_api.get_tags(appID)
rate = steam_api.get_rating(appID)
play = steam_api.get_playtime(appID)
name = steam_api.get_name(appID)

tagTest = steam_api.get_games_with_tag("Indie")

check = steam_api.save_game_data_to_cache()

prices = itad_api.get_prices(itad_api.get_plain(appID))

print(appID)
print(genres)
print(tags)
print(rate)
print(play)
print(name)
print(check)
print(prices)
print()
print(tagTest)
print(len(tagTest))


