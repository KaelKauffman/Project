
from PyQt5 import QtCore, QtGui, QtWidgets
from SteamSpy_API_Calls import SteamSpy_API_Caller
from ITAD_API_Calls import ITAD_API_Caller
from User import SteamUser
import requests
from PIL import Image
from io import BytesIO
from PIL.ImageQt import ImageQt
from datetime import datetime


class GUI_Content_Model():
    
    def __init__(self):
        #API Call objects
        self.steam_api = SteamSpy_API_Caller(appFile="SteamSpy_App_Cache.txt", tagFile="SteamSpy_Tags_Cache.txt")
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


    def loadWishlistItems(self, gamesList):
        wishlist = [ self.steam_api.get_name(g_id) for g_id in gamesList ]

        raw_prices = [ self.itad_api.get_prices(self.itad_api.get_plain(g_id)) for g_id in gamesList ]
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
            self.wishListContent.append([wishlist[g], revised_prices[g]])

    def loadRecommendItems(self, gamesList):
        reclist = [ self.steam_api.get_name(g_id) for g_id in gamesList ]

        for g in range(len(reclist)):
            self.recommendListContent.append([gamesList[g], reclist[g]])

    def addToWishlist(self, gameID):
        if gameID != "999999999":
            found = False
            name = self.steam_api.get_name(gameID)
            for item in self.wishListContent:
                print(item[0])
                print(name)
                if item[0] == name:
                    found = True
                    break
            if not found:       
                self.loadWishlistItems([gameID])
                self.steam_user.addDesiredGame(gameID)
            
                self.steam_user.save_user_data_to_cache()

    def removeSelectedFromWishlist(self):
        if self.selectedWishItem >= 0 and len(self.wishListContent) > self.selectedWishItem:
            removeID = self.wishListContent[self.selectedWishItem][0]
            del self.wishListContent[self.selectedWishItem]
            self.steam_user.deleteDesiredGame(removeID)

            self.steam_user.save_user_data_to_cache()

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

    def removeSelectedFromReclist(self):
        if self.selectedRecItem >= 0 and len(self.recommendListContent) > self.selectedRecItem:
            removeID = self.recommendListContent[self.selectedRecItem][0]
            del self.recommendListContent[self.selectedRecItem]
            self.steam_user.deleteRecommendGame(removeID)

            self.steam_user.save_user_data_to_cache()

    def switchToUser(self, userID):
        self.steam_user.loginSteamID(userID)
        self.wishListContent = []
        self.selectedWishItem = 0
        self.recommendListContent = []
        self.selectedRecItem = 0
        self.loadWishlistItems(self.steam_user.getDesiredGames())
        self.loadRecommendItems(self.steam_user.getRecommendGames())



class Main_GUI_Visuals(object):

    def __init__(self):
        
        self.model = GUI_Content_Model()
    
    def setupUi(self, Widget):

        # Start of Graphics Objects for Main Program Window
        Widget.setObjectName("Widget")
        Widget.resize(1200, 900)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Widget.sizePolicy().hasHeightForWidth())
        Widget.setSizePolicy(sizePolicy)
        Widget.setMinimumSize(QtCore.QSize(1200, 900))
        Widget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.gridLayout = QtWidgets.QGridLayout(Widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        
        self.BottomBar = QtWidgets.QWidget(Widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BottomBar.sizePolicy().hasHeightForWidth())
        self.BottomBar.setSizePolicy(sizePolicy)
        self.BottomBar.setMinimumSize(QtCore.QSize(800, 25))
        self.BottomBar.setMaximumSize(QtCore.QSize(16777215, 50))
        self.BottomBar.setStyleSheet("background-color: rgb(55, 55, 55);")
        self.BottomBar.setObjectName("BottomBar")
        self.gridLayout.addWidget(self.BottomBar, 2, 0, 1, 1)
        
        self.MenuBar = QtWidgets.QWidget(Widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MenuBar.sizePolicy().hasHeightForWidth())
        self.MenuBar.setSizePolicy(sizePolicy)
        self.MenuBar.setMinimumSize(QtCore.QSize(800, 0))
        self.MenuBar.setMaximumSize(QtCore.QSize(16777215, 100))
        self.MenuBar.setBaseSize(QtCore.QSize(0, 0))
        self.MenuBar.setStyleSheet("background-color: rgb(55, 55, 55);")
        self.MenuBar.setObjectName("MenuBar")
        self.MenuBarLayout = QtWidgets.QGridLayout(self.MenuBar)
        self.MenuBarLayout.setContentsMargins(20, 11, 11, 11)
        self.MenuBarLayout.setSpacing(6)
        self.MenuBarLayout.setObjectName("MenuBarLayout")
        
        spacerItem = QtWidgets.QSpacerItem(300, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.MenuBarLayout.addItem(spacerItem, 0, 3, 1, 1)
        
        self.LoginButton = QtWidgets.QPushButton(self.MenuBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LoginButton.sizePolicy().hasHeightForWidth())
        self.LoginButton.setSizePolicy(sizePolicy)
        self.LoginButton.setMinimumSize(QtCore.QSize(0, 30))
        self.LoginButton.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.LoginButton.setFont(font)
        self.LoginButton.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(30, 180, 175);")
        self.LoginButton.setObjectName("LoginButton")
        self.LoginButton.clicked.connect(self.setPageLogin)
        self.MenuBarLayout.addWidget(self.LoginButton, 0, 4, 1, 1)
        
        self.SteamRushIcon = QtWidgets.QLabel(self.MenuBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SteamRushIcon.sizePolicy().hasHeightForWidth())
        self.SteamRushIcon.setSizePolicy(sizePolicy)
        self.SteamRushIcon.setMinimumSize(QtCore.QSize(70, 40))
        self.SteamRushIcon.setMaximumSize(QtCore.QSize(70, 40))
        self.SteamRushIcon.setBaseSize(QtCore.QSize(70, 40))
        self.SteamRushIcon.setText("")
        self.SteamRushIcon.setPixmap(QtGui.QPixmap(":/icon/steam_icon.gif"))
        self.SteamRushIcon.setScaledContents(True)
        self.SteamRushIcon.setObjectName("SteamRushIcon")
        self.MenuBarLayout.addWidget(self.SteamRushIcon, 0, 0, 1, 1)
        
        self.SteamRushText = QtWidgets.QPushButton(self.MenuBar)
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(26)
        self.SteamRushText.setFont(font)
        self.SteamRushText.setStyleSheet("color: rgb(255, 255, 255);")
        self.SteamRushText.setFlat(True)
        self.SteamRushText.setObjectName("SteamRushText")
        self.SteamRushText.clicked.connect(self.setPageHome)
        self.MenuBarLayout.addWidget(self.SteamRushText, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.MenuBar, 0, 0, 1, 1)

        # Start of Graphics Objects for GUI Page Stack
        self.Pages = QtWidgets.QStackedWidget(Widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Pages.sizePolicy().hasHeightForWidth())
        self.Pages.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        self.Pages.setFont(font)
        self.Pages.setStyleSheet("background-color: rgb(83, 83, 83);")
        self.Pages.setObjectName("Pages")

        # Start of Graphics Objects for Home Page
        self.HomePage = QtWidgets.QWidget()
        self.HomePage.setStyleSheet("background-color: rgb(83, 83, 83);")
        self.HomePage.setObjectName("HomePage")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.HomePage)
        self.gridLayout_2.setContentsMargins(75, 75, 75, 75)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.HomePageLayout = QtWidgets.QGridLayout()
        self.HomePageLayout.setContentsMargins(0, -1, -1, -1)
        self.HomePageLayout.setSpacing(20)
        self.HomePageLayout.setObjectName("HomePageLayout")

        self.UserButton = QtWidgets.QPushButton(self.HomePage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.UserButton.sizePolicy().hasHeightForWidth())
        self.UserButton.setSizePolicy(sizePolicy)
        self.UserButton.setMinimumSize(QtCore.QSize(150, 0))
        self.UserButton.setMaximumSize(QtCore.QSize(800, 800))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(15)
        self.UserButton.setFont(font)
        self.UserButton.setStyleSheet("color: rgb(255, 255, 255);")
        self.UserButton.setAutoDefault(False)
        self.UserButton.setDefault(False)
        self.UserButton.setFlat(False)
        self.UserButton.setObjectName("UserButton")
        self.UserButton.clicked.connect(self.setPageUser)
        self.HomePageLayout.addWidget(self.UserButton, 0, 1, 1, 1)

        self.PriceCheckButton = QtWidgets.QPushButton(self.HomePage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PriceCheckButton.sizePolicy().hasHeightForWidth())
        self.PriceCheckButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(15)
        self.PriceCheckButton.setFont(font)
        self.PriceCheckButton.setStyleSheet("color: rgb(255, 255, 255);")
        self.PriceCheckButton.setObjectName("PriceCheckButton")
        self.PriceCheckButton.clicked.connect(self.setPagePrice)
        self.HomePageLayout.addWidget(self.PriceCheckButton, 2, 1, 1, 2)
 
        self.RankingButton = QtWidgets.QPushButton(self.HomePage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RankingButton.sizePolicy().hasHeightForWidth())
        self.RankingButton.setSizePolicy(sizePolicy)
        self.RankingButton.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(15)
        self.RankingButton.setFont(font)
        self.RankingButton.setStyleSheet("color: rgb(255, 255, 255);")
        self.RankingButton.setObjectName("RankingButton")
        self.RankingButton.clicked.connect(self.setPageRanked)
        self.HomePageLayout.addWidget(self.RankingButton, 1, 1, 1, 1)
 
        self.GameRecommendationButton = QtWidgets.QPushButton(self.HomePage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GameRecommendationButton.sizePolicy().hasHeightForWidth())
        self.GameRecommendationButton.setSizePolicy(sizePolicy)
        self.GameRecommendationButton.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(15)
        self.GameRecommendationButton.setFont(font)
        self.GameRecommendationButton.setStyleSheet("color: rgb(255, 255, 255);")
        self.GameRecommendationButton.setIconSize(QtCore.QSize(14, 14))
        self.GameRecommendationButton.setObjectName("GameRecommendationButton")
        self.GameRecommendationButton.clicked.connect(self.setPageRec)
        self.HomePageLayout.addWidget(self.GameRecommendationButton, 0, 2, 2, 1)
        
        # Start of Graphics Objects for Search Panel in Home Page
        self.SearchPanel = QtWidgets.QWidget(self.HomePage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearchPanel.sizePolicy().hasHeightForWidth())
        self.SearchPanel.setSizePolicy(sizePolicy)
        self.SearchPanel.setMinimumSize(QtCore.QSize(400, 0))
        self.SearchPanel.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.SearchPanel.setStyleSheet("background-color: rgb(68, 68, 68);")
        self.SearchPanel.setObjectName("SearchPanel")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.SearchPanel)
        self.gridLayout_4.setContentsMargins(15, 20, 15, 20)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.SearchLayout = QtWidgets.QGridLayout()
        self.SearchLayout.setHorizontalSpacing(6)
        self.SearchLayout.setVerticalSpacing(15)
        self.SearchLayout.setObjectName("SearchLayout")
        
        self.SearchBar = QtWidgets.QLineEdit(self.SearchPanel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearchBar.sizePolicy().hasHeightForWidth())
        self.SearchBar.setSizePolicy(sizePolicy)
        self.SearchBar.setMinimumSize(QtCore.QSize(400, 20))
        self.SearchBar.setMaximumSize(QtCore.QSize(450, 30))
        self.SearchBar.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.SearchBar.setInputMethodHints(QtCore.Qt.ImhNoAutoUppercase)
        self.SearchBar.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.SearchBar.setObjectName("SearchBar")
        self.SearchBar.returnPressed.connect(self.processSearchBar)
        self.SearchLayout.addWidget(self.SearchBar, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        
        self.SearchInnerLayout = QtWidgets.QGridLayout()
        self.SearchInnerLayout.setContentsMargins(-1, 0, -1, 0)
        self.SearchInnerLayout.setHorizontalSpacing(7)
        self.SearchInnerLayout.setVerticalSpacing(6)
        self.SearchInnerLayout.setObjectName("SearchInnerLayout")
        self.SearchDisplayLayout = QtWidgets.QGridLayout()
        self.SearchDisplayLayout.setSpacing(6)
        self.SearchDisplayLayout.setObjectName("SearchDisplayLayout")
        
        self.GenreInfo = QtWidgets.QLabel(self.SearchPanel)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.GenreInfo.setFont(font)
        self.GenreInfo.setStyleSheet("color:rgb(255, 255, 255); background-color: rgb(81, 81, 81);")
        self.GenreInfo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.GenreInfo.setIndent(10)
        self.GenreInfo.setObjectName("GenreInfo")
        self.SearchDisplayLayout.addWidget(self.GenreInfo, 4, 1, 1, 2)
        
        self.GenreLabel = QtWidgets.QLabel(self.SearchPanel)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.GenreLabel.setFont(font)
        self.GenreLabel.setStyleSheet("color:rgb(30, 180, 175); background-color: rgb(81, 81, 81);")
        self.GenreLabel.setIndent(8)
        self.GenreLabel.setObjectName("GenreLabel")
        self.SearchDisplayLayout.addWidget(self.GenreLabel, 4, 0, 1, 1)

        self.TopVotedTagsInfo = QtWidgets.QLabel(self.SearchPanel)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.TopVotedTagsInfo.setFont(font)
        self.TopVotedTagsInfo.setStyleSheet("color:rgb(255, 255, 255); background-color: rgb(81, 81, 81);")
        self.TopVotedTagsInfo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.TopVotedTagsInfo.setIndent(10)
        self.TopVotedTagsInfo.setObjectName("TopVotedTagsInfo")
        self.SearchDisplayLayout.addWidget(self.TopVotedTagsInfo, 5, 1, 1, 2)

        self.AvgHrsInfo = QtWidgets.QLabel(self.SearchPanel)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.AvgHrsInfo.setFont(font)
        self.AvgHrsInfo.setStyleSheet("color:rgb(255, 255, 255); background-color: rgb(81, 81, 81);")
        self.AvgHrsInfo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.AvgHrsInfo.setIndent(10)
        self.AvgHrsInfo.setObjectName("AvgHrsInfo")
        self.SearchDisplayLayout.addWidget(self.AvgHrsInfo, 1, 1, 1, 2)

        self.AvgHrsLabel = QtWidgets.QLabel(self.SearchPanel)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.AvgHrsLabel.setFont(font)
        self.AvgHrsLabel.setStyleSheet("color:rgb(30, 180, 175); background-color: rgb(81, 81, 81);")
        self.AvgHrsLabel.setIndent(8)
        self.AvgHrsLabel.setObjectName("AvgHrsLabel")
        self.SearchDisplayLayout.addWidget(self.AvgHrsLabel, 1, 0, 1, 1)
        
        self.TopVotedTagsLabel = QtWidgets.QLabel(self.SearchPanel)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.TopVotedTagsLabel.setFont(font)
        self.TopVotedTagsLabel.setStyleSheet("color:rgb(30, 180, 175); background-color: rgb(81, 81, 81);")
        self.TopVotedTagsLabel.setIndent(8)
        self.TopVotedTagsLabel.setObjectName("TopVotedTagsLabel")
        self.SearchDisplayLayout.addWidget(self.TopVotedTagsLabel, 5, 0, 1, 1)
        
        self.TotalReviewsLabel = QtWidgets.QLabel(self.SearchPanel)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.TotalReviewsLabel.setFont(font)
        self.TotalReviewsLabel.setStyleSheet("color:rgb(30, 180, 175); background-color: rgb(81, 81, 81);")
        self.TotalReviewsLabel.setIndent(8)
        self.TotalReviewsLabel.setObjectName("TotalReviewsLabel")
        self.SearchDisplayLayout.addWidget(self.TotalReviewsLabel, 3, 0, 1, 1)
        
        self.PositiveReviewsInfo_2 = QtWidgets.QLabel(self.SearchPanel)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.PositiveReviewsInfo_2.setFont(font)
        self.PositiveReviewsInfo_2.setStyleSheet("color:rgb(255, 255, 255); background-color: rgb(81, 81, 81);")
        self.PositiveReviewsInfo_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.PositiveReviewsInfo_2.setIndent(10)
        self.PositiveReviewsInfo_2.setObjectName("PositiveReviewsInfo_2")
        self.SearchDisplayLayout.addWidget(self.PositiveReviewsInfo_2, 2, 1, 1, 2)
        
        self.TotalReviewsInfo = QtWidgets.QLabel(self.SearchPanel)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.TotalReviewsInfo.setFont(font)
        self.TotalReviewsInfo.setStyleSheet("color:rgb(255, 255, 255); background-color: rgb(81, 81, 81);")
        self.TotalReviewsInfo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.TotalReviewsInfo.setIndent(10)
        self.TotalReviewsInfo.setObjectName("TotalReviewsInfo")
        self.SearchDisplayLayout.addWidget(self.TotalReviewsInfo, 3, 1, 1, 2)
        
        self.PositiveReviewsInfo = QtWidgets.QLabel(self.SearchPanel)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PositiveReviewsInfo.setFont(font)
        self.PositiveReviewsInfo.setStyleSheet("color:rgb(30, 180, 175); background-color: rgb(81, 81, 81);")
        self.PositiveReviewsInfo.setIndent(8)
        self.PositiveReviewsInfo.setObjectName("PositiveReviewsInfo")
        self.SearchDisplayLayout.addWidget(self.PositiveReviewsInfo, 2, 0, 1, 1)
        self.SearchInnerLayout.addLayout(self.SearchDisplayLayout, 3, 0, 1, 2)
        
        self.GamePic = QtWidgets.QLabel(self.SearchPanel)
        self.GamePic.setMinimumSize(QtCore.QSize(192, 72))
        self.GamePic.setMaximumSize(QtCore.QSize(192, 72))
        self.GamePic.setText("")
        self.GamePic.setPixmap(QtGui.QPixmap(":/icon/steam_icon.gif"))
        self.GamePic.setScaledContents(True)
        self.GamePic.setObjectName("GamePic")
        self.SearchInnerLayout.addWidget(self.GamePic, 1, 1, 1, 1)
        
        self.GameTitle = QtWidgets.QLabel(self.SearchPanel)
        self.GameTitle.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.GameTitle.setFont(font)
        self.GameTitle.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.GameTitle.setStyleSheet("color:rgb(255, 255, 255)")
        self.GameTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.GameTitle.setObjectName("GameTitle")
        self.SearchInnerLayout.addWidget(self.GameTitle, 1, 0, 1, 1)
        
        self.pushButton = QtWidgets.QPushButton(self.SearchPanel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(100, 10))
        self.pushButton.setMaximumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(101, 203, 150); color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.addWishlistButton)
        self.SearchInnerLayout.addWidget(self.pushButton, 2, 0, 1, 1)

        self.SearchLayout.addLayout(self.SearchInnerLayout, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.SearchLayout, 0, 0, 1, 1)
        self.HomePageLayout.addWidget(self.SearchPanel, 0, 3, 3, 1)
        # End of Graphics Objects for Search Panel

        self.gridLayout_2.addLayout(self.HomePageLayout, 1, 0, 1, 2)
        self.Pages.addWidget(self.HomePage)
        # End of Graphics Objects for Home Page
        

        # Start of Graphics Objects for Rankings Page
        self.RankingPage = QtWidgets.QWidget()
        self.RankingPage.setStyleSheet("background-color: rgb(83, 83, 83);")
        self.RankingPage.setObjectName("RankingPage")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.RankingPage)
        self.gridLayout_7.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_7.setSpacing(6)
        self.gridLayout_7.setObjectName("gridLayout_7")
        
        self.RankingPageLayout = QtWidgets.QGridLayout()
        self.RankingPageLayout.setSpacing(6)
        self.RankingPageLayout.setObjectName("RankingPageLayout")
        
        self.GameRecommendationLayout_3 = QtWidgets.QGridLayout()
        self.GameRecommendationLayout_3.setContentsMargins(5, -1, -1, 1)
        self.GameRecommendationLayout_3.setSpacing(6)
        self.GameRecommendationLayout_3.setObjectName("GameRecommendationLayout_3")
        
        self.Title_3 = QtWidgets.QLabel(self.RankingPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Title_3.sizePolicy().hasHeightForWidth())
        self.Title_3.setSizePolicy(sizePolicy)
        self.Title_3.setMaximumSize(QtCore.QSize(16777215, 300))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.Title_3.setFont(font)
        self.Title_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.Title_3.setObjectName("Title_3")
        self.GameRecommendationLayout_3.addWidget(self.Title_3, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.RankingPageLayout.addLayout(self.GameRecommendationLayout_3, 0, 0, 1, 2)
        self.RankingLayout = QtWidgets.QGridLayout()
        self.RankingLayout.setContentsMargins(20, -1, 10, -1)
        self.RankingLayout.setHorizontalSpacing(30)
        self.RankingLayout.setVerticalSpacing(20)
        self.RankingLayout.setObjectName("RankingLayout")
        
        self.MostPlayedList = QtWidgets.QTextBrowser(self.RankingPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MostPlayedList.sizePolicy().hasHeightForWidth())
        self.MostPlayedList.setSizePolicy(sizePolicy)
        self.MostPlayedList.setMinimumSize(QtCore.QSize(500, 0))
        self.MostPlayedList.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.MostPlayedList.setFont(font)
        self.MostPlayedList.setStyleSheet("color:rgb(255, 255, 255); background-color: rgb(140, 140, 140);")
        self.MostPlayedList.setObjectName("MostPlayedList")
        self.RankingLayout.addWidget(self.MostPlayedList, 1, 1, 1, 1)
        
        self.MostPositiveList = QtWidgets.QTextBrowser(self.RankingPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MostPositiveList.sizePolicy().hasHeightForWidth())
        self.MostPositiveList.setSizePolicy(sizePolicy)
        self.MostPositiveList.setMinimumSize(QtCore.QSize(500, 0))
        self.MostPositiveList.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.MostPositiveList.setFont(font)
        self.MostPositiveList.setStyleSheet("color:rgb(255, 255, 255); background-color: rgb(140, 140, 140);")
        self.MostPositiveList.setObjectName("MostPositiveList")
        self.RankingLayout.addWidget(self.MostPositiveList, 1, 0, 1, 1)
        
        self.MostPlayedLabel = QtWidgets.QLabel(self.RankingPage)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.MostPlayedLabel.setFont(font)
        self.MostPlayedLabel.setStyleSheet("color: rgb(101, 203, 150);")
        self.MostPlayedLabel.setObjectName("MostPlayedLabel")
        self.RankingLayout.addWidget(self.MostPlayedLabel, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)
        
        self.MostPositiveLabel = QtWidgets.QLabel(self.RankingPage)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.MostPositiveLabel.setFont(font)
        self.MostPositiveLabel.setStyleSheet("color: rgb(30, 180, 175);")
        self.MostPositiveLabel.setObjectName("MostPositiveLabel")
        self.RankingLayout.addWidget(self.MostPositiveLabel, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        
        self.RankingPageLayout.addLayout(self.RankingLayout, 4, 0, 1, 1)
        self.gridLayout_7.addLayout(self.RankingPageLayout, 0, 0, 1, 1)
        self.Pages.addWidget(self.RankingPage)
        # End of Graphics Objects for Rankings Page


        # Start of Graphics Objects for User Page
        self.UserPage = QtWidgets.QWidget()
        self.UserPage.setStyleSheet("background-color: rgb(83, 83, 83);")
        self.UserPage.setObjectName("UserPage")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.UserPage)
        self.gridLayout_6.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.UserLayout = QtWidgets.QGridLayout()
        self.UserLayout.setContentsMargins(15, -1, 15, 15)
        self.UserLayout.setHorizontalSpacing(25)
        self.UserLayout.setVerticalSpacing(15)
        self.UserLayout.setObjectName("UserLayout")
        
        self.HoursPlayedLabel = QtWidgets.QLabel(self.UserPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HoursPlayedLabel.sizePolicy().hasHeightForWidth())
        self.HoursPlayedLabel.setSizePolicy(sizePolicy)
        self.HoursPlayedLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.HoursPlayedLabel.setFont(font)
        self.HoursPlayedLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.HoursPlayedLabel.setObjectName("HoursPlayedLabel")
        self.UserLayout.addWidget(self.HoursPlayedLabel, 2, 2, 1, 1, QtCore.Qt.AlignRight)

        self.AccountCreationLabel = QtWidgets.QLabel(self.UserPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AccountCreationLabel.sizePolicy().hasHeightForWidth())
        self.AccountCreationLabel.setSizePolicy(sizePolicy)
        self.AccountCreationLabel.setMinimumSize(QtCore.QSize(0, 30))
        self.AccountCreationLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.AccountCreationLabel.setFont(font)
        self.AccountCreationLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.AccountCreationLabel.setObjectName("AccountCreationLabel")
        self.UserLayout.addWidget(self.AccountCreationLabel, 2, 0, 1, 1, QtCore.Qt.AlignRight)
        
        self.GamesOwnedLabel = QtWidgets.QLabel(self.UserPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GamesOwnedLabel.sizePolicy().hasHeightForWidth())
        self.GamesOwnedLabel.setSizePolicy(sizePolicy)
        self.GamesOwnedLabel.setMinimumSize(QtCore.QSize(0, 30))
        self.GamesOwnedLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.GamesOwnedLabel.setFont(font)
        self.GamesOwnedLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.GamesOwnedLabel.setObjectName("GamesOwnedLabel")
        self.UserLayout.addWidget(self.GamesOwnedLabel, 3, 0, 1, 1, QtCore.Qt.AlignRight)
        
        self.GameLibraryLabel = QtWidgets.QLabel(self.UserPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GameLibraryLabel.sizePolicy().hasHeightForWidth())
        self.GameLibraryLabel.setSizePolicy(sizePolicy)
        self.GameLibraryLabel.setMinimumSize(QtCore.QSize(0, 30))
        self.GameLibraryLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.GameLibraryLabel.setFont(font)
        self.GameLibraryLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.GameLibraryLabel.setObjectName("GameLibraryLabel")
        self.UserLayout.addWidget(self.GameLibraryLabel, 4, 0, 1, 4)
        
        self.AccountCreationInfo = QtWidgets.QLabel(self.UserPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AccountCreationInfo.sizePolicy().hasHeightForWidth())
        self.AccountCreationInfo.setSizePolicy(sizePolicy)
        self.AccountCreationInfo.setMinimumSize(QtCore.QSize(0, 30))
        self.AccountCreationInfo.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.AccountCreationInfo.setFont(font)
        self.AccountCreationInfo.setStyleSheet("color: rgb(255, 255, 255);")
        self.AccountCreationInfo.setObjectName("AccountCreationInfo")
        self.UserLayout.addWidget(self.AccountCreationInfo, 2, 1, 1, 1, QtCore.Qt.AlignHCenter)
        
        self.GamesOwnedInfo = QtWidgets.QLabel(self.UserPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GamesOwnedInfo.sizePolicy().hasHeightForWidth())
        self.GamesOwnedInfo.setSizePolicy(sizePolicy)
        self.GamesOwnedInfo.setMinimumSize(QtCore.QSize(0, 30))
        self.GamesOwnedInfo.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.GamesOwnedInfo.setFont(font)
        self.GamesOwnedInfo.setStyleSheet("color: rgb(255, 255, 255);")
        self.GamesOwnedInfo.setObjectName("GamesOwnedInfo")
        self.UserLayout.addWidget(self.GamesOwnedInfo, 3, 1, 1, 1, QtCore.Qt.AlignHCenter)
        
        self.HoursPlayedInfo = QtWidgets.QLabel(self.UserPage)
        self.HoursPlayedInfo.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.HoursPlayedInfo.setFont(font)
        self.HoursPlayedInfo.setStyleSheet("color: rgb(255, 255, 255);")
        self.HoursPlayedInfo.setObjectName("HoursPlayedInfo")
        self.UserLayout.addWidget(self.HoursPlayedInfo, 2, 3, 1, 1, QtCore.Qt.AlignHCenter)
        
        self.AccountWorthInfo = QtWidgets.QLabel(self.UserPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AccountWorthInfo.sizePolicy().hasHeightForWidth())
        self.AccountWorthInfo.setSizePolicy(sizePolicy)
        self.AccountWorthInfo.setMinimumSize(QtCore.QSize(0, 30))
        self.AccountWorthInfo.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.AccountWorthInfo.setFont(font)
        self.AccountWorthInfo.setStyleSheet("color: rgb(255, 255, 255);")
        self.AccountWorthInfo.setObjectName("AccountWorthInfo")
        self.UserLayout.addWidget(self.AccountWorthInfo, 3, 3, 1, 1, QtCore.Qt.AlignHCenter)
        
        self.AccountWorthLabel = QtWidgets.QLabel(self.UserPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AccountWorthLabel.sizePolicy().hasHeightForWidth())
        self.AccountWorthLabel.setSizePolicy(sizePolicy)
        self.AccountWorthLabel.setMinimumSize(QtCore.QSize(0, 30))
        self.AccountWorthLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.AccountWorthLabel.setFont(font)
        self.AccountWorthLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.AccountWorthLabel.setObjectName("AccountWorthLabel")
        self.UserLayout.addWidget(self.AccountWorthLabel, 3, 2, 1, 1, QtCore.Qt.AlignRight)
        
        self.removeSelectedWishlist = QtWidgets.QPushButton(self.UserPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removeSelectedWishlist.sizePolicy().hasHeightForWidth())
        self.removeSelectedWishlist.setSizePolicy(sizePolicy)
        self.removeSelectedWishlist.setMinimumSize(QtCore.QSize(175, 40))
        self.removeSelectedWishlist.setMaximumSize(QtCore.QSize(250, 16777215))
        self.removeSelectedWishlist.setStyleSheet("background-color: rgb(244, 140, 164); color: rgb(255, 255, 255);")
        self.removeSelectedWishlist.setObjectName("removeSelectedWishlist")
        self.removeSelectedWishlist.clicked.connect(self.removeFromWishlist)
        self.UserLayout.addWidget(self.removeSelectedWishlist, 7, 5, 1, 1, QtCore.Qt.AlignHCenter)
        
        self.Wishlist = QtWidgets.QListWidget(self.UserPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Wishlist.sizePolicy().hasHeightForWidth())
        self.Wishlist.setSizePolicy(sizePolicy)
        self.Wishlist.setMinimumSize(QtCore.QSize(500, 0))
        self.Wishlist.setMaximumSize(QtCore.QSize(600, 600))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(16)
        self.Wishlist.setFont(font)
        self.Wishlist.setStyleSheet("color: rgb(255, 255, 255);")
        self.Wishlist.setObjectName("Wishlist")
        self.Wishlist.currentItemChanged.connect(self.onWishlistClick)
        self.UserLayout.addWidget(self.Wishlist, 2, 5, 5, 1)
        
        self.WishlistLabel = QtWidgets.QLabel(self.UserPage)
        self.WishlistLabel.setMaximumSize(QtCore.QSize(16777215, 36))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.WishlistLabel.setFont(font)
        self.WishlistLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.WishlistLabel.setObjectName("WishlistLabel")
        self.UserLayout.addWidget(self.WishlistLabel, 1, 5, 1, 1, QtCore.Qt.AlignHCenter)
        
        self.UsernameLabel = QtWidgets.QLabel(self.UserPage)
        self.UsernameLabel.setMaximumSize(QtCore.QSize(16777215, 180))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        self.UsernameLabel.setFont(font)
        self.UsernameLabel.setStyleSheet("color: rgb(30, 180, 175);")
        self.UsernameLabel.setWordWrap(False)
        self.UsernameLabel.setObjectName("UsernameLabel")
        self.UserLayout.addWidget(self.UsernameLabel, 0, 1, 2, 3)

        self.ProfilePicture = QtWidgets.QLabel(self.UserPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ProfilePicture.sizePolicy().hasHeightForWidth())
        self.ProfilePicture.setSizePolicy(sizePolicy)
        self.ProfilePicture.setMinimumSize(QtCore.QSize(150, 150))
        self.ProfilePicture.setMaximumSize(QtCore.QSize(150, 150))
        self.ProfilePicture.setText("")
        self.ProfilePicture.setPixmap(QtGui.QPixmap(":/icon/steam_icon.gif"))
        self.ProfilePicture.setScaledContents(True)
        self.ProfilePicture.setObjectName("ProfilePicture")
        self.UserLayout.addWidget(self.ProfilePicture, 0, 0, 2, 1)
        
        self.GameLibraryInfo = QtWidgets.QListWidget(self.UserPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GameLibraryInfo.sizePolicy().hasHeightForWidth())
        self.GameLibraryInfo.setSizePolicy(sizePolicy)
        self.GameLibraryInfo.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.GameLibraryInfo.setFont(font)
        self.GameLibraryInfo.setStyleSheet("color: rgb(255, 255, 255);")
        self.GameLibraryInfo.setObjectName("GameLibraryInfo")
        self.UserLayout.addWidget(self.GameLibraryInfo, 5, 0, 2, 4)

        self.gridLayout_6.addLayout(self.UserLayout, 0, 0, 1, 1)
        self.Pages.addWidget(self.UserPage)
        # End of Graphics Objects for User Page


        # Start of Graphics Objects for Recommend Page
        self.GameRecommendationPage = QtWidgets.QWidget()
        self.GameRecommendationPage.setStyleSheet("background-color: rgb(83, 83, 83);")
        self.GameRecommendationPage.setObjectName("GameRecommendationPage")
        self.GameRecommendationLayout_2 = QtWidgets.QGridLayout(self.GameRecommendationPage)
        self.GameRecommendationLayout_2.setContentsMargins(11, 11, 11, 11)
        self.GameRecommendationLayout_2.setHorizontalSpacing(0)
        self.GameRecommendationLayout_2.setVerticalSpacing(15)
        self.GameRecommendationLayout_2.setObjectName("GameRecommendationLayout_2")
        self.TextViewLayout = QtWidgets.QGridLayout()
        self.TextViewLayout.setContentsMargins(20, -1, 10, -1)
        self.TextViewLayout.setHorizontalSpacing(30)
        self.TextViewLayout.setVerticalSpacing(20)
        self.TextViewLayout.setObjectName("TextViewLayout")
        
        self.GenerateButton = QtWidgets.QPushButton(self.GameRecommendationPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GenerateButton.sizePolicy().hasHeightForWidth())
        self.GenerateButton.setSizePolicy(sizePolicy)
        self.GenerateButton.setMinimumSize(QtCore.QSize(200, 40))
        self.GenerateButton.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.GenerateButton.setFont(font)
        self.GenerateButton.setStyleSheet("background-color: rgb(101, 203, 150); color: rgb(255, 255, 255);")
        self.GenerateButton.setObjectName("GenerateButton")
        self.GenerateButton.clicked.connect(self.processRecommendRequest)
        self.TextViewLayout.addWidget(self.GenerateButton, 1, 1, 1, 1)
        
        self.RecommendationInput = QtWidgets.QListWidget(self.GameRecommendationPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RecommendationInput.sizePolicy().hasHeightForWidth())
        self.RecommendationInput.setSizePolicy(sizePolicy)
        self.RecommendationInput.setMinimumSize(QtCore.QSize(500, 0))
        self.RecommendationInput.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(24)
        self.RecommendationInput.setFont(font)
        self.RecommendationInput.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(140, 140, 140);")
        self.RecommendationInput.setObjectName("RecommendationInput")
        self.RecommendationInput.currentItemChanged.connect(self.onReclistClick)
        self.TextViewLayout.addWidget(self.RecommendationInput, 0, 0, 1, 1)
        
        self.pushButton_2 = QtWidgets.QPushButton(self.GameRecommendationPage)
        self.pushButton_2.setMaximumSize(QtCore.QSize(300, 40))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: rgb(244, 140, 164); color: rgb(255, 255, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.removeFromReclist)
        self.TextViewLayout.addWidget(self.pushButton_2, 1, 0, 1, 1)
        
        self.RecommendationResults = QtWidgets.QTextBrowser(self.GameRecommendationPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RecommendationResults.sizePolicy().hasHeightForWidth())
        self.RecommendationResults.setSizePolicy(sizePolicy)
        self.RecommendationResults.setMinimumSize(QtCore.QSize(500, 0))
        self.RecommendationResults.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(16)
        self.RecommendationResults.setFont(font)
        self.RecommendationResults.setStyleSheet("color: rgb(0, 0, 0); background-color: rgb(193, 193, 193);")
        self.RecommendationResults.setObjectName("RecommendationResults")
        self.TextViewLayout.addWidget(self.RecommendationResults, 0, 1, 1, 1)
        self.GameRecommendationLayout_2.addLayout(self.TextViewLayout, 2, 0, 1, 1)
        
        self.GameRecommendationLayout = QtWidgets.QGridLayout()
        self.GameRecommendationLayout.setContentsMargins(5, -1, -1, 1)
        self.GameRecommendationLayout.setSpacing(6)
        self.GameRecommendationLayout.setObjectName("GameRecommendationLayout")
        
        self.Title = QtWidgets.QLabel(self.GameRecommendationPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Title.sizePolicy().hasHeightForWidth())
        self.Title.setSizePolicy(sizePolicy)
        self.Title.setMaximumSize(QtCore.QSize(16777215, 300))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.Title.setFont(font)
        self.Title.setStyleSheet("color: rgb(255, 255, 255);")
        self.Title.setObjectName("Title")
        self.GameRecommendationLayout.addWidget(self.Title, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        
        self.Instructions = QtWidgets.QLabel(self.GameRecommendationPage)
        self.Instructions.setMinimumSize(QtCore.QSize(1050, 30))
        self.Instructions.setMaximumSize(QtCore.QSize(800, 30))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Instructions.setFont(font)
        self.Instructions.setStyleSheet("color: rgb(255, 255, 255);")
        self.Instructions.setWordWrap(True)
        self.Instructions.setObjectName("Instructions")
        self.GameRecommendationLayout.addWidget(self.Instructions, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.GameRecommendationLayout_2.addLayout(self.GameRecommendationLayout, 0, 0, 1, 1)
        
        self.AddGameLayout = QtWidgets.QGridLayout()
        self.AddGameLayout.setContentsMargins(20, -1, 10, -1)
        self.AddGameLayout.setSpacing(6)
        self.AddGameLayout.setObjectName("AddGameLayout")
        
        self.GameRecommendationEntry = QtWidgets.QLineEdit(self.GameRecommendationPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GameRecommendationEntry.sizePolicy().hasHeightForWidth())
        self.GameRecommendationEntry.setSizePolicy(sizePolicy)
        self.GameRecommendationEntry.setMinimumSize(QtCore.QSize(400, 40))
        self.GameRecommendationEntry.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.GameRecommendationEntry.setObjectName("GameRecommendationEntry")
        self.GameRecommendationEntry.editingFinished.connect(self.addReclistButton)
        self.AddGameLayout.addWidget(self.GameRecommendationEntry, 0, 0, 1, 1)
        
        self.AddGame = QtWidgets.QPushButton(self.GameRecommendationPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddGame.sizePolicy().hasHeightForWidth())
        self.AddGame.setSizePolicy(sizePolicy)
        self.AddGame.setMinimumSize(QtCore.QSize(25, 0))
        self.AddGame.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.AddGame.setFont(font)
        self.AddGame.setStyleSheet("background-color: rgb(101, 203, 150); color: rgb(255, 255, 255);")
        self.AddGame.setObjectName("AddGame")
        self.AddGameLayout.addWidget(self.AddGame, 0, 1, 1, 1)
        
        self.GameRecommendationLayout_2.addLayout(self.AddGameLayout, 1, 0, 1, 1)
        self.Pages.addWidget(self.GameRecommendationPage)
        # End of Graphics Objects for Recommend Page


        # Start of Graphics Objects for Price Page
        self.PriceCheckPage = QtWidgets.QWidget()
        self.PriceCheckPage.setObjectName("PriceCheckPage")
        self.PriceCheckPageLayout = QtWidgets.QGridLayout(self.PriceCheckPage)
        self.PriceCheckPageLayout.setContentsMargins(11, 11, 11, 11)
        self.PriceCheckPageLayout.setSpacing(6)
        self.PriceCheckPageLayout.setObjectName("PriceCheckPageLayout")
        self.PriceCheckTitleLayout = QtWidgets.QGridLayout()
        self.PriceCheckTitleLayout.setContentsMargins(5, -1, -1, 1)
        self.PriceCheckTitleLayout.setSpacing(6)
        self.PriceCheckTitleLayout.setObjectName("PriceCheckTitleLayout")
        
        self.PriceCheckTitle = QtWidgets.QLabel(self.PriceCheckPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PriceCheckTitle.sizePolicy().hasHeightForWidth())
        self.PriceCheckTitle.setSizePolicy(sizePolicy)
        self.PriceCheckTitle.setMaximumSize(QtCore.QSize(16777215, 300))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.PriceCheckTitle.setFont(font)
        self.PriceCheckTitle.setStyleSheet("color: rgb(255, 255, 255);")
        self.PriceCheckTitle.setObjectName("PriceCheckTitle")
        self.PriceCheckTitleLayout.addWidget(self.PriceCheckTitle, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.PriceCheckPageLayout.addLayout(self.PriceCheckTitleLayout, 0, 0, 1, 1)
        
        self.PriceCheckLayout = QtWidgets.QGridLayout()
        self.PriceCheckLayout.setContentsMargins(20, -1, 10, -1)
        self.PriceCheckLayout.setSpacing(6)
        self.PriceCheckLayout.setObjectName("PriceCheckLayout")
        
        self.PriceCheckEntry = QtWidgets.QLineEdit(self.PriceCheckPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PriceCheckEntry.sizePolicy().hasHeightForWidth())
        self.PriceCheckEntry.setSizePolicy(sizePolicy)
        self.PriceCheckEntry.setMinimumSize(QtCore.QSize(400, 40))
        self.PriceCheckEntry.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.PriceCheckEntry.setCursorPosition(0)
        self.PriceCheckEntry.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.PriceCheckEntry.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.PriceCheckEntry.setObjectName("PriceCheckEntry")
        self.PriceCheckEntry.editingFinished.connect(self.processPriceCheck)
        self.PriceCheckLayout.addWidget(self.PriceCheckEntry, 0, 0, 1, 1)
        
        self.GetPriceButton = QtWidgets.QPushButton(self.PriceCheckPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GetPriceButton.sizePolicy().hasHeightForWidth())
        self.GetPriceButton.setSizePolicy(sizePolicy)
        self.GetPriceButton.setMinimumSize(QtCore.QSize(25, 0))
        self.GetPriceButton.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.GetPriceButton.setFont(font)
        self.GetPriceButton.setStyleSheet("background-color: rgb(101, 203, 150); color: rgb(255, 255, 255);")
        self.GetPriceButton.setObjectName("GetPriceButton")
        self.PriceCheckLayout.addWidget(self.GetPriceButton, 0, 1, 1, 1)
        self.PriceCheckPageLayout.addLayout(self.PriceCheckLayout, 1, 0, 1, 1)
        
        self.PriceViewLayout = QtWidgets.QGridLayout()
        self.PriceViewLayout.setContentsMargins(20, -1, 10, -1)
        self.PriceViewLayout.setHorizontalSpacing(30)
        self.PriceViewLayout.setVerticalSpacing(20)
        self.PriceViewLayout.setObjectName("PriceViewLayout")
        
        self.PriceCheckResults = QtWidgets.QTextBrowser(self.PriceCheckPage)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.PriceCheckResults.setFont(font)
        self.PriceCheckResults.setStyleSheet("color: rgb(0, 0, 0); background-color: rgb(193, 193, 193);")
        self.PriceCheckResults.setObjectName("listWidget")
        self.PriceViewLayout.addWidget(self.PriceCheckResults, 0, 0, 1, 1)
        
        self.PriceCheckPageLayout.addLayout(self.PriceViewLayout, 2, 0, 1, 1)
        self.Pages.addWidget(self.PriceCheckPage)
        # End of Graphics Objects for Price Page


        # Start of Graphics Objects for Login Page
        self.LogInPage = QtWidgets.QWidget()
        self.LogInPage.setObjectName("LogInPage")
        self.LoginPageLayout = QtWidgets.QGridLayout(self.LogInPage)
        self.LoginPageLayout.setContentsMargins(75, 75, 75, 75)
        self.LoginPageLayout.setSpacing(6)
        self.LoginPageLayout.setObjectName("LoginPageLayout")
        self.LoginLayout = QtWidgets.QGridLayout()
        self.LoginLayout.setSpacing(6)
        self.LoginLayout.setObjectName("LoginLayout")
        
        self.ActiveUsers = QtWidgets.QGroupBox(self.LogInPage)
        self.ActiveUsers.setMinimumSize(QtCore.QSize(800, 0))
        self.ActiveUsers.setMaximumSize(QtCore.QSize(800, 16777215))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.ActiveUsers.setFont(font)
        self.ActiveUsers.setStyleSheet("color: rgb(255, 255, 255);")
        self.ActiveUsers.setObjectName("ActiveUsers")

        self.userRadioButtons = []
        font = QtGui.QFont()
        font.setPointSize(10)
        users = self.model.steam_user.getAllUsers()
        for i in range(7):
            self.userRadioButtons.append(QtWidgets.QRadioButton(self.ActiveUsers))
            self.userRadioButtons[-1].setGeometry(QtCore.QRect(25, 20+40*(i+1), 500, 20))
            self.userRadioButtons[-1].setFont(font)
            self.userRadioButtons[-1].setObjectName("radioButton"+str(i+1))
            if len(users) > i:
                self.userRadioButtons[-1].setText(users[i][1])
            else:
                self.userRadioButtons[-1].setText("<Unregistered>")
            self.userRadioButtons[-1].clicked.connect(self.userSelect)
            if i==0:
                self.userRadioButtons[-1].setChecked(True)
            
        self.LoginLayout.addWidget(self.ActiveUsers, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        
        self.ConfirmButton = QtWidgets.QPushButton(self.LogInPage)
        self.ConfirmButton.setMinimumSize(QtCore.QSize(200, 50))
        self.ConfirmButton.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.ConfirmButton.setFont(font)
        self.ConfirmButton.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(30, 180, 175);")
        self.ConfirmButton.setObjectName("ConfirmButton")
        self.ConfirmButton.clicked.connect(self.newUserLogin)
        self.LoginLayout.addWidget(self.ConfirmButton, 5, 0, 1, 1, QtCore.Qt.AlignHCenter)
        
        self.Entry_2 = QtWidgets.QLineEdit(self.LogInPage)
        self.Entry_2.setMinimumSize(QtCore.QSize(200, 30))
        self.Entry_2.setMaximumSize(QtCore.QSize(300, 16777215))
        self.Entry_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Entry_2.setObjectName("Entry_2")
        self.LoginLayout.addWidget(self.Entry_2, 4, 0, 1, 1, QtCore.Qt.AlignHCenter)
        
        self.Title_2 = QtWidgets.QLabel(self.LogInPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Title_2.sizePolicy().hasHeightForWidth())
        self.Title_2.setSizePolicy(sizePolicy)
        self.Title_2.setMaximumSize(QtCore.QSize(16777215, 75))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.Title_2.setFont(font)
        self.Title_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.Title_2.setAlignment(QtCore.Qt.AlignCenter)
        self.Title_2.setObjectName("Title_2")
        self.LoginLayout.addWidget(self.Title_2, 0, 0, 1, 1)
        
        self.Instructions_2 = QtWidgets.QLabel(self.LogInPage)
        self.Instructions_2.setMaximumSize(QtCore.QSize(16777215, 60))
        self.Instructions_2.setStyleSheet("color: rgb(255, 255, 255)")
        self.Instructions_2.setAlignment(QtCore.Qt.AlignCenter)
        self.Instructions_2.setObjectName("Instructions_2")
        self.LoginLayout.addWidget(self.Instructions_2, 1, 0, 1, 1)
        
        spacerItem1 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.LoginLayout.addItem(spacerItem1, 3, 0, 1, 1)
        self.LoginPageLayout.addLayout(self.LoginLayout, 0, 0, 1, 1)
        self.Pages.addWidget(self.LogInPage)
        # End of Graphics Objects for Login Page
        
        self.gridLayout.addWidget(self.Pages, 1, 0, 1, 1)
        # End of Graphics Objects for GUI Page Stack

        self.retranslateUi(Widget)
        self.Pages.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Widget)
        self.userSelect()
        self.refreshRankings()
        # End of Graphics Objects for Main Program Window

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.LoginButton.setText(_translate("Widget", "Change User"))
        self.SteamRushText.setText(_translate("Widget", "SteamRush"))
        self.UserButton.setText(_translate("Widget", "User"))
        self.PriceCheckButton.setText(_translate("Widget", "Price Check"))
        self.RankingButton.setText(_translate("Widget", "Ranking"))
        self.GameRecommendationButton.setText(_translate("Widget", "Game Recommendation"))
        self.SearchBar.setPlaceholderText(_translate("Widget", "Input game name. Press Enter to search."))
        self.GenreInfo.setText(_translate("Widget", "TextLabel"))
        self.GenreLabel.setText(_translate("Widget", "Genres:"))
        self.TopVotedTagsInfo.setText(_translate("Widget", "TextLabel"))
        self.AvgHrsInfo.setText(_translate("Widget", "TextLabel"))
        self.AvgHrsLabel.setText(_translate("Widget", "Average Hours Played:"))
        self.TopVotedTagsLabel.setText(_translate("Widget", "Top-Voted Tags:"))
        self.TotalReviewsLabel.setText(_translate("Widget", "Total Reviews:"))
        self.PositiveReviewsInfo_2.setText(_translate("Widget", "TextLabel"))
        self.TotalReviewsInfo.setText(_translate("Widget", "TextLabel"))
        self.PositiveReviewsInfo.setText(_translate("Widget", "Percentage Positive Reviews:"))
        self.GameTitle.setText(_translate("Widget", "Welcome to SteamRush!"))
        self.pushButton.setText(_translate("Widget", "Add to Wishlist"))
        self.Title_3.setText(_translate("Widget", "Rankings"))
        self.MostPlayedList.setHtml(_translate("Widget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Dubai Light\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.MostPositiveList.setHtml(_translate("Widget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Consolas\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.MostPlayedLabel.setText(_translate("Widget", "    Most Hours Played  \n(Average, Past 2 Weeks)"))
        self.MostPositiveLabel.setText(_translate("Widget", "Strongest Positive Ratings"))
        self.HoursPlayedLabel.setText(_translate("Widget", "Total Hours Played"))
        self.AccountCreationLabel.setText(_translate("Widget", "Account Created On:"))
        self.GamesOwnedLabel.setText(_translate("Widget", "Total Games Owned"))
        self.GameLibraryLabel.setText(_translate("Widget", "Your Games:"))
        self.AccountCreationInfo.setText(_translate("Widget", "TextLabel"))
        self.GamesOwnedInfo.setText(_translate("Widget", "TextLabel"))
        self.HoursPlayedInfo.setText(_translate("Widget", "TextLabel"))
        self.AccountWorthInfo.setText(_translate("Widget", "TextLabel"))
        self.AccountWorthLabel.setText(_translate("Widget", "Total Account Worth"))
        self.removeSelectedWishlist.setText(_translate("Widget", "Remove Selected"))
        self.WishlistLabel.setText(_translate("Widget", "Wishlist"))
        self.UsernameLabel.setText(_translate("Widget", "Username"))
        self.GenerateButton.setText(_translate("Widget", "Generate!"))
##        self.RecommendationInput.setHtml(_translate("Widget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
##        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
##        "p, li { white-space: pre-wrap; }\n"
##        "</style></head><body style=\" font-family:\'Agency FB\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
##        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton_2.setText(_translate("Widget", "Remove Selected"))
        self.RecommendationResults.setHtml(_translate("Widget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Agency FB\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.Title.setText(_translate("Widget", "Game Recommendation"))
        self.Instructions.setText(_translate("Widget", "<html><head/><body><p>To use the game recommendation engine, search for and add any games you would like to be factored into the algorithm. When you\'re finished, click the Generate button below!</p></body></html>"))
        self.GameRecommendationEntry.setPlaceholderText(_translate("Widget", "Add a game."))
        self.AddGame.setText(_translate("Widget", "Add Game"))
        self.PriceCheckTitle.setText(_translate("Widget", "Price Check"))
        self.PriceCheckEntry.setPlaceholderText(_translate("Widget", "Enter the name of a game you would like to check the price of"))
        self.GetPriceButton.setText(_translate("Widget", "Get Price!"))
        self.ActiveUsers.setTitle(_translate("Widget", "Users"))
        #self.radioButton.setText(_translate("Widget", "User 1"))
        self.ConfirmButton.setText(_translate("Widget", "Connect to Steam!"))
        self.Entry_2.setPlaceholderText(_translate("Widget", "Enter your Steam ID here."))
        self.Title_2.setText(_translate("Widget", "Welcome to SteamRush!"))
        self.Instructions_2.setText(_translate("Widget", "Choose one of the active users below or connect to a new Steam ID. Note: This feature only works for public Steam IDs."))

    # Begin Event Handling Functions
    # Events are generated by interaction with GUI objects
    # Those objects have been attached to these functions,
    # which are called in response to Events.

    def refreshWishlist(self):
        self.Wishlist.clear()
        for g in range(len(self.model.wishListContent)):
            lineString = ""
            lineString += self.model.wishListContent[g][0] + "\n"
            lineString += "Current Steam Price: " + str(self.model.wishListContent[g][1][0][1]) + "\n"
            lineString += "Lowest Price: " + str(self.model.wishListContent[g][1][1][1]) + "\n"
            lineString += "Vendor: " + self.model.wishListContent[g][1][1][0] + "\n"
            self.Wishlist.addItem(lineString)

    def refreshReclist(self):
        self.RecommendationInput.clear()
        for g in range(len(self.model.recommendListContent)):
            lineString = self.model.recommendListContent[g][1]
            self.RecommendationInput.addItem(lineString)

    def refreshRankings(self):
        ratings = self.model.steam_api.get_ranked_by_rating(100)
        hours = self.model.steam_api.get_ranked_by_hours(100)

        rateString = ""
        hourString = ""

        self.MostPositiveList.clear()
        for i,game in enumerate(ratings):
            rateString += str(i+1) + ". " + game[1] + "\n   " + "{0:.3f}% Positive, ".format(game[2][0]) + str(game[2][1]) + " Total.\n"
        self.MostPositiveList.setText(rateString)

        self.MostPlayedList.clear()
        for i,game in enumerate(hours):
            hourString += str(i+1) + ". " + game[1] + "\n   " + "{0:.2f} Hours, ".format(game[2]/float(60)) + "\n"
        self.MostPlayedList.setText(hourString)
        
    
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

    def onWishlistClick(self):
        self.model.selectedWishItem = self.Wishlist.currentRow()

    def removeFromWishlist(self):
        self.model.removeSelectedFromWishlist()
        self.refreshWishlist()

    def addWishlistButton(self):
        self.model.addToWishlist(self.model.lastGameSearched)

    def onReclistClick(self):
        self.model.selectedRecItem = self.RecommendationInput.currentRow()

    def removeFromReclist(self):
        self.model.removeSelectedFromReclist()
        self.RecommendationResults.clear()
        self.refreshReclist()

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
        

    def processRecommendRequest(self):
        
        game_ids = []
        for game in self.model.recommendListContent:
            game_ids.append(game[0])

        all_results = self.model.steam_api.recommend_multi_input(gameIDs=game_ids, required_genres=[], banned_genres=[], banned_games=[], showTop=10, cross_thresh=2, matchRate=0.5, cutoff=10, ratePower=1, confPower=3)
        
        resultString = ""
        resultString += "Cross-Recommendation Results:\n"
        for r in all_results[0]:
            resultString += str(r[1]) + "\n"
        resultString += "\n"
        for results in all_results[1]:
            resultString += "Recommendations from " + results[1] + " (" + results[0] + "):\n"
            for r in results[2]:
                resultString += str(r[1]) + "\n"
            resultString += "\n"
            
        self.RecommendationResults.setText(resultString)


    def processPriceCheck(self):
        text = self.PriceCheckEntry.text()
        self.PriceCheckEntry.clear()
        if text != "":
            app_parse = self.model.steam_api.get_game_id_from_steam(text)
            app_id = app_parse[0]
            if app_id != "999999999":
                prices = self.model.itad_api.get_prices(self.model.itad_api.get_plain(app_id))
                self.PriceCheckResults.clear()
                if len(prices) == 0:
                    resultString = "Game not found."
                else:            
                    resultString = "Prices for: " + self.model.steam_api.get_name(app_id) + "\n\n"
                    resultString += "Lowest Price in History:\n"
                    resultString += str(prices[0]) + "\n\n"
                    resultString += "Current Prices: \n"
                    for p in prices[1:]:
                         resultString += str(p) + "\n"
                self.PriceCheckResults.setText(resultString)
                     


    def processSearchBar(self):
        text = self.SearchBar.text()
      
        if text != "":
            app_parse = self.model.steam_api.get_game_id_from_steam(text)
            app_id = app_parse[0]
            name = "Game not found"
            pix = QtGui.QPixmap(":/icon/steam_icon.gif")
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
                    app_img = Image.open(BytesIO(app_parse[1]))
                    qim = ImageQt(app_img)
                    pix = QtGui.QPixmap.fromImage(qim)
                except:
                    pass

            self.GameTitle.setText(name)
            self.GamePic.setPixmap(pix)
            self.AvgHrsInfo.setText("{0:.2f}".format(hours))
            self.PositiveReviewsInfo_2.setText("{0:.2f}%".format(100*reviews[0]))
            self.TotalReviewsInfo.setText(str(reviews[1]))
            self.GenreInfo.setText(str(genres))
            self.TopVotedTagsInfo.setText(str(tags))
            self.model.lastGameSearched = app_id
        
        self.SearchBar.clear()
      
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
        
    def newUserLogin(self):
        userID = self.Entry_2.text()
        self.Entry_2.clear()
        if userID.isdigit():
            self.model.switchToUser(userID)
            self.updateUserInfo()
            uName = self.model.steam_user.getName()
            
            for button in self.userRadioButtons:
                if button.text() == "<Unregistered>":
                    button.setText(uName)
                    button.setChecked(True)
                    break

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
            image_scrape = requests.get(imgUrl).content
            user_img = Image.open(BytesIO(image_scrape))
            qim = ImageQt(user_img)
            pix = QtGui.QPixmap.fromImage(qim)
        else:
            pix = QtGui.QPixmap(":/icon/steam_icon.gif")
        self.UsernameLabel.setText(name)
        self.AccountCreationInfo.setText(str(start.date()))
        self.GamesOwnedInfo.setText(str(number))
        self.HoursPlayedInfo.setText("{0:.2f}".format(hours))
        self.AccountWorthInfo.setText("{0:.2f}".format(worth))
        self.ProfilePicture.setPixmap(pix)

        self.GameLibraryInfo.clear()
        for g in range(len(played)):
            lineString = played[g][0] + "\n    Hours Played: {0:.2f}".format(played[g][1])
            self.GameLibraryInfo.addItem(lineString)



import resources_rc


if __name__ == "__main__":
    import sys

    
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Main_GUI_Visuals()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())
