import numpy as np
from astropy import units as u
def ray_cross_section(x,*args):
    # cross sections (cm2), x=wavelength
    x_ang = x.to(u.si.Angstrom).value
    return  np.vstack( [ args[i]/x_ang**(4+2*i) for i in range(len(args))] ).sum(0) * (u.cm * u.cm)

#Contains the scattering information of a single molecule.
class rayleigh(object):
    def __init__(self,name):
        if name.upper() == 'H2':
            self.name = 'H2'
            self.args = [1.01e-12,3.26e-7,1.47]
        if name.upper() == 'CO2':
            self.name = 'CO2'
            self.args = [1.22e-12,3.26e-6,-14.60]
        if name.upper() == 'N2':
            self.name = 'N2'
            self.args = [3.50e-12,1.22e-5,-21.83]
        else:
            print("{} Not yet supported".format(name))

    #Returns the object's cross section at the given wavelength (given as an astropy unit, usually nanometers)
    def cross_section(self,wave):
        return ray_cross_section(wave,*self.args)
"""
if __name__ == "__main__":
    molecules = [ rayleigh('H2'), rayleigh('CO2'), rayleigh('N2') ]
    waves = np.linspace(3000,5000,100)

    for i in molecules:
        print("{} {:.3e} cm2".format( i.name, i.c ross_section(waves)[0] ))
    
"""