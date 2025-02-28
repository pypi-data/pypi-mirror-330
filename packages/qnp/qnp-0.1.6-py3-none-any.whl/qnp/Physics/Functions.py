import numpy as np
from qnp.Physics.Constants import Plancks_Constant, Speed_of_Light, pi
from typing import Union


def frequency(wavelength_nm: Union[np.ndarray, float]) -> Union[np.ndarray, float]:
    """get wavelength in [nm] and return frequency in [Hz]"""

    return Speed_of_Light.MperS / (wavelength_nm * 1e-9)


def omega(wavelength_nm: Union[np.ndarray, float]) -> Union[np.ndarray, float]:
    """get wavelength in [nm] and return omega in [rad/s]"""

    return 2 * pi * frequency(wavelength_nm)


class Energy:
    def __init__(self, wavelength_nm: Union[np.ndarray, float]):
        self.frequency = frequency(wavelength_nm)

    def joule(self) -> Union[np.ndarray, float]:
        """return Energy in [J] unit"""

        return Plancks_Constant.JS * self.frequency

    def eV(self) -> Union[np.ndarray, float]:
        """return Energy in [eV] unit"""

        return Plancks_Constant.eVS * self.frequency
