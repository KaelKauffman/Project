from PyQt5 import QtGui, QtWidgets
import requests
from io import BytesIO
from PIL import Image
from PIL.ImageQt import ImageQt
from datetime import datetime

from SteamSpy_API_Calls import SteamSpy_API_Caller
from SteamRush_PyQT_Setup import Main_GUI_Visuals
from ITAD_API_Calls import ITAD_API_Caller
from User import SteamUser


# This class encapsulates the "Model" component of our Model-View-Controller application pattern.
# Attributes include instances of the API call objects with internal cache databases, the
# User object with internal cache of user information, and several list structures, between which
# the internal state of the GUI is represented. Operations allow for manulipation of the internal
# state through the list contents and state of the User object.
class GUI_Content_Model():

    def __init__(self):
        #API Call objects
        self.steam_api = SteamSpy_API_Caller(appFile="SteamSpy_App_Cache.txt",\
        									 tagFile="SteamSpy_Tags_Cache.txt")
        self.itad_api = ITAD_API_Caller()

        #User object
        self.steam_user = SteamUser(userFile="User_Data_Cache.txt")
        #self.steam_user.loginSteamID("76561198046994663")

        #Model Information
        self.wishListContent = []
        self.selectedWishItem = 0
        self.recommendListContent = []
        self.selectedRecItem = 0
        self.lastGameSearched = "999999999"

        self.loadWishlistItems(self.steam_user.getDesiredGames())

    # Sets wish list to that of the currently active User
    def loadWishlistItems(self, gamesList):
        wishlist = [self.steam_api.get_name(g_id) for g_id in gamesList]

        raw_prices = [self.itad_api.get_prices(self.itad_api.get_plain(g_id)) for g_id in gamesList]
        revised_prices = []
        for item in raw_prices:
            if len(item) > 1:
                s_p = ("Steam", 9999)
                l_p = ("Steam", 9999)
                for i in range(1, len(item)):
                    if item[i][0] == "Steam":
                        s_p = item[i]
                    if (l_p[1] - item[i][1]) > 0.1:
                        l_p = item[i]
                revised_prices.append([s_p, l_p])
            else:
                revised_prices.append([("Steam", -1), ("Steam", -1)])

        for g in range(len(wishlist)):
            self.wishListContent.append([wishlist[g], revised_prices[g], gamesList[g]])

    # Sets recommend input list to that of the currently active User
    def loadRecommendItems(self, gamesList):
        reclist = [self.steam_api.get_name(g_id) for g_id in gamesList]

        for g in range(len(reclist)):
            self.recommendListContent.append([gamesList[g], reclist[g]])

    # Adds a game by ID to the wishlist and to the active User
    def addToWishlist(self, gameID):
        if gameID != "999999999":
            found = False
            name = self.steam_api.get_name(gameID)
            for item in self.wishListContent:
                if item[0] == name:
                    found = True
                    break
            if not found:
                self.loadWishlistItems([gameID])
                self.steam_user.addDesiredGame(gameID)
                self.steam_user.save_user_data_to_cache()

    # Removes a game by ID from the wishlist and the active User
    def removeSelectedFromWishlist(self):
        if self.selectedWishItem >= 0 and len(self.wishListContent) > self.selectedWishItem:
            removeID = self.wishListContent[self.selectedWishItem][2]
            del self.wishListContent[self.selectedWishItem]
            self.steam_user.deleteDesiredGame(removeID)

            self.steam_user.save_user_data_to_cache()

    # Adds a game by ID to the recommend input and to the active User
    def addToReclist(self, gameID):
        if gameID != "999999999":
            found = False
            for item in self.recommendListContent:
                if str(item[0]) == str(gameID):
                    found = True
                    break
            if not found:
                self.loadRecommendItems([gameID])
                self.steam_user.addRecommendGame(gameID)
                self.steam_user.save_user_data_to_cache()

    # Removes a game by ID from the recommend input and the active User
    def removeSelectedFromReclist(self):
        if self.selectedRecItem >= 0 and len(self.recommendListContent) > self.selectedRecItem:
            removeID = self.recommendListContent[self.selectedRecItem][0]
            del self.recommendListContent[self.selectedRecItem]
            self.steam_user.deleteRecommendGame(removeID)

            self.steam_user.save_user_data_to_cache()

    # Change the active user of the GUI. Switch the active dataset in
    # the User object and reload GUI state data.
    def switchToUser(self, userID):
        self.steam_user.loginSteamID(userID)
        self.wishListContent = []
        self.selectedWishItem = 0
        self.recommendListContent = []
        self.selectedRecItem = 0
        self.loadWishlistItems(self.steam_user.getDesiredGames())
        self.loadRecommendItems(self.steam_user.getRecommendGames())



# This class extends the View component of the GUI, encapsulates the Model component,
# and contains the methods that handle events, comprising the controller component.
# After instantiating all the visual objects and calling methods to connect functions to Events,
# the operations include a series of Event handling functions. These functions are connected to signals
# from graphical objects and are called in response to user input such as button presses or text entry. These
# functions manipulate the previously declared graphical objects to change what is displayed, using
# data sent and retrieved through the encapsulated GUI_Content_Model.
class Main_GUI_Controller(QtWidgets.QWidget, Main_GUI_Visuals):

    def __init__(self, ContentModel):
        super().__init__()
        
        self.model = ContentModel
        
        # Create the GUI elements from the view object
        self.setupUi(self)

        self.attachEventHandlers()

        self.Pages.setCurrentIndex(0)
        self.userSelect()
        self.refreshRankings()

        

    # Attach the GUI elements that are subject to user interaction
    # to the appropriate event handling functions
    def attachEventHandlers(self): 
        self.LoginButton.clicked.connect(self.setPageLogin)
        self.SteamRushText.clicked.connect(self.setPageHome)
        self.UserButton.clicked.connect(self.setPageUser)
        self.PriceCheckButton.clicked.connect(self.setPagePrice)
        self.RankingButton.clicked.connect(self.setPageRanked)
        self.GameRecommendationButton.clicked.connect(self.setPageRec)
        self.SearchBar.textEdited.connect(self.searchLoading)
        self.SearchBar.returnPressed.connect(self.processSearchBar)
        self.addToWishlistButton.clicked.connect(self.addWishlistButton)
        self.removeSelectedWishlist.clicked.connect(self.removeFromWishlist)
        self.Wishlist.currentItemChanged.connect(self.onWishlistClick)
        self.GenerateButton.clicked.connect(self.processRecommendRequest)
        self.RecommendationInput.currentItemChanged.connect(self.onReclistClick)
        self.pushButton_2.clicked.connect(self.removeFromReclist)
        self.GameRecommendationEntry.editingFinished.connect(self.addReclistButton)
        self.GetPriceButton.clicked.connect(self.processPriceCheck)
        self.ConfirmButton.clicked.connect(self.newUserLogin)
        self.Entry_2.textEdited.connect(self.userLoading)
        self.Entry_2.editingFinished.connect(self.newUserLogin)

        self.defaultPix = QtGui.QPixmap(":/icon/steam_icon.gif")
        self.activeUserPix = self.defaultPix
        self.activeSearchPix = self.defaultPix


        users = self.model.steam_user.getAllUsers()
        for i in range(len(self.userRadioButtons)):
            self.userRadioButtons[i].toggled.connect(self.userLoading)
            self.userRadioButtons[i].clicked.connect(self.userSelect)
            if i < len(users):
                self.userRadioButtons[i].setText(users[i][1])
                if i == 0:
                    self.userRadioButtons[i].setChecked(True)
  

    # Begin Event Handling Functions
    # Events are generated by interaction with GUI objects
    # Those objects have been attached to these functions,
    # which are called in response to Events.

    # Gets the contents of the model wishlist and updates the display
    def refreshWishlist(self):
        self.Wishlist.clear()
        for g in range(len(self.model.wishListContent)):
            lineString = ""
            lineString += self.model.wishListContent[g][0] + "\n"
            lineString += "Current Steam Price: " +\
            			   str(self.model.wishListContent[g][1][0][1]) + "\n"
            lineString += "Lowest Price: " + str(self.model.wishListContent[g][1][1][1])
            lineString += "\nVendor: " + self.model.wishListContent[g][1][1][0] + "\n"
            self.Wishlist.addItem(lineString)

    # Gets the contents of the model recommend input list and updates the display
    def refreshReclist(self):
        self.RecommendationInput.clear()
        for g in range(len(self.model.recommendListContent)):
            lineString = self.model.recommendListContent[g][1]
            self.RecommendationInput.addItem(lineString)

    # Gets the contents of the model's API's ranked lists and updates the display
    def refreshRankings(self):
        ratings = self.model.steam_api.get_ranked_by_rating(100)
        hours = self.model.steam_api.get_ranked_by_hours(100)

        rateString = ""
        hourString = ""

        self.MostPositiveList.clear()

        for i,game in enumerate(ratings):
            rateString += str(i+1) + ". " + game[1] + "\n   " + "{0:.1f}% Positive, ".format(game[2][0]*100) + str(game[2][1]) + " Total.\n"

        self.MostPositiveList.setText(rateString)

        self.MostPlayedList.clear()
        for i, game in enumerate(hours):
            hourString += str(i+1) + ". " + game[1] + "\n   " + "{0:.2f} Hours, ".\
            			  format(game[2]/float(60)) + "\n"
        self.MostPlayedList.setText(hourString)

        
    # Set Page X functions: Changes the currently visible page.
    # Used for navigation.
    
    def setPageHome(self):
        self.Pages.setCurrentIndex(0)

    def setPageRanked(self):
        self.Pages.setCurrentIndex(1)

    def setPageUser(self):
        self.Pages.setCurrentIndex(2)
        self.refreshWishlist()

    def setPageRec(self):
        self.Pages.setCurrentIndex(3)
        self.refreshReclist()

    def setPagePrice(self):
        self.Pages.setCurrentIndex(4)

    def setPageLogin(self):
        self.Pages.setCurrentIndex(5)
        
    # Updates model for selected wishlist item
    def onWishlistClick(self):
        self.model.selectedWishItem = self.Wishlist.currentRow()

    # Updates model to remove selected wishlist item
    def removeFromWishlist(self):
        self.model.removeSelectedFromWishlist()
        self.refreshWishlist()

    # Updates model to add last game searched to wishlist
    def addWishlistButton(self):
        self.model.addToWishlist(self.model.lastGameSearched)

    # Updates model for selected recommend input list item 
    def onReclistClick(self):
        self.model.selectedRecItem = self.RecommendationInput.currentRow()

    # Updates model to remove selected recommend input list item 
    def removeFromReclist(self):
        self.model.removeSelectedFromReclist()
        self.RecommendationResults.clear()
        self.refreshReclist()

    # Updates model to lookup typed entry in API, adds result to recommend input list
    def addReclistButton(self):
        text = self.GameRecommendationEntry.text()
        if text != "":
            app_parse = self.model.steam_api.get_game_id_from_steam(text)
            app_id = app_parse[0]
            if app_id != "999999999":
                self.model.addToReclist(app_id)
                self.RecommendationResults.clear()
        self.GameRecommendationEntry.clear()
        self.refreshReclist()

    # Invokes the recomendation engine from the model's API handlers, then
    # updates the display with the results.
    def processRecommendRequest(self):
        
        game_ids = []
        for game in self.model.recommendListContent:
            game_ids.append(game[0])


        all_results = self.model.steam_api.recommend_multi_input(gameIDs=game_ids, required_genres=[], banned_genres=[], banned_games=[], showTop=10, cross_thresh=max(2, int(len(game_ids)/5)), matchRate=0.5, cutoff=10, ratePower=1, confPower=3)
        

        resultString = ""
        resultString += "Cross-Recommendation Results:\n"
        for r in all_results[0]:
            resultString += "    " + str(r[1]) + "\n"
        resultString += "\n"
        for results in all_results[1]:
            resultString += "Recommendations from " + results[1] + " (" + results[0] + "):\n"
            for r in results[2]:
                resultString += "    " + str(r[1]) + "\n"
            resultString += "\n"

        self.RecommendationResults.setText(resultString)


    # Invokes the price-check function from the model's API handlers,
    # then updates the display with the results.
    def processPriceCheck(self):
        text = self.PriceCheckEntry.text()
        self.PriceCheckEntry.clear()
        self.PriceCheckResults.clear()
        resultString = "Game not found."
        if text != "":
            app_parse = self.model.steam_api.get_game_id_from_steam(text)
            app_id = app_parse[0]
            if app_id != "999999999":
                prices = self.model.itad_api.get_prices(self.model.itad_api.get_plain(app_id))
                
                if len(prices) == 0:
                    resultString = "Game not found."
                else:            
                    resultString = "Prices for: " + self.model.steam_api.get_name(app_id) + "\n\n"
                    resultString += "Lowest Price in History:\n"
                    resultString += "Vendor: " + str(prices[0][0]) + ", Price: $" + str(prices[0][1]) + "\n\n"
                    resultString += "Current Prices: \n"
                    for p in prices[1:]:
                         resultString += "Vendor: " + str(p[0]) + "\n   Price: $" + str(p[1]) + ",    Sale Running at Vendor: " + str(p[2]) + "% off." + "\n"
        self.PriceCheckResults.setText(resultString)
                     
    # Updates the display with a "Loading..." message while a search is not yet complete.
    def searchLoading(self):
        self.GameTitle.setStyleSheet("color:rgb(254, 215, 102);")
        self.GameTitle.setText("Loading...")
        self.GamePic.setPixmap(QtGui.QPixmap(":/icon/steam_icon.gif"))
        self.AvgHrsInfo.setText("{0:.2f}".format(0))
        self.PositiveReviewsInfo.setText("{0:.2f}%".format(0))
        self.TotalReviewsInfo.setText(str(0))
        self.GenreInfo.setText(str(""))
        self.TopVotedTagsInfo.setText(str(""))
        self.model.lastGameSearched = "999999999"

    # Uses model API handlers to lookup typed game entry, then
    # updates the display with the results.
    def processSearchBar(self):
        text = self.SearchBar.text()
        self.SearchBar.clear()

        app_id = "999999999"
        if text != "":
            app_parse = self.model.steam_api.get_game_id_from_steam(text)
            app_id = app_parse[0]
        name = "Game not found"
        self.activeSearchPix = self.defaultPix
        hours = 0
        reviews = [0,0]
        genres = []
        tags = []

        if app_id != "999999999":
            name = self.model.steam_api.get_name(app_id)
            hours = self.model.steam_api.get_playtime(app_id)[0]
            reviews = self.model.steam_api.get_rating(app_id)
            genres = self.model.steam_api.get_genres(app_id)
            tags = self.model.steam_api.get_tags(app_id)
            if len(tags) > 3:
                tags = tags[0:3]
            try:
                self.activeSearchPix = QtGui.QPixmap.fromImage(ImageQt(Image.open(BytesIO(app_parse[1]))))
            except:
                pass
        self.GameTitle.setStyleSheet("color:rgb(255, 255, 255);")
        self.GameTitle.setText(name)
        self.GamePic.setPixmap(self.activeSearchPix)
        self.AvgHrsInfo.setText("{0:.2f}".format(hours))
        self.PositiveReviewsInfo.setText("{0:.2f}%".format(100*reviews[0]))
        self.TotalReviewsInfo.setText(str(reviews[1]))
        self.GenreInfo.setText(str(genres))
        self.TopVotedTagsInfo.setText(str(tags))
        self.model.lastGameSearched = app_id
        
        
    # Updates the model when a different user profile is selected
    def userSelect(self):
        selectedID = ""
        for i in range(len(self.userRadioButtons)):
            if self.userRadioButtons[i].isChecked():
                users = self.model.steam_user.getAllUsers()
                
                if len(users) > i:
                    selectedID = users[i][0]
                break
        
        if selectedID != "":
            self.model.switchToUser(selectedID)
            self.updateUserInfo()
            
        self.loginLoadingLabel.clear()

    # Uses the model API handlers to lookup a new Steam user ID entry,
    # then updates the model and view to log in the new user
    def newUserLogin(self):
        userID = self.Entry_2.text()
        self.Entry_2.clear()
        if userID.isdigit():
            self.model.switchToUser(userID)
            self.updateUserInfo()
            uName = self.model.steam_user.getName()
            
            for button in self.userRadioButtons:
                if button.text() == "< Unregistered >":
                    button.setText(uName)
                    button.setChecked(True)
                    break
        self.loginLoadingLabel.clear()

    # Updates the display with a "Loading..." message while a user transfer is not yet complete.
    def userLoading(self):
        self.loginLoadingLabel.setText("Loading User Data...\n    Please Wait.")

    # Updates the display to refer to the information of the currently logged in user.
    def updateUserInfo(self):
        name = self.model.steam_user.getName()
        try:
            start = datetime.fromtimestamp(self.model.steam_user.getStartDate())
        except:
            start = datetime.today()
        hours = self.model.steam_user.getTotalHours()
        worth = self.model.steam_user.getSteamWorth()
        played_raw = self.model.steam_user.getPlayedGames()
        played = []
        for game in played_raw:
            played.append([self.model.steam_api.get_name(game[0]), game[1]/float(60)])
        number = len(played)
        played = sorted(played, key=lambda x: x[1], reverse=True)
        imgUrl = self.model.steam_user.getAvatar()
        if imgUrl != "":
            try:
                image_scrape = requests.get(imgUrl)
                content = image_scrape.content
                self.activeUserPix = QtGui.QPixmap.fromImage(ImageQt(Image.open(BytesIO(content))))
            except:
                self.activeUserPix = self.defaultPix
        else:
            self.activeUserPix = self.defaultPix
            
        self.UsernameLabel.setText(name)
        self.AccountCreationInfo.setText(str(start.date()))
        self.GamesOwnedInfo.setText(str(number))
        self.HoursPlayedInfo.setText("{0:.2f}".format(hours))
        self.AccountWorthInfo.setText("{0:.2f}".format(worth))
        self.ProfilePicture.setPixmap(self.activeUserPix)

        self.GameLibraryInfo.clear()
        for g in range(len(played)):
            lineString = played[g][0] + "\n    Hours Played: {0:.2f}\n".format(played[g][1])
            self.GameLibraryInfo.addItem(lineString)


import resources_rc


if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    model = GUI_Content_Model()
    ui = Main_GUI_Controller(model)
    ui.setWindowTitle("SteamRush")
    ui.show()
    sys.exit(app.exec_())
