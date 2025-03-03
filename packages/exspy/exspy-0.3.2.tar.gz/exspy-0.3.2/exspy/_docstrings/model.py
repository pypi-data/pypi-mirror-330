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


"""Common docstring snippets for model."""

from exspy._misc.eels.gosh_gos import _GOSH_SOURCES

GOS_PARAMETER = """GOS : 'hydrogenic', 'dft', 'dirac', 'Hartree-Slater'.
            The GOS to use. Default is ``'dft'``.

        gos_file_path : str, None
            Only with GOS='dft' or 'dirac'. Specify the file path of the gosh file
            to use. If None, use the file from doi:{}""".format(
    _GOSH_SOURCES["dft"]["DOI"]
)

EELSMODEL_PARAMETERS = """low_loss : None or EELSSpectrum
            If an EELSSpectrum is provided, it will be assumed that it is
            a low-loss EELS spectrum, and it will be used to simulate the
            effect of multiple scattering by convolving it with the EELS
            spectrum.
        auto_background : bool
            If True, and if spectrum is an EELS instance adds automatically
            a powerlaw to the model and estimate the parameters by the
            two-area method.
        auto_add_edges : bool
            If True, and if spectrum is an EELS instance, it will automatically
            add the ionization edges as defined in the
            :class:`~.api.signals.EELSSpectrum` instance. Adding a new element to
            the spectrum using the :meth:`~.api.signals.EELSSpectrum.add_elements`
            method automatically add the corresponding ionisation edges to the model.
        {}
        dictionary : None or dict
            A dictionary to be used to recreate a model. Usually generated using
            :meth:`~.model.BaseModel.as_dictionary`""".format(GOS_PARAMETER)
