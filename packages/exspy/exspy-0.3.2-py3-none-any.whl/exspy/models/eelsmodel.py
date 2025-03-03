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

import copy
import logging
import warnings

from hyperspy import components1d
from hyperspy.components1d import PowerLaw
from hyperspy.docstrings.model import FIT_PARAMETERS_ARG
from hyperspy.misc.utils import dummy_context_manager
from hyperspy.misc.axis_tools import calculate_convolution1D_axis
from hyperspy.models.model1d import Model1D

from exspy._docstrings.model import EELSMODEL_PARAMETERS
from exspy.components import EELSCLEdge
from exspy.signals.eels import EELSSpectrum


_logger = logging.getLogger(__name__)


class EELSModel(Model1D):
    def __init__(
        self,
        signal1D,
        auto_background=True,
        auto_add_edges=True,
        low_loss=None,
        GOS="dft",
        dictionary=None,
        gos_file_path=None,
    ):
        """
        Build an EELS model.

        Parameters
        ----------
        GOS : Generalized Oscillator Strength, availiable option in ['hydrogenic', 'dft', 'dirac', 'Hartree-Slater'], default is 'dft'.
        spectrum : a EELSSpectrum instance
        %s

        """
        super().__init__(signal1D)

        # When automatically setting the fine structure energy regions,
        # the fine structure of an EELS edge component is automatically
        # disable if the next ionisation edge onset distance to the
        # higher energy side of the fine structure region is lower that
        # the value of this parameter
        self._min_distance_between_edges_for_fine_structure = 0
        self._preedge_safe_window_width = 2
        self._suspend_auto_fine_structure_width = False
        self._low_loss = None
        self._convolved = False
        self._convolution_axis = None
        self.low_loss = low_loss
        self.GOS = GOS
        self.gos_file_path = gos_file_path
        self.edges = []
        self._background_components = []
        self._whitelist.update(
            {
                "_convolved": None,
                "low_loss": ("sig", None),
            }
        )
        self._slicing_whitelist["low_loss"] = "inav"
        if dictionary is not None:
            auto_background = False
            auto_add_edges = False
            self._load_dictionary(dictionary)
            for edge in self.edges:
                fine_structure_components = set()
                for comp_name in edge.fine_structure_components:
                    fine_structure_components.add(self[comp_name])
                edge.fine_structure_components = fine_structure_components

        if auto_background is True:
            background = PowerLaw()
            self.append(background)

        if self.signal.subshells and auto_add_edges is True:
            self._add_edges_from_subshells_names()

    __init__.__doc__ %= EELSMODEL_PARAMETERS

    @property
    def convolution_axis(self):
        _logger.warning("The `convolution_axis` attribute has been privatized.")
        return self._convolution_axis

    @convolution_axis.setter
    def convolution_axis(self, value):
        _logger.warning("The `convolution_axis` attribute has been privatized.")
        self._convolution_axis = value

    @property
    def signal(self):
        return self._signal

    @signal.setter
    def signal(self, value):
        if isinstance(value, EELSSpectrum):
            self._signal = value
        else:
            raise ValueError(
                "This attribute can only contain an EELSSpectrum "
                "but an object of type %s was provided" % str(type(value))
            )

    @property
    def convolved(self):
        return self._convolved

    @convolved.setter
    def convolved(self, value):
        if isinstance(value, bool):
            if value is not self._convolved:
                if value and not self.low_loss:
                    raise RuntimeError(
                        "Cannot set `convolved` to True as the "
                        "`low_loss` attribute"
                        "is not set."
                    )
                else:
                    self._convolved = value
                    self.update_plot()
        else:
            raise ValueError("`convolved` must be a boolean.")

    @property
    def low_loss(self):
        return self._low_loss

    @low_loss.setter
    def low_loss(self, value):
        if value is not None:
            if (
                value.axes_manager.navigation_shape
                != self.signal.axes_manager.navigation_shape
            ):
                raise ValueError(
                    "The signal does not have the same navigation dimension "
                    "as the signal it will be convolved with."
                )
            if not value.axes_manager.signal_axes[0].is_uniform:
                raise ValueError(
                    "Convolution is not supported with non-uniform signal axes."
                )
            self._low_loss = value
            self._set_convolution_axis()
            self.convolved = True
        else:
            self._low_loss = value
            self._convolution_axis = None
            self.convolved = False

    # Extend the list methods to call the _touch when the model is modified

    def set_convolution_axis(self):
        _logger.warning("The `set_convolution_axis` method has been privatized.")
        self._set_convolution_axis()

    def _set_convolution_axis(self):
        """
        Creates an axis to use when calculating the values of convolved
        components. The scale and offset are calculated so that there is
        suitable padding before taking the convolution - see hyperspy
        documentation on convolution implementation.
        """
        self._convolution_axis = calculate_convolution1D_axis(
            self.axes_manager.signal_axes[0], self._low_loss.axes_manager.signal_axes[0]
        )

    @property
    def _signal_to_convolve(self):
        # Used in hyperspy
        return self._low_loss

    def append(self, component):
        """Append component to EELS model.

        Parameters
        ----------
        component
            HyperSpy component1D object.

        Raises
        ------
        NotImplementedError
            If the signal axis is a non-uniform axis.
        """
        super().append(component)
        if isinstance(component, EELSCLEdge):
            # Test that signal axis is uniform
            if not self.axes_manager[-1].is_uniform:
                raise NotImplementedError(
                    "This operation is not yet implemented for non-uniform energy axes"
                )
            tem = self.signal.metadata.Acquisition_instrument.TEM
            component.set_microscope_parameters(
                E0=tem.beam_energy,
                alpha=tem.convergence_angle,
                beta=tem.Detector.EELS.collection_angle,
                energy_scale=self.axis.scale,
            )
            component.energy_scale = self.axis.scale
            component._set_fine_structure_coeff()
        self._classify_components()

    append.__doc__ = Model1D.append.__doc__

    def remove(self, component):
        super().remove(component)
        self._classify_components()

    remove.__doc__ = Model1D.remove.__doc__

    def _classify_components(self):
        """Classify components between background and ionization edge
        components.

        This method should be called every time that components are added and
        removed. An ionization edge becomes background when its onset falls to
        the left of the first non-masked energy channel. The ionization edges
        are stored in a list in the `edges` attribute. They are sorted by
        increasing `onset_energy`. The background components are stored in
        `_background_components`.

        """
        self.edges = []
        self._background_components = []
        for component in self:
            if isinstance(component, EELSCLEdge):
                if (
                    component.onset_energy.value
                    < self.axis.axis[self._channel_switches][0]
                ):
                    component.isbackground = True
                if component.isbackground is not True:
                    self.edges.append(component)
                else:
                    component.fine_structure_active = False
                    component.fine_structure_coeff.free = False
            elif isinstance(component, PowerLaw) or component.isbackground is True:
                self._background_components.append(component)

        if self.edges:
            self.edges.sort(key=EELSCLEdge._onset_energy)
            self.resolve_fine_structure()
        if len(self._background_components) > 1:
            self._backgroundtype = "mix"
        elif len(self._background_components) == 1:
            self._backgroundtype = self._background_components[0].__repr__()
            bg = self._background_components[0]
            if isinstance(bg, PowerLaw) and self.edges and not bg.A.map["is_set"].any():
                self.two_area_background_estimation()

    @property
    def _active_edges(self):
        return [edge for edge in self.edges if edge.active]

    @property
    def _active_background_components(self):
        return [bc for bc in self._background_components if bc.active]

    def _add_edges_from_subshells_names(self, e_shells=None):
        """Create the Edge instances and configure them appropriately

        Parameters
        ----------
        e_shells : list of strings
        """
        if self.signal._are_microscope_parameters_missing():
            raise ValueError(
                "The required microscope parameters are not defined in "
                "the EELS spectrum signal metadata. Use "
                "``set_microscope_parameters`` to set them."
            )
        if e_shells is None:
            e_shells = list(self.signal.subshells)
        e_shells.sort()
        master_edge = EELSCLEdge(
            e_shells.pop(), self.GOS, gos_file_path=self.gos_file_path
        )
        self.append(master_edge)
        element = master_edge.element
        while len(e_shells) > 0:
            next_element = e_shells[-1].split("_")[0]
            if next_element != element:
                # New master edge
                self._add_edges_from_subshells_names(e_shells=e_shells)
            elif self.GOS == "hydrogenic":
                # The hydrogenic GOS includes all the L subshells in one
                # so we get rid of the others
                e_shells.pop()
            else:
                # Add the other subshells of the same element
                # and couple their intensity and onset_energy to that of the
                # master edge
                edge = EELSCLEdge(
                    e_shells.pop(), GOS=self.GOS, gos_file_path=self.gos_file_path
                )

                edge.intensity.twin = master_edge.intensity
                edge.onset_energy.twin = master_edge.onset_energy
                edge.onset_energy.twin_function_expr = "x + {}".format(
                    (edge.GOS.onset_energy - master_edge.GOS.onset_energy)
                )
                edge.free_onset_energy = False
                self.append(edge)

    def resolve_fine_structure(self, preedge_safe_window_width=2, i1=0):
        """Adjust the fine structure of all edges to avoid overlapping

        This function is called automatically every time the position of an edge
        changes

        Parameters
        ----------
        preedge_safe_window_width : float
            minimum distance between the fine structure of an ionization edge
            and that of the following one. Default 2 (eV).

        """

        if self._suspend_auto_fine_structure_width is True:
            return

        if not self._active_edges:
            return

        while (
            self._active_edges[i1].fine_structure_active is False
            and i1 < len(self._active_edges) - 1
        ):
            i1 += 1
        if i1 < len(self._active_edges) - 1:
            i2 = i1 + 1
            while (
                self._active_edges[i2].fine_structure_active is False
                and i2 < len(self._active_edges) - 1
            ):
                i2 += 1
            if self._active_edges[i2].fine_structure_active is True:
                distance_between_edges = (
                    self._active_edges[i2].onset_energy.value
                    - self._active_edges[i1].onset_energy.value
                )
                if (
                    self._active_edges[i1].fine_structure_width
                    > distance_between_edges - self._preedge_safe_window_width
                ):
                    min_d = self._min_distance_between_edges_for_fine_structure
                    if (
                        distance_between_edges - self._preedge_safe_window_width
                    ) <= min_d:
                        _logger.info(
                            (
                                "Automatically deactivating the fine structure "
                                "of edge number %d to avoid conflicts with edge "
                                "number %d"
                            )
                            % (i2 + 1, i1 + 1)
                        )
                        self._active_edges[i2].fine_structure_active = False
                        self._active_edges[i2].fine_structure_coeff.free = False
                        self.resolve_fine_structure(i1=i2)
                    else:
                        new_fine_structure_width = (
                            distance_between_edges - self._preedge_safe_window_width
                        )
                        _logger.info(
                            (
                                "Automatically changing the fine structure "
                                "width of edge %d from %s eV to %s eV to avoid "
                                "conflicts with edge number %d"
                            )
                            % (
                                i1 + 1,
                                self._active_edges[i1].fine_structure_width,
                                new_fine_structure_width,
                                i2 + 1,
                            )
                        )
                        self._active_edges[
                            i1
                        ].fine_structure_width = new_fine_structure_width
                        self.resolve_fine_structure(i1=i2)
                else:
                    self.resolve_fine_structure(i1=i2)
        else:
            return

    def fit(self, kind="std", **kwargs):
        """Fits the model to the experimental data.

        Read more in the :ref:`User Guide <model.fitting>`.

        Parameters
        ----------
        kind : {"std", "smart"}, default "std"
            If "std", performs standard fit. If "smart",
            performs a smart_fit - for more details see
            the :ref:`User Guide <eels.fitting>`.
        %s

        Returns
        -------
        None

        See Also
        --------
        * :py:meth:`~hyperspy.model.BaseModel.fit`
        * :py:meth:`~hyperspy.model.BaseModel.multifit`
        * :py:meth:`~hyperspy.model.EELSModel.smart_fit`

        """
        if kind not in ["smart", "std"]:
            raise ValueError(f"kind must be either 'std' or 'smart', not '{kind}'")
        elif kind == "smart":
            return self.smart_fit(**kwargs)
        elif kind == "std":
            return Model1D.fit(self, **kwargs)

    fit.__doc__ %= FIT_PARAMETERS_ARG

    def smart_fit(self, start_energy=None, **kwargs):
        """Fits EELS edges in a cascade style.

        The fitting procedure acts in iterative manner along
        the energy-loss-axis. First it fits only the background
        up to the first edge. It continues by deactivating all
        edges except the first one, then performs the fit. Then
        it only activates the first two, fits, and repeats
        this until all edges are fitted simultaneously.

        Other, non-EELSCLEdge components, are never deactivated,
        and fitted on every iteration.

        Parameters
        ----------
        start_energy : {float, None}
            If float, limit the range of energies from the left to the
            given value.
        %s

        See Also
        --------
        * :py:meth:`~hyperspy.model.BaseModel.fit`
        * :py:meth:`~hyperspy.model.BaseModel.multifit`
        * :py:meth:`~hyperspy.model.EELSModel.fit`

        """
        cm = self.suspend_update if self._plot_active else dummy_context_manager
        with cm(update_on_resume=True):
            # Fit background
            self.fit_background(start_energy, **kwargs)

            # Fit the edges
            for i in range(0, len(self._active_edges)):
                self._fit_edge(i, start_energy, **kwargs)

    smart_fit.__doc__ %= FIT_PARAMETERS_ARG

    def _get_first_ionization_edge_energy(self, start_energy=None):
        """Calculate the first ionization edge energy.

        Returns
        -------
        iee : float or None
            The first ionization edge energy or None if no edge is defined in
            the model.

        """
        if not self._active_edges:
            return None
        start_energy = self._get_start_energy(start_energy)
        iee_list = [
            edge.onset_energy.value
            for edge in self._active_edges
            if edge.onset_energy.value > start_energy
        ]
        iee = min(iee_list) if iee_list else None
        return iee

    def _get_start_energy(self, start_energy=None):
        E0 = self.axis.axis[self._channel_switches][0]
        if not start_energy or start_energy < E0:
            start_energy = E0
        return start_energy

    def fit_background(self, start_energy=None, only_current=True, **kwargs):
        """Fit the background to the first active ionization edge
        in the energy range.

        Parameters
        ----------
        start_energy : {float, None}, optional
            If float, limit the range of energies from the left to the
            given value. Default None.
        only_current : bool, optional
            If True, only fit the background at the current coordinates.
            Default True.
        **kwargs : extra key word arguments
            All extra key word arguments are passed to fit or
            multifit.

        """

        # If there is no active background component do nothing
        if not self._active_background_components:
            return
        iee = self._get_first_ionization_edge_energy(start_energy=start_energy)
        if iee is not None:
            to_disable = [
                edge for edge in self._active_edges if edge.onset_energy.value >= iee
            ]
            E2 = iee - self._preedge_safe_window_width
            self.disable_edges(to_disable)
        else:
            E2 = None
        self.set_signal_range(start_energy, E2)
        if only_current:
            self.fit(**kwargs)
        else:
            self.multifit(**kwargs)
        self._channel_switches = copy.copy(self._backup_channel_switches)
        if iee is not None:
            self.enable_edges(to_disable)

    def two_area_background_estimation(self, E1=None, E2=None, powerlaw=None):
        """Estimates the parameters of a power law background with the two
        area method.

        Parameters
        ----------
        E1 : float
        E2 : float
        powerlaw : PowerLaw component or None
            If None, it will try to guess the right component from the
            background components of the model

        """
        if powerlaw is None:
            for component in self._active_background_components:
                if isinstance(component, components1d.PowerLaw):
                    if powerlaw is None:
                        powerlaw = component
                    else:
                        _logger.warning(
                            "There are more than two power law "
                            "background components defined in this model, "
                            "please use the powerlaw keyword to specify one"
                            " of them"
                        )
                        return
                else:  # No power law component
                    return

        ea = self.axis.axis[self._channel_switches]
        E1 = self._get_start_energy(E1)
        if E2 is None:
            E2 = self._get_first_ionization_edge_energy(start_energy=E1)
            if E2 is None:
                E2 = ea[-1]
            else:
                E2 = E2 - self._preedge_safe_window_width

        if not powerlaw.estimate_parameters(self.signal, E1, E2, only_current=False):
            _logger.warning(
                "The power law background parameters could not "
                "be estimated.\n"
                "Try choosing a different energy range for the estimation"
            )
            return

    def _fit_edge(self, edgenumber, start_energy=None, **kwargs):
        backup_channel_switches = self._channel_switches.copy()
        ea = self.axis.axis[self._channel_switches]
        if start_energy is None:
            start_energy = ea[0]
        # Declare variables
        active_edges = self._active_edges
        edge = active_edges[edgenumber]
        if (
            edge.intensity.twin is not None
            or edge.active is False
            or edge.onset_energy.value < start_energy
            or edge.onset_energy.value > ea[-1]
        ):
            return 1
        # Fitting edge 'edge.name'
        last_index = len(self._active_edges) - 1  # Last edge index
        i = 1
        twins = []
        # find twins
        while edgenumber + i <= last_index and (
            active_edges[edgenumber + i].intensity.twin is not None
            or active_edges[edgenumber + i].active is False
        ):
            if active_edges[edgenumber + i].intensity.twin is not None:
                twins.append(self._active_edges[edgenumber + i])
            i += 1
        if (edgenumber + i) > last_index:
            nextedgeenergy = ea[-1]
        else:
            nextedgeenergy = (
                active_edges[edgenumber + i].onset_energy.value
                - self._preedge_safe_window_width
            )

        # Backup the fsstate
        to_activate_fs = []
        for edge_ in [
            edge,
        ] + twins:
            if (
                edge_.fine_structure_active is True
                and edge_.fine_structure_coeff.free is True
                or edge_.fine_structure_components
            ):
                to_activate_fs.append(edge_)
        self.disable_fine_structure(to_activate_fs)

        # Smart Fitting

        # Without fine structure to determine onset_energy
        edges_to_activate = []
        for edge_ in self._active_edges[edgenumber + 1 :]:
            if edge_.active is True and edge_.onset_energy.value >= nextedgeenergy:
                edge_.active = False
                edges_to_activate.append(edge_)

        self.set_signal_range(start_energy, nextedgeenergy)
        if edge.free_onset_energy is True:
            edge.onset_energy.free = True
            self.fit(**kwargs)
            edge.onset_energy.free = False
            _logger.info("onset_energy = %s", edge.onset_energy.value)
            self._classify_components()
        elif edge.intensity.free is True:
            self.enable_fine_structure(to_activate_fs)
            self.remove_fine_structure_data(to_activate_fs)
            self.disable_fine_structure(to_activate_fs)
            self.fit(**kwargs)

        if len(to_activate_fs) > 0:
            self.set_signal_range(start_energy, nextedgeenergy)
            self.enable_fine_structure(to_activate_fs)
            self.fit(**kwargs)

        self.enable_edges(edges_to_activate)
        # Recover the _channel_switches. Remove it or make it smarter.
        self._channel_switches = backup_channel_switches

    def quantify(self):
        """Prints the value of the intensity of all the independent
        active EELS core loss edges defined in the model

        """
        elements = {}
        for edge in self._active_edges:
            if edge.active and edge.intensity.twin is None:
                element = edge.element
                subshell = edge.subshell
                if element not in elements:
                    elements[element] = {}
                elements[element][subshell] = edge.intensity.value
        print()
        print("Absolute quantification:")
        print("Elem.\tIntensity")
        for element in elements:
            if len(elements[element]) == 1:
                for subshell in elements[element]:
                    print("%s\t%f" % (element, elements[element][subshell]))
            else:
                for subshell in elements[element]:
                    print(
                        "%s_%s\t%f" % (element, subshell, elements[element][subshell])
                    )

    def remove_fine_structure_data(self, edges_list=None):
        """Remove the fine structure data from the fitting routine as
        defined in the fine_structure_width parameter of the
        component.EELSCLEdge

        Parameters
        ----------
        edges_list : None or list of EELSCLEdge or list of edge names
            If None, the operation is performed on all the edges in the model.
            Otherwise, it will be performed only on the listed components.

        See Also
        --------
        enable_edges, disable_edges, enable_background,
        disable_background, enable_fine_structure,
        disable_fine_structure, set_all_edges_intensities_positive,
        unset_all_edges_intensities_positive, enable_free_onset_energy,
        disable_free_onset_energy, fix_edges, free_edges, fix_fine_structure,
        free_fine_structure

        """
        if edges_list is None:
            edges_list = self._active_edges
        else:
            edges_list = [self._get_component(x) for x in edges_list]
        for edge in edges_list:
            if edge.isbackground is False and edge.fine_structure_active is True:
                start = edge.onset_energy.value
                stop = start + edge.fine_structure_width
                self.remove_signal_range(start, stop)

    def enable_edges(self, edges_list=None):
        """Enable the edges listed in edges_list. If edges_list is
        None (default) all the edges with onset in the spectrum energy
        region will be enabled.

        Parameters
        ----------
        edges_list : None or list of EELSCLEdge or list of edge names
            If None, the operation is performed on all the edges in the model.
            Otherwise, it will be performed only on the listed components.

        See Also
        --------
        enable_edges, disable_edges, enable_background,
        disable_background, enable_fine_structure,
        disable_fine_structure, set_all_edges_intensities_positive,
        unset_all_edges_intensities_positive, enable_free_onset_energy,
        disable_free_onset_energy, fix_edges, free_edges, fix_fine_structure,
        free_fine_structure

        """

        if edges_list is None:
            edges_list = self.edges
        else:
            edges_list = [self._get_component(x) for x in edges_list]
        for edge in edges_list:
            if edge.isbackground is False:
                edge.active = True
        self.resolve_fine_structure()

    def disable_edges(self, edges_list=None):
        """Disable the edges listed in edges_list. If edges_list is None (default)
        all the edges with onset in the spectrum energy region will be
        disabled.

        Parameters
        ----------
        edges_list : None or list of EELSCLEdge or list of edge names
            If None, the operation is performed on all the edges in the model.
            Otherwise, it will be performed only on the listed components.

        See Also
        --------
        enable_edges, disable_edges, enable_background,
        disable_background, enable_fine_structure,
        disable_fine_structure, set_all_edges_intensities_positive,
        unset_all_edges_intensities_positive, enable_free_onset_energy,
        disable_free_onset_energy, fix_edges, free_edges, fix_fine_structure,
        free_fine_structure

        """
        if edges_list is None:
            edges_list = self._active_edges
        else:
            edges_list = [self._get_component(x) for x in edges_list]
        for edge in edges_list:
            if edge.isbackground is False:
                edge.active = False
        self.resolve_fine_structure()

    def enable_background(self):
        """Enable the background components."""
        for component in self._background_components:
            component.active = True

    def disable_background(self):
        """Disable the background components."""
        for component in self._active_background_components:
            component.active = False

    def enable_fine_structure(self, edges_list=None):
        """Enable the fine structure of the edges listed in edges_list.

        If edges_list is None (default) the fine structure of all the edges
        with onset in the spectrum energy region will be enabled.

        Parameters
        ----------
        edges_list : None or list of EELSCLEdge or list of edge names
            If None, the operation is performed on all the edges in the model.
            Otherwise, it will be performed only on the listed components.

        See Also
        --------
        enable_edges, disable_edges, enable_background,
        disable_background, enable_fine_structure,
        disable_fine_structure, set_all_edges_intensities_positive,
        unset_all_edges_intensities_positive, enable_free_onset_energy,
        disable_free_onset_energy, fix_edges, free_edges, fix_fine_structure,
        free_fine_structure

        """
        if edges_list is None:
            edges_list = self._active_edges
        else:
            edges_list = [self._get_component(x) for x in edges_list]
        for edge in edges_list:
            if edge.isbackground is False:
                edge.fine_structure_active = True
        self.resolve_fine_structure()

    def disable_fine_structure(self, edges_list=None):
        """Disable the fine structure of the edges listed in edges_list.
        If edges_list is None (default) the fine structure of all the edges
        with onset in the spectrum energy region will be disabled.

        Parameters
        ----------
        edges_list : None or list of EELSCLEdge or list of edge names
            If None, the operation is performed on all the edges in the model.
            Otherwise, it will be performed only on the listed components.

        See Also
        --------
        enable_edges, disable_edges, enable_background,
        disable_background, enable_fine_structure,
        disable_fine_structure, set_all_edges_intensities_positive,
        unset_all_edges_intensities_positive, enable_free_onset_energy,
        disable_free_onset_energy, fix_edges, free_edges, fix_fine_structure,
        free_fine_structure

        """
        if edges_list is None:
            edges_list = self._active_edges
        else:
            edges_list = [self._get_component(x) for x in edges_list]
        for edge in edges_list:
            if edge.isbackground is False:
                edge.fine_structure_active = False
        self.resolve_fine_structure()

    def set_all_edges_intensities_positive(self):
        """
        Set all edges intensities positive by setting ``ext_force_positive``
        and ``ext_bounded`` to ``True``.

        Returns
        -------
        None.

        """
        for edge in self._active_edges:
            edge.intensity.ext_force_positive = True
            edge.intensity.ext_bounded = True

    def unset_all_edges_intensities_positive(self):
        """
        Unset all edges intensities positive by setting ``ext_force_positive``
        and ``ext_bounded`` to ``False``.

        Returns
        -------
        None.

        """
        for edge in self._active_edges:
            edge.intensity.ext_force_positive = False
            edge.intensity.ext_bounded = False

    def enable_free_onset_energy(self, edges_list=None):
        """Enable the automatic freeing of the onset_energy parameter during a
        smart fit for the edges listed in edges_list.
        If edges_list is None (default) the onset_energy of all the edges
        with onset in the spectrum energy region will be freed.

        Parameters
        ----------
        edges_list : None or list of EELSCLEdge or list of edge names
            If None, the operation is performed on all the edges in the model.
            Otherwise, it will be performed only on the listed components.

        See Also
        --------
        enable_edges, disable_edges, enable_background,
        disable_background, enable_fine_structure,
        disable_fine_structure, set_all_edges_intensities_positive,
        unset_all_edges_intensities_positive, enable_free_onset_energy,
        disable_free_onset_energy, fix_edges, free_edges, fix_fine_structure,
        free_fine_structure

        """
        if edges_list is None:
            edges_list = self._active_edges
        else:
            edges_list = [self._get_component(x) for x in edges_list]
        for edge in edges_list:
            if edge.isbackground is False:
                edge.free_onset_energy = True

    def disable_free_onset_energy(self, edges_list=None):
        """Disable the automatic freeing of the onset_energy parameter during a
        smart fit for the edges listed in edges_list.
        If edges_list is None (default) the onset_energy of all the edges
        with onset in the spectrum energy region will not be freed.
        Note that if their attribute edge.onset_energy.free is True, the
        parameter will be free during the smart fit.

        Parameters
        ----------
        edges_list : None or list of EELSCLEdge or list of edge names
            If None, the operation is performed on all the edges in the model.
            Otherwise, it will be performed only on the listed components.

        See Also
        --------
        enable_edges, disable_edges, enable_background,
        disable_background, enable_fine_structure,
        disable_fine_structure, set_all_edges_intensities_positive,
        unset_all_edges_intensities_positive, enable_free_onset_energy,
        disable_free_onset_energy, fix_edges, free_edges, fix_fine_structure,
        free_fine_structure

        """

        if edges_list is None:
            edges_list = self._active_edges
        else:
            edges_list = [self._get_component(x) for x in edges_list]
        for edge in edges_list:
            if edge.isbackground is False:
                edge.free_onset_energy = True

    def fix_edges(self, edges_list=None):
        """Fixes all the parameters of the edges given in edges_list.
        If edges_list is None (default) all the edges will be fixed.

        Parameters
        ----------
        edges_list : None or list of EELSCLEdge or list of edge names
            If None, the operation is performed on all the edges in the model.
            Otherwise, it will be performed only on the listed components.

        See Also
        --------
        enable_edges, disable_edges, enable_background,
        disable_background, enable_fine_structure,
        disable_fine_structure, set_all_edges_intensities_positive,
        unset_all_edges_intensities_positive, enable_free_onset_energy,
        disable_free_onset_energy, fix_edges, free_edges, fix_fine_structure,
        free_fine_structure

        """
        if edges_list is None:
            edges_list = self._active_edges
        else:
            edges_list = [self._get_component(x) for x in edges_list]
        for edge in edges_list:
            if edge.isbackground is False:
                edge.intensity.free = False
                edge.onset_energy.free = False
                edge.fine_structure_coeff.free = False

    def free_edges(self, edges_list=None):
        """Frees all the parameters of the edges given in edges_list.
        If edges_list is None (default) all the edges will be freed.

        Parameters
        ----------
        edges_list : None or list of EELSCLEdge or list of edge names
            If None, the operation is performed on all the edges in the model.
            Otherwise, it will be performed only on the listed components.

        See Also
        --------
        enable_edges, disable_edges, enable_background,
        disable_background, enable_fine_structure,
        disable_fine_structure, set_all_edges_intensities_positive,
        unset_all_edges_intensities_positive, enable_free_onset_energy,
        disable_free_onset_energy, fix_edges, free_edges, fix_fine_structure,
        free_fine_structure

        """

        if edges_list is None:
            edges_list = self._active_edges
        else:
            edges_list = [self._get_component(x) for x in edges_list]
        for edge in edges_list:
            if edge.isbackground is False:
                edge.set_parameters_free(
                    parameter_name_list=[
                        "intensity",
                        "onset_energy",
                        "fine_structure_coeff",
                    ]
                )

    def fix_fine_structure(self, edges_list=None):
        """Fixes the fine structure of the edges given in edges_list.
        If edges_list is None (default) all the edges will be fixed.

        Parameters
        ----------
        edges_list : None or list of EELSCLEdge or list of edge names
            If None, the operation is performed on all the edges in the model.
            Otherwise, it will be performed only on the listed components.

        See Also
        --------
        enable_edges, disable_edges, enable_background,
        disable_background, enable_fine_structure,
        disable_fine_structure, set_all_edges_intensities_positive,
        unset_all_edges_intensities_positive, enable_free_onset_energy,
        disable_free_onset_energy, fix_edges, free_edges, fix_fine_structure,
        free_fine_structure

        """
        if edges_list is None:
            edges_list = self._active_edges
        else:
            edges_list = [self._get_component(x) for x in edges_list]
        for edge in edges_list:
            if edge.isbackground is False:
                edge.fix_fine_structure()

    def free_fine_structure(self, edges_list=None):
        """Frees the fine structure of the edges given in edges_list.
        If edges_list is None (default) all the edges will be freed.

        Parameters
        ----------
        edges_list : None or list of EELSCLEdge or list of edge names
            If None, the operation is performed on all the edges in the model.
            Otherwise, it will be performed only on the listed components.

        See Also
        --------
        enable_edges, disable_edges, enable_background,
        disable_background, enable_fine_structure,
        disable_fine_structure, set_all_edges_intensities_positive,
        unset_all_edges_intensities_positive, enable_free_onset_energy,
        disable_free_onset_energy, fix_edges, free_edges, fix_fine_structure,
        free_fine_structure

        """
        if edges_list is None:
            edges_list = self._active_edges
        else:
            edges_list = [self._get_component(x) for x in edges_list]
        for edge in edges_list:
            if edge.isbackground is False:
                edge.free_fine_structure()

    def suspend_auto_fine_structure_width(self):
        """Disable the automatic adjustment of the core-loss edges fine
        structure width.

        See Also
        --------
        resume_auto_fine_structure_width

        """
        if self._suspend_auto_fine_structure_width is False:
            self._suspend_auto_fine_structure_width = True
        else:
            warnings.warn("Already suspended, does nothing.")

    def resume_auto_fine_structure_width(self, update=True):
        """Enable the automatic adjustment of the core-loss edges fine
        structure width.

        Parameters
        ----------
        update : bool, optional
            If True, also execute the automatic adjustment (default).

        See Also
        --------
        suspend_auto_fine_structure_width

        """
        if self._suspend_auto_fine_structure_width is True:
            self._suspend_auto_fine_structure_width = False
            if update is True:
                self.resolve_fine_structure()
        else:
            warnings.warn("Not suspended, nothing to resume.")
