import os
import math
from ThirdParty.graphics import *

class DrawUtil:
    @staticmethod
    def rotate_point(px, py, cx, cy, angle):
        #Rotate point (px, py) around center (cx, cy) by angle in radians
        new_x = cx + (px - cx) * math.cos(angle) - (py - cy) * math.sin(angle)
        new_y = cy + (px - cx) * math.sin(angle) + (py - cy) * math.cos(angle)
        return Point(new_x, new_y)
        
    @staticmethod
    def create_triangle(x, y, rotation, color="black"):
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
        triangle.setOutline(color)
        triangle.setWidth(1)

        return triangle, [rotated_point1, rotated_point2, rotated_point3]
        
    @staticmethod   
    def create_line(pointStart,pointEnd,color="red"):
        line = Line(pointStart, pointEnd)
        line.setOutline(color)
        line.setWidth(1)

        return line