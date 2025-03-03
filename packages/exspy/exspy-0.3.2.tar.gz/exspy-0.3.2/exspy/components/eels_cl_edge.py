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


import functools
import logging
import warnings
import math

import numpy as np
from scipy.interpolate import splev

from hyperspy.component import Component
from exspy._misc.eels.gosh_gos import GoshGOS, _GOSH_SOURCES
from exspy._misc.eels.hartree_slater_gos import HartreeSlaterGOS
from exspy._misc.eels.hydrogenic_gos import HydrogenicGOS
from exspy._misc.eels.effective_angle import effective_angle
from hyperspy.ui_registry import add_gui_method
from hyperspy.exceptions import VisibleDeprecationWarning

_logger = logging.getLogger(__name__)


class FSet(set):
    def __init__(self, component, *args, **kwargs):
        """Creates a set that knows about the Component

        Parameters:
        -----------
        component : Component
            The component to which the FSet belongs.
        """
        self.component = component
        super().__init__(*args, **kwargs)

    @functools.wraps(set.add)
    def add(self, item):
        item.active = self.component.fine_structure_active
        if self.component.model and item not in self.component.model:
            self.component.model.append(item)
        super().add(item)

    @functools.wraps(set.update)
    def update(self, iterable):
        for item in iterable:
            item.active = self.component.fine_structure_active
            if self.component.model and item not in self.component.model:
                self.component.model.append(item)
        super().update(iterable)


@add_gui_method(toolkey="exspy.EELSCLEdge_Component")
class EELSCLEdge(Component):
    """
    EELS core loss ionisation edge from hydrogenic or tabulated
    GOS with splines for fine structure fitting.

    Hydrogenic GOS are limited to K and L shells.

    Several possibilities are available for tabulated GOS.

    The preferred option is to use a database of cross sections in GOSH
    format. One such database can be freely downloaded from Zenodo at:
    https://doi.org/%s while information on the GOSH format are available at: https://gitlab.com/gguzzina/gosh. Alternatively,
    one can use the Dirac GOSH database to include relativistic effects,
    available at: https://doi.org/%s.

    eXSpy also supports Peter Rez's Hartree Slater cross sections
    parametrised as distributed by Gatan in their Digital Micrograph (DM)
    software. If Digital Micrograph is installed in the system in the
    standard location, eXSpy should find the path to the HS GOS folder.
    Otherwise, the location of the folder can be defined in the eXSpy
    preferences, which can be done through :func:`hyperspy.api.preferences.gui` or
    the :attr:`hyperspy.api.preferences.EELS.eels_gos_files_path` variable.

    Parameters
    ----------
    element_subshell : str or dict
        Usually a string, for example, ``'Ti_L3'`` for the GOS of the titanium L3
        subshell. If a dictionary is passed, it is assumed that Hartree Slater
        GOS was exported using `GOS.as_dictionary`, and will be reconstructed.
    GOS : ``'dft'``,``'dirac'``, ``'hydrogenic'``, ``'Hartree-Slater'`` or str
        The GOS to use. Default is ``'dft'``. If str, it must the path to gosh GOS file.
        The ``'dft'`` and ``'dirac'`` databases are in the ``'gosh'`` format.
    gos_file_path : str, None
        Only with ``GOS='dft' or 'dirac'``. Specify the file path of the gosh file
        to use. If None, use the file from  https://doi.org/%s

    Attributes
    ----------
    onset_energy : Parameter
        The edge onset position
    intensity : Parameter
        The factor by which the cross section is multiplied, what in
        favourable cases is proportional to the number of atoms of
        the element. It is a component.Parameter instance.
        It is fixed by default.
    effective_angle : Parameter
        The effective collection semi-angle. It is automatically
        calculated by ``set_microscope_parameters``. It is a
        component.Parameter instance. It is fixed by default.
    fine_structure_active : bool, default False
        Activates/deactivates the fine structure features. When active,
        the fine structure region
        is not defined by the simulated
        EELS core-loss edge, but by a spline (if ``fine_structure_spline_active``
        is ``True``) and/or any component in ``fine_structure_components``.
    fine_structure_spline_active : bool, default True
        If True and ``fine_structure_active`` is True, the region from
        ``fine_structure_spline_onset`` until ``fine_structure_width``
        are modelled with a spline.
    fine_structure_coeff : Parameter
        The coefficients of the spline that fits the fine structure.
        Fix this parameter to fix the fine structure. It is a
        ``component.Parameter`` instance.
    fine_structure_smoothing : float between 0 and 1, default 0.3
        Controls the level of smoothing of the fine structure model.
        Decreasing the value increases the level of smoothing.
    fine_structure_spline_onset : float, default 0.
        The position, from the ionization edge onset, at which the region
        modelled by the spline function starts.
    fine_structure_width : float, default 30.
        The width of the energy region, from the ionization edge onset, where
        the model is a spline function and/or any component
        in ``fine_structure_components`` instead of the EELS ionization
        edges simulation.
    fine_structure_components : set, default ``set()``
        A set containing components to model the fine structure region
        of the EELS ionization edge.
    """

    _fine_structure_smoothing = 0.3
    _fine_structure_coeff_free = True
    _fine_structure_spline_active = True

    def __init__(self, element_subshell, GOS="dft", gos_file_path=None):
        # Declare the parameters
        self.fine_structure_components = FSet(component=self)
        Component.__init__(
            self,
            ["intensity", "fine_structure_coeff", "effective_angle", "onset_energy"],
            linear_parameter_list=["intensity"],
        )
        if isinstance(element_subshell, dict):
            self.element = element_subshell["element"]
            self.subshell = element_subshell["subshell"]
        else:
            self.element, self.subshell = element_subshell.split("_")
        self.name = "_".join([self.element, self.subshell])
        self.energy_scale = None
        self.effective_angle.free = False
        self.fine_structure_active = False
        self.fine_structure_width = 30.0
        self.fine_structure_coeff.ext_force_positive = False
        self.GOS = None

        if GOS == "gosh":
            warnings.warn(
                "The value 'gosh' of the `GOS` parameter has been renamed to 'dft' in "
                "eXSpy 0.3.0, use `GOS='dft'` instead. "
                "Using `GOS='gosh'` will stop working in eXSpy 1.0.",
                VisibleDeprecationWarning,
            )
            GOS = "dft"
        if GOS == "dft":
            self.GOS = GoshGOS(
                element_subshell, gos_file_path=gos_file_path, source="dft"
            )
        elif GOS == "dirac":
            self.GOS = GoshGOS(
                element_subshell, gos_file_path=gos_file_path, source="dirac"
            )
        elif GOS == "Hartree-Slater":  # pragma: no cover
            self.GOS = HartreeSlaterGOS(element_subshell)
        elif GOS == "hydrogenic":
            self.GOS = HydrogenicGOS(element_subshell)
        else:
            raise ValueError(
                "GOS must be one of 'dft', 'dirac','hydrogenic' or 'Hartree-Slater'."
            )
        self.onset_energy.value = self.GOS.onset_energy
        self.onset_energy.free = False
        self._position = self.onset_energy
        self.free_onset_energy = False
        self.intensity.grad = self.grad_intensity
        self.intensity.value = 1
        self.intensity.bmin = 0.0
        self.intensity.bmax = None

        self._whitelist["GOS"] = ("init", GOS)
        if GOS == "dft":
            self._whitelist["element_subshell"] = ("init", self.GOS.as_dictionary(True))
        elif GOS == "dirac":
            self._whitelist["element_subshell"] = ("init", self.GOS.as_dictionary(True))
        elif GOS == "Hartree-Slater":  # pragma: no cover
            self._whitelist["element_subshell"] = ("init", self.GOS.as_dictionary(True))
        elif GOS == "hydrogenic":
            self._whitelist["element_subshell"] = ("init", element_subshell)
        self._whitelist["fine_structure_active"] = None
        self._whitelist["fine_structure_width"] = None
        self._whitelist["fine_structure_smoothing"] = None
        self._whitelist["fine_structure_spline_onset"] = None
        self._whitelist["fine_structure_spline_active"] = None
        self._whitelist["_fine_structure_coeff_free"] = None
        self.effective_angle.events.value_changed.connect(self._integrate_GOS, [])
        self.onset_energy.events.value_changed.connect(self._integrate_GOS, [])
        self.onset_energy.events.value_changed.connect(self._calculate_knots, [])
        self._fine_structure_spline_onset = 0
        self.events.active_changed.connect(self._set_active_fine_structure_components)

    # Automatically fix the fine structure when the fine structure is
    # disable.
    # In this way we avoid a common source of problems when fitting
    # However the fine structure must be *manually* freed when we
    # reactivate the fine structure.
    @property
    def fine_structure_active(self):
        return self.__fine_structure_active

    @fine_structure_active.setter
    def fine_structure_active(self, arg):
        if self.fine_structure_spline_active:
            if arg:
                self.fine_structure_coeff.free = self._fine_structure_coeff_free
            else:
                self._fine_structure_coeff_free = self.fine_structure_coeff.free
                self.fine_structure_coeff.free = False
        for comp in self.fine_structure_components:
            if isinstance(comp, str):
                # Loading from a dictionary and the external fine structure components are still strings
                break
            comp.active = arg
        self.__fine_structure_active = arg
        if self.fine_structure_spline_active and self.model:
            self.model.update_plot()

    @property
    def fine_structure_width(self):
        return self.__fine_structure_width

    @fine_structure_width.setter
    def fine_structure_width(self, arg):
        self.__fine_structure_width = arg
        self._set_fine_structure_coeff()
        if self.fine_structure_active and self.model:
            self.model.update_plot()

    # E0
    @property
    def E0(self):
        return self.__E0

    @E0.setter
    def E0(self, arg):
        self.__E0 = arg
        self._calculate_effective_angle()

    @property
    def collection_angle(self):
        return self.__collection_angle

    @collection_angle.setter
    def collection_angle(self, arg):
        self.__collection_angle = arg
        self._calculate_effective_angle()

    @property
    def convergence_angle(self):
        return self.__convergence_angle

    @convergence_angle.setter
    def convergence_angle(self, arg):
        self.__convergence_angle = arg
        self._calculate_effective_angle()

    def _calculate_effective_angle(self):
        try:
            self.effective_angle.value = effective_angle(
                self.E0,
                self.GOS.onset_energy,
                self.convergence_angle,
                self.collection_angle,
            )
        except BaseException:
            # All the parameters may not be defined yet...
            pass

    def _set_active_fine_structure_components(self, active, **kwargs):
        if not self.fine_structure_active:
            return
        for comp in self.fine_structure_components:
            comp.active = active

    @property
    def fine_structure_smoothing(self):
        return self._fine_structure_smoothing

    @fine_structure_smoothing.setter
    def fine_structure_smoothing(self, value):
        if 0 <= value <= 1:
            self._fine_structure_smoothing = value
            self._set_fine_structure_coeff()
            if self.fine_structure_active and self.model:
                self.model.update_plot()
        else:
            raise ValueError("The value must be a number between 0 and 1")

    # It is needed because the property cannot be used to sort the edges
    def _onset_energy(self):
        return self.onset_energy.value

    @property
    def fine_structure_spline_onset(self):
        return self._fine_structure_spline_onset

    @fine_structure_spline_onset.setter
    def fine_structure_spline_onset(self, value):
        if not np.allclose(value, self._fine_structure_spline_onset):
            self._fine_structure_spline_onset = value
            self._set_fine_structure_coeff()
            if self.fine_structure_active and self.model:
                self.model.update_plot()

    @property
    def fine_structure_spline_active(self):
        return self._fine_structure_spline_active

    @fine_structure_spline_active.setter
    def fine_structure_spline_active(self, value):
        if value:
            if self.fine_structure_active:
                self.fine_structure_coeff.free = self._fine_structure_coeff_free
            self._fine_structure_spline_active = value
        else:
            self._fine_structure_coeff_free = self.fine_structure_coeff.free
            self.fine_structure_coeff.free = False
            self._fine_structure_spline_active = value
        if self.fine_structure_active and self.model:
            self.model.update_plot()

    def _set_fine_structure_coeff(self):
        if self.energy_scale is None:
            return
        self.fine_structure_coeff._number_of_elements = (
            int(
                round(
                    self.fine_structure_smoothing
                    * (self.fine_structure_width - self.fine_structure_spline_onset)
                    / self.energy_scale
                )
            )
            + 4
        )
        self.fine_structure_coeff.bmin = None
        self.fine_structure_coeff.bmax = None
        self._calculate_knots()
        if self.fine_structure_coeff.map is not None:
            self.fine_structure_coeff._create_array()

    def fix_fine_structure(self):
        """Fixes the fine structure spline and the parameters of the fine
        structure components, if any.

        See Also
        --------
        free_fine_structure

        """
        self.fine_structure_coeff.free = False
        for component in self.fine_structure_components:
            component._auto_free_parameters = []
            for parameter in component.free_parameters:
                parameter.free = False
                component._auto_free_parameters.append(parameter)

    def free_fine_structure(self):
        """Frees the parameters of the fine structure

        If there are fine structure components, only the
        parameters that have been previously fixed with
        ``fix_fine_structure`` will be set free.

        The spline parameters set free only if
        ``fine_structure_spline_active`` is ``True``.

        See Also
        --------
        free_fine_structure

        """
        if self.fine_structure_spline_active:
            self.fine_structure_coeff.free = True
        for component in self.fine_structure_components:
            if hasattr(component, "_auto_free_parameters"):
                for parameter in component._auto_free_parameters:
                    parameter.free = True
                del component._auto_free_parameters

    def set_microscope_parameters(self, E0, alpha, beta, energy_scale):
        """
        Set the microscope parameters.

        Parameters
        ----------
        E0 : float
            Electron beam energy in keV.
        alpha: float
            Convergence semi-angle in mrad.
        beta: float
            Collection semi-angle in mrad.
        energy_scale : float
            The energy step in eV.
        """
        # Relativistic correction factors
        old = self.effective_angle.value
        with self.effective_angle.events.value_changed.suppress_callback(
            self._integrate_GOS
        ):
            self.convergence_angle = alpha
            self.collection_angle = beta
            self.energy_scale = energy_scale
            self.E0 = E0
        if self.effective_angle.value != old:
            self._integrate_GOS()

    def _integrate_GOS(self):
        # Integration over q using splines
        angle = self.effective_angle.value * 1e-3  # in rad
        self.tab_xsection = self.GOS.integrateq(self.onset_energy.value, angle, self.E0)
        # Calculate extrapolation powerlaw extrapolation parameters
        E1 = self.GOS.energy_axis[-2] + self.GOS.energy_shift
        E2 = self.GOS.energy_axis[-1] + self.GOS.energy_shift
        y1 = self.GOS.qint[-2]  # in m**2/bin */
        y2 = self.GOS.qint[-1]  # in m**2/bin */
        self._power_law_r = math.log(y2 / y1) / math.log(E1 / E2)
        self._power_law_A = y1 / E1**-self._power_law_r

    def _calculate_knots(self):
        start = self.onset_energy.value
        stop = start + self.fine_structure_width
        self.__knots = np.r_[
            [start] * 4,
            np.linspace(start, stop, self.fine_structure_coeff._number_of_elements)[
                2:-2
            ],
            [stop] * 4,
        ]

    def function(self, E):
        """Returns the number of counts in barns"""
        shift = self.onset_energy.value - self.GOS.onset_energy
        if shift != self.GOS.energy_shift:
            # Because hspy Events are not executed in any given order,
            # an external function could be in the same event execution list
            # as _integrate_GOS and be executed first. That can potentially
            # cause an error that enforcing _integrate_GOS here prevents. Note
            # that this is suboptimal because _integrate_GOS is computed twice
            # unnecessarily.
            self._integrate_GOS()
        Emax = self.GOS.energy_axis[-1] + self.GOS.energy_shift
        cts = np.zeros_like(E, dtype="float")
        if self.fine_structure_active:
            ifsx1 = self.onset_energy.value + self.fine_structure_spline_onset
            ifsx2 = self.onset_energy.value + self.fine_structure_width
            if self.fine_structure_spline_active:
                bifs = (E >= ifsx1) & (E < ifsx2)
                # Only set the spline values if the spline is in the energy region
                if np.any(bifs):
                    cts[bifs] = splev(
                        E[bifs],
                        (self.__knots, self.fine_structure_coeff.value + (0,) * 4, 3),
                    )
            # The cross-section is set to 0 in the fine structure region
            itab = (E < Emax) & (E >= ifsx2)
        else:
            itab = (E < Emax) & (E >= self.onset_energy.value)
        if itab.any():
            cts[itab] = self.tab_xsection(E[itab])
        bext = E >= Emax
        if bext.any():
            cts[bext] = self._power_law_A * E[bext] ** -self._power_law_r
        return cts * self.intensity.value

    def grad_intensity(self, E):
        return self.function(E) / self.intensity.value

    def fine_structure_coeff_to_txt(self, filename):
        np.savetxt(filename + ".dat", self.fine_structure_coeff.value, fmt="%12.6G")

    def txt_to_fine_structure_coeff(self, filename):
        fs = np.loadtxt(filename)
        self._calculate_knots()
        if len(fs) == len(self.__knots):
            self.fine_structure_coeff.value = fs
        else:
            raise ValueError(
                "The provided fine structure file "
                "doesn't match the size of the current fine structure"
            )

    def get_fine_structure_as_signal1D(self):
        """
        Returns a spectrum containing the fine structure.

        Notes
        -----
        The fine structure is corrected from multiple scattering if
        the model was convolved with a low-loss spectrum

        """
        from exspy.signals.eels import EELSSpectrum

        channels = int(np.floor(self.fine_structure_width / self.energy_scale))
        data = np.zeros(self.fine_structure_coeff.map.shape + (channels,))
        s = EELSSpectrum(data, axes=self.intensity._axes_manager._get_axes_dicts())
        s.get_dimensions_from_data()
        s.axes_manager.signal_axes[0].offset = self.onset_energy.value
        # Backup the axes_manager
        original_axes_manager = self._axes_manager
        self._axes_manager = s.axes_manager
        for spectrum in s:
            self.fetch_stored_values()
            spectrum.data[:] = self.function(s.axes_manager.signal_axes[0].axis)
        # Restore the axes_manager and the values
        self._axes_manager = original_axes_manager
        self.fetch_stored_values()

        s.metadata.General.title = self.name.replace("_", " ") + " fine structure"

        return s

    def as_dictionary(self, fullcopy=True):
        dic = super().as_dictionary(fullcopy=fullcopy)
        dic["fine_structure_components"] = [
            t.name for t in self.fine_structure_components
        ]
        dic["_whitelist"]["fine_structure_components"] = ""
        return dic


EELSCLEdge.__doc__ %= (
    _GOSH_SOURCES["dft"]["DOI"],
    _GOSH_SOURCES["dirac"]["DOI"],
    _GOSH_SOURCES["dft"]["DOI"],
)
