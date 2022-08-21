from cmath import pi
import wave
from astropy import units as u
from astropy import constants as const

from color_index import get_rgb
from math import e, sqrt
import numpy as np

u_solSurfTemp = u.def_unit("solSurfaceTemp",5778 * u.K)
u_irradiance = u.def_unit("j / sm2", u.si.J / (u.s * u.meter**2))
def temp_to_CI(temp):
    temp_k = temp.to(u.K).value
    return (1/92) * (-111 + sqrt(2401 + (211600000000/temp_k**2)) + (460000/temp_k))

#Contins the given and calculated information for a fictional star.
class star:
    #Luminosity in sol lumiosities, surface_temp in Kelvin.
    def __init__(self, luminosity = 1, surface_temp = 1):
        self.luminosity = luminosity * u.astrophys.solLum
        self.surface_temp = surface_temp * u_solSurfTemp
        #I've absolutely forgotten where this equation came from, but it seems to generate very accurate radii.
        self.radius = (((self.surface_temp)**2)*(self.luminosity**0.5)).value * u.astrophys.solRad
        #Color index, used in stellar color calculations
        self.col_index = temp_to_CI(self.surface_temp)
        #The visual color of the star
        self.rgb_color = get_rgb(self.col_index)
        
    #Print all of the star's information to the terminal
    def display(self):
        print("Luminosity:", self.luminosity)
        print("Surface Temp:", self.surface_temp)
        print("Radius:",self.radius)
        print("Color Index:",self.col_index)    
        print("RGB:", self.rgb_color[0], self.rgb_color[1], self.rgb_color[2])
        print("Spectral Power at 1000 nm:", self.spectral_power_at(1000 * u.nanometer))

    #spectral power at the given wavelength
    def spectral_power_at(self, wavelength): 
        A = (2 * pi * const.c ** 2 * const.h) / (wavelength ** 5)
        B = 1 / (e ** (const.h * const.c / (wavelength * const.k_B * self.surface_temp.to(u.K))) - 1)
        return (A * B).value * u_irradiance