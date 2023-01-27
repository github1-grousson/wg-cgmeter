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

class DrawerHelper :
    """Helper to draw some shapes on a canvas"""
    
    @staticmethod
    def draw_circle(canvas : tk.Canvas, center : tuple[int,int], radius = 10, color="white", width=1) :
        """Draw a circle on the canvas

        Args:
            canvas (tk.Canvas): The canvas
            center (tuple[int,int]): The center of the circle
            radius (int, optional): The radius of the circle. Defaults to 10.
            color (str, optional): The color of the circle. Defaults to "white".
            width (int, optional): The width of the circle. Defaults to 1.

        Returns:
            [int]: [the object ID of the circle]
        """
        if center is not None :
            x = center[0]
            y = center[1]
            return canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline=color, fill=color, width=width)
        else :
            return None


    @staticmethod
    def move_item_to(canvas : tk.Canvas, item_id, center : tuple[int,int]) :
        """Move an item to a new center

        Args:
            canvas (tk.Canvas): The canvas
            item_id (Any): The canvas object ID
            center (tuple[int,int]): The new center
        """
        if center is not None and item_id is not None:
            canvas.moveto(item_id, center[0], center[1])
        
    @staticmethod
    def change_item_color(canvas : tk.Canvas, item_id, color) :
        """Change the color of an item

        Args:
            canvas (tk.Canvas): The canvas
            item_id (Any): The canvas object ID
            color (str): The new color
        """
        canvas.itemconfig(item_id, fill=color, outline=color)