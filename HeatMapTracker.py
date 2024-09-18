import json
import os
from PlayerMatchData import PlayerMatchData
from DrawUtil import DrawUtil
from ThirdParty.graphics import *

window_size = 600
max_axis = 1000

class HeatMap:
    def __init__(self, win):
        self.win = win  # Store the graphical window in the class
        self.window_size = window_size
        self.max_axis = max_axis

    def load_heatmap(self, filename):
        base_dir = os.path.dirname(__file__)  # Gets the directory where the script is located
        file_path = os.path.join(base_dir, 'data', filename)

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

            heatmap_data = PlayerMatchData(**data)
            return heatmap_data

    def draw_player_triangle(self, x, y, rotation):
        triangle, points = DrawUtil.create_triangle( x, y, rotation)
        triangle.draw(self.win)

        # Calculate the bottom middle point (midpoint of rotated_point2 and rotated_point3)
        bottom_middle_x = (points[1].x + points[2].x) / 2
        bottom_middle_y = (points[1].y + points[2].y) / 2

        # Return the bottom middle point as a Point object
        return Point(bottom_middle_x, bottom_middle_y)
    
    def draw_heatmap(self, heatmap_data):
        for player in heatmap_data.players:
            position_data = sorted(player.positionData, key=lambda pos: pos.timestamp) 
            prev_point = None
            worldOffset = self.max_axis/self.window_size
            for position in position_data:
                x = position.x/worldOffset
                y = position.y/worldOffset
                current_point = self.draw_player_triangle(x, y, position.rotation)
                
                if prev_point:
                    line = DrawUtil.create_line(prev_point,current_point)
                    line.draw(self.win)

                # Update the previous point to be the current one
                prev_point = current_point
        

if __name__ == "__main__":
    win = GraphWin("Heatmap Example", window_size, window_size)

    # Create a HeatMap instance
    heatmap = HeatMap(win)

    # Load the heatmap data
    heatmap_data = heatmap.load_heatmap('playerMatchData_001.json')

    # Draw the heatmap with player triangles
    heatmap.draw_heatmap(heatmap_data)

    # Keep the window open until the ESC key is pressed
    try:
        while True:
            key = win.getKey() 
            if key == 'Escape':
                break
    except GraphicsError as e:
        print(f"GraphicsError occurred: {e}")
    
    win.close()