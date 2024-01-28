from typing import Union

from fastapi import FastAPI

from vlr import*

app = FastAPI()

#getVCTPlayers
@app.get("/players/rounds:{minRounds}/agent:{agent}/map:{mapid}/timespan:{timespan}")
async def getMatch(match_id):
    return getMatchStats(match_id)

#getMatchStats
@app.get("/match/{match_id}")
async def getMatch(match_id):
    return getMatchStats(match_id)

#getPlayerStats
@app.get("/player/{player_id}")
async def getPlayer(player_id):
    return getPlayerStats(player_id)

#getLiveMatches
@app.get("/live")
async def getLive():
    return getLiveMatches()

#updateMatchDatabase
@app.get("/updateMatch")
async def updateMatchData():
    updateMatchDatabase()

#searchMatchDatabase
@app.get("/searchMatch/team01:{team01}/team02:{team02}/event:{event}/date:{date}")
async def searchMatchData(team01, team02, event, date):
    if(team01 == "?"):
        team01 = None
    if(team02 == "?"):
        team02 = None
    if(event == "?"):
        event = None
    if(date == "?"):
        date = None
    if(team01 == "?" and team02 == "?" and event == "?" and date == "?"):
        return "Not Valid"
    
    results = searchMatchDatabase(Team1 = team01, Team2 = team02, Event = event, Date = date)
    results += searchMatchDatabase(Team1 = team02, Team2 = team01, Event = event, Date = date)
    return results

#getNews
@app.get("/getNews/page:{pageNum}")
async def getNewsPage(pageNum):
    return getNews(pageNum)

#getArticle
@app.get("/getArticle/articleNum:{articleNum}")
async def getArticlePage(articleNum):
    return getArticle(articleNum)

#search
@app.get("/search/query:{query}/type:{type}")
async def searchVLR(query, type):
    return search(query, type)