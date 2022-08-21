from math import pi
from astropy import units as u
from astropy import constants as const

EARTH_DENSITY_KGPM3 = 5520
EARTH_GRAV_ACC_MPS2 = 9.81

u_earthDensity = u.def_unit("earthDensity", 5520 * u.kg / (u.meter ** 3))
u_earthVolume = u.def_unit("earthVolume", 1.083727274614e+21 * (u.meter ** 3))
u_earthG = u.def_unit("g", 9.8 * (u.meter / u.s**2))
class planet:
    #Radius in earth radii, density in earth densities.
    def __init__(self, radius, density):
        self.radius = radius * u.astrophys.earthRad
        self.density = density * u_earthDensity
        self.volume = ((4/3) * pi * self.radius ** 3).to(u_earthVolume)
        self.mass = (self.density * self.volume).to(u.astrophys.earthMass)
        self.gravity = (const.G * self.mass / (self.radius**2)).to(u_earthG)

    def display(self):
        print("Radius: {}".format(self.radius))
        print("Density: {}".format(self.density))
        print("Volume: {}".format(self.volume))
        print("Mass: {}".format(self.mass))
        print("Gravity: {}".format(self.gravity))