def search_database(**kwargs):
    print(kwargs)
    # Sample database of dictionaries
    database = [
        {
            "ID": "1",
            "PUG123": "PUG123",
            "TORCH": "TORCH",
            "Team1": "PUG123",
            "Team2": "TORCH",
            "Event": "EventX",
            "matchInEvent": "MatchA"
        },
        {
            "ID": "2",
            "EG": "EG",
            "EG": "EG",
            "Team1": "TeamB",
            "PRX": "PRX",
            "Event": "EventX",
            "matchInEvent": "MatchB"
        },
        # Add more entries as needed
    ]

    # Filter the database based on the provided keyword arguments
    results = []
    for entry in database:
        match = True
        for key, value in kwargs.items():
            if key not in entry or entry[key] != value:
                match = False
                break
        if match:
            results.append(entry)

    return results

# Example usage:
filtered_entries = search_database(Event = "EventX")
for entry in filtered_entries:
    print("First")
    print(entry)

# filtered_entries = search_database(Event="EventX", Team1="TORCH", Team2="PUG123")
# for entry in filtered_entries:
#     print(entry)
