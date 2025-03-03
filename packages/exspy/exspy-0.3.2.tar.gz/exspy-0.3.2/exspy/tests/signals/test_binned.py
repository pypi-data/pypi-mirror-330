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

import hyperspy.api as hs

import exspy


def test_dielectric_function_binned_default():
    s = exspy.signals.DielectricFunction([0])
    assert not s.axes_manager[-1].is_binned


def test_signal_binned_default():
    s = hs.signals.BaseSignal([0])
    assert not s.axes_manager[-1].is_binned


def test_eels_spectrum_binned_default():
    s = exspy.signals.EELSSpectrum([0])
    assert s.axes_manager[-1].is_binned


def test_eds_tem_binned_default():
    s = exspy.signals.EDSTEMSpectrum([0])
    assert s.axes_manager[-1].is_binned


def test_eds_sem_binned_default():
    s = exspy.signals.EDSSEMSpectrum([0])
    assert s.axes_manager[-1].is_binned
