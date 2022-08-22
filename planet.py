#SOURCES:
#Orbit calculations: https://www.sciencedirect.com/topics/engineering/orbit-formula

from math import pi, sqrt
import re
import string
from astropy import units as u
from astropy import constants as const

u_earthDensity = u.def_unit("earthDensity", 5520 * u.kg / (u.meter ** 3))
u_earthVolume = u.def_unit("earthVolume", 1.083727274614e+21 * (u.meter ** 3))
u_earthG = u.def_unit("g", 9.8 * (u.meter / u.s**2))

class planet:
    #Radius in earth radii
    #Density in earth densities
    #Semi_major_axis in AU (earth orbits). Represents furthest distance from the star during orbit
    #Eccentricity as a ratio (0 = circular, 0 < e < 1 = elliptical)
    #Axial tilt in degrees (0 = no tilt, 90 = pole facing star, 180 = no tilt, retrograde spin)
    def __init__(self, parent_star, radius = 1, density = 1, semi_major_axis = 1, eccentricity = 0.01671, axial_tilt = 23.5, day_length = 1):
        self.PARENT_STAR = parent_star
        self.RADIUS = radius * u.astrophys.earthRad
        self.DENSITY = density * u_earthDensity

        self.SEMI_MAJOR_AXIS = semi_major_axis * u.astrophys.AU
        self.ECCENTRICITY = eccentricity
        self.AXIAL_TILT = axial_tilt * u.si.deg
        self.DAY_LENGTH = day_length * u.si.day

    #Print all of the planet's information to the terminal
    def display(self):
        print("__Physical Characteristics__")
        print("Radius: {:.2f}".format(self.radius()))
        print("Density: {:.2f}".format(self.density()))
        print("Volume: {:.2f}".format(self.volume()))
        print("Mass: {:.2f}".format(self.mass()))
        print("Gravity: {:.2f}".format(self.gravity()))
        print()
        print("__Spatial Characteristics__")
        print("Semi-major Axis: {:.2f}".format(self.semi_major_axis()))
        print("Semi-minor Axis: {:.2f}".format(self.semi_minor_axis()))
        print("Average Orbital Distance: {:.2f}".format(self.average_orbit()))
        print("Eccentricity: {:.2f}".format(self.eccentricity()))

        print("Year Length: {:.2f}".format(self.period()))
        print("Axial Tilt: {:.2f}".format(self.axial_tilt()))
        print("Day Length: {:.2f}".format(self.day_length()))

    def radius(self):
        return self.RADIUS

    def density(self):
        return self.DENSITY

    def semi_major_axis(self):
        return self.SEMI_MAJOR_AXIS

    def eccentricity(self):
        return self.ECCENTRICITY
    
    def axial_tilt(self):
        return self.AXIAL_TILT

    def day_length(self):
        return self.DAY_LENGTH

    def volume(self):
        return ((4/3) * pi * self.radius() ** 3).to(u_earthVolume)
    
    def mass(self):
        return (self.density() * self.volume()).to(u.astrophys.earthMass)
    
    def gravity(self):
        return (const.G * self.mass() / (self.radius()**2)).to(u_earthG)

    def semi_minor_axis(self):
        return sqrt(self.semi_major_axis().value**2*(1-self.eccentricity()**2)) * u.astrophys.AU

    def average_orbit(self):
        return (self.semi_major_axis() + self.semi_minor_axis()) / 2
    
    def period(self):
        return (sqrt(self.average_orbit().value**3) * u.si.yr).to(u.si.day)

    #Update semi-major axis and derived values
    def change_semi_major(self, new_value):
        self.semi_major_axis = new_value * u.astrophys.AU
        self.semi_minor_axis = sqrt(self.semi_major_axis**2*(1-self.eccentricity**2)) * u.astrophys.AU
        self.average_orbit = (self.semi_major_axis + self.semi_minor_axis) / 2
        self.period = (sqrt(self.average_orbit.value**3) * u.si.yr).to(u.si.day)

    #Update eccentricity and derived values
    def change_eccentricity(self, new_value):
        self.eccentricity = new_value
        self.semi_minor_axis = sqrt(self.semi_major_axis**2*(1-self.eccentricity**2)) * u.astrophys.AU
        self.average_orbit = (self.semi_major_axis + self.semi_minor_axis) / 2
        self.period = (sqrt(self.average_orbit.value**3) * u.si.yr).to(u.si.day)

    #Compare planets, used for ordering in the star system list
    def __lt__(self, other):
        return self.orbit < other.orbit