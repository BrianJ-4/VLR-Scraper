from typing import Union

from fastapi import FastAPI

from vlr import*

app = FastAPI()



@app.get("/match/{match_id}")
async def getMatch(match_id):
    return getMatchStats(match_id)


@app.get("/search/team01:{team01}/team02:{team02}/event:{event}/date:{date}")
async def read_item(team01, team02, event, date):
    print(type(team01))
    print(type(team02))
    print(type(event))
    print(type(date))
    print(team01)
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
    
    print()
    print()
    print(team01)
    print(team02)
    print(event)
    print(date)
    results = searchDatabase(Team1 = team01, Team2 = team02, Event = event, Date = date)
    results += searchDatabase(Team1 = team02, Team2 = team01, Event = event, Date = date)
    return results