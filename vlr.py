import requests
import json
from bs4 import BeautifulSoup, Comment
import collections
from collections import OrderedDict
from datetime import datetime
from dateutil.parser import parse


def getPlayerStats(playerID):
    url = "https://www.vlr.gg/player/" + str(playerID) + "/?timespan=all"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    playerHeader = soup.find('div', class_ = "player-header")
    ign = playerHeader.find('h1').getText().strip()
    name = playerHeader.find('h2').getText().strip()

    agentSection = soup.find('table', class_="wf-table").find('tbody').find_all('tr')
    agentDict = {}

    for agent in agentSection:
        agentInfo = {}
        name = agent.findAll('td')[0].find('img')["alt"]
        pick = agent.findAll('td')[1].getText().strip()
        pick = pick[pick.index(")") + 1:].strip()
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

    mapSection = soup.find('div', class_ = "match-header-note")
    if(mapSection != None):
        mapText = mapSection.getText().strip()
        picksAndBans = mapText.split(";")
        for i in range(0, len(picksAndBans)):
            picksAndBans[i] = picksAndBans[i].strip()
    else:
        picksAndBans = ["None"]
    
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
    matchStats["PicksAndBans"] = picksAndBans
    matchStats["Maps"] = mapDetails

    return matchStats

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
    return matchStats

def loadPlayerData(players): #to help with getPlayerDataMatch
    playerStats = {}
    for player in players:
        playerDic = {}
        info = player.findAll('td')
        playerDic["name"] = player.find('div', class_ = "text-of").getText().strip().split()[0]
        playerDic["agent"] = player.find('img')["alt"]
        try:
            playerDic["rating"] = info[2].getText().strip().split()[0]
        except IndexError:
            playerDic["rating"] = "Not Available"
        playerDic["acs"] = info[3].getText().strip().split()[0]
        playerDic["kills"] = info[4].getText().strip().split()[0]
        playerDic["deaths"] = info[5].find('span', class_ = "side mod-both").getText().strip().split()[0]
        playerDic["assists"] = info[6].getText().strip().split()[0]
        playerDic["kdDiff"] = info[7].getText().strip().split()[0]
        try:
            playerDic["kast"] = info[8].getText().strip().split()[0]
        except IndexError:
            playerDic["kast"] = "Not Available"
        playerDic["adr"] = info[9].getText().strip().split()[0]
        playerDic["hsPercent"] = info[10].getText().strip().split()[0]
        playerDic["firstKills"] = info[11].getText().strip().split()[0]
        playerDic["firstDeaths"] = info[12].getText().strip().split()[0]
        playerDic["fkDiff"] = info[13].getText().strip().split()[0]

        playerStats[playerDic["name"]] = playerDic
    return playerStats

def updateMatchDatabase():
    matches = OrderedDict()

    url = "https://www.vlr.gg/matches/results"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    pages = soup.find('div', class_ = "action-container-pages").findAll('a')
    numTotalPages = int(pages[3].getText().strip())

    format_string = "%a, %B %d, %Y" #For Datetime conversion

    with open('matchesDatabase.json', 'r') as openfile:
        matches = json.load(openfile)
        matches = collections.OrderedDict(matches)
    
    secondToLatestDay = list(matches.keys())[1]

    matches[list(matches.keys())[0]] = {} #Clear latest day in matches

    beforesecondToLatestDay = True

    for i in range(1, numTotalPages + 1): #Loop through every page
        url = "https://www.vlr.gg/matches/results/?page=" + str(i)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        page = soup.find('div', class_ = "col mod-1")
        datesInPage = page.findAll('div', class_ = "wf-label mod-large")
        matchesInPage = page.findAll('div', class_ = "wf-card")
        
        for i in range(1, len(datesInPage) + 1): #Loop through all dates in page
            date = datesInPage[i - 1].getText().strip()
            
            #Strips extra text from dates
            if("Today" in date):                    
                date = date[:date.index("\n") - 1]
            elif("Yesterday" in date):  
                date = date[:date.index("\n") - 1]

            dateObj = datetime.strptime(date, format_string)
            dateObj = dateObj.strftime("%Y-%m-%d")

            #Loop until hit secondToLatestDay
            if(dateObj == secondToLatestDay):
                beforesecondToLatestDay = False
                break     

            matchesInDate = matchesInPage[i].findAll('a')
            
            matchOfDay = 0
            dayMatches = {}

            for match in matchesInDate: #Loop through matches in the date
                matchDetails = {}

                #Get all details to store
                matchUrl = match['href']
                matchId = matchUrl[1:matchUrl.find("/", matchUrl.find("/") + 1)]

                teamA = match.findAll('div', class_ = "text-of")[0].getText().strip().upper()
                teamB = match.findAll('div', class_ = "text-of")[1].getText().strip().upper()

                eventText = match.find('div', class_ = "match-item-event text-of").getText().strip()
                mainEvent = eventText[eventText.index("\t"):].strip().upper()
                subEvent = eventText[:eventText.index("\t")].strip().upper()
                
                matchDetails['ID'] = matchId
                matchDetails[teamA] = teamA
                matchDetails[teamB] = teamB
                matchDetails['Team1'] = teamA
                matchDetails['Team2'] = teamB
                matchDetails['Event'] = mainEvent
                matchDetails['matchInEvent'] = subEvent
                matchDetails['Date'] = dateObj

                #If date already exists in matches then do not override it
                #This is to deal with matches from the same day that stretch over two pages
                if(dateObj in matches):                              
                    numMatches = (len(matches[dateObj]) - 1)
                    matches[dateObj][numMatches + 1] = matchDetails
                
                else:
                    dayMatches[matchOfDay] = matchDetails
                    matchOfDay += 1
                    matches[dateObj] = dayMatches

            matches.move_to_end(dateObj, last = True)

        #Sort matches by date and write to file
        matches = OrderedDict(sorted(matches.items(), key = lambda x: parse(x[0]), reverse = True))
        with open("matchesDatabase.json", "w") as outfile:
            json.dump(matches, outfile)

        #Loop beforesecondToLatestDay no longer true 
        if(beforesecondToLatestDay == False):
            break    

def searchMatchDatabase(**kwargs):
    with open('matchesDatabase.json', 'r') as openfile:
        matches = json.load(openfile)
        matches = collections.OrderedDict(matches)

    validFilters = OrderedDict()
    for arg in kwargs:
        if kwargs[arg] != None:
            validFilters[arg] = kwargs[arg]         

    results = []
    for date in matches:
        for match in matches[date]:
            valid = True
            for key, value in validFilters.items():
                if matches[date][match][key] != value.upper():
                    valid = False
                    break
            if valid:
                results.append(matches[date][match])
    return results


def search(query, type):
    #Accepted types are all, teams, players, events, series
    url = "https://www.vlr.gg/search/?q=" + query + "&type=" + type

    results = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    toDelete = soup.find('div', class_ = 'wf-card mod-dark')
    toDelete.decompose()
    res = soup.find('div', class_ = 'wf-card').findAll('a', href = True)

    i = 0
    for item in res:
        link = item['href']
        title = item.find('div', class_ = 'search-item-title').getText().strip()
        title = title.replace("\t","").replace("\n", "")
        description = item.find('div', class_ = 'search-item-desc')

        if(description != None):
            description = description.getText().strip()
            description = description.replace("\t", "").replace("\n", "")
        else:
            description = "None"
            
        imageLink = item.find('img')['src']
        results[i] = {
            "title": title,
            "description": description,
            "link": link,
            "imageLink": imageLink
        }
        i += 1
    return results