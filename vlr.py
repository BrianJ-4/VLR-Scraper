import requests
from bs4 import BeautifulSoup

def getVCTPlayers(minRounds = 200, agent = "all", mapid = "all", timespan = 60):
    minRounds = str(minRounds)
    timespan = str(timespan)
    mapid = str(mapid)
    url = "https://www.vlr.gg/stats/?event_group_id=all&event_id=1189&series_id=all&region=all&country=all&min_rounds=" + minRounds + "&min_rating=1550&agent=" + agent + "&map_id=" + mapid + "&timespan=" + timespan + "d"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(url)

    players = []
    


getVCTPlayers(minRounds = 0, agent = "Skye")