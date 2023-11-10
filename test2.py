import requests


api_key = "RGAPI-fb20c0a7-f9ae-4738-8aea-adafd61427b6"

# Summoner's username and the region they play in
summoner_name = "Hi Im Misfit"
region = "eun1"  # Replace with the appropriate region

print(f"Summoners name: {summoner_name}")


# Define the API endpoint
base_url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
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
            for rank in ranks:
                print(f"Queue: {rank['queueType']}, Tier: {rank['tier']} {rank['rank']}, LP: {rank['leaguePoints']}")
        else:
            print(f"Error getting rank information: {rank_response.status_code}")
    else:
        print(f"Error getting summoner information: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")