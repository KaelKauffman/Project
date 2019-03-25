from tkinter import *
from tkinter import messagebox
from SteamSpy_API_Calls import SteamSpy_API_Caller
from ITAD_API_Calls import ITAD_API_Caller
from User import SteamUser
import Search

#API Call objects
steam_api = SteamSpy_API_Caller(appFile="SteamSpy_App_Cache.txt", tagFile="SteamSpy_Tags_Cache.txt")
itad_api = ITAD_API_Caller()

#User object
steam_user = SteamUser(userFile="User_Data_Cache.txt")

## Module to connect to public Steam profile 
def connect_to_steam():
        filewin = Toplevel(root)
        filewin.title("Connect to Steam.")
        
        #Have popup window follow parent object placement.
        x=root.winfo_rootx()
        y=root.winfo_rooty()
        geom="+%d+%d" % (x,y)
        filewin.geometry(geom)

        description ='Connect to your public Steam account here by entering your SteamID'
        Label(filewin, text=description).pack(padx=30, pady=3)
        steamID = Entry(filewin)
        steamID.pack(padx=3, pady=3, ipadx=10, ipady=4)

        def log_in():
                print(steamID.get())
                if steamID != "":
                        steam_user.loginSteamID(steamID.get())

        Button(filewin, text= "Login here", command=log_in).pack()

## Module to switch current user. 
def switch_user():
        filewin = Toplevel(root)
        filewin.title("Users")
        
        x=root.winfo_rootx()
        y=root.winfo_rooty()
        geom="+%d+%d" % (x,y)
        filewin.geometry(geom)
        #Suppose every account that ever login is stored in users
        users = steam_user.getAllUsers()
        def selection():
                u_id = users[var.get()][0]
                steam_user.loginSteamID(u_id)
                
        Label(filewin, text='Choose Your Account Below').pack()
        var=IntVar()
        var.set(1)
        row_num=0
        for user in users:
                r = Radiobutton(filewin, text=user[1], variable=var, value=row_num, command=selection)
                r.pack(anchor=W)
                row_num+=1
        # #Username and password labels
        # Label(filewin, text='Username').grid(row=0)
        # Label(filewin, text='Password').grid(row=1)

        # #Entry fields for username, password
        # e1 = Entry(filewin).grid(row=0,column=1, padx=3)
        # e2 = Entry(filewin, show='*').grid(row=1, column=1, padx=3)
        
        # #Keep user logged in
        # Checkbutton(filewin, text = "Keep Me Logged In").grid(columnspan=2)
        # #Submit
        # Button(filewin, text= "Login!", activebackground='pink1').grid(columnspan=2, pady=3)


# Return popup window of game recommendations given a game.
def get_game_rec(text):
        names_list = [x.strip() for x in text.split(",")]
        game_ids = []
        for name in names_list:
            g = steam_api.get_game_id_from_steam(name)
            if g != "999999999":
                game_ids.append(g)
           
        
        all_results = steam_api.recommend_multi_input(gameIDs=game_ids, required_genres=steam_api.getRequiredGenres(), banned_genres=[], banned_games=[], showTop=5, cross_thresh=2, matchRate=0.5, cutoff=10, ratePower=1, confPower=3)

        #check = steam_api.save_game_data_to_cache()
        resultString = ""
        resultString += "Cross-Recommendation Results:\n"
        for r in all_results[0]:
            resultString += str(r) + "\n"
        resultString += "\n"
        for results in all_results[1]:
            resultString += "Recommendations from " + results[1] + " (" + results[0] + "):\n"
            for r in results[2]:
                resultString += str(r) + "\n"
            resultString += "\n"
            
        messagebox.showinfo("search command", resultString)


## Module to generate game recommendations based on 2 parameters, by type or by name.
def generate_recommendation():
        genres = [('Action', 'Action'), ('Adventure', 'Adventure'), ('Casual', 'Casual'), ('Indie','Indie') , ('Massively Multiplayer', 'Massively'), ('Racing','Racing') ,
                  ('RPG', 'RPG'), ('Simulation', 'Simulation'), ('Sports','Sports'), ('Strategy','Strategy')]
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
                for genre in genres:
                        var = IntVar()
                        chk = Checkbutton(filewin1, text=genre[0], variable=var)
                        chk.grid(row=row_num, sticky=W)
                        row_num+=1
                        vars.append(var)
                def submit():
                        checks.clear()
                        count=0
                        for i in vars:
                                if i.get() == 1 and genres[count][1] not in checks:
                                        checks.append(genres[count][1])
                                count+=1
                        steam_api.setRequiredGenres(checks)

                def clear_checkbox():
                        for i in vars:
                                i.set(0)
                        checks.clear()
                        steam_api.setRequiredGenres(checks)
                
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

                Search.SearchBox(filewin2, command=get_game_rec, placeholder="Enter game name").pack(pady=6, padx=3)
                
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
        wishlist = [ steam_api.get_name(g_id) for g_id in steam_user.getDesiredGames() ]
        raw_prices = [ itad_api.get_prices(itad_api.get_plain(g_id)) for g_id in steam_user.getDesiredGames() ]
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


        filewin = Toplevel(root)
        filewin.title("Wishlist")

        x=root.winfo_rootx()
        y=root.winfo_rooty()
        geom="+%d+%d" % (x,y)
        filewin.geometry(geom)

        Label(filewin, text="Your wishlist is displayed below.", font=("", 10, "italic")).grid(pady=3, columnspan=4)
        row_num = 2
        for g in range(len(wishlist)):
                #Game name, price information, and current rating are displayed. Rating is optional.
                Label(filewin, text=wishlist[g], font="fixedsys 12 bold").grid(row=row_num, sticky=W, columnspan=4)
                Label(filewin, text="Current Steam Price: {}".format(revised_prices[g][0][1])).grid(row=row_num+1, columnspan=2, sticky=W, padx=8)
                Label(filewin, text="Lowest Price: {}".format(revised_prices[g][1][1])).grid(row=row_num+2, columnspan=2, sticky=W, padx=8)
                Label(filewin, text="Vendor: {}".format(revised_prices[g][1][0])).grid(row=row_num+3, columnspan=2, sticky=W, padx=12)
                Label(filewin, text="").grid(row=row_num+4, columnspan=4)

                row_num += 5

## Module to check price of one game.
def pricecheck():
        filewin = Toplevel(root)
        filewin.title("Price Check")

        x=root.winfo_rootx()
        y=root.winfo_rooty()
        geom="+%d+%d" % (x,y)
        filewin.geometry(geom)

        def command(text):
                app_id = steam_api.get_game_id_from_steam(text)
                prices = itad_api.get_prices(itad_api.get_plain(app_id))
                if len(prices) == 0:
                      resultString = "Game not found."
                else:            
                        resultString = "Prices for: " + text + "\n\n"
                        resultString += "Lowest Price in History:\n"
                        resultString += str(prices[0]) + "\n\n"
                        resultString += "Current Prices: \n"
                        for p in prices[1:]:
                             resultString += str(p) + "\n"
                             
                messagebox.showinfo("Search Results", resultString )

                
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

## View a game's information.
def see_game_info(text_):
        app_id = steam_api.get_game_id_from_steam(text_)
        name = "Game not found"
        hours = 0
        reviews = [0,0]
        genres = []
        tags = []

        if app_id != "999999999":
                name = steam_api.get_name(app_id)
                hours = steam_api.get_playtime(app_id)[0]
                reviews = steam_api.get_rating(app_id)
                genres = steam_api.get_genres(app_id)
                tags = steam_api.get_tags(app_id)
                if len(tags) > 3:
                        tags = tags[0:3]
        
        filewin = Toplevel(root)
        filewin.title(text_)

        x=root.winfo_rootx()
        y=root.winfo_rooty()
        geom="+%d+%d" % (x,y)
        filewin.geometry(geom)

        Label(filewin, text=name, font=("fixedsys", 26, "bold")).grid(padx=5, pady=3)
        Label(filewin, text="Game image here", fg='white', bg='black').grid(row=1,column=1, rowspan=5, padx=5, pady=2, ipady=40, sticky=W)
        Label(filewin, text="Avg Hours Played: {0:.2f}".format(hours)).grid(row=1, sticky=W)
        Label(filewin, text="Percentage Positive Reviews: {0:.2f}%".format(100*reviews[0])).grid(row=2, sticky=W)
        Label(filewin, text="Total Reviews: {}".format(reviews[1])).grid(row=3, sticky=W)
        Label(filewin, text="Genres: {}".format(str(genres))).grid(row=4, sticky=W)
        Label(filewin, text="Top-Voted Tags: {}".format(str(tags))).grid(row=5, sticky=W)
        Label(filewin, text="").grid(row=6)




#Create initial window.
root = Tk()
root.title("SteamRush")
root.geometry("800x600")
posRight = int(root.winfo_screenwidth()/2 - 800/2)
posDown = int(root.winfo_screenheight()/2 - 600/2)
root.geometry("+{}+{}".format(posRight, posDown))
root.configure(background='black')
make_menus()

#Show welcome message and home page graphics.
steam_icon = PhotoImage(file= "images/steam_icon.gif")
Label(root, bg='black', image=steam_icon).pack()
Label(root, text="Welcome to SteamRush!", font=("fixedsys", 26, "bold"), bg='black', fg='white').pack()

Search.SearchBox(root, command=see_game_info, placeholder="Search for a game here").pack(pady=6, padx=3)

root.mainloop()

