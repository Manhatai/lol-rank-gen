import tkinter
import customtkinter
import random as rd
from pyprobs import Probability as pr

rank_types = {"iron IV": 0, "iron III": 100, "iron II": 200, "iron I": 300, "bronze IV": 400, "bronze III": 500,
              "bronze II": 600, "bronze I": 700, "silver IV": 800, "silver III": 900, "silver II": 1000,
              "silver I": 1100, "gold IV": 1200, "gold III": 1300, "gold II": 1400, "gold I": 1500,
              "platinum IV": 1600, "platinum III": 1700, "platinum II": 1800, "platinum I": 1900,
              "emerald IV": 2000, "emerald III": 2100, "emerald II": 2200, "emerald I": 2300, "diamond IV": 2400,
              "diamond III": 2500, "diamond II": 2600, "diamond I": 2700}
game_count_prob = []
lp_total = []


# Input rangi
def rank_current():
    user_rank = rankInput.get()
    if (user_rank not in rank_types) or (isinstance(user_rank, str) == False):
        print("Rank not found")
        foundLabel.configure(text="Rank not found (example: gold IV)", text_color="red")
        return None
    else:
        print("Rank found!!!")
        foundLabel.configure(text="Rank found!", text_color="green")
        print(user_rank)
        return user_rank



# Input ilosci lp
def lp_count():
    try:
        user_lp = leaguePoints.get()
        user_lp = int(user_lp)
        if (user_lp > 99) or (user_lp < 0):
            print("Lp count invalid")
            foundLabel2.configure(text="Lp count invalid (should be 0 - 99)", text_color="red")
            return None
        else:
            print("Lp count is valid!")
            foundLabel2.configure(text="Lp count is valid!", text_color="green")
            return user_lp
    except ValueError:
        print("Lp count invalid")
        foundLabel2.configure(text="Lp count invalid (should be 0 - 99)", text_color="red")
        return None



# Input winratio
def winrate():
    try:
        wr = winrateInput.get()
        wr = int(wr)
        wr = (wr / 100)
        if (wr > 1) or (wr < 0):
            print("Invalid winrate value (should be 1 - 100)")
            foundLabel3.configure(text="Invalid winrate value (should be 1 - 100)", text_color="red")
            return None
        else:
            print("Winrate value is valid!")
            foundLabel3.configure(text="Winrate value is valid!", text_color="green")
            return wr
    except ValueError:
        print("Invalid winrate value (should be 1 - 100)")
        foundLabel3.configure(text="Invalid winrate value (should be 1 - 100)", text_color="red")
        return None


# Input games expected
def games_expected():
    try:
        games_expected = gamesExpected.get()
        games_expected = int(games_expected)
        foundLabel4.configure(root, text="Games expected value is valid!", text_color="green")
        print(games_expected)
        return games_expected
    except ValueError:
        foundLabel4.configure(root, text="Games expected value is invalid", text_color="red")
        return None


# "Enter desired rank" checkbox
def checkbox():
    if check_var.get() == "on":
        checkboxLabel.configure(text="Your desired rank cant be lower than exactly one rank up.", text_color="white")
        rankNewInput.pack()
    else:
        checkboxLabel.configure(text="")
        rankNewInput.delete(0, 'end')
        rankNewInput.pack_forget()


# Calculations in "Enter desired rank" textbox
def rankProb():
    rank1 = rankInput.get()
    rank2 = rankNewInput.get()
    if rank_types.get(rank2) < (rank_types.get(rank1) + 399):
        checkboxLabel.configure(text="Your desired rank cant be lower than exactly one rank up!", text_color="red")
    else:
        checkboxLabel.configure(text="Able to calculate!", text_color="green")


# Loop calculating the lp value (ranked games simulator)

def ranked_games(wr, games_expected):
    games = []
    lp = 0
    game_count = 0
    while True:
        result = pr.prob(wr)  # returns True or False based on "wr" value
        if result:
            lp += rd.randint(20, 25)  # +20lp / +25lp
        else:
            lp += rd.randint(-22, -18)  # -18lp / -22lp

        if check_var.get() == "on":
            if lp + rank_types[rank_current] >= rank_types[rankNew_var]:
                game_count_prob.append(game_count)
                break

        if game_count == games_expected:
            break

        games.append(lp)
        game_count += 1
    return lp


# Function calculating your final rank, passing it to rank_gained

def ranked_calculations(lp, user_lp):
    for i in range(1000):  # 1000 * "games_expected" samples
        lp_total.append(lp)
    result = sum(lp_total) / 1000
    result_whole = round(result)
    result_whole += user_lp + rank_types.get(rank_current)  # rank_current is the key bound to lp value
    return result_whole


# Function outputting your rank on the screen

def rank_gained(result_whole):
    rank_ranges = {(0, 99): "iron IV", (100, 199): "iron III", (200, 299): "iron II", (300, 399): "iron I",
                   (400, 499): "bronze IV", (500, 599): "bronze III", (600, 699): "bronze II",
                   (700, 799): "bronze I", (800, 899): "silver IV", (900, 999): "silver III",
                   (1000, 1099): "silver II", (1100, 1199): "silver I", (1200, 1299): "gold IV",
                   (1300, 1399): "gold III", (1400, 1499): "gold II", (1500, 1599): "gold I",
                   (1600, 1699): "platinum IV", (1700, 1799): "platinum III",
                   (1800, 1899): "platinum II", (1900, 1999): "platinum I", (2000, 2099): "emerald IV",
                   (2100, 2199): "emerald III", (2200, 2299): "emerald II", (2300, 2399): "emerald I",
                   (2400, 2499): "diamond IV", (2500, 2599): "diamond III",
                   (2600, 2699): "diamond II", (2700, 2799): "diamond I"}

    for (start, end), rank in rank_ranges.items():
        proper_lp_count = round(result_whole / 100)
        if start <= result_whole <= end:
            result_final = f"Your rank should be: {rank} {proper_lp_count}LP"
            return result_final
        if result_whole >= 2800:
            result_final = f"Your rank should be: master+ {proper_lp_count}LP"
            return result_final


def calculate_and_update():
    rank_current()
    lp_count()
    winrate()
    games_expected()
    rankProb()


# System settings
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# App frame
root = customtkinter.CTk()
root.geometry("720x780")
root.title("SoloQ Simulator")

# Rank input
title = customtkinter.CTkLabel(root, text="Enter your rank")
title.pack()
rank_var = tkinter.StringVar()
rankInput = customtkinter.CTkEntry(root, width=150, height=25, textvariable=rank_var)
rankInput.pack()
foundLabel = customtkinter.CTkLabel(root, text="")
foundLabel.pack()

# Lp count
title2 = customtkinter.CTkLabel(root, text="Enter your lp count (0 - 99)")
title2.pack()
lp_var = tkinter.StringVar()
leaguePoints = customtkinter.CTkEntry(root, width=150, height=25, textvariable=lp_var)
leaguePoints.pack()
foundLabel2 = customtkinter.CTkLabel(root, text="")
foundLabel2.pack()

# Winrate input
title3 = customtkinter.CTkLabel(root, text="Enter your winrate (1 - 100)")
title3.pack()
wr_var = tkinter.StringVar()
winrateInput = customtkinter.CTkEntry(root, width=150, height=25, textvariable=wr_var)
winrateInput.pack()
foundLabel3 = customtkinter.CTkLabel(root, text="")
foundLabel3.pack()

# Expected games input
title4 = customtkinter.CTkLabel(root, text="Enter how many games you want to play")
title4.pack()
games_var = tkinter.StringVar()
gamesExpected = customtkinter.CTkEntry(root, width=150, height=25, textvariable=games_var)
gamesExpected.pack()
foundLabel4 = customtkinter.CTkLabel(root, text="")
foundLabel4.pack()

# Yes/No checkbox
check_var = customtkinter.StringVar(value="off")
my_check = customtkinter.CTkCheckBox(root,
                                     text="Would you like to calculate how many games it would take to get to a certain rank?",
                                     variable=check_var, onvalue="on", offvalue="off", command=checkbox)
my_check.pack()
checkboxLabel = customtkinter.CTkLabel(root, text="")
checkboxLabel.pack()
rankNew_var = tkinter.StringVar()
rankNewInput = customtkinter.CTkEntry(root, width=150, height=25, textvariable=rankNew_var)

# Rank result output

title5 = customtkinter.CTkLabel(root, text=f"Your expected rank is: {rank_gained(result_whole=123)}")

# Calculate button
calculate = customtkinter.CTkButton(root, width=300, height=50, text="Calculate rank", font=("Roboto", 30),
                                    command=calculate_and_update)
calculate.pack(side="bottom", padx=100, pady=10)

# Run app
root.mainloop()
