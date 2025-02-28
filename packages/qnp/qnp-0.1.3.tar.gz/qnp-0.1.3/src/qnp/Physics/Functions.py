import numpy as np
from qnp.Physics.Constants import Plancks_Constant, Speed_of_Light, pi


def frequency(wavelength_nm: np.ndarray | float) -> np.ndarray | float:
    """get wavelength in [nm] and return frequency in [Hz]"""

    return Speed_of_Light.MperS / (wavelength_nm * 1e-9)


def omega(wavelength_nm: np.ndarray | float) -> np.ndarray | float:
    """get wavelength in [nm] and return omega in [rad/s]"""

    return 2 * pi * frequency(wavelength_nm)


class Energy:
    def __init__(self, wavelength_nm: np.ndarray | float):
        self.frequency = frequency(wavelength_nm)

    def joule(self) -> np.ndarray | float:
        """return Energy in [J] unit"""

        return Plancks_Constant.JS * self.frequency

    def eV(self) -> np.ndarray | float:
        """return Energy in [eV] unit"""

        return Plancks_Constant.eVS * self.frequency
