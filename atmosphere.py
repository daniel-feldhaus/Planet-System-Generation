#SOURCES
#Saturation vapor pressure: https://icoads.noaa.gov/software/other/profs (Search for "FUNCTION ESW(T)")
#Geopotential energy: https://en.wikipedia.org/wiki/Geopotential
#Gas constants: https://en.wikipedia.org/wiki/Gas_constant#Specific_gas_constant
#Air density: https://www.omnicalculator.com/physics/air-density
from planet import planet
from astropy import units as u
from astropy.units import cds
from astropy import constants as const
from Libs.rayleigh import rayleigh
import units

#Description from NOAA.gov: 
#   THIS FUNCTION RETURNS THE SATURATION VAPOR PRESSURE ESW (MILLIBARS)
#   OVER LIQUID WATER GIVEN THE TEMPERATURE T (CELSIUS). THE POLYNOMIAL
#   APPROXIMATION BELOW IS DUE TO HERMAN WOBUS, A MATHEMATICIAN WHO
#   WORKED AT THE NAVY WEATHER RESEARCH FACILITY, NORFOLK, VIRGINIA,
#   BUT WHO IS NOW RETIRED. THE COEFFICIENTS OF THE POLYNOMIAL WERE
#   CHOSEN TO FIT THE VALUES IN TABLE 94 ON PP. 351-353 OF THE SMITH-
#   SONIAN METEOROLOGICAL TABLES BY ROLAND LIST (6TH EDITION). THE
#   APPROXIMATION IS VALID FOR -50 < T < 100C.
#temp: Temperature of air parcel in K
def saturation_vapor_pressure(temp):
    temp_c = temp.to(u.deg_C, equivalencies = u.temperature()).value
    es0 = 6.1078 #Saturation at 0 degrees c
    pol = 0.99999683 + temp_c*(-0.90826951E-02 + temp_c*( 0.78736169E-04 + temp_c*(-0.61117958E-06 +
                        temp_c*(0.43884187E-08  + temp_c*(-0.29883885E-10 + temp_c*( 0.21874425E-12 + 
                        temp_c*(-0.17892321E-14 + temp_c*( 0.11112018E-16 + temp_c*(-0.30994571E-19)))))))))
    return ((es0/pol**8) / 1013.25) * cds.atm

def specific_gas_constant(molar_mass):
    return units.c_gas_constant / molar_mass

class atmosphere:
    molecules = {}
    #Planet: The planet that this atmosphere belongs to
    #Composition: A list with the shape [(molecule name, molecule proportion)] 
    #   E.x.: [("O2",1),("N2",3)] indicates an oxygen/nitrogen atmosphere with 3x more nitrogen than oxygen
    #Surface pressure: Average air pressure at the surface in atmospheres
    #Surface humidity: Average relative humidity at surface
    def __init__(self, _planet, composition, surface_pressure = 1, surface_humidity = 0.5):
        self.PLANET = _planet
        self.SURFACE_PRESSURE = surface_pressure * cds.atm
        self.SURFACE_HUMIDITY = surface_humidity
        self.SURFACE_MOLAR_MASS = 0
        weight_sum = 0
        for c in composition:
            self.molecules[c[0]] = rayleigh(c[0])
            weight_sum += c[1]
            self.SURFACE_MOLAR_MASS += self.molecules[c[0]].molar_mass * c[1]
        self.SURFACE_MOLAR_MASS /= weight_sum
        self.specific_heat = 0
        for c in composition:
            self.specific_heat += (c[1] / weight_sum) * self.molecules[c[0]].specific_heat

        #for c in composition:

    def surface_pressure(self):
        return self.SURFACE_PRESSURE
    
    def surface_humidity(self):
        return self.SURFACE_HUMIDITY


    def surface_density(self, temp = None, relative_humidity = None):
        if(temp == None):
            temp = self.PLANET.surface_temp()
        if(relative_humidity == None):
            relative_humidity = self.surface_humidity()
        svp = saturation_vapor_pressure(temp)
        vapor_pressure = (svp * relative_humidity).to(u.si.Pa)
        dry_pressure = self.surface_pressure().to(u.si.Pa) - vapor_pressure
        print("Vapor pressure:", vapor_pressure, "Dry pressure", dry_pressure)
        print("Surface molar mass: ", self.SURFACE_MOLAR_MASS)
        print("A: ",(dry_pressure / (specific_gas_constant(self.SURFACE_MOLAR_MASS)*temp)).to(u.si.kg / (u.meter**3)))
        print("B: ", (vapor_pressure / (units.c_water_gas_constant * temp)).to(u.si.kg / (u.meter**3)))
        
        p = ((dry_pressure / (specific_gas_constant(self.SURFACE_MOLAR_MASS)*temp)) + (vapor_pressure / (units.c_water_gas_constant * temp))).to(u.si.kg / (u.meter**3))
        return p


    #The temperature lapse rate of a given air parcel
    #Altitude: The altitude of the air parcel
    #Surface_temp: The temperature of the surface under the air parcel
    #Resolution: The step size of the altitudes that the lapse rate is iteratively calculated from
    def lapse_rate(self):
        dry_rate = (self.PLANET.gravity() / self.specific_heat).to(u.K / u.meter)
        return dry_rate

    def temperature_at(self, altitude, surface_temp = None):
        #If the surface temperature isn't specified, the planet average is used.
        if(surface_temp == None):
            surface_temp = self.PLANET.surface_temp()
        return self.PLANET.surface_temp() - self.lapse_rate() * altitude * u.meter

    def pressure_at(self, altitude, surface_temp = None):
        #If the surface temperature isn't specified, the planet average is used.
        if(surface_temp == None):
            Tb = self.PLANET.surface_temp()
        else:
            Tb = surface_temp
        pb = self.surface_pressure()
        Lb = self.lapse_rate()
        h = altitude * u.meter
        R = units.c_gas_constant
        g = self.PLANET.gravity()
        M = self.SURFACE_MOLAR_MASS

        a = ((Tb + h * Lb) / Tb)
        b =  (-g*M) / (R*Lb)
        p = pb * (a ** b)
        return p