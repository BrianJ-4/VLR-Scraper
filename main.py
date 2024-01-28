from vlr import *
import time

# players = getVCTPlayers(agent = "astra", minRounds = 100, timespan = "all")

# for name in players:
#     print(name)


print()
print()

start = time.time()


#print(getLiveMatches())
# stats = getMatchStats(7095)
# print(stats)
#print(getPlayerStats(11225))
#print(getLiveMatches())

#updateMatchDatabase() 

# team01 = "100 tHievEs"
# team02 = None
# mainEvent = None
# date = None

# print(team01)
# print(team02)
# print(mainEvent)
# print(date)
# filtered_entries = searchMatchDatabase(Team1 = team01, Team2 = team02, Event = mainEvent, Date = date)
# filtered_entries += (searchMatchDatabase(Team1 = team02, Team2 = team01, Event = mainEvent, Date = date))

# for entry in filtered_entries:
#     print(entry)
#     print()

#updatePlayerDatabase(1)

# print(searchPlayerDatabase(0, "potter"))

# getArticle("https://www.vlr.gg/264266/riot-previews-major-balance-changes-to-11-agents")

search("vct", "all")

end = time.time()
print("Time elapsed :",

      (end-start) * 10**3, "ms")

print()
print()