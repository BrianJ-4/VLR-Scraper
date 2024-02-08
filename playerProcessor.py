#----------------------------------------------------------------------------------------------------------------
#   playerProcessor.py
#       - Processes player pages and gives info
#       - Currently gives...
#           - Player Name
#           - Player Real Name (When Available)
#           - Player Image Link
#           - Country
#           - Socials (When Available)
#           - Winnings
#           - Team
#           - Team Link
#           - Team Image Link
#           - Team Joined Date
#           - Past Teams
#               - Team Name
#               - Duration
#               - Status
#               - Team Image Link
#           - Agent Stats by time range
#           - Recent Results
#
#   2/8/2024 
#       - Created
#       - Added all features listed above
#----------------------------------------------------------------------------------------------------------------
import requests 
import json
import re
from bs4 import BeautifulSoup, Comment

def getPlayerPage(playerID):
    url = "https://www.vlr.gg/player/" + str(playerID)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    playerHeader = soup.find('div', class_ = 'player-header')
    playerImageLink = playerHeader.find('img')['src']
    if 'owcdn' not in playerImageLink : playerImageLink = 'https://vlr.gg' + playerImageLink
    playerIGN = playerHeader.find('h1').getText().strip()
    playerName = playerHeader.find('h2').getText().strip()
    country = playerHeader.find('div', class_ = 'ge-text-light').getText().strip()

    socials = playerHeader.findAll('a', href = True)
    playerSocials = {}
    for social in socials:
        socialName = social.getText().strip()
        socialLink = social['href']
        if socialName != "" : playerSocials[socialName] = socialLink

    teamContainers = soup.find('div', class_ = 'player-summary-container-1').findAll('div', class_ = 'wf-card')
    teamLink = teamContainers[1].find('a')['href']
    teamImageLink = teamContainers[1].find('img')['src']
    team = teamContainers[1].getText().strip()
    team = team.split('\n')
    teamName = re.sub(r'\s+', ' ', team[0])
    joined = re.sub(r'\s+', ' ', team[5]).strip()

    try:
        pastTeams = getPastTeams(teamContainers[2])
    except IndexError:
        pastTeams = {}

    winnings = soup.find('div', class_ = 'player-summary-container-2').find('span', style = True).getText().strip()

    playerStats = {
        'playerIGN' : playerIGN,
        'playerName' : playerName,
        'playerImageLink' : playerImageLink,
        'country' : country,
        'socials' : playerSocials,
        'winnings' : winnings,
        'teamName' : teamName,
        'teamLink' : teamLink,
        'teamImageLink' : teamImageLink,
        'joined' : joined,
        'pastTeams' : pastTeams
    }
    return playerStats
    
def getPlayerAgentStats(playerID, timespan):
    url = "https://www.vlr.gg/player/" + str(playerID) + "/?timespan=" + timespan
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

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
        agentInfo["FkFdDiff"] = str(fkfdDiff)
        agentDict[name] = agentInfo
    return agentDict

def getPlayerMatchResults(playerID, page):
    url = "https://www.vlr.gg/player/matches/" + str(playerID) + "/?page=" + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    allResults = soup.find('div', class_ = 'mod-dark').findAll('div', recursive = False)
    results = {}
    i = 0
    for result in allResults:
        resultStats = {}
        resultLink = result.find('a')['href']
        eventText = result.find('div', class_ = 'm-item-event text-of').getText().strip()
        eventText = eventText.split('\n', 1)
        event = eventText[0].strip('\t')
        matchInEvent = re.sub(r'\s+', ' ', eventText[1]).replace('⋅', '-')
        eventImageLink = result.find('div', class_ = 'fc-flex m-item-thumb').find('img')['src']
        playerTeam, opponentTeam = [tag.getText().strip() for tag in result.findAll('span', class_='m-item-team-tag')]
        teamScore = result.find('div', class_ = 'm-item-result').findAll('span')[0].getText().strip()
        opponentScore = result.find('div', class_ = 'm-item-result').findAll('span')[1].getText().strip()
        date = result.find('div', class_ = 'm-item-date').find('div').getText().strip()
        resultStats = {
            "resultLink" : resultLink,
            "event" : event,
            "matchInEvent" : matchInEvent,
            "eventImageLink" : eventImageLink,
            "playerTeam" : playerTeam,
            "opponentTeam" : opponentTeam,
            "teamScore" : teamScore,
            "opponentScore" : opponentScore,
            "date" : date
        }
        results[i] = resultStats
        i += 1
    return results

def getPastTeams(teamContainer):
    pastTeams = {}
    teams = teamContainer.findAll('a')
    i = 0
    for team in teams:
        teamImageLink = team.find('img')['src']
        textDivs = team.findAll('div', recursive = False)[1].findAll('div')
        texts = []
        for div in textDivs:
            text = div.getText().strip()
            if(text != ""):
                texts.append(text)
        if(len(texts) == 3):
            pastTeams[i] = {
                'team' : texts[0],
                'status' : texts[1],
                'duration' : texts[2],
                'imageLink' : teamImageLink
            }
        elif(len(texts) == 2):
            pastTeams[i] = {
                'team' : texts[0],
                'duration' : texts[1],
                'imageLink' : teamImageLink
            }
        else:
            pastTeams[i] = {
                'team' : texts[0],
                'imageLink' : teamImageLink
            }
            
        i += 1
    return pastTeams