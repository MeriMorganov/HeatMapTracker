class PlayerMatchData:
    def __init__(self, levelMap, players):
        self.levelMap = LevelMap(**levelMap)
        self.players = [Player(**pla) for pla in players]
 
class Player:
    def __init__(self, playerId, positionData):
        self.playerId = playerId
        self.positionData = [Position(**pos) for pos in positionData]
        
class Position:
    def __init__(self, x, y, rotation, timestamp):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.timestamp = timestamp

class LevelMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
