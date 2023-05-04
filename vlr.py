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

    playerList = []
    players = soup.find('table', class_ = "wf-table mod-stats mod-scroll").find('tbody').find_all('tr')
    
    for player in players:
        name = player.find('div', class_ = "text-of").getText().strip()
        playerList.append(name)
    return playerList

def getPlayerStats(playerID):
    url = "https://www.vlr.gg/player/" + str(playerID)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    playerHeader = soup.find('div', class_ = "player-header")
    ign = playerHeader.find('h1').getText().strip()
    name = playerHeader.find('h2').getText().strip()
    print(ign + "\n" + name)
    agentSection = soup.find('table', class_="wf-table").find('tbody').find_all('tr')
    agentDict = {}
    # agentInfo = {
    #     # "name": "",
    #     # "pick": "",
    #     # "rnds": "",
    #     # "acs": "",
    #     # "kd": "",
    #     # "adr": "",
    #     # "kast": "",
    #     # "kpr": "",
    #     # "apr": "",
    #     # "fkpr": "",
    #     # "fdpr": "",
    #     # "kills": "",
    #     # "deaths": "",
    #     # "assists": "",
    #     # "fk": "",
    #     # "fd": ""
    # }
    for agent in agentSection:
        agentInfo = {}
        name = agent.findAll('td')[0].find('img')["alt"]
        pick = agent.findAll('td')[1].getText().strip()[3:].strip()
        rnds = agent.findAll('td')[2].getText().strip()
        rating = agent.findAll('td')[3].getText().strip()
        acs = agent.findAll('td')[4].getText().strip()
        kd = agent.findAll('td')[5].getText().strip()
        adr = agent.findAll('td')[6].getText().strip()
        kast = agent.findAll('td')[7].getText().strip()
        kpr = agent.findAll('td')[8].getText().strip()
        apr = agent.findAll('td')[9].getText().strip()
        fkpr = agent.findAll('td')[10].getText().strip()
        fdpr = agent.findAll('td')[11].getText().strip()
        kills = agent.findAll('td')[12].getText().strip()
        deaths = agent.findAll('td')[13].getText().strip()
        assists = agent.findAll('td')[14].getText().strip()
        fk = agent.findAll('td')[15].getText().strip()
        fd = agent.findAll('td')[16].getText().strip()
        fkfdDiff = int(fk) - int(fd)
        
        agentInfo["Pick"] = pick
        agentInfo["Rounds"] = rnds
        agentInfo["Rating"] = rating
        agentInfo["ACS"] = acs
        agentInfo["KD"] = kd
        agentInfo["ADR"] = adr
        agentInfo["KAST"] = kast
        agentInfo["KPR"] = kpr
        agentInfo["APR"] = apr
        agentInfo["FKPR"] = fkpr
        agentInfo["FDPR"] = fdpr
        agentInfo["Kills"] = kills
        agentInfo["Deaths"] = deaths
        agentInfo["Assists"] = assists
        agentInfo["FK"] = fk
        agentInfo["FD"] = fd
        agentInfo["FkFdDiff"] = fkfdDiff


        agentDict[name] = agentInfo
        return agentDict

def getLiveMatches():
    liveMatches = {}
    tempMatch = {}
    url = "https://www.vlr.gg"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    matches = soup.find('div', class_ = "wf-module wf-card mod-home-matches").find_all('a')

    for match in matches:
        tempMatch = {}
        if(match.find('div', class_ = "h-match-eta mod-live")):
            tempMatch["teamA"] = match.findAll('div', class_ = "h-match-team-name")[0].getText().strip()
            tempMatch["teamB"] = match.findAll('div', class_ = "h-match-team-name")[1].getText().strip()
            tempMatch["teamAMaps"] = match.findAll('div', class_ = "h-match-team-score mod-count js-spoiler")[0].getText().strip()
            tempMatch["teamBMaps"] = match.findAll('div', class_ = "h-match-team-score mod-count js-spoiler")[1].getText().strip()
            
            if(match.find('div', class_ = "h-match-team-rounds js-spoiler")):
                tempMatch["currMapRndsA"] = match.findAll('div', class_ = "h-match-team-rounds js-spoiler")[0].getText().strip()
                tempMatch["currMapRndsB"] = match.findAll('div', class_ = "h-match-team-rounds js-spoiler")[1].getText().strip()
            else:
                tempMatch["currMapRndsA"] = 0
                tempMatch["currMapRndsB"] = 0

            liveMatches[tempMatch["teamA"] + " vs " + tempMatch["teamB"]] = tempMatch
    return liveMatches
