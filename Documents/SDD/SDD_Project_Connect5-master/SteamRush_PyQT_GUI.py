# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\kauffk\Documents\GitHub\SDD_Project_Connect5\Documents\SDD\SDD_Project_Connect5-master\untitled1\widget.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from SteamSpy_API_Calls import SteamSpy_API_Caller
from ITAD_API_Calls import ITAD_API_Caller
from User import SteamUser


class GUI_Content_Model():
    
    def __init__(self):
        #API Call objects
        self.steam_api = SteamSpy_API_Caller(appFile="SteamSpy_App_Cache.txt", tagFile="SteamSpy_Tags_Cache.txt")
        self.itad_api = ITAD_API_Caller()

        #User object
        self.steam_user = SteamUser(userFile="User_Data_Cache.txt")
        self.steam_user.loginSteamID("76561198046994663")

        #Model Information
        self.wishListContent = []
        self.selectedWishItem = 0
        self.recommendListContent = []
        self.selectedRecItem = 0



class Main_GUI_Visuals(object):

    def __init__(self):
        
        self.model = GUI_Content_Model()
    
    def setupUi(self, Widget):

        #Overall Window
        Widget.setObjectName("Widget")
        Widget.resize(1200, 900)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Widget.sizePolicy().hasHeightForWidth())
        Widget.setSizePolicy(sizePolicy)
        Widget.setMinimumSize(QtCore.QSize(1200, 900))
        Widget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.gridLayout_8 = QtWidgets.QGridLayout(Widget)
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_8.setSpacing(2)
        self.gridLayout_8.setObjectName("gridLayout_8")
        
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
        self.gridLayout_4 = QtWidgets.QGridLayout(self.MenuBar)
        self.gridLayout_4.setContentsMargins(20, 11, 11, 11)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        
        spacerItem = QtWidgets.QSpacerItem(300, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 3, 1, 1)

        
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
        self.LoginButton.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(30, 180, 175);)
        self.LoginButton.setObjectName("LoginButton")
        self.gridLayout_4.addWidget(self.LoginButton, 0, 6, 1, 1)


        self.SearchButton = QtWidgets.QPushButton(self.MenuBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearchButton.sizePolicy().hasHeightForWidth())
        self.SearchButton.setSizePolicy(sizePolicy)
        self.SearchButton.setMinimumSize(QtCore.QSize(100, 30))
        self.SearchButton.setMaximumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.SearchButton.setFont(font)
        self.SearchButton.setStyleSheet("background-color: rgb(101, 203, 150); color: rgb(255, 255, 255);")
        self.SearchButton.setObjectName("SearchButton")
        self.gridLayout_4.addWidget(self.SearchButton, 0, 5, 1, 1)


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
        self.gridLayout_4.addWidget(self.SteamRushIcon, 0, 0, 1, 1)

                                       
        self.SteamRushText = QtWidgets.QPushButton(self.MenuBar)
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(26)
        self.SteamRushText.setFont(font)
        self.SteamRushText.setStyleSheet("color: rgb(255, 255, 255);")
        self.SteamRushText.setFlat(True)
        self.SteamRushText.setObjectName("SteamRushText")
        self.gridLayout_4.addWidget(self.SteamRushText, 0, 1, 1, 1)

                                       
        self.SearchBar = QtWidgets.QLineEdit(self.MenuBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearchBar.sizePolicy().hasHeightForWidth())
        self.SearchBar.setSizePolicy(sizePolicy)
        self.SearchBar.setMinimumSize(QtCore.QSize(200, 20))
        self.SearchBar.setMaximumSize(QtCore.QSize(450, 30))
        self.SearchBar.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.SearchBar.setInputMethodHints(QtCore.Qt.ImhNoAutoUppercase)
        self.SearchBar.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.SearchBar.setObjectName("SearchBar")
        self.gridLayout_4.addWidget(self.SearchBar, 0, 4, 1, 1)
        self.gridLayout_8.addWidget(self.MenuBar, 0, 0, 1, 1)

                                       
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

                                       
        self.HomePage = QtWidgets.QWidget()
        self.HomePage.setStyleSheet("background-color: rgb(83, 83, 83);")
        self.HomePage.setObjectName("HomePage")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.HomePage)
        self.gridLayout_2.setContentsMargins(75, 75, 75, 75)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 0, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 1)
        self.HomePageLayout = QtWidgets.QGridLayout()
        self.HomePageLayout.setContentsMargins(0, -1, -1, -1)
        self.HomePageLayout.setSpacing(20)
        self.HomePageLayout.setObjectName("HomePageLayout")

                                       
        self.GameRecommendationButton = QtWidgets.QPushButton(self.HomePage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GameRecommendationButton.sizePolicy().hasHeightForWidth())
        self.GameRecommendationButton.setSizePolicy(sizePolicy)
        self.GameRecommendationButton.setMinimumSize(QtCore.QSize(300, 0))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(15)
        self.GameRecommendationButton.setFont(font)
        self.GameRecommendationButton.setStyleSheet("color: rgb(255, 255, 255);")
        self.GameRecommendationButton.setIconSize(QtCore.QSize(14, 14))
        self.GameRecommendationButton.setObjectName("GameRecommendationButton")
        self.HomePageLayout.addWidget(self.GameRecommendationButton, 0, 2, 2, 1)

                                       
        self.Gallery = QtWidgets.QTabWidget(self.HomePage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Gallery.sizePolicy().hasHeightForWidth())
        self.Gallery.setSizePolicy(sizePolicy)
        self.Gallery.setMinimumSize(QtCore.QSize(200, 400))
        self.Gallery.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.Gallery.setStyleSheet("background-color: rgb(193, 193, 193);")
        self.Gallery.setObjectName("Gallery")
                                       
        self.Image1 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Image1.sizePolicy().hasHeightForWidth())
        self.Image1.setSizePolicy(sizePolicy)
        self.Image1.setMinimumSize(QtCore.QSize(0, 0))
        self.Image1.setObjectName("Image1")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.Image1)
        self.gridLayout_5.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_4 = QtWidgets.QLabel(self.Image1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(0, 0))
        self.label_4.setMaximumSize(QtCore.QSize(500, 400))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap(":/icon/Overcooked-Banner.jpg"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.gridLayout_5.addWidget(self.label_4, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem2, 2, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem3, 0, 0, 1, 1)
        self.Gallery.addTab(self.Image1, "")
        self.Image2 = QtWidgets.QWidget()
        self.Image2.setObjectName("Image2")
        self.Gallery.addTab(self.Image2, "")
        self.HomePageLayout.addWidget(self.Gallery, 0, 3, 3, 1)

                                       
        self.WishlistButton = QtWidgets.QPushButton(self.HomePage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.WishlistButton.sizePolicy().hasHeightForWidth())
        self.WishlistButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(15)
        self.WishlistButton.setFont(font)
        self.WishlistButton.setStyleSheet("color: rgb(255, 255, 255);")
        self.WishlistButton.setObjectName("WishlistButton")
        self.HomePageLayout.addWidget(self.WishlistButton, 1, 1, 1, 1)
        self.UserButton = QtWidgets.QPushButton(self.HomePage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.UserButton.sizePolicy().hasHeightForWidth())

                                       
        self.UserButton.setSizePolicy(sizePolicy)
        self.UserButton.setMinimumSize(QtCore.QSize(100, 0))
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
        self.HomePageLayout.addWidget(self.PriceCheckButton, 2, 1, 1, 2)
        self.gridLayout_2.addLayout(self.HomePageLayout, 1, 0, 1, 2)
        self.Pages.addWidget(self.HomePage)
        self.UserPage = QtWidgets.QWidget()
        self.UserPage.setStyleSheet("background-color: rgb(83, 83, 83);")
        self.UserPage.setObjectName("UserPage")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.UserPage)
        self.gridLayout_7.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_7.setSpacing(6)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.Pages.addWidget(self.UserPage)
        
        self.WishlistPage = QtWidgets.QWidget()
        self.WishlistPage.setStyleSheet("background-color: rgb(83, 83, 83);")
        self.WishlistPage.setObjectName("WishlistPage")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.WishlistPage)
        self.gridLayout_6.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName("gridLayout_6")
        
        self.WishlistLayout = QtWidgets.QGridLayout()
        self.WishlistLayout.setContentsMargins(15, -1, 15, 15)
        self.WishlistLayout.setHorizontalSpacing(7)
        self.WishlistLayout.setVerticalSpacing(20)
        self.WishlistLayout.setObjectName("WishlistLayout")
        
        self.WishlistLabel = QtWidgets.QLabel(self.WishlistPage)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.WishlistLabel.setFont(font)
        self.WishlistLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.WishlistLabel.setWordWrap(False)
        self.WishlistLabel.setObjectName("WishlistLabel")
        self.WishlistLayout.addWidget(self.WishlistLabel, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.listWidget = QtWidgets.QListWidget(self.WishlistPage)
        self.listWidget.setMinimumSize(QtCore.QSize(900, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.listWidget.setFont(font)
        self.listWidget.setStyleSheet("background-color: rgb(140, 140, 140);")
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.listWidget.setMovement(QtWidgets.QListView.Static)
        self.listWidget.setFlow(QtWidgets.QListView.TopToBottom)
        self.listWidget.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.listWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.listWidget.setModelColumn(0)
        self.listWidget.setUniformItemSizes(True)
        self.listWidget.setBatchSize(100)
        self.listWidget.setSelectionRectVisible(False)
        self.listWidget.setObjectName("listWidget")
        self.WishlistLayout.addWidget(self.listWidget, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.pushButton = QtWidgets.QPushButton(self.WishlistPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(175, 40))
        self.pushButton.setMaximumSize(QtCore.QSize(250, 16777215))
        self.pushButton.setStyleSheet("background-color: rgb(244, 140, 164);\n"
"color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.WishlistLayout.addWidget(self.pushButton, 3, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.gridLayout_6.addLayout(self.WishlistLayout, 0, 0, 1, 1)
        self.Pages.addWidget(self.WishlistPage)
        
        self.GameRecommendationPage = QtWidgets.QWidget()
        self.GameRecommendationPage.setStyleSheet("background-color: rgb(83, 83, 83);")
        self.GameRecommendationPage.setObjectName("GameRecommendationPage")
        self.gridLayout = QtWidgets.QGridLayout(self.GameRecommendationPage)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.TextViewLayout = QtWidgets.QGridLayout()
        self.TextViewLayout.setContentsMargins(20, -1, 10, -1)
        self.TextViewLayout.setHorizontalSpacing(30)
        self.TextViewLayout.setVerticalSpacing(20)
        self.TextViewLayout.setObjectName("TextViewLayout")
        self.RecommendationInput = QtWidgets.QTextBrowser(self.GameRecommendationPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RecommendationInput.sizePolicy().hasHeightForWidth())
        self.RecommendationInput.setSizePolicy(sizePolicy)
        self.RecommendationInput.setMinimumSize(QtCore.QSize(500, 0))
        self.RecommendationInput.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.RecommendationInput.setFont(font)
        self.RecommendationInput.setStyleSheet("background-color: rgb(140, 140, 140);")
        self.RecommendationInput.setObjectName("RecommendationInput")
        self.TextViewLayout.addWidget(self.RecommendationInput, 0, 0, 1, 1)
        self.RecommendationResults = QtWidgets.QTextBrowser(self.GameRecommendationPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RecommendationResults.sizePolicy().hasHeightForWidth())
        self.RecommendationResults.setSizePolicy(sizePolicy)
        self.RecommendationResults.setMinimumSize(QtCore.QSize(500, 0))
        self.RecommendationResults.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Dubai Light")
        self.RecommendationResults.setFont(font)
        self.RecommendationResults.setStyleSheet("background-color: rgb(193, 193, 193);\n"
"")
        self.RecommendationResults.setObjectName("RecommendationResults")
        self.TextViewLayout.addWidget(self.RecommendationResults, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.TextViewLayout, 2, 0, 1, 1)
        self.AddGameLayout = QtWidgets.QGridLayout()
        self.AddGameLayout.setContentsMargins(20, -1, 10, -1)
        self.AddGameLayout.setSpacing(6)
        self.AddGameLayout.setObjectName("AddGameLayout")
        self.Entry = QtWidgets.QLineEdit(self.GameRecommendationPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Entry.sizePolicy().hasHeightForWidth())
        self.Entry.setSizePolicy(sizePolicy)
        self.Entry.setMinimumSize(QtCore.QSize(400, 40))
        self.Entry.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Entry.setObjectName("Entry")
        self.AddGameLayout.addWidget(self.Entry, 0, 0, 1, 1)
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
        self.AddGame.setStyleSheet("background-color: rgb(101, 203, 150);\n"
"color: rgb(255, 255, 255);")
        self.AddGame.setObjectName("AddGame")
        self.AddGameLayout.addWidget(self.AddGame, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.AddGameLayout, 1, 0, 1, 1)
        self.TopLayout = QtWidgets.QGridLayout()
        self.TopLayout.setContentsMargins(5, -1, -1, 1)
        self.TopLayout.setSpacing(6)
        self.TopLayout.setObjectName("TopLayout")
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
        self.TopLayout.addWidget(self.Title, 0, 0, 1, 1)
        self.Instructions = QtWidgets.QLabel(self.GameRecommendationPage)
        self.Instructions.setMinimumSize(QtCore.QSize(0, 25))
        self.Instructions.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Instructions.setFont(font)
        self.Instructions.setStyleSheet("color: rgb(255, 255, 255);")
        self.Instructions.setWordWrap(True)
        self.Instructions.setObjectName("Instructions")
        self.TopLayout.addWidget(self.Instructions, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.TopLayout, 0, 0, 1, 1)
        
        self.pushButton_2 = QtWidgets.QPushButton(self.GameRecommendationPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMinimumSize(QtCore.QSize(200, 40))
        self.pushButton_2.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: rgb(101, 203, 150);\n"
"color: rgb(255, 255, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 3, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.Pages.addWidget(self.GameRecommendationPage)
        
        self.PriceCheckPage = QtWidgets.QWidget()
        self.PriceCheckPage.setObjectName("PriceCheckPage")
        self.Pages.addWidget(self.PriceCheckPage)
        
        self.LogInPage = QtWidgets.QWidget()
        self.LogInPage.setObjectName("LogInPage")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.LogInPage)
        self.gridLayout_9.setContentsMargins(75, 75, 75, 75)
        self.gridLayout_9.setSpacing(6)
        self.gridLayout_9.setObjectName("gridLayout_9")
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
        self.ActiveUsers.setStyleSheet("color: rgb(255, 255, 255);\n"
"")
        self.ActiveUsers.setObjectName("ActiveUsers")
        self.radioButton = QtWidgets.QRadioButton(self.ActiveUsers)
        self.radioButton.setGeometry(QtCore.QRect(25, 50, 95, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton.setFont(font)
        self.radioButton.setObjectName("radioButton")
        self.LoginLayout.addWidget(self.ActiveUsers, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.ConfirmButton = QtWidgets.QPushButton(self.LogInPage)
        self.ConfirmButton.setMinimumSize(QtCore.QSize(200, 50))
        self.ConfirmButton.setMaximumSize(QtCore.QSize(300, 16777215))
        self.ConfirmButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(30, 180, 175);\n"
"\n"
"")
        self.ConfirmButton.setObjectName("ConfirmButton")
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
        spacerItem4 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.LoginLayout.addItem(spacerItem4, 3, 0, 1, 1)
        self.gridLayout_9.addLayout(self.LoginLayout, 0, 0, 1, 1)
        self.Pages.addWidget(self.LogInPage)
        
        self.gridLayout_8.addWidget(self.Pages, 1, 0, 1, 1)
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
        self.gridLayout_8.addWidget(self.BottomBar, 2, 0, 1, 1)

        self.retranslateUi(Widget)
        self.Pages.setCurrentIndex(3)
        self.Gallery.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.LoginButton.setText(_translate("Widget", "Change User"))
        self.SearchButton.setText(_translate("Widget", "Search"))
        self.SteamRushText.setText(_translate("Widget", "SteamRush"))
        self.SearchBar.setPlaceholderText(_translate("Widget", "Search for a game here"))
        self.GameRecommendationButton.setText(_translate("Widget", "Game\n"
"Recommendation"))
        self.WishlistButton.setText(_translate("Widget", "Wishlist"))
        self.UserButton.setText(_translate("Widget", "User"))
        self.PriceCheckButton.setText(_translate("Widget", "Price Check"))
        self.WishlistLabel.setText(_translate("Widget", "Wishlist"))
        self.pushButton.setText(_translate("Widget", "Remove Selected"))
        self.RecommendationInput.setHtml(_translate("Widget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.RecommendationResults.setHtml(_translate("Widget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Dubai Light\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.Entry.setPlaceholderText(_translate("Widget", "Add a game."))
        self.AddGame.setText(_translate("Widget", "Add Game"))
        self.Title.setText(_translate("Widget", "Game Recommendation"))
        self.Instructions.setText(_translate("Widget", "<html><head/><body><p>To use the game recommendation engine, search for and add any games you would like to be factored into the algorithm. When you\'re finished, click the Generate button below!</p></body></html>"))
        self.pushButton_2.setText(_translate("Widget", "Generate!"))
        self.ActiveUsers.setTitle(_translate("Widget", "Users"))
        self.radioButton.setText(_translate("Widget", "User 1"))
        self.ConfirmButton.setText(_translate("Widget", "Connect to Steam!"))
        self.Entry_2.setPlaceholderText(_translate("Widget", "Enter your Steam ID here."))
        self.Title_2.setText(_translate("Widget", "Welcome to SteamRush!"))
        self.Instructions_2.setText(_translate("Widget", "Choose one of the active users below or connect to a new Steam ID.\n"
"Note: This feature only works for public Steam IDs."))

    # Page object index: home = 0, user = 1, wishlist = 2 
    def setPageHome(self):
        self.Pages.setCurrentIndex(0)
    def setPageUser(self):
        self.Pages.setCurrentIndex(1)
        
    def setPageWishlist(self):
        self.Pages.setCurrentIndex(2)

        wishlist = [ self.model.steam_api.get_name(g_id) for g_id in self.model.steam_user.getDesiredGames() ]
        refresh = False
        if len(wishlist) == len(self.model.wishListContent):
            for w in range(len(wishlist)):
                if wishlist[w] != self.model.wishListContent[w][0]:
                    refresh = True
                    break
        else:
            refresh = True

        if refresh:
            raw_prices = [ self.model.itad_api.get_prices(self.model.itad_api.get_plain(g_id)) for g_id in self.model.steam_user.getDesiredGames() ]
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
            self.model.wishListContent = []
            for g in range(len(wishlist)):
                self.model.wishListContent.append([wishlist[g], revised_prices[g]])
        self.listWidget.clear()
        for g in range(len(self.model.wishListContent)):
            lineString = ""
            lineString += self.model.wishListContent[g][0] + "\n"
            lineString += "Current Steam Price: " + str(self.model.wishListContent[g][1][0][1]) + "\n"
            lineString += "Lowest Price: " + str(self.model.wishListContent[g][1][1][1]) + "\n"
            lineString += "Vendor: " + self.model.wishListContent[g][1][1][0] + "\n"
            self.listWidget.addItem(lineString)    
        
        
    def setPageRecommend(self):
        self.Pages.setCurrentIndex(3)
    def setPagePrice(self):
        self.Pages.setCurrentIndex(0)


import resources_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Main_GUI_Visuals()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())
