from tkinter import *
import os

def connect_to_steam():
	filewin = Toplevel(root)
	filewin.title("Connect to Steam.")
	filewin.geometry("400x300")

	Label(filewin, text='Connect to your public Steam account here.').pack(padx=30, pady=30)
	Button(filewin, text= "Login here").pack()

def switch_user():
	filewin = Toplevel(root)
	filewin.title("Change User")

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
	

	# Attempts to make a drop down list for login, currently not working.

	# Label(filewin, text='Select from available accounts below.').pack(padx=30, pady=30)
	# mainframe = Frame(filewin)
	# mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
	# mainframe.columnconfigure(0, weight = 1)
	# mainframe.rowconfigure(0, weight = 1)
	# mainframe.pack(pady = 100, padx = 100)

	# tkvar = StringVar(filewin)
	# choices = { " ----- ", "Michelle Zhou", "Yaoyu Cheng"}
	# tkvar.set(" ----- ")

	# dropdown = OptionMenu(mainframe, tkvar, *choices)
	# dropdown.grid(row=2, column=1)

def generate_recommendation():
	TYPES = ['Action', 'Adventure', 'Casual', 'Indie', 'Massively Multiplayer', 'Racing', 'RPG', 'Simulation', 'Sports', 'Strategy']
	def types():
		filewin1 = Toplevel(filewin)
		filewin1.title("Recommend by Types")
		vars=[]
		for type in TYPES:
			var = IntVar()
			chk = Checkbutton(filewin1, text=type, variable=var)
			chk.pack(side=LEFT, anchor=W, expand=YES)
			vars.append(var)
		Button(filewin1, text="Submit", command=submit).pack(side=RIGHT)
		Button(filewin1, text="Clear", command=clear).pack(side=RIGHT)


	def names():
		os.system('python3 Search.py')
	filewin = Toplevel(root)
	filewin.title("Game Recommendation")
	type_button = Button(filewin, text="Recommend by Types", width=20, command=types)
	type_button.grid(row=0,column=0)
	name_button = Button(filewin, text="Recommend by Names", width=20, command=names)
	name_button.grid(row=0, column=1)

def search_game():
	os.system('python3 Search.py')

def wishlist():
	Label(root, text="See wishlist").pack()

def gamewatch():
	os.System("pyhon3 Search.py")

def rank_by_account_value():
	Label(root, text="See rankings by account value").pack()

def rank_by_account_level():
	Label(root, text="See rankings by account level").pack()

def submit():
	Label(root, text="Submit Succeed!").pack()

def clear():
	Label(root, text="Clear Succeed!").pack()

def make_menus():
	menu = Menu(root)
	root.config(menu=menu)

	user_menu = Menu(menu, tearoff=0)
	user_menu.add_command(label="Connect to Steam", command=connect_to_steam)
	user_menu.add_command(label="Change local user", command=switch_user)
	user_menu.add_separator()
	user_menu.add_command(label="Quit", command=root.quit)
	menu.add_cascade(label="User", menu=user_menu)

	gamerec_menu = Menu(menu, tearoff=0)
	menu.add_cascade(label="Game", menu=gamerec_menu)
	gamerec_menu.add_command(label="Recommendation", command=generate_recommendation)
	gamerec_menu.add_command(label="Search", command=search_game)

	pricewarch_menu = Menu(menu, tearoff=0)
	menu.add_cascade(label="PriceWatch", menu=pricewarch_menu)
	pricewarch_menu.add_command(label="Wishlist", command=wishlist)
	pricewarch_menu.add_command(label="Gamewatch", command=gamewatch)

	ranking_menu = Menu(menu, tearoff=0)
	menu.add_cascade(label="Ranking", menu=ranking_menu)
	ranking_menu.add_command(label="By account value", command=rank_by_account_value)
	ranking_menu.add_command(label="By account level", command=rank_by_account_level)


root = Tk()
root.title("SteamRush")
root.geometry("800x600")
make_menus()
root.mainloop()