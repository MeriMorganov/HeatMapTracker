import json
import os
import math
from PlayerMatchData import PlayerMatchData
from ThirdParty.graphics import *


#def install(package):
#    """Install the given package using pip."""
#    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check if matplotlib is installed, if not install it
#try:
#    import matplotlib.pyplot as plt
#except ImportError:
#    print("matplotlib not found. Installing...")
#    install("matplotlib")
#    import matplotlib.pyplot as plt  # Try importing again after installation


class HeatMap:
    def __init__(self, win):
        self.win = win  # Store the graphical window in the class
        self.window_size = 600
        self.max_axis = 1000

    def load_heatmap(self, filename):
        base_dir = os.path.dirname(__file__)  # Gets the directory where the script is located
        file_path = os.path.join(base_dir, 'data', filename)

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

            heatmap_data = PlayerMatchData(**data)
            return heatmap_data
            
    def rotate_point(self, px, py, cx, cy, angle):
        """ Rotate point (px, py) around center (cx, cy) by angle in radians """
        new_x = cx + (px - cx) * math.cos(angle) - (py - cy) * math.sin(angle)
        new_y = cy + (px - cx) * math.sin(angle) + (py - cy) * math.cos(angle)
        return Point(new_x, new_y)

    def draw_player_triangle(self, x, y, rotation):
        xOffset = 4
        yOffset = 10

        # Define triangle points based on position (x, y)
        point1 = Point(x, y)  # Top point
        point2 = Point(x + xOffset, y + yOffset)  # Bottom-right point
        point3 = Point(x - xOffset, y + yOffset)  # Bottom-left point

        # Convert rotation from degrees to radians
        theta = math.radians(rotation)

        # Rotate each point around (x, y)
        rotated_point1 = self.rotate_point(point1.x, point1.y, x, y, theta)
        rotated_point2 = self.rotate_point(point2.x, point2.y, x, y, theta)
        rotated_point3 = self.rotate_point(point3.x, point3.y, x, y, theta)

        # Create the triangle polygon using rotated points
        triangle = Polygon(rotated_point1, rotated_point2, rotated_point3)

        # Set visual properties
        triangle.setOutline("black")
        triangle.setWidth(1)

        # Draw the triangle in the window
        triangle.draw(self.win)

        # Calculate the bottom middle point (midpoint of rotated_point2 and rotated_point3)
        bottom_middle_x = (rotated_point2.x + rotated_point3.x) / 2
        bottom_middle_y = (rotated_point2.y + rotated_point3.y) / 2

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
            
                print("==========")
                print(x)
                print(y)
                print(position.rotation)
                print(position.timestamp)
                current_point = self.draw_player_triangle(x, y, position.rotation)
                
                if prev_point:
                    line = Line(prev_point, current_point)
                    line.setOutline("red")  # Set the line color
                    line.setWidth(1)        # Set the line width
                    line.draw(self.win)

                # Update the previous point to be the current one
                prev_point = current_point
        

if __name__ == "__main__":
    win = GraphWin("Heatmap Example", 600, 600)

    # Create a HeatMap instance
    heatmap = HeatMap(win)

    # Load the heatmap data
    heatmap_data = heatmap.load_heatmap('playerMatchData_001.json')

    # Draw the heatmap with player triangles
    heatmap.draw_heatmap(heatmap_data)
    
    # Wait for a mouse click to close the window
    win.getMouse()
    win.close()
