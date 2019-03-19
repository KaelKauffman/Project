from lxml import html
import requests


ITAD_KEY = "d8afa81cf7dc8b756e919d557ce68ccadf5405eb"


# Performs web scraping on steam store to search for the given game's app ID
# Argument: search_string ; A string containing the name of the game; example: "Dota 2"
# Returns: A string containing the steam app ID if the search contained a game that matched
#          the search string, or an empty string if no matches were found
def get_game_id_from_steam(search_string):
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
    return ""


# Calls the ITAD API to get the "plain", which is the ITAD game identifier within the API
# Argument: steam_game_id ; A string or int containing a steam app ID
# Returns: A string containing the ITAD plain for that game, or an empty string if the app ID was not found
def get_plain_from_itad_api(steam_game_id):
    api_call_url = "https://api.isthereanydeal.com/v02/game/plain/?key=" + ITAD_KEY + "&shop=steam&game_id=app%2F" + str(steam_game_id)
    parsed_result = requests.get(api_call_url).json()
    if parsed_result['.meta']['match'] == False:
        return ""
    return parsed_result['data']['plain']


# Calls the ITAD API to get the current prices on all vendors and the historically lowest price
# Argument: itad_game_plain ; A string containing the ITAD game plain
# Returns: A list containing the price information for the game, or an empty list if the game plain was not invalid
# List structure: [ [ vendor_lowest, lowest_price ] , [ vendor_1, price_1 ] , [ vendor_2, price_2 ] ... [ vendor_x, price_x ] ]
def get_prices_from_itad_api(itad_game_plain):
    if itad_game_plain == "":
        return []
    
    api_call_url = "https://api.isthereanydeal.com/v01/game/prices/?key=" + ITAD_KEY + "&plains=" + itad_game_plain + "&country=US"
    parsed_result = requests.get(api_call_url).json()
    price_list = parsed_result['data'][itad_game_plain]['list']
    if len(price_list) == 0:
        return []

    api_call_url = "https://api.isthereanydeal.com/v01/game/lowest/?key=" + ITAD_KEY + "&plains=" + itad_game_plain + "&country=US"
    parsed_result = requests.get(api_call_url).json()
    lowest_price = [parsed_result['data'][itad_game_plain]['shop']['name'], parsed_result['data'][itad_game_plain]['price']]
    
    results = []
    results.append(lowest_price)
    for price in price_list:
        results.append([price['shop']['name'], price['price_new'], price['price_cut']])
    return results
