import math as mt
pi = mt.pi

class Geometry():
    def rectangle(a, b):
        return a*b
    
    def square(a):
        return a*a
    
    def circle(r):
        return pi * r * r
    
    def triangle(a, t):
        return a * t / 2