from star import star
from planet import planet
from star_system import star_system
import numpy as np
from Libs import rayleigh
import matplotlib.pyplot as plt
import astropy.units as u


my_system = star_system(star(1,1))
my_system.add_planet(planet(1,1,eccentricity=0.2))

my_system.display()
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