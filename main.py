from pathlib import Path


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
        pass
    
    def giveMeTheOdds(self, empireJsonFilePath: Path) -> float:
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
        pass
    
    