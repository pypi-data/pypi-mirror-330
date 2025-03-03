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
import logging

import hyperspy.api as hs

from exspy._utils import parse_component_module


_logger = logging.getLogger(__name__)


class SEE(hs.model.components1D.Expression):
    r"""Secondary electron emission component for Photoemission Spectroscopy.

    .. math::
        :nowrap:

        \[
        f(x) =
        \begin{cases}
            0, & x \leq \Phi\\
            A\cdot{ (x-\Phi) / (x-\Phi+B)^{4}}, & x >  \Phi
        \end{cases}
        \]

    ============= =============
     Variable      Parameter
    ============= =============
     :math:`A`     A
     :math:`\Phi`  Phi
     :math:`B`     B
    ============= =============

    Parameters
    ----------
    A : float
        Height parameter
    Phi : float
        Position parameter
    B : float
        Tail or asymmetry parameter
    **kwargs
        Extra keyword arguments are passed to the
        :py:class:`~._components.expression.Expression` component.

    """

    def __init__(
        self, A=1.0, Phi=1.0, B=0.0, module="numexpr", compute_gradients=False, **kwargs
    ):
        if kwargs.pop("sigma", False):
            _logger.warning("The `sigma` parameter was broken and it has been removed.")

        super().__init__(
            expression="where(x > Phi, A * (x - Phi) / (x - Phi + B) ** 4, 0)",
            name="SEE",
            A=A,
            Phi=Phi,
            B=B,
            position="Phi",
            module=parse_component_module(module),
            autodoc=False,
            compute_gradients=compute_gradients,
            linear_parameter_list=["A"],
            check_parameter_linearity=False,
            **kwargs,
        )

        # Boundaries
        self.A.bmin = 0.0
        self.A.bmax = None

        self.convolved = True

    def grad_A(self, x):
        """ """
        return np.where(
            x > self.Phi.value,
            (x - self.Phi.value) / (x - self.Phi.value + self.B.value) ** 4,
            0,
        )

    def grad_Phi(self, x):
        """ """
        return np.where(
            x > self.Phi.value,
            (4 * (x - self.Phi.value) * self.A.value)
            / (self.B.value + x - self.Phi.value) ** 5
            - self.A.value / (self.B.value + x - self.Phi.value) ** 4,
            0,
        )

    def grad_B(self, x):
        return np.where(
            x > self.Phi.value,
            -(4 * (x - self.Phi.value) * self.A.value)
            / (self.B.value + x - self.Phi.value) ** 5,
            0,
        )
