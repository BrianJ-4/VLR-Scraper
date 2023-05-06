import requests
from bs4 import BeautifulSoup

def getVCTPlayers(minRounds = 200, agent = "all", mapid = "all", timespan = 60):
    minRounds = str(minRounds)
    timespan = str(timespan)
    mapid = str(mapid)
    url = "https://www.vlr.gg/stats/?event_group_id=all&event_id=1189&series_id=all&region=all&country=all&min_rounds=" + minRounds + "&min_rating=1550&agent=" + agent + "&map_id=" + mapid + "&timespan=" + timespan + "d"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    #print(url)

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
    #print(ign + "\n" + name)
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

def getLiveMatches(): #Scrapes vlr homepage to get live matches and their stats
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

def getMatchStats(matchID): #returns a dictionary of the stats of match given by id
    matchStats = {}
    url = "https://www.vlr.gg/" + str(matchID)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    mainHeader = soup.find('div', class_ = "match-header-vs")

    teamAName = mainHeader.find('div', class_ = "match-header-link-name mod-1").findAll('div')[0].getText().strip()
    teamBName = mainHeader.find('div', class_ = "match-header-link-name mod-2").findAll('div')[0].getText().strip()

    teamAScore = int(mainHeader.find('div', class_ = "js-spoiler").findAll('span')[0].getText().strip())
    teamBScore = int(mainHeader.find('div', class_ = "js-spoiler").findAll('span')[2].getText().strip())
    
    winner = ""
    if(teamAScore > teamBScore):
        winner = teamAName
        loser = teamBName
    else:
        winner = teamBName
        loser = teamAName

    superHeader = soup.find('div', class_ = "match-header-super")
    mainEvent = superHeader.find('a').find('div').findAll('div')[0].getText().strip()
    eventSubtext = superHeader.find('a').find('div').findAll('div')[1].getText().strip()
    eventSubtext = eventSubtext.replace("\t", "")
    eventSubtext = eventSubtext.replace("\n", "")

    statsContainer = soup.find('div', class_ = "vm-stats-container").findAll('div', class_ = "vm-stats-game")
    mapDetails = getPlayerDataMatch(statsContainer, teamAName, teamBName)
    
    matchStats["Event"] = mainEvent
    matchStats["eventDetail"] = eventSubtext
    matchStats["Teams"] = teamAName + " vs " + teamBName
    matchStats["teamA"] = teamAName
    matchStats["teamB"] = teamBName
    matchStats["scoreA"] = teamAScore
    matchStats["scoreB"] = teamBScore
    matchStats["Winner"] = winner
    matchStats["Loser"] = loser
    matchStats["Maps"] = mapDetails

def getPlayerDataMatch(statsContainer, teamAName, teamBName): #to help with getMatchStats
    matchStats = {}
    for game in statsContainer:
        mapDetails = {}
        if(not 'mod-active' in game['class']):
            mapName = game.find('div', class_ = "map").getText().strip().split()[0]
            mapDetails["rndsA"] = game.findAll('div', class_ = "score")[0].getText().strip().split()[0]
            mapDetails["rndsB"] = game.findAll('div', class_ = "score")[1].getText().strip().split()[0]
            mapDetails["TrndsA"] = game.findAll('span', class_ = "mod-t")[0].getText().strip()
            mapDetails["TrndsB"] = game.findAll('span', class_ = "mod-t")[1].getText().strip()
            mapDetails["CTrndsA"] = game.findAll('span', class_ = "mod-ct")[0].getText().strip()
            mapDetails["CTrndsB"] = game.findAll('span', class_ = "mod-ct")[1].getText().strip()

            playerTables = game.findAll('tbody')
            mapDetails[teamAName] = loadPlayerData(playerTables[0].findAll('tr'))
            mapDetails[teamBName] = loadPlayerData(playerTables[1].findAll('tr'))

            matchStats[mapName] = mapDetails
    print(matchStats)

def loadPlayerData(players): #to help with getPlayerDataMatch
    playerStats = {}
    for player in players:
        playerDic = {}
        info = player.findAll('td')
        playerDic["name"] = player.find('div', class_ = "text-of").getText().strip().split()[0]
        playerDic["agent"] = player.find('img')["alt"]
        playerDic["rating"] = info[2].getText().strip().split()[0]
        playerDic["acs"] = info[3].getText().strip().split()[0]
        playerDic["kills"] = info[4].getText().strip().split()[0]
        playerDic["deaths"] = info[5].find('span', class_ = "side mod-both").getText().strip().split()[0]
        playerDic["assists"] = info[6].getText().strip().split()[0]
        playerDic["kdDiff"] = info[7].getText().strip().split()[0]
        playerDic["kast"] = info[8].getText().strip().split()[0]
        playerDic["adr"] = info[9].getText().strip().split()[0]
        playerDic["hsPercent"] = info[10].getText().strip().split()[0]
        playerDic["firstKills"] = info[11].getText().strip().split()[0]
        playerDic["firstDeaths"] = info[12].getText().strip().split()[0]
        playerDic["fkDiff"] = info[13].getText().strip().split()[0]

        playerStats[playerDic["name"]] = playerDic
    return playerStats



                    



                    



