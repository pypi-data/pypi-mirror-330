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
import pytest
from pathlib import Path

import hyperspy.api as hs
from hyperspy.components1d import Gaussian
from hyperspy.exceptions import VisibleDeprecationWarning
from exspy.signals import EELSSpectrum

my_path = Path(__file__).resolve().parent
baseline_dir = "plot_model"
default_tol = 2.0


def create_ll_signal(signal_shape=1000):
    offset = 0
    zlp_param = {"A": 10000.0, "centre": 0.0 + offset, "sigma": 15.0}
    zlp = Gaussian(**zlp_param)
    plasmon_param = {"A": 2000.0, "centre": 200.0 + offset, "sigma": 75.0}
    plasmon = Gaussian(**plasmon_param)
    axis = np.arange(signal_shape)
    data = zlp.function(axis) + plasmon.function(axis)
    ll = EELSSpectrum(data)
    ll.axes_manager[-1].offset = -offset
    ll.axes_manager[-1].scale = 0.1
    return ll


A_value_gaussian = [1000.0, 600.0, 2000.0]
centre_value_gaussian = [50.0, 20.0, 60.0]
sigma_value_gaussian = [5.0, 3.0, 1.0]
scale = 0.1


def create_sum_of_gaussians(convolved=False):
    param1 = {
        "A": A_value_gaussian[0],
        "centre": centre_value_gaussian[0] / scale,
        "sigma": sigma_value_gaussian[0] / scale,
    }
    gs1 = Gaussian(**param1)
    param2 = {
        "A": A_value_gaussian[1],
        "centre": centre_value_gaussian[1] / scale,
        "sigma": sigma_value_gaussian[1] / scale,
    }
    gs2 = Gaussian(**param2)
    param3 = {
        "A": A_value_gaussian[2],
        "centre": centre_value_gaussian[2] / scale,
        "sigma": sigma_value_gaussian[2] / scale,
    }
    gs3 = Gaussian(**param3)

    axis = np.arange(1000)
    data = gs1.function(axis) + gs2.function(axis) + gs3.function(axis)

    if convolved:
        to_convolved = create_ll_signal(data.shape[0]).data
        data = np.convolve(data, to_convolved) / sum(to_convolved)

    s = EELSSpectrum(data[:1000])
    s.axes_manager[-1].scale = scale
    return s


@pytest.mark.parametrize("binned", [True, False])
@pytest.mark.parametrize("plot_component", [True, False])
@pytest.mark.parametrize("convolved", [True, False])
@pytest.mark.mpl_image_compare(baseline_dir=baseline_dir, tolerance=default_tol)
def test_plot_gaussian_EELSSpectrum(convolved, plot_component, binned):
    s = create_sum_of_gaussians(convolved)
    s.axes_manager[-1].is_binned == binned
    s.metadata.General.title = "Convolved: {}, plot_component: {}, binned: {}".format(
        convolved, plot_component, binned
    )

    s.axes_manager[-1].is_binned = binned
    m = s.create_model(auto_add_edges=False, auto_background=False)
    m.low_loss = create_ll_signal(1000) if convolved else None

    m.extend([Gaussian(), Gaussian(), Gaussian()])

    for gaussian, centre, sigma in zip(m, centre_value_gaussian, sigma_value_gaussian):
        gaussian.centre.value = centre
        gaussian.centre.free = False
        gaussian.sigma.value = sigma
        gaussian.sigma.free = False

    m.fit()
    m.plot(plot_components=plot_component)

    def A_value(component, binned):
        if binned:
            return component.A.value * scale
        else:
            return component.A.value

    if convolved:
        np.testing.assert_almost_equal(A_value(m[0], binned), 0.014034, decimal=5)
        np.testing.assert_almost_equal(A_value(m[1], binned), 0.008420, decimal=5)
        np.testing.assert_almost_equal(A_value(m[2], binned), 0.028068, decimal=5)
    else:
        np.testing.assert_almost_equal(A_value(m[0], binned), 100.0, decimal=5)
        np.testing.assert_almost_equal(A_value(m[1], binned), 60.0, decimal=5)
        np.testing.assert_almost_equal(A_value(m[2], binned), 200.0, decimal=5)

    return m._plot.signal_plot.figure


@pytest.mark.parametrize(("convolved"), [False, True])
@pytest.mark.mpl_image_compare(baseline_dir=baseline_dir, tolerance=default_tol)
def test_fit_EELS_convolved(convolved):
    # Keep this test here to avoid having to add image comparison in exspy
    pytest.importorskip("exspy", reason="exspy not installed.")
    dname = my_path.joinpath("data")
    with pytest.warns(VisibleDeprecationWarning):
        cl = hs.load(dname.joinpath("Cr_L_cl.hspy"))
    cl.axes_manager[-1].is_binned = False
    cl.metadata.General.title = "Convolved: {}".format(convolved)
    ll = None
    if convolved:
        with pytest.warns(VisibleDeprecationWarning):
            ll = hs.load(dname.joinpath("Cr_L_ll.hspy"))
    m = cl.create_model(auto_background=False, low_loss=ll, GOS="hydrogenic")
    m.fit(kind="smart")
    m.plot(plot_components=True)
    return m._plot.signal_plot.figure
