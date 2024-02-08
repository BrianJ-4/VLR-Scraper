from fastapi import FastAPI

from vlr import*
from news import*   
from matches import*
from matchProcessor import*
from playerProcessor import*

app = FastAPI()

#matches.py-------------------------------------------

#getUpcomingAndLive
@app.get("/matches/getUpcomingAndLive/page:{page}")
async def getUpcomingAndLiveMatches(page):
    return getUpcomingAndLive(page)

#getResults
@app.get("/matches/getResults/page:{page}")
async def getMatchResults(page):
    return getResults(page)

#news.py----------------------------------------------

#getNews
@app.get("/getNews/page:{pageNum}")
async def getNewsPage(pageNum):
    return getNews(pageNum)

#getArticle
@app.get("/getArticle/articleNum:{articleNum}")
async def getArticlePage(articleNum):
    return getArticle(articleNum)


#matchProcessor.py------------------------------------

#getMatchStats
@app.get("/getMatchPage/{match_id}")
async def getMatch(match_id):
    return getMatchPage(match_id)

#playerProcessor.py-----------------------------------

#getPlayerPage
@app.get("/getPlayerPage/{playerID}")
async def getPlayer(playerID):
    return getPlayerPage(playerID)

#getPlayerAgentStats
@app.get("/getPlayerAgentStats/{playerID}/{timespan}")
async def getAgentStats(playerID, timespan):
    return getPlayerAgentStats(playerID, timespan)

#getPlayerMatchResults
@app.get("/getPlayerMatchResults/{playerID}/{page}")
async def getPlayerResults(playerID, page):
    return getPlayerMatchResults(playerID, page)

#Others-----------------------------------------------

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
    results = sorted(results, key=lambda x: x["Date"], reverse = True)
    return results

#search
@app.get("/search/query:{query}/type:{type}")
async def searchVLR(query, type):
    return search(query, type)

