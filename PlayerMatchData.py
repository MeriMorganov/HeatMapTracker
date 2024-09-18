class Position:
    def __init__(self, x= 0, y= 0, rotation= 0, timestamp= 0):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.timestamp = timestamp

class LevelMap:
    def __init__(self, width= 100, height= 100):
        self.width = width
        self.height = height
        
        
class Player:
    def __init__(self, playerId, positionData):
        self.playerId = playerId
        self.positionData = [Position(**pos) for pos in positionData]
        
class PlayerMatchData:
    def __init__(self, levelMap, players):
        self.levelMap = LevelMap(**levelMap)
        self.players = [Player(**pla) for pla in players]


