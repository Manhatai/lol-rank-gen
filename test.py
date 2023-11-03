import tkinter
import customtkinter
import random as rd
from pyprobs import Probability as pr

# App frame
root = customtkinter.CTk()
root.geometry("720x780")
root.title("SoloQ Simulator")

# System settings
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


rank_types = {"iron IV": 0, "iron III": 100, "iron II": 200, "iron I": 300, "bronze IV": 400, "bronze III": 500,
              "bronze II": 600, "bronze I": 700, "silver IV": 800, "silver III": 900, "silver II": 1000,
              "silver I": 1100, "gold IV": 1200, "gold III": 1300, "gold II": 1400, "gold I": 1500,
              "platinum IV": 1600, "platinum III": 1700, "platinum II": 1800, "platinum I": 1900,
              "emerald IV": 2000, "emerald III": 2100, "emerald II": 2200, "emerald I": 2300, "diamond IV": 2400,
              "diamond III": 2500, "diamond II": 2600, "diamond I": 2700}
game_count_prob = []
lp_total = []


# Class doing all the work
class Calculations():
    def __init__(self):
        self.user_rank = None
        self.user_lp = None
        self.wr = None
        self.games_expected = None
        self.lp = None
        self.result_whole = None
        self.result_final = None

    # Rank input (class)
    def rank_current(self):
        user_rank = rankInput.get()
        if (user_rank not in rank_types) or (isinstance(user_rank, str) == False):
            print("Rank not found")
            foundLabel.configure(text="Rank not found (example: gold IV)", text_color="red")
        else:
            print("Rank found!!!")
            foundLabel.configure(text="Rank found!", text_color="green")
            print(f"Users rank: {user_rank}")
            self.user_rank = user_rank

    # Lp count input (class)
    def lp_count(self):
        try:
            user_lp = leaguePoints.get()
            user_lp = int(user_lp)
            if (user_lp > 99) or (user_lp < 0):
                print("Lp count invalid")
                foundLabel2.configure(text="Lp count invalid (should be 0 - 99)", text_color="red")
            else:
                print("Lp count is valid!")
                foundLabel2.configure(text="Lp count is valid!", text_color="green")
                print(f"Users lp count: {user_lp}")
                self.user_lp = user_lp
        except (ValueError, KeyError):
            print("Lp count invalid")
            foundLabel2.configure(text="Lp count invalid (should be 0 - 99)", text_color="red")


    # Winrate input (class)
    def winrate(self):
        try:
            wr = winrateInput.get()
            wr = int(wr)
            wr = (wr / 100)
            if (wr > 1) or (wr < 0):
                print("Invalid winrate value (should be 1 - 100)")
                foundLabel3.configure(text="Invalid winrate value (should be 1 - 100)", text_color="red")
            else:
                print("Winrate value is valid!")
                foundLabel3.configure(text="Winrate value is valid!", text_color="green")
                print(f"Users winrate: {wr}")
                self.wr = wr
        except (ValueError, KeyError):
            print("Invalid winrate value (should be 1 - 100)")
            foundLabel3.configure(text="Invalid winrate value (should be 1 - 100)", text_color="red")

    # Input games expected (class)
    def set_games_expected(self):
        try:
            games_expected = gamesExpected.get()
            games_expected = int(games_expected)
            foundLabel4.configure(root, text="Games expected value is valid!", text_color="green")
            print(f"Number of games user expects to play: {games_expected}")
            self.games_expected = games_expected
        except (ValueError, KeyError):
            foundLabel4.configure(root, text="Games expected value is invalid", text_color="red")

    # Loop calculating the lp value (ranked games simulator) (class)
    def ranked_games(self):
        games = []
        lp = 0
        game_count = 0
        while True:
            result = pr.prob(self.wr)  # returns True or False based on "wr" value
            if result:
                lp += rd.randint(20, 25)  # +20lp / +25lp
            else:
                lp += rd.randint(-22, -18)  # -18lp / -22lp

            if check_var.get() == "on":
                self.games_expected = 10000
                if lp + rank_types[self.user_rank] >= rank_types[rankNewInput.get()]:
                    game_count_prob.append(game_count)
                    break

            if game_count == self.games_expected:
                break

            games.append(lp)
            game_count += 1
        self.lp = lp

    # Function calculating your final rank, passing it to rank_gained (class)
    def ranked_calculations(self):
        for i in range(1000):  # 1000 * "games_expected" samples
            self.ranked_games()
            lp_total.append(self.lp)

        result = sum(lp_total) / 1000
        result_whole = round(result)
        result_whole += self.user_lp + rank_types.get(self.user_rank)
        self.result_whole = result_whole

    # Function outputting your rank on the screen (class)
    def rank_gained(self):
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
            proper_lp_count = round(self.result_whole / 100)
            if start <= self.result_whole <= end:
                result_final = f"Your rank should be: {rank} {proper_lp_count}LP"
                print(result_final)
                self.result_final = result_final
            if self.result_whole >= 2800:
                result_final = f"Your rank should be: master+ {proper_lp_count}LP"
                print(result_final)
                self.result_final = result_final

    # Clears all lists everytime the class instance is called (class)
    def clear(self):
        game_count_prob.clear()
        lp_total.clear()


calculations = Calculations()


# "Enter desired rank" checkbox
def checkbox():
    if check_var.get() == "on":
        gamesExpected.configure(state="disabled")
        title5.forget()
        title6.pack()
        checkboxLabel.configure(text="Your desired rank cant be lower than exactly one rank up.",
                                text_color="white")
        rankNewInput.pack()
    else:
        gamesExpected.configure(state="normal")
        title5.pack()
        title6.forget()
        checkboxLabel.configure(text="")
        rankNewInput.delete(0, 'end')
        rankNewInput.pack_forget()



# Calculations in "Enter desired rank" textbox
def rankProb():
    if check_var.get() == "on":
        rank1 = rankInput.get()
        rank2 = rankNewInput.get()
        diff1 = rank_types.get(rank1)
        diff2 = rank_types.get(rank2)
        if diff2 < (diff1 + 399):
            checkboxLabel.configure(text="Your desired rank cant be lower than exactly one rank up!", text_color="red")
        else:
            checkboxLabel.configure(text="Able to calculate!", text_color="green")




# Gives "Calculate rank" button the data it needs
def calculate_and_update():
    calculations.rank_current()
    calculations.lp_count()
    calculations.winrate()
    calculations.set_games_expected()
    calculations.ranked_games()
    calculations.ranked_calculations()
    calculations.rank_gained()
    checkbox()
    rankProb()
    result_final = calculations.result_final
    title5.configure(text=f"{result_final}")
    if check_var.get() == "on":
        title5.configure(text="")
        title6.configure(
            text=f"Games needed to reach the desired rank ({rankNewInput.get()}): {round((sum(game_count_prob)) / len(game_count_prob))}")
    else:
        title6.configure(text="")
    calculations.clear()


# Rank input (app)
title = customtkinter.CTkLabel(root, text="Enter your rank:", font=("Roboto", 16))
title.pack(pady=5)
rank_var = tkinter.StringVar()
rankInput = customtkinter.CTkEntry(root, width=150, height=25, textvariable=rank_var)
rankInput.pack()
foundLabel = customtkinter.CTkLabel(root, text="")
foundLabel.pack()

# Lp count (app)
title2 = customtkinter.CTkLabel(root, text="Enter your lp count (0 - 99):", font=("Roboto", 16))
title2.pack(pady=5)
lp_var = tkinter.StringVar()
leaguePoints = customtkinter.CTkEntry(root, width=150, height=25, textvariable=lp_var)
leaguePoints.pack()
foundLabel2 = customtkinter.CTkLabel(root, text="")
foundLabel2.pack()

# Winrate input (app)
title3 = customtkinter.CTkLabel(root, text="Enter your winrate (1 - 100):", font=("Roboto", 16))
title3.pack(pady=5)
wr_var = tkinter.StringVar()
winrateInput = customtkinter.CTkEntry(root, width=150, height=25, textvariable=wr_var)
winrateInput.pack()
foundLabel3 = customtkinter.CTkLabel(root, text="")
foundLabel3.pack()

# Expected games input (app)
title4 = customtkinter.CTkLabel(root, text="Enter how many games you want to play:", font=("Roboto", 16))
title4.pack(pady=5)
games_var = tkinter.StringVar()
gamesExpected = customtkinter.CTkEntry(root, width=150, height=25, textvariable=games_var)
gamesExpected.pack()
foundLabel4 = customtkinter.CTkLabel(root, text="")
foundLabel4.pack()

# Yes/No checkbox (app)
check_var = customtkinter.StringVar(value="off")
my_check = customtkinter.CTkCheckBox(
    root,
    text="Would you like to calculate how many games it would take to get to a certain rank?",
    variable=check_var,
    onvalue="on",
    offvalue="off",
    command=checkbox,
    font=("Roboto", 16)
)

my_check.pack()
checkboxLabel = customtkinter.CTkLabel(root, text="")
checkboxLabel.pack()
rankNew_var = tkinter.StringVar()
rankNewInput = customtkinter.CTkEntry(root, width=150, height=25, textvariable=rankNew_var)

# Rank result output (app)
title5 = customtkinter.CTkLabel(root, text="")
title5.pack(padx=10, pady=10)


# Average games to achieve x rank output (app)
title6 = customtkinter.CTkLabel(root, text="")


# Calculate button (app)
calculate = customtkinter.CTkButton(root, width=300, height=50, text="Calculate rank", font=("Roboto", 30),
                                    command=calculate_and_update)
calculate.pack(side="bottom", padx=100, pady=10)

# Run app
root.mainloop()
