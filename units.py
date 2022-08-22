from astropy import units as u
from astropy.units import cds
from astropy import constants as const

#Earth ratios
u_earthDensity = u.def_unit("earthDensity", 5520 * u.kg / (u.meter ** 3))
u_earthVolume = u.def_unit("earthVolume", 1.083727274614e+21 * (u.meter ** 3))
u_earthG = u.def_unit("g", 9.8 * (u.meter / u.s**2))

#Sol ratios
u_solSurfTemp = u.def_unit("solSurfaceTemp",5778 * u.K)
u_irradiance = u.def_unit("j / sm2", u.si.J / (u.s * u.meter**2))

#Chemical units

c_water_hvap = const.Constant("Water hvap", "Water Heat of Evaporation", 2501000, u.si.J / u.si.kg, 0, "https://en.wikipedia.org/wiki/Enthalpy_of_vaporization")
c_gas_constant = const.Constant("gas const", "Universal Gas Constant", 8.31446261815324, u.si.J / (u.K * u.mol), 0, "https://en.wikipedia.org/wiki/Gas_constant#Specific_gas_constant")
c_water_gas_constant = const.Constant("Water gas const", "Water Gas Constant", 461.52, u.si.J / (u.kg * u.K), 0, "https://en.wikipedia.org/wiki/Gas_constant#Specific_gas_constant")