from pathlib import Path
from collections import deque
import json
import math


class C3PO:
    
    def __init__(self, milleniumFalconJsonFilePath: Path) -> None:
        """
        input: millieniumFalconJsonFilePath is the Path to the json file which is in the form
            {
                "autonomy": int,
                "routes": [
                    {
                        "origin": str,
                        "destination": str,
                        "travelTime": int
                    },
                    ...
                ]
            }

        """
        self.milleniumFalconJsonFilePath = milleniumFalconJsonFilePath
    
    def giveMeTheOdds(self, empireJsonFilePath: Path):
        """
        input: empireJsonFilePath is the Path to the json file which is in the form
            {
                "countdown": int,
                "bounty_hunters": [
                    {
                        "planet": str,
                        "day": int
                    },
                    ...
                ]
            }
        
        output: the solution x of the problem which is 
            ==> 0 if the Millennium Falcon cannot reach Endor before the Death Star annihilates Endor
            ==> x (0 < x < 1) if the Millennium Falcon can reach Endor before the Death Star annihilates Endor but might be captured by bounty hunters with x the probability of being captured
            ==> 1 if the Millennium Falcon can reach Endor before the Death Star annihilates Endor without crossing a planet with bounty hunters on it.
        """
        
    
        with self.milleniumFalconJsonFilePath.open(encoding="utf-8") as milleniumFalconJsonFile:
            milleniumFalcon = json.load(milleniumFalconJsonFile)
        with empireJsonFilePath.open(encoding="utf-8") as empireJsonFile:
            empire = json.load(empireJsonFile)
            
        # VARIABLES
        autonomy = milleniumFalcon["autonomy"]
        galaxies_roads = milleniumFalcon["routes"]
        countdown = empire["countdown"]
        bounty_hunters = empire["bounty_hunters"]
        
        # Graph construction (dictionary: planet -> list of (neighbour, travel_time))
        graph = {}
        for route in galaxies_roads:
            origin = route["origin"]
            destination = route["destination"]
            travel_time = route["travelTime"]
            
            # The roads are two-way.
            if origin not in graph:
                graph[origin] = []
            if destination not in graph:
                graph[destination] = []
            
            graph[origin].append((destination, travel_time))
            graph[destination].append((origin, travel_time))
        
        # Hunters location (list of (planet, days))
        hunters_locations = []
        for hunters in bounty_hunters:
            hunters_locations.append((hunters["planet"], hunters["day"]))

        # Initialise queue with initial state
        # State: (planet, time_remaining, fuel_remaining, hunters_encounters)
        # We start on Tatooine with the countdown complete and fuel full
        queue = deque([("Tatooine", countdown, autonomy, 0)])
        
        # Set to avoid revisiting the same states
        visited = set()
        
        min_encounters = math.inf #min of the encounters that we have
        
        while queue:
            
            """
            CONDITION:
            for each (planet, countdown, current_autonomy, hunters_encounters) in queue, 
            we have that:
                => countdown >= 0
                => current_autonomy >= 0 
                => hunters_encounters < min_encounters
            """
            
            planet, current_countdown, current_autonomy, hunters_encounters = queue.popleft()
            visited.add((planet, current_countdown, current_autonomy, hunters_encounters))
            
            if planet == "Endor":
                min_encounters = hunters_encounters
            else:
                
                # We can move to a other planet
                for next_planet, travel_time in graph[planet]:
                    
                    new_planet, new_current_countdown, new_current_autonomy = next_planet, current_countdown - travel_time, current_autonomy - travel_time
                    
                    new_current_day = countdown - new_current_countdown 
                    if (new_planet, new_current_day) in hunters_locations:
                        new_hunters_encounters = hunters_encounters + 1
                    else:
                        new_hunters_encounters = hunters_encounters
                        
                        
                    if new_current_countdown >= 0 and new_current_autonomy >= 0 and new_hunters_encounters < min_encounters and not (new_planet, new_current_countdown, new_current_autonomy, new_hunters_encounters) in visited: 
                        queue.append((new_planet, new_current_countdown, new_current_autonomy, new_hunters_encounters))
                
                # Or we can stay in the current planet to fuel
                if current_countdown > 0:
                    
                    current_day = countdown - current_countdown + 1
                    if (planet, current_day) in hunters_locations:
                        new_hunters_encounters = hunters_encounters + 1
                    else:
                        new_hunters_encounters = hunters_encounters
                    
                    if new_hunters_encounters < min_encounters and not (planet, current_countdown - 1, autonomy, new_hunters_encounters) in visited:
                        queue.append((planet, current_countdown - 1, autonomy, new_hunters_encounters))
                        
        
        if min_encounters == math.inf:
            return 0
        elif min_encounters == 0:
            return 1
        else:
            # Probabilité de succès avec k rencontres = (9/10)^k
            return (9/10) ** min_encounters
        
    
    
    