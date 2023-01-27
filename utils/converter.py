#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
## Plane world to screen world coordinate converter

Author: Wilfried Grousson
Created Date: 2023/01/26
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
#SCREEN_COORDINATES = {'ORIGIN': ORIGIN, 'RWHEEL': RWHEEL, 'LWHEEL': LWHEEL, 'TWHEEL': TWHEEL, 'NOSE': NOSE}

class CoordinateConverter:
    """ Coordinate converter from mm to screen"""

    def __init__(self, screen_coords : dict[int,int], mm_coords : dict[float,float]):

        pixel_delta_x = abs(screen_coords['TWHEEL'][0] - screen_coords['ORIGIN'][0])
        pixel_delta_y = abs(screen_coords['LWHEEL'][1] - screen_coords['RWHEEL'][1])

        mm_delta_x = abs(mm_coords['TWHEEL'][0] - mm_coords['ORIGIN'][0])
        mm_delta_y = abs(mm_coords['LWHEEL'][1] - mm_coords['RWHEEL'][1])

        px = pixel_delta_x / mm_delta_x if mm_delta_x != 0 else 0
        py = pixel_delta_y / mm_delta_y if mm_delta_y != 0 else 0
        self.pixel_spacing = (px, py)
        self.screen_origin = screen_coords['ORIGIN']
        
    def mm_to_screen(self, mm_point : tuple[float,float]):
        if mm_point is None:
            return None

        mm_x, mm_y = mm_point
        screen_x = (mm_x * self.pixel_spacing[0]) + self.screen_origin[0]
        screen_y = (mm_y * self.pixel_spacing[1]) * (-1.0) + self.screen_origin[1] # Y (mm) axis is inverted compared to screen y axis
        return (screen_x, screen_y)

    def screen_to_mm(self, screen_point):
        raise NotImplementedError


if __name__ == '__main__':
   raise Exception('This is a module, not a script, please use it as a module.')