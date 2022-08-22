from astropy import units as u
from star import star
from planet import planet
import numpy as np
from bisect import insort
class star_system:
    s_star : star
    planets : np.array
    def __init__(self, s_star):
        self.s_star = s_star
        self.planets = []
    def add_planet(self, s_planet):
        insort(self.planets, s_planet)
    def display(self):
        self.s_star.display()
        print()
        for p in self.planets:
            p.display()
            print()