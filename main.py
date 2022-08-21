from star import star
import numpy as np
from Libs import rayleigh
import matplotlib.pyplot as plt
import astropy.units as u

all_waves = []
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
        all_cross.append(molecule.cross_section(w * 10))
        all_colors.append(my_star.rgb_color.astype(float) / 255)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.plot_trisurf(all_temp, all_waves, all_irr)
#ax.scatter(all_temp, all_waves, all_cross)
ax.set_xlabel("Temperature")
ax.set_ylabel("Wavelength (nm)")
ax.set_zlabel("Irradiance")
plt.show()