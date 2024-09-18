import json
import os
from PlayerMatchData import PlayerMatchData
from DrawUtil import DrawUtil
from ThirdParty.graphics import *
from tkinter import filedialog

window_size = 600
max_axis = 1000

class HeatMap:
    def __init__(self, win):
        self.win = win  # Store the graphical window in the class
        self.window_size = window_size
        self.max_axis = max_axis

    def load_heatmap(self, filename):
        base_dir = os.path.dirname(__file__) 
        file_path = os.path.join(base_dir, 'data', filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {filename} does not exist.")
        
        try:
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                heatmap_data = PlayerMatchData(**data)
                return heatmap_data
        except json.JSONDecodeError:
            raise ValueError("The JSON file is not properly formatted.")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred while loading the heatmap data: {e}")

    def draw_player_triangle(self, x, y, rotation):
        triangle, points = DrawUtil.create_triangle( x, y, rotation)
        triangle.draw(self.win)

        # Calculate the bottom middle point (midpoint of rotated_point2 and rotated_point3)
        bottom_middle_x = (points[1].x + points[2].x) / 2
        bottom_middle_y = (points[1].y + points[2].y) / 2

        # Return the bottom middle point as a Point object
        return Point(bottom_middle_x, bottom_middle_y)
    
    def draw_heatmap(self, heatmap_data):
        if heatmap_data:
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
        else:
            raise ValueError("No heatmap data found.")
        

def open_file_dialog():
    # Open file dialog
    file_path = filedialog.askopenfilename(
        filetypes=[("JSON files", "*.json")],
        title="Select a JSON File"
    )
    
    return file_path


if __name__ == "__main__":
    win = GraphWin("Heatmap Tracker", window_size, window_size)
    heatmap = HeatMap(win)

    json_file = open_file_dialog()

    if json_file:
        heatmap_data = heatmap.load_heatmap(os.path.basename(json_file))
        heatmap.draw_heatmap(heatmap_data)

        # Keep the window open until the ESC key is pressed
        try:
            while True:
                key = win.getKey() 
                if key == 'Escape':
                    break
        except GraphicsError as e:
            print(f"GraphicsError occurred: {e}")
    else:
        raise ValueError("A JSON was not selected, exiting program.")
    
    win.close()