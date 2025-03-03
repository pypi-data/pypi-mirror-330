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

from ._misc.material import (
    atomic_to_weight,
    density_of_mixture,
    mass_absorption_coefficient,
    mass_absorption_mixture,
    weight_to_atomic,
)
from ._misc.elements import elements_db as elements


__all__ = [
    "atomic_to_weight",
    "density_of_mixture",
    "elements",
    "mass_absorption_coefficient",
    "mass_absorption_mixture",
    "weight_to_atomic",
]


def __dir__():
    return sorted(__all__)
