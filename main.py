from star import star
from planet import planet
from atmosphere import atmosphere
from star_system import star_system
import numpy as np
from Libs import rayleigh
import matplotlib.pyplot as plt
import astropy.units as u

my_planet = planet(1,1,eccentricity=0.2)
my_atmo = atmosphere(my_planet, [('N2',0.78),('O2',21),('H2',0.1)])
print("Surface density:", my_atmo.surface_density())
print("Specific heat: ", my_atmo.specific_heat)
print("Lapse Rate:", my_atmo.lapse_rate())
print("Temperature at Surface: ", my_planet.surface_temp())
print("Temperature at 6km Altitude: ", my_atmo.temperature_at(6000))
print("Pressure at 6km altitude:", my_atmo.pressure_at(6000))
my_system = star_system(star(1,1))
my_system.add_planet(my_planet)

alt = []
p = []
for m in range(0,12000):
    alt.append(m)
    p.append(my_atmo.temperature_at(m).value)

fig = plt.figure()
ax = fig.add_subplot()

ax.plot(alt,p)
plt.show()

#my_system.display()
"""all_waves = []
all_irr = []
all_cross = []
all_temp = []
all_colors = []

temperatures = np.linspace(2000,6000,20)
wavelengths = np.linspace(250,2500,100)
molecule = rayleigh.rayleigh('N2')
for t in temperatures:
    my_star = star(1, t)
    for w in wavelengths:
        all_temp.append(t)
        all_waves.append(w)
        all_irr.append(my_star.spectral_power_at(w * u.nanometer).value)
        all_cross.append(molecule.cross_section(w * u.nanometer)[0].to(u.meter * u.meter).value)
        all_colors.append(my_star.rgb_color.astype(float) / 255)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

for c in all_cross:
    print(c)

ax.plot_trisurf(all_temp, all_waves, all_cross)
#ax.scatter(all_temp, all_waves, all_cross)
ax.set_xlabel("Temperature")
ax.set_ylabel("Wavelength (nm)")
ax.set_zlabel("Cross Section")
plt.show()"""