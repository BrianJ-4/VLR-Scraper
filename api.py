from fastapi import FastAPI

from vlr import*
from news import*   
from matches import*

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

#news.py-------------------------------------------

#getNews
@app.get("/getNews/page:{pageNum}")
async def getNewsPage(pageNum):
    return getNews(pageNum)

#getArticle
@app.get("/getArticle/articleNum:{articleNum}")
async def getArticlePage(articleNum):
    return getArticle(articleNum)


#--------------------------------------------------

#getMatchStats
@app.get("/match/{match_id}")
async def getMatch(match_id):
    return getMatchStats(match_id)

#getPlayerStats
@app.get("/player/{player_id}")
async def getPlayer(player_id):
    return getPlayerStats(player_id)

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

