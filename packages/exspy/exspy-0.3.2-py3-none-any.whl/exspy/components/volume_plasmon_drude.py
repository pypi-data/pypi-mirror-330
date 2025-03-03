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

import numpy as np

import hyperspy.api as hs

from exspy._utils import parse_component_module


class VolumePlasmonDrude(hs.model.components1D.Expression):
    r"""
    Drude volume plasmon energy loss function component, the energy loss
    function is defined as:

    .. math::

       f(E) = I_0 \frac{E(\Delta E_p)E_p^2}{(E^2-E_p^2)^2+(E\Delta E_p)^2}

    ================== ===============
    Variable            Parameter
    ================== ===============
    :math:`I_0`         intensity
    :math:`E_p`         plasmon_energy
    :math:`\Delta E_p`  fwhm
    ================== ===============

    Parameters
    ----------
    intensity : float
    plasmon_energy : float
    fwhm : float
    **kwargs
        Extra keyword arguments are passed to the
        :py:class:`hyperspy._components.expression.Expression` component.

    Notes
    -----
    Refer to Egerton, R. F., Electron Energy-Loss Spectroscopy in the
    Electron Microscope, 2nd edition, Plenum Press 1996, pp. 154-158
    for details, including original equations.
    """

    def __init__(
        self,
        intensity=1.0,
        plasmon_energy=15.0,
        fwhm=1.5,
        module="numexpr",
        compute_gradients=False,
        **kwargs,
    ):
        super().__init__(
            expression="where(x > 0, intensity * (pe2 * x * fwhm) \
                        / ((x ** 2 - pe2) ** 2 + (x * fwhm) ** 2), 0); \
                        pe2 = plasmon_energy ** 2",
            name="VolumePlasmonDrude",
            intensity=intensity,
            plasmon_energy=plasmon_energy,
            fwhm=fwhm,
            position="plasmon_energy",
            module=parse_component_module(module),
            autodoc=False,
            compute_gradients=compute_gradients,
            linear_parameter_list=["intensity"],
            check_parameter_linearity=False,
            **kwargs,
        )

    # Partial derivative with respect to the plasmon energy E_p
    def grad_plasmon_energy(self, x):
        plasmon_energy = self.plasmon_energy.value
        fwhm = self.fwhm.value
        intensity = self.intensity.value

        return np.where(
            x > 0,
            2
            * x
            * fwhm
            * plasmon_energy
            * intensity
            * (
                (x**4 + (x * fwhm) ** 2 - plasmon_energy**4)
                / (x**4 + x**2 * (fwhm**2 - 2 * plasmon_energy**2) + plasmon_energy**4)
                ** 2
            ),
            0,
        )

    # Partial derivative with respect to the plasmon linewidth delta_E_p
    def grad_fwhm(self, x):
        plasmon_energy = self.plasmon_energy.value
        fwhm = self.fwhm.value
        intensity = self.intensity.value

        return np.where(
            x > 0,
            x
            * plasmon_energy
            * intensity
            * (
                (x**4 - x**2 * (2 * plasmon_energy**2 + fwhm**2) + plasmon_energy**4)
                / (x**4 + x**2 * (fwhm**2 - 2 * plasmon_energy**2) + plasmon_energy**4)
                ** 2
            ),
            0,
        )

    def grad_intensity(self, x):
        return self.function(x) / self.intensity.value
