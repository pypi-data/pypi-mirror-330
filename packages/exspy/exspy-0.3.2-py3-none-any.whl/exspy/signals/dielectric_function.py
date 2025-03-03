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
from scipy import constants
from scipy.integrate import simpson, cumulative_trapezoid

from hyperspy._signals.complex_signal1d import (
    ComplexSignal1D,
    LazyComplexSignal1D,
)
from hyperspy.docstrings.signal import LAZYSIGNAL_DOC
from exspy._misc.eels.tools import eels_constant


class DielectricFunction(ComplexSignal1D):
    """Signal class for dielectric functions."""

    _signal_type = "DielectricFunction"
    _alias_signal_types = ["dielectric function"]

    def get_number_of_effective_electrons(self, nat, cumulative=False):
        r"""
        Compute the number of effective electrons using the Bethe f-sum
        rule.

        The Bethe f-sum rule gives rise to two definitions of the effective
        number (see [*]_), neff1 and neff2:

        .. math::

            n_{\mathrm{eff_{1}}} = n_{\mathrm{eff}}\left(-\Im\left(\epsilon^{-1}\right)\right)

        and:

        .. math::

            n_{\mathrm{eff_{2}}} = n_{\mathrm{eff}}\left(\epsilon_{2}\right)

        This method computes and return both.

        Parameters
        ----------
        nat : float
            Number of atoms (or molecules) per unit volume of the sample.

        Returns
        -------
        neff1, neff2 : :py:class:`hyperspy.api.signals.Signal1D`
            Signal1D instances containing neff1 and neff2. The signal and
            navigation dimensions are the same as the current signal if
            `cumulative` is True, otherwise the signal dimension is 0
            and the navigation dimension is the same as the current
            signal.

        Notes
        -----
        .. [*] Ray Egerton, "Electron Energy-Loss Spectroscopy
           in the Electron Microscope", Springer-Verlag, 2011.

        """

        m0 = constants.value("electron mass")
        epsilon0 = constants.epsilon_0  # Vacuum permittivity [F/m]
        hbar = constants.hbar  # Reduced Plank constant [J·s]
        k = 2 * epsilon0 * m0 / (np.pi * nat * hbar**2)

        axis = self.axes_manager.signal_axes[0]
        if cumulative is False:
            dneff1 = k * simpson(
                (-1.0 / self.data).imag * axis.axis,
                x=axis.axis,
                axis=axis.index_in_array,
            )
            dneff2 = k * simpson(
                self.data.imag * axis.axis, x=axis.axis, axis=axis.index_in_array
            )
            neff1 = self._get_navigation_signal(data=dneff1)
            neff2 = self._get_navigation_signal(data=dneff2)
        else:
            neff1 = self._deepcopy_with_new_data(
                k
                * cumulative_trapezoid(
                    (-1.0 / self.data).imag * axis.axis,
                    x=axis.axis,
                    axis=axis.index_in_array,
                    initial=0,
                )
            )
            neff2 = self._deepcopy_with_new_data(
                k
                * cumulative_trapezoid(
                    self.data.imag * axis.axis,
                    x=axis.axis,
                    axis=axis.index_in_array,
                    initial=0,
                )
            )

        # Prepare return
        neff1.metadata.General.title = (
            r"$n_{\mathrm{eff}}\left(-\Im\left(\epsilon^{-1}\right)\right)$ "
            "calculated from "
            + self.metadata.General.title
            + " using the Bethe f-sum rule."
        )
        neff2.metadata.General.title = (
            r"$n_{\mathrm{eff}}\left(\epsilon_{2}\right)$ "
            "calculated from "
            + self.metadata.General.title
            + " using the Bethe f-sum rule."
        )

        return neff1, neff2

    def get_electron_energy_loss_spectrum(self, zlp, t):
        """
        Compute single-scattering electron-energy loss spectrum from
        the dielectric function.

        Parameters
        ----------
        zlp: float or :py:class:`hyperspy.api.signals.BaseSignal`
            If the ZLP is the same for all spectra, the intengral of the ZLP
            can be provided as a number. Otherwise, if the ZLP intensity is not
            the same for all spectra, it can be provided as i) a Signal
            of the same dimensions as the current signal containing the ZLP
            spectra for each location ii) a Signal of signal dimension 0
            and navigation_dimension equal to the current signal containing the
            integrated ZLP intensity.
        t: None, float or :py:class:`hyperspy.api.signals.BaseSignal`
            The sample thickness in nm. If the thickness is the same for all
            spectra it can be given by a number. Otherwise, it can be provided
            as a Signal with signal dimension 0 and navigation_dimension equal
            to the current signal.

        Returns
        -------
        :py:class:`hyperspy.api.signals.BaseSignal`
        """
        for axis in self.axes_manager.signal_axes:
            if not axis.is_uniform:
                raise NotImplementedError(
                    "The function is not implemented for non-uniform axes."
                )
        data = (
            (-1 / self.data).imag
            * eels_constant(self, zlp, t).data
            * self.axes_manager.signal_axes[0].scale
        )
        s = self._deepcopy_with_new_data(data)
        s.data = s.data.real
        s.set_signal_type("EELS")
        s.metadata.General.title = "EELS calculated from " + self.metadata.General.title
        return s


class LazyDielectricFunction(DielectricFunction, LazyComplexSignal1D):
    """Lazy signal class for dielectric functions."""

    __doc__ += LAZYSIGNAL_DOC.replace("__BASECLASS__", "DielectricFunction")
