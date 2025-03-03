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

from exspy.models.edsmodel import EDSModel


class EDSTEMModel(EDSModel):
    """Build and fit a model to EDS data acquired in the TEM.

    Parameters
    ----------
    spectrum : EDSTEMSpectrum

    auto_add_lines : bool
        If True, automatically add Gaussians for all X-rays generated
        in the energy range by an element, using the edsmodel.add_family_lines
        method.
    auto_background : bool
        If True, adds automatically a polynomial order 6 to the model,
        using the edsmodel.add_polynomial_background method.

    Any extra arguments are passed to the Model constructor.
    """

    def __init__(
        self, spectrum, auto_background=True, auto_add_lines=True, *args, **kwargs
    ):
        EDSModel.__init__(
            self, spectrum, auto_background, auto_add_lines, *args, **kwargs
        )
