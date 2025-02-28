import numpy as np
from qnp.Physics.Constants import Plancks_Constant, Speed_of_Light, pi
from typing import Union


def frequency(wavelength_um: Union[np.ndarray, float]) -> Union[np.ndarray, float]:
    """get wavelength in [um] and return frequency in [Hz]"""

    return Speed_of_Light.MperS / (wavelength_um * 1e-6)


def omega(wavelength_um: Union[np.ndarray, float]) -> Union[np.ndarray, float]:
    """get wavelength in [um] and return omega in [rad/s]"""

    return 2 * pi * frequency(wavelength_um)


class Energy:
    def __init__(self, wavelength_um: Union[np.ndarray, float]):
        self.frequency = frequency(wavelength_um)

    def joule(self) -> Union[np.ndarray, float]:
        """return Energy in [J] unit"""

        return Plancks_Constant.JS * self.frequency

    def eV(self) -> Union[np.ndarray, float]:
        """return Energy in [eV] unit"""

        return Plancks_Constant.eVS * self.frequency
