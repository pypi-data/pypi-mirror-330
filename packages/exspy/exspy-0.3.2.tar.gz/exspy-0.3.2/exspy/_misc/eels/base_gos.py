# -*- coding: utf-8 -*-
# Copyright 2007-2024 The eXSpy developers
#
# This file is part of eXSpy.
#
# eXSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# eXSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with eXSpy. If not, see <https://www.gnu.org/licenses/#GPL>.


import math

import numpy as np
from scipy import constants, integrate, interpolate

from exspy._misc.elements import elements
from hyperspy.misc.export_dictionary import (
    export_to_dictionary,
    load_from_dictionary,
)
from hyperspy.misc.math_tools import get_linear_interpolation


R = constants.value("Rydberg constant times hc in eV")
a0 = constants.value("Bohr radius")


class BaseGOS:
    def read_elements(self):
        element = self.element
        subshell = self.subshell
        # Convert to the "GATAN" nomenclature
        if (element in elements) is not True:
            raise ValueError(f"The given element {element} is not in the database.")
        elif subshell not in elements[element]["Atomic_properties"]["Binding_energies"]:
            subshells = ", ".join(
                list(elements[element]["Atomic_properties"]["Binding_energies"].keys())
            )
            raise ValueError(
                f"The given subshell {subshell} is not in the database. The "
                f"available subshells are:\n{subshells}"
            )

        self.onset_energy = elements[element]["Atomic_properties"]["Binding_energies"][
            subshell
        ]["onset_energy (eV)"]
        self.Z = elements[element]["General_properties"]["Z"]
        self.element_dict = elements[element]

    def get_parametrized_qaxis(self, k1, k2, n):
        return k1 * (np.exp(np.arange(n) * k2) - 1) * 1e10

    def get_parametrized_energy_axis(self, k1, k2, n):
        return k1 * (np.exp(np.arange(n) * k2 / k1) - 1)

    def get_qaxis_and_gos(self, ienergy, qmin, qmax):
        qgosi = self.gos_array[ienergy, :]
        if qmax > self.qaxis[-1]:
            # Linear extrapolation
            g1, g2 = qgosi[-2:]
            q1, q2 = self.qaxis[-2:]
            gosqmax = get_linear_interpolation((q1, g1), (q2, g2), qmax)
            qaxis = np.hstack((self.qaxis, qmax))
            qgosi = np.hstack((qgosi, gosqmax))
        else:
            index = self.qaxis.searchsorted(qmax)
            g1, g2 = qgosi[index - 1 : index + 1]
            q1, q2 = self.qaxis[index - 1 : index + 1]
            gosqmax = get_linear_interpolation((q1, g1), (q2, g2), qmax)
            qaxis = np.hstack((self.qaxis[:index], qmax))
            qgosi = np.hstack((qgosi[:index,], gosqmax))

        if qmin > 0:
            index = self.qaxis.searchsorted(qmin)
            g1, g2 = qgosi[index - 1 : index + 1]
            q1, q2 = qaxis[index - 1 : index + 1]
            gosqmin = get_linear_interpolation((q1, g1), (q2, g2), qmin)
            qaxis = np.hstack((qmin, qaxis[index:]))
            qgosi = np.hstack(
                (
                    gosqmin,
                    qgosi[index:],
                )
            )
        return qaxis, qgosi.clip(0)


class TabulatedGOS(BaseGOS):
    def __init__(self, element_subshell):
        """
        Parameters
        ----------
        element_subshell : str
            For example, 'Ti_L3' for the GOS of the titanium L3 subshell

        """
        self.subshell_factor = 1.0
        if isinstance(element_subshell, dict):
            self.element = element_subshell["element"]
            self.subshell = element_subshell["subshell"]
            self.read_elements()
            self._load_dictionary(element_subshell)
        else:
            self.element, self.subshell = element_subshell.split("_")
            self.read_elements()
            self.read_gos_data()

    def _load_dictionary(self, dictionary):
        load_from_dictionary(self, dictionary)
        self.energy_axis = self.rel_energy_axis + self.onset_energy

    def as_dictionary(self, fullcopy=True):
        """Export the GOS as a dictionary."""
        dic = {}
        export_to_dictionary(self, self._whitelist, dic, fullcopy)
        return dic

    def integrateq(self, onset_energy, angle, E0):
        energy_shift = onset_energy - self.onset_energy
        self.energy_shift = energy_shift
        qint = np.zeros((self.energy_axis.shape[0]))
        # Calculate the cross section at each energy position of the
        # tabulated GOS
        gamma = 1 + E0 / 511.06
        T = 511060 * (1 - 1 / gamma**2) / 2
        for i in range(0, self.gos_array.shape[0]):
            E = self.energy_axis[i] + energy_shift
            # Calculate the limits of the q integral
            qa0sqmin = (E**2) / (4 * R * T) + (E**3) / (8 * gamma**3 * R * T**2)
            p02 = T / (R * (1 - 2 * T / 511060))
            pp2 = p02 - E / R * (gamma - E / 1022120)
            qa0sqmax = qa0sqmin + 4 * np.sqrt(p02 * pp2) * (math.sin(angle / 2)) ** 2
            qmin = math.sqrt(qa0sqmin) / a0
            qmax = math.sqrt(qa0sqmax) / a0
            # Perform the integration in a log grid
            qaxis, gos = self.get_qaxis_and_gos(i, qmin, qmax)
            logsqa0qaxis = np.log((a0 * qaxis) ** 2)
            qint[i] = integrate.simpson(gos, x=logsqa0qaxis)
        E = self.energy_axis + energy_shift
        # Energy differential cross section in (barn/eV/atom)
        qint *= (4.0 * np.pi * a0**2.0 * R**2 / E / T * self.subshell_factor) * 1e28
        self.qint = qint
        return interpolate.make_interp_spline(E, qint, k=3)
