#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
## the plane manager

Author: Wilfried Grousson
Created Date: 2023/01/24
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

import json
import logging
from constants import APP_NAME, APP_PLANES_FILENAME

class Plane:
    """A plane and it's configuration"""
    def __init__(self, name:str, wheelbase:int, wheeltrack:int, edge2cg:int, edge2mainwheels:int, edge2cgrange:tuple):
        """Constructor

        Args:
            name (str): Plane name
            wheelbase (int): The wheelbase in mm
            wheeltrack (int): The wheeltrack in mm
            edge2cg (int): The distance from the leading edge to the center of gravity in mm
            edge2cgrange (tuple): The range of the distance from the leading edge to the center of gravity in mm
            edge2mainwheels (int): The distance from the leading edge to the main wheels in mm
        """
        self.name = name
        self.wheelbase = wheelbase
        self.wheeltrack = wheeltrack
        self.edge2cg = edge2cg
        self.edge2cgrange = edge2cgrange
        self.edge2mainwheels = edge2mainwheels

    def __str__(self):
        return f'Plane {self.name} has wheelbase {self.wheelbase} mm, wheeltrack {self.wheeltrack} mm, edge2cg {self.edge2cg} mm, edge2mainwheels {self.edge2mainwheels} mm'


class PlaneManager:
    """The plane manager class, it is a singleton
    """
    _instance = None
    def  __new__(cls):
        if not cls._instance:
            cls._instance = super(PlaneManager, cls).__new__(cls)
            cls._instance.__planes = []
            cls._instance.__configfile = APP_PLANES_FILENAME
            cls._instance.__current_plane = None
            cls._instance.__logger = logging.getLogger(APP_NAME)
        return cls._instance

    def __init__(self):
        """Nothing to do here, the singleton is already initialized and this methos is calld by every instance"""
        pass
        
    def __to_json(self, filename:str):
        with open(filename, 'w') as f:
            json.dump(self.__planes, f, default=lambda o: o.__dict__, indent=4)

    def __from_json(self, filename:str):
        try:
            with open(filename, 'r') as f:
                self.__planes = json.load(f, object_hook=lambda d: Plane(**d))
                return True
        except FileNotFoundError:
            self.__logger.error(f'File {filename} not found')
            return False

    def add_plane(self, plane:Plane):
        """Add a new plane to the planes manager list

        Args:
            plane (Plane): a new plane. If the plane name already exists, it is not added
        """
        names = [p.name for p in self.__planes]
        if plane.name not in names:
            self.__planes.append(plane)
        else:
            self.__logger.debug(f'Plane {plane.name} already exists')
            

    def remove_plane(self, plane:Plane):
        """Remove a plane from the planes manager list

        Args:
            plane (Plane): the plane to remove. If the plane is not found, nothing is done
        """
        if plane is not None:
            self.__planes = [p for p in self.planes if p.name != plane.name]
        else:
            self.__logger.debug('No plane to remove')
            

    def get_plane_by_name(self, name:str):
        """Get a plane by its name

        Args:
            name (str): name of the plane to get. If the plane is not found, None is returned

        Returns:
            _type_: _description_
        """
        try:
            plane = [p for p in self.__planes if p.name == name]
            return plane[0]
        except IndexError:
            self.__logger.error(f'Plane {name} not found')
            return None

    def get_planes_names_list(self):
        """Get the list of planes names

        Returns:
            List[str]: the list of planes names
        """
        return [p.name for p in self.__planes]

    def get_current_plane(self):
        """Get the current plane

        Returns:
            Plane: the current plane
        """
        return self.__current_plane

    def set_current_plane_by_name(self, name:str):
        """Set the current plane by its name only if the plane name exists. If not, an exception is raised

        Args:
            name (str): name of the plane to set as current
        """
        # test if plane name exist
        plane = self.get_plane_by_name(name)
        if plane is not None:
            self.__current_plane = plane
        else:
            raise ValueError(f'Plane {name} not found')

    def save(self):
        """Save the planes manager list to the config json file
        """
        self.__to_json(self.__configfile)

    def load(self):
        """Load the planes manager list from the config json file
        """
        result = self.__from_json(self.__configfile)
        #select first plane as current if result is True else create an empty default plane and save it
        if result:
            self.__current_plane = self.__planes[0]
        else:
            self.__current_plane = Plane('Default', 0, 0, 0, 0, (0,0))
            self.__planes.append(self.__current_plane)
            self.save()

    def print_planes(self):
        for p in self.__planes:
            self.__logger.debug(p)
