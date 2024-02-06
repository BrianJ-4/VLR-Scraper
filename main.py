from vlr import *
from news import *
from matches import*
from matchProcessor import*

import time

# players = getVCTPlayers(agent = "astra", minRounds = 0, timespan = "all")

# for name in players:
#     print(name)


print()
print()

start = time.time()

#print(getLiveMatches())
#getLiveMatchesVLR()
#print(getMatchStats(248275))
#print(getPlayerStats(11225))
#print(getLiveMatches())

#updateMatchDatabase() 

# team01 = ""
# team02 = ""
# mainEvent = ""
# date = "2020-12-06"

# filtered_entries = searchDatabase(Team1 = team01, Team2 = team02, Event = mainEvent, Date = date)
# filtered_entries += (searchDatabase(Team1 = team02, Team2 = team01, Event = mainEvent, Date = date))

# for entry in filtered_entries:
#     print(entry)
#     print()


print(getEconomyStats(79075))

end = time.time()
print("Time elapsed :",
      (end-start) * 10**3, "ms")

print()
print()