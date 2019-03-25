from tkinter import *
from tkinter import messagebox
from SteamSpy_API_Calls import SteamSpy_API_Caller
from ITAD_API_Calls import ITAD_API_Caller

import os
import Search

## Module to connect to public Steam profile 
def connect_to_steam():
	filewin = Toplevel(root)
	filewin.title("Connect to Steam.")
	
	#Have popup window follow parent object placement.
	x=root.winfo_rootx()
	y=root.winfo_rooty()
	geom="+%d+%d" % (x,y)
	filewin.geometry(geom)

	Label(filewin, text='Connect to your public Steam account here.').pack(padx=30, pady=30)
	Button(filewin, text= "Login here").pack()

## Module to switch current user. Currently uses a username/password system. 
## Want to implement a dropdown menu for users to get rid of password authentication;
## Not sure about security for that choice.
def switch_user():
	filewin = Toplevel(root)
	filewin.title("Change User")
	
	x=root.winfo_rootx()
	y=root.winfo_rooty()
	geom="+%d+%d" % (x,y)
	filewin.geometry(geom)

	#Username and password labels
	Label(filewin, text='Username').grid(row=0)
	Label(filewin, text='Password').grid(row=1)

	#Entry fields for username, password
	e1 = Entry(filewin).grid(row=0,column=1, padx=3)
	e2 = Entry(filewin, show='*').grid(row=1, column=1, padx=3)
	
	#Keep user logged in
	Checkbutton(filewin, text = "Keep Me Logged In").grid(columnspan=2)
	#Submit
	Button(filewin, text= "Login!", activebackground='pink1').grid(columnspan=2, pady=3)

## Module to generate game recommendations based on 2 parameters, by type or by name.
def generate_recommendation():
	TYPES = ['Action', 'Adventure', 'Casual', 'Indie', 'Massively Multiplayer', 'Racing', 'RPG', 'Simulation', 
		 'Sports', 'Strategy']
	## Module to generate game recommendations by type.
	def by_types():
		x=root.winfo_rootx()
		y=root.winfo_rooty()
		geom="+%d+%d" % (x,y)
		filewin1 = Toplevel(root)
		filewin1.title("Recommend by Types")
		filewin1.geometry(geom)
		#Obtain user input types.
		vars=[]
		checks=[]
		row_num=1
		#Output checkboxes in column format.
		for type in TYPES:
			var = IntVar()
			chk = Checkbutton(filewin1, text=type, variable=var)
			chk.grid(row=row_num, sticky=W)
			row_num+=1
			vars.append(var)
		def submit():
			checks.clear()
			count=0
			for i in vars:
				if i.get() == 1 and TYPES[count] not in checks:
					checks.append(TYPES[count])
				count+=1
			print(checks)

		def clear_checkbox():
			for i in vars:
				i.set(0)
			checks.clear()
			print(checks)
		
		Button(filewin1, text="Submit", activebackground='pink1', command=submit).grid(row=row_num, pady=3)
		Button(filewin1, text="Clear", activebackground='pink1', command=clear_checkbox).grid(row=row_num+1)

	## Module to generate game recommendations by game names. Incomplete.
	def by_names():
		filewin2 = Toplevel(root)
		filewin2.title("Recommend by Names")

		x=root.winfo_rootx()
		y=root.winfo_rooty()
		geom="+%d+%d" % (x,y)
		filewin2.geometry(geom)

		def command_temp(text):
			messagebox.showinfo("Search Results", "Searching for: %s"%text)
		Search.SearchBox(filewin2, command=command_temp, placeholder="Enter game name").pack(pady=6, padx=3)
		
	## User game recommendation method selection: by type or by name.	
	x=root.winfo_rootx()
	y=root.winfo_rooty()
	geom="+%d+%d" % (x,y)
	filewin = Toplevel(root)
	filewin.title("Game Recommendation")
	filewin.geometry(geom)
	type_button = Button(filewin, text="Recommend by Types", width=20, command=by_types)
	type_button.grid(row=0,column=0)
	name_button = Button(filewin, text="Recommend by Names", width=20, command=by_names)
	name_button.grid(row=0, column=1)

## Module to view user's wishlist.
def wishlist():
	wishlist = ["Cuphead", "Overcooked", "Overcooked 2", "DOTA 2"]
	filewin = Toplevel(root)
	filewin.title("Wishlist")

	Label(filewin, text="Your wishlist is displayed below.", font=("", 10, "italic")).grid(pady=3, columnspan=4)
	row_num = 2
	for game in wishlist:
		#Game name, price information, and current rating are displayed. Rating is optional.
		Label(filewin, text=game, font="fixedsys 12 bold").grid(row=row_num, sticky=W, columnspan=4)
		Label(filewin, text="Current Price: $9.99").grid(row=row_num+1, columnspan=2, sticky=W, padx=8)
		Label(filewin, text="Rating: 7.9/10").grid(row=row_num+2, columnspan=2, sticky=W, padx=8)
		Label(filewin, text="").grid(row=row_num+3, columnspan=4)

		row_num += 4

## Module to check price of one game.
def pricecheck():
	filewin = Toplevel(root)
	filewin.title("Price Check")
	def command(text):
		messagebox.showinfo("Search Results", "Searching for: %s"%text)
	Search.SearchBox(filewin, command=command, placeholder="Enter game name").pack(pady=6, padx=3)

## See rankings by account value.
def rank_by_account_value():
	Label(root, text="See rankings by account value").pack()

## See rankings by account level.
def rank_by_account_level():
	Label(root, text="See rankings by account level").pack()

## Helper function to create menu bar and corresponding cascading options.
def make_menus():
	menu = Menu(root)
	root.config(menu=menu)

	#User menu
	user_menu = Menu(menu, tearoff=0)
	user_menu.add_command(label="Connect to Steam", command=connect_to_steam)
	user_menu.add_command(label="Change local user", command=switch_user)
	user_menu.add_separator()
	user_menu.add_command(label="Quit", command=root.quit)
	menu.add_cascade(label="User", menu=user_menu)

	#Game menu
	gamerec_menu = Menu(menu, tearoff=0)
	gamerec_menu.add_command(label="Recommendation", command=generate_recommendation)
	menu.add_cascade(label="Game", menu=gamerec_menu)

	#Price watching menu
	pricewatch_menu = Menu(menu, tearoff=0)	
	pricewatch_menu.add_command(label="View Wishlist", command=wishlist)
	pricewatch_menu.add_command(label="Price Check", command=pricecheck)
	menu.add_cascade(label="Price Watch", menu=pricewatch_menu)

	#Ranking menu
	ranking_menu = Menu(menu, tearoff=0)
	ranking_menu.add_command(label="By account value", command=rank_by_account_value)
	ranking_menu.add_command(label="By account level", command=rank_by_account_level)
	menu.add_cascade(label="Ranking", menu=ranking_menu)


#API Call objects
steam_api = SteamSpy_API_Caller(appFile="SteamSpy_App_Cache.txt", tagFile="SteamSpy_Tags_Cache.txt")
itad_api = ITAD_API_Caller()

#Create initial window.
root = Tk()
root.title("SteamRush")
root.geometry("800x600+500+200")
root.configure(background='black')
make_menus()

#Show welcome message and home page graphics.
steam_icon = PhotoImage(file= "images/steam_icon.gif")
Label(root, bg='black', image=steam_icon).pack()
Label(root, text="Welcome to SteamRush!", font=("fixedsys", 26, "bold"), bg='black', fg='white').pack()

#text represents the user's input.
def get_game_rec(text):
        global steam_api
        global itad_api
        appID = steam_api.get_game_id_from_steam(text)
        prices = itad_api.get_prices(itad_api.get_plain(appID))
        recommend = steam_api.recommend_similar_games(appID, matchRate=0.5, cutoff=10, ratePower=0)
        #check = steam_api.save_game_data_to_cache()
        resultString = ""
        resultString += "Lowest Price in History: " + str(prices[0]) + "\n"
        resultString += "Current Prices: " + str(prices[1:]) + "\n\n"
        resultString += "Recommendations:  [ id, name, score ]\n"
        for r in recommend:
                resultString += str(r) + "\n"
        messagebox.showinfo("search command", resultString)
        
Search.SearchBox(root, command=get_game_rec, placeholder="Search for a game here").pack(pady=6, padx=3)

root.mainloop()

