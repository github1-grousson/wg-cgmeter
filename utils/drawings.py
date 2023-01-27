#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
## Canvas drawing helpers

Author: Wilfried Grousson
Created Date: 2023/01/23
------------------------------------
MIT License

Copyright (c) 2023 WG

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import tkinter as tk

DEFAULT_RADIUS = 5
X_CORRECTION = 0
Y_CORRECTION = -3

# class circle to draw a circle on a given canvas with a given center and radius
class Circle:
    """Circle class to draw a circle on a canvas"""
    def __init__(self, canvas : tk.Canvas, center : tuple[int,int], radius = DEFAULT_RADIUS, color="white", width=1):
        """Constructor
        
        Args:
            canvas (tk.Canvas): canvas to draw on
            center (tuple[int,int]): center of the circle
            radius (int, optional): radius of the circle. Defaults to constant DEFAULT_RADIUS.
            color (str, optional): color of the circle. Defaults to "white".
            width (int, optional): width of the circle. Defaults to 1.
        """
        self.canvas = canvas
        self.center = center
        self.radius = radius
        self.color = color
        self.width = width
        self.id = None

    def draw(self):
        """Draw the circle on the canvas"""
        if self.center is not None and self.canvas is not None:
            x = self.center[0] + X_CORRECTION
            y = self.center[1] + Y_CORRECTION
            self.id = self.canvas.create_oval(x - self.radius, y - self.radius, x + self.radius, y + self.radius, outline=self.color, fill=self.color, width=self.width)
        else :
            self.id = None
            raise Exception(f'Cannot draw circle with center {self.center} on canvas {self.canvas}')

    def move_to(self, center : tuple[int,int]):
        """Move the circle to a new center

        Args:
            center (tuple[int,int]): The new center
        """
        try:
            if center is not None and self.id is not None:
                x = center[0] + X_CORRECTION
                y = center[1] + Y_CORRECTION
                self.canvas.moveto(self.id, x - self.radius, y - self.radius)
        except Exception as e:
            raise e

    def change_color(self, color):
        """Change the color of the circle

        Args:
            color (str): The new color
        """
        if self.id is not None:
            self.canvas.itemconfig(self.id, fill=color, outline=color)

    def delete(self):
        """Delete the circle from the canvas"""
        if self.id is not None:
            self.canvas.delete(self.id)
    

class RoundedRectangle:
    """Rounded rectangle class to draw a rounded rectangle on a canvas"""
    
    def __init__(self, canvas : tk.Canvas, nw_point : tuple[int,int], se_point : tuple[int,int], radius : int = DEFAULT_RADIUS, color="white", border_width=1):
        """Constructor

        Args:
            canvas (tk.Canvas): canvas to draw on
            nw_point (tuple[int,int]): north west point of the rectangle
            se_point (tuple[int,int]): south east point of the rectangle
            radius (int, optional): radius of the rounded corner. Defaults to constant DEFAULT_RADIUS.
            color (str, optional): color of the rectangle. Defaults to "white".
            border_width (int, optional): border width of the rectangle. Defaults to 1.
        """
        self.canvas = canvas
        self.nw_point = nw_point
        self.se_point = se_point
        self.radius = radius
        self.color = color
        self.border_width = border_width
        self.id = None

    def draw(self):
        """Draw the rectangle on the canvas"""
        if self.canvas is not None:
            x1 = self.nw_point[0] + X_CORRECTION
            y1 = self.nw_point[1] + Y_CORRECTION
            x2 = self.se_point[0] + X_CORRECTION
            y2 = self.se_point[1] + Y_CORRECTION
            self.id = self.__round_rectangle(x1, y1, x2, y2, self.radius, outline=self.color, width=self.border_width, fill='')
        else :
            self.id = None
            raise Exception(f'Cannot draw rectangle on canvas {self.canvas}')

    def delete(self):
        """Delete the rectangle from the canvas"""
        if self.id is not None:
            self.canvas.delete(self.id)

    '''Private methods below'''    
    def __round_rectangle(self, x1, y1, x2, y2, radius, **kwargs):

        points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def __update_rectangle_coords(self, x1, y1, x2, y2):
        r = self.radius
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
        self.canvas.coords(self.id, *points)

if __name__ == "__main__":
    raise Exception("This is a module, not a program. It should not be run directly.")