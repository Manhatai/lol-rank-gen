import requests
from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()

api_key = os.getenv("API_KEY")

if not api_key:
    print("API key is missing. Make sure to set it in your environment variables.")
    exit()

# Summoners username and the region they play in
summoner_name = "Hi Im Misfit"
region = "eun1"  # Replace with the appropriate region

print(f"Summoner's name: {summoner_name}")

# Encode summoner name for the URL
encoded_summoner_name = urllib.parse.quote_plus(summoner_name.replace("#", "%23"))


# Define the API endpoint
base_url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{encoded_summoner_name}"
headers = {"X-Riot-Token": api_key}

try:
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        summoner_data = response.json()
        summoner_id = summoner_data['id']

        # Get the summoner's rank information
        rank_url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
        rank_response = requests.get(rank_url, headers=headers)

        if rank_response.status_code == 200:
            ranks = rank_response.json()

            # Extract rank information
            rank_data = [
                {
                    "Queue": rank["queueType"],
                    "Tier": rank.get("tier", "Unranked"),
                    "Rank": rank.get("rank", ""),
                    "LP": rank.get("leaguePoints", 0)
                }
                for rank in ranks
            ]

            print(rank_data)

        else:
            print(f"Error getting rank information: {rank_response.status_code}")
    else:
        print(f"Error getting summoner information: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")
