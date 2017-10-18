#!/usr/bin/env python3

# Name: Maksym Solodovskyi & Chris Watkins
# Student ID: 2299101 & 1450263
# Email:  solodovs@chapman.edu & watki115@mail.chapman.edu
# Course: CS510 Fall 2017
# Assignment: Classwork 7
###

import csv
import numpy as np
import matplotlib.pyplot as plt
from cplane_np import ArrayComplexPlane

def julia(c):
    """Builds function to store for use later.
    
    Args:
        c: Complex Number
    
    Returns:
        f: Function
    """
    def f(z, m = 100): 
        """Function that takes a complex number and iterates 
           it until the condition abs(z) >=2 is reached.
        
        Args:
            z: Complex Number
            
        Returns:
            n: Number of iterations of function
        """
        if abs(z) > 2:
            return 1
        else:
            n = 1
            while abs(z) < 2:
                n += 1
                if n > 100:
                    return 0
                else:
                    z = z**2 + c
            return n
    return f

    

class JuliaPlane(ArrayComplexPlane):
    def __init__(self,c):
        self.c = c
        super(JuliaPlane,self).__init__(-2,2,1000,-2,2,1000)
        self.plane = super(JuliaPlane,self).apply(np.vectorize(julia(self.c)))

    def refresh(self, c):
        """Regenerate Julia plane.
        Populate self.plane with new points (x + y*1j), using
        the stored attributes of xmax, xmin, xlen, ymax, ymin,
        and ylen to set plane dimensions and resolution. Reset
        the attribute fs to an empty list so that no functions 
        are transforming the fresh plane.

        Returns:
            Complex plane after generating points.
        """
        
        self.fs = []
        super(JuliaPlane,self).__init__(self.xmin,self.xmax,self.xlen,self.ymin,self.ymax,self.ylen)
        self.apply(np.vectorize(julia(self.c)))
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
        print(self.plane)
        for i in range(len(self.fs)):
            self.apply(self.fs[i]) #Applies all functions in order.
        return self.plane

    def toCSV(self,filename):
        """Makes a CSV file of parameters of Julia Plane.
        
        Args: filename: file name
        """
        with open(filename,'w') as csvfile:
            np.savetxt("plane.csv",self.plane, delimiter = ',', fmt = '%.0f') #File to save plane in serperate file
            fi = csv.writer(csvfile, quotechar=' ', delimiter = ',', quoting = csv.QUOTE_MINIMAL)
            param = [[self.c],[self.xmin],[self.xmax],[self.xlen],[self.ymin],[self.ymax],[self.ylen],[self.fs],[self.plane]]
            for row in param:
                fi.writerow(row)

    def fromCSV(self, filename):
        """Reads a CSV file to initialize parameters of Julia Plane.
        
        Args: filename: file name
        """
        with open(filename, newline = '') as csvfile:
            read = csv.reader(csvfile, delimiter = ',')
            param = []
            for row in read:
                param.append(row)
            self.c = complex(param[0][0])
            self.xmin = int(param[1][0])
            self.xmax = int(param[2][0])
            self.xlen = int(param[3][0])
            self.ymin = int(param[4][0])
            self.ymax = int(param[5][0])
            self.ylen = int(param[6][0])
            self.fs = np.vectorize(param[7][0])
            self.plane = np.loadtxt("plane.csv", delimiter = ',', dtype = 'int') #Read plane from plane.csv file 
           
    def show(self):
        plt.imshow(self.plane, interpolation = 'bicubic', extent = (self.xmin,self.xmax,self.ymin,self.ymax) )
        plt.text(0,1.5, self.c, fontsize = 20, color = 'white')
        plt.text(-0.5,1.5, 'c =', fontsize = 20, color = 'white')