import requests


class ITAD_API_Caller:

    def __init__(self, key="d8afa81cf7dc8b756e919d557ce68ccadf5405eb"):
        self.ITAD_KEY = key

    # Calls the ITAD API to get the "plain", which is the ITAD game identifier within the API
    # Argument: steam_game_id ; A string or int containing a steam app ID
    # Returns: A string containing the ITAD plain for that game, or an empty string if the app ID was not found
    def get_plain(self, steam_game_id):
        api_call_url = "https://api.isthereanydeal.com/v02/game/plain/?key=" + self.ITAD_KEY + "&shop=steam&game_id=app%2F" + str(steam_game_id)
        parsed_result = requests.get(api_call_url).json()
        if parsed_result['.meta']['match'] == False:
            return ""
        return parsed_result['data']['plain']


    # Calls the ITAD API to get the current prices on all vendors and the historically lowest price
    # Argument: itad_game_plain ; A string containing the ITAD game plain
    # Returns: A list containing the price information for the game, or an empty list if the game plain was not invalid
    # List structure: [ [ vendor_lowest, lowest_price ] , [ vendor_1, price_1 ] , [ vendor_2, price_2 ] ... [ vendor_x, price_x ] ]
    def get_prices(self, itad_game_plain):
        if itad_game_plain == "":
            return []
        
        api_call_url = "https://api.isthereanydeal.com/v01/game/prices/?key=" + self.ITAD_KEY + "&plains=" + itad_game_plain + "&country=US"
        parsed_result = requests.get(api_call_url).json()
        price_list = parsed_result['data'][itad_game_plain]['list']
        if len(price_list) == 0:
            return []

        api_call_url = "https://api.isthereanydeal.com/v01/game/lowest/?key=" + self.ITAD_KEY + "&plains=" + itad_game_plain + "&country=US"
        parsed_result = requests.get(api_call_url).json()
        lowest_price = [parsed_result['data'][itad_game_plain]['shop']['name'], parsed_result['data'][itad_game_plain]['price']]
        
        results = []
        results.append(lowest_price)
        for price in price_list:
            results.append([price['shop']['name'], price['price_new'], price['price_cut']])
        return results
