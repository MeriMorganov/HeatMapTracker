import os
import math
import random
from PIL import Image as PILImage
from ThirdParty.graphics import *

class DrawUtil:
    @staticmethod
    def create_window(name,size):
        return GraphWin(name, size[0], size[1])
    @staticmethod
    def rotate_point(px, py, cx, cy, angle):
        #Rotate point (px, py) around center (cx, cy) by angle in radians
        new_x = cx + (px - cx) * math.cos(angle) - (py - cy) * math.sin(angle)
        new_y = cy + (px - cx) * math.sin(angle) + (py - cy) * math.cos(angle)
        return Point(new_x, new_y)
        
    @staticmethod
    def create_triangle(x, y, rotation, color=(255,255,255)):
        xOffset = 4
        yOffset = 10

        # Define triangle points based on position (x, y)
        point1 = Point(x, y)  # Top point
        point2 = Point(x + xOffset, y + yOffset)  # Bottom-right point
        point3 = Point(x - xOffset, y + yOffset)  # Bottom-left point

        # Convert rotation from degrees to radians
        theta = math.radians(rotation)

        # Rotate each point around (x, y)
        rotated_point1 = DrawUtil.rotate_point(point1.x, point1.y, x, y, theta)
        rotated_point2 = DrawUtil.rotate_point(point2.x, point2.y, x, y, theta)
        rotated_point3 = DrawUtil.rotate_point(point3.x, point3.y, x, y, theta)

        # Create the triangle polygon using rotated points
        triangle = Polygon(rotated_point1, rotated_point2, rotated_point3)

        # Set visual properties
        triangle.setOutline(DrawUtil.rgb_to_hex(color))
        triangle.setWidth(1)

        return triangle, [rotated_point1, rotated_point2, rotated_point3]
        
    @staticmethod   
    def create_line(pointStart,pointEnd,color=(255,255,255)):
        line = Line(pointStart, pointEnd)
        line.setOutline(DrawUtil.rgb_to_hex(color))
        line.setWidth(1)

        return line
      
    @staticmethod 
    def create_image(x, y, width, height, path):
        # Resize image using Pillow
        img = PILImage.open(path)
        if width and height:
            img = img.resize((width, height), PILImage.Resampling.LANCZOS)

        # Check if the ResizedMaps directory exists, if not, create it
        output_dir = "ResizedMaps"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        resized_path = os.path.join(output_dir, os.path.basename(path))
        img.save(resized_path)

        return Image(Point(x, y), resized_path)
        
    @staticmethod  
    def rgb_to_hex(color):
        """Convert RGB tuple to hex color code."""
        return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
        
    @staticmethod     
    def random_color():
        min = 0
        max = 255
        return (random.randint(min, max), random.randint(min, max), random.randint(min, max))