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
        self.LUMINOSITY = luminosity * u.astrophys.solLum
        self.SURFACE_TEMP = surface_temp * u_solSurfTemp


        
    #Print all of the star's information to the terminal
    def display(self):
        print("Luminosity:", self.luminosity())
        print("Surface Temp:", self.surface_temp())
        print("Radius:",self.radius())
        print("Color Index:",self.color_index())    
        print("RGB:", self.rgb_color()[0], self.rgb_color()[1], self.rgb_color()[2])
        print("Spectral Power at 1000 nm:", self.spectral_power_at(1000 * u.nanometer))

    def luminosity(self):
        return self.LUMINOSITY
    
    def surface_temp(self):
        return self.SURFACE_TEMP

    def radius(self):
        #I've absolutely forgotten where this equation came from, but it seems to generate very accurate radii.
        return (((self.surface_temp())**2)*(self.luminosity()**0.5)).value * u.astrophys.solRad

    def color_index(self):
        #Color index, used in stellar color calculations
        return temp_to_CI(self.surface_temp())
    
    def rgb_color(self):
        #The visual color of the star
        return get_rgb(self.color_index())
    
    #spectral power at the given wavelength
    def spectral_power_at(self, wavelength): 
        A = (2 * pi * const.c ** 2 * const.h) / (wavelength ** 5)
        B = 1 / (e ** (const.h * const.c / (wavelength * const.k_B * self.surface_temp().to(u.K))) - 1)
        return (A * B).value * u_irradiance