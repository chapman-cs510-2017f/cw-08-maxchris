#!/usr/bin/env python3

# Name: Maksym Solodovskyi & Chris Watkins
# Student ID: 2299101 & 1450263
# Email:  solodovs@chapman.edu & watki115@mail.chapman.edu
# Course: CS510 Fall 2017
# Assignment: Classwork 7
###

import numpy as np
from abscplane import AbsComplexPlane
class ArrayComplexPlane(AbsComplexPlane):
    def __init__(self, xmin, xmax, xlen, ymin, ymax, ylen):
        """
        Attributes:
        xmax (float) : maximum horizontal axis value
        xmin (float) : minimum horizontal axis value
        xlen (int)   : number of horizontal points
        ymax (float) : maximum vertical axis value
        ymin (float) : minimum vertical axis value
        ylen (int)   : number of vertical points
        plane        : stored complex plane implementation
        fs (list[function]) : function sequence to transform plane
        """
        
        self.xmin  = xmin
        self.xmax  = xmax
        self.xlen  = xlen
        self.ymin  = ymin
        self.ymax  = ymax
        self.ylen  = ylen
        # The implementation type of plane is up to the user
        r = np.linspace(self.xmin, self.xmax,self.xlen)
        q = np.linspace(self.ymin, self.ymax, self.ylen)
        x,y = np.meshgrid(r,q,)
        self.plane = x+y*1j
        # fs should be a list of functions, initialized to be empty
        self.fs = []


    def refresh(self):
        """Regenerate complex plane.
        Populate self.plane with new points (x + y*1j), using
        the stored attributes of xmax, xmin, xlen, ymax, ymin,
        and ylen to set plane dimensions and resolution. Reset
        the attribute fs to an empty list so that no functions 
        are transforming the fresh plane.

        Returns:
            Complex plane after generating points.
        """
        self.fs = []    
        r = np.linspace(self.xmin, self.xmax,self.xlen)
        q = np.linspace(self.ymin, self.ymax, self.ylen)
        x,y = np.meshgrid(r,q)
        self.plane = x+y*1j
        return self.plane
       
        
    def apply(self, f):
        """Add the function f as the last element of self.fs. 
        Apply f to every point of the plane, so that the resulting
        value of self.plane is the final output of the sequence of
        transformations collected in the list self.fs.
        
        Args:
            f(func): Function
            
        Returns:
            Complex plane after applying the function.
        """
        
        self.f = f
        self.fs.append(self.f)        
        self.plane = f(self.plane) #Applies the function to the complex numbers
        return self.plane
        
       
        
    
    def zoom(self,xmin,xmax,xlen,ymin,ymax,ylen):
        """Reset self.xmin, self.xmax, and self.xlen.
        Also reset self.ymin, self.ymax, and self.ylen.
        Regenerate the plane with the new range of the x- and y-axes,
        then apply all transformations in fs in the correct order to
        the new points so that the resulting value of self.plane is the
        final output of the sequence of transformations collected in
        the list self.fs.
        
        Args:
            xmax(float) : maximum horizontal axis value
            xmin(float) : minimum horizontal axis value
            xlen(int)   : number of horizontal points
            ymax(float) : maximum vertical axis value
            ymin(float) : minimum vertical axis value
            ylen(int)   : number of vertical points
        
        Returns:
            Complex plane after reinitializing the attributes and applying the functions. 
        """
        
        self.xmin  = xmin
        self.xmax  = xmax
        self.xlen  = xlen
        self.ymin  = ymin
        self.ymax  = ymax
        self.ylen  = ylen
        r = np.linspace(self.xmin, self.xmax,self.xlen)
        q = np.linspace(self.ymin, self.ymax, self.ylen)
        x,y = np.meshgrid(r,q)
        self.plane = x+y*1j
        for i in range(len(self.fs)):
            self.apply(self.fs[i]) #Applies all functions in order.
        return self.plane
    

