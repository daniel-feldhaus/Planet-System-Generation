from cmath import pi
import wave
from astropy import units as u
from astropy import constants as const

from color_index import get_rgb
from math import e, sqrt
import numpy as np

SOL_TEMP_K = 5778

def temp_to_CI(temp):
    return (1/92) * (-111 + sqrt(2401 + (211600000000/temp**2)) + (460000/temp))

class star:
    def __init__(self, luminosity = 1, surface_temp = 5778):
        self.luminosity = luminosity * u.astrophys.solLum
        self.surface_temp = surface_temp * u.K
        self.radius = (((self.surface_temp/SOL_TEMP_K)**2)*(self.luminosity**0.5)).value * u.astrophys.solRad
        self.col_index = temp_to_CI(self.surface_temp.value)
        self.rgb_color = get_rgb(self.col_index)
        

    def display(self):
        print("Luminosity:", self.luminosity)
        print("Surface Temp:", self.surface_temp)
        print("Radius:",self.radius)
        print("Color Index:",self.col_index)    
        print("RGB:", self.rgb_color[0], self.rgb_color[1], self.rgb_color[2])
        print("Spectral Power at 1000 nm:", self.spectral_power_at(1000 * u.nanometer))

    def spectral_power_at(self, wavelength): #spectral power at the given wavelength
        #A = 3.74192e-16 * u.si.W * u.meter * u.meter; # is 2πhc^2 in units of watts*m^2
        #B = 1.438770e7 * u.nanometer * u.K;  #is hc/k in units of nanometer-kelvin
        #W = A.value /  ((wavelength ** 5) * (np.exp(B.value / (wavelength * self.surface_temp.value)) - 1))
        #W = A / (( wavelength** 5) * (np.exp(B / ( wavelength * self.surface_temp ) ) - 1 ))
        
        #print("A:",A)
        #print("B:",B)
        A = (2 * pi * const.c ** 2 * const.h) / (wavelength ** 5)
        B = 1 / (e ** (const.h * const.c / (wavelength * const.k_B * self.surface_temp)) - 1)
        return A * B
