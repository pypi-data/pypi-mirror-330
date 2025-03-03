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

import contextlib
import logging
from packaging.version import Version
import io
from unittest import mock

import dask
import numpy as np
import pooch
import pytest

import hyperspy.api as hs
from hyperspy.decorators import lazifyTestClass
from hyperspy.exceptions import VisibleDeprecationWarning

from exspy._misc.eels.gosh_gos import _DFT_GOSH, _DIRAC_GOSH
from exspy._misc.elements import elements_db as elements
from exspy.signals import EELSSpectrum


# Dask does not always work nicely with np.errstate,
# see: https://github.com/dask/dask/issues/3245, so
# filter out divide-by-zero warnings that only appear
# when the test is lazy. When the test is not lazy,
# internal use of np.errstate means the warnings never
# appear in the first place.
@pytest.mark.filterwarnings(
    "ignore:invalid value encountered in subtract:RuntimeWarning"
)
@pytest.mark.filterwarnings("ignore:divide by zero encountered in log:RuntimeWarning")
@lazifyTestClass
class TestCreateEELSModel:
    def setup_method(self, method):
        s = EELSSpectrum(np.zeros(200))
        s.set_microscope_parameters(100, 10, 10)
        s.axes_manager[-1].offset = 150
        s.add_elements(("B", "C"))
        self.s = s

    def test_create_eelsmodel(self):
        from exspy.models.eelsmodel import EELSModel

        assert isinstance(self.s.create_model(), EELSModel)

    def test_create_eelsmodel_no_md(self):
        s = self.s
        del s.metadata.Acquisition_instrument
        with pytest.raises(ValueError):
            s.create_model()

    def test_auto_add_edges_true(self):
        m = self.s.create_model(auto_add_edges=True)
        cnames = [component.name for component in m]
        assert "B_K" in cnames and "C_K" in cnames

    def test_gos_hydrogenic(self):
        m = self.s.create_model(auto_add_edges=True, GOS="hydrogenic")
        assert m["B_K"].GOS._name == "hydrogenic"
        m.fit()

    def test_gos_gosh(self):
        with pytest.warns(VisibleDeprecationWarning):
            m = self.s.create_model(auto_add_edges=True, GOS="gosh")
        assert m["B_K"].GOS._name == "dft"
        m.fit()

        with pytest.raises(ValueError):
            self.s.create_model(auto_add_edges=True, GOS="not_a_GOS")

    def test_gos_gosh_dft(self):
        m = self.s.create_model(auto_add_edges=True, GOS="dft")
        assert m["B_K"].GOS._name == "dft"
        m.fit()

        with pytest.raises(ValueError):
            self.s.create_model(auto_add_edges=True, GOS="not_a_GOS")

    def test_gos_gosh_dirac(self):
        m = self.s.create_model(auto_add_edges=True, GOS="dirac")
        assert m["B_K"].GOS._name == "dirac"
        m.fit()

        with pytest.raises(ValueError):
            self.s.create_model(auto_add_edges=True, GOS="not_a_GOS")

    def test_gos_file(self):
        gos_file_path = pooch.retrieve(
            url=_DFT_GOSH["URL"],
            known_hash=_DFT_GOSH["KNOWN_HASH"],
        )
        self.s.create_model(auto_add_edges=True, gos_file_path=gos_file_path)

    def test_gos_file_dirac(self):
        gos_file_path = pooch.retrieve(
            url=_DIRAC_GOSH["URL"],
            known_hash=_DIRAC_GOSH["KNOWN_HASH"],
        )
        self.s.create_model(
            auto_add_edges=True, gos_file_path=gos_file_path, GOS="dirac"
        )

    def test_auto_add_background_true(self):
        m = self.s.create_model(auto_background=True)
        from hyperspy.components1d import PowerLaw

        is_pl_instance = [isinstance(c, PowerLaw) for c in m]
        assert True in is_pl_instance

    def test_auto_add_edges_false(self):
        m = self.s.create_model(auto_background=False)
        from hyperspy.components1d import PowerLaw

        is_pl_instance = [isinstance(c, PowerLaw) for c in m]
        assert True not in is_pl_instance

    def test_auto_add_edges_false_names(self):
        m = self.s.create_model(auto_add_edges=False)
        cnames = [component.name for component in m]
        assert "B_K" not in cnames or "C_K" in cnames

    def test_convolved_ll_not_set(self):
        m = self.s.create_model(auto_add_edges=False)
        with pytest.raises(RuntimeError, match="not set"):
            m.convolved = True

    def test_low_loss(self):
        s = self.s
        low_loss = s.deepcopy()
        low_loss.axes_manager[-1].offset = -20
        m = s.create_model(low_loss=low_loss)
        assert m.low_loss is low_loss
        assert m.convolved

    def test_low_loss_bad_shape(self):
        low_loss = hs.stack([self.s] * 2)
        with pytest.raises(ValueError):
            _ = self.s.create_model(low_loss=low_loss)


@lazifyTestClass
class TestEELSModel:
    def setup_method(self, method):
        s = EELSSpectrum(np.ones(200))
        s.set_microscope_parameters(100, 10, 10)
        s.axes_manager[-1].offset = 150
        s.add_elements(("B", "C"))
        self.s = s
        self.m = s.create_model()

    def test_suspend_auto_fsw(self):
        m = self.m
        m["B_K"].fine_structure_width = 140.0
        m.suspend_auto_fine_structure_width()
        m.enable_fine_structure()
        m.resolve_fine_structure()
        assert 140 == m["B_K"].fine_structure_width

    def test_resume_fsw(self):
        m = self.m
        m["B_K"].fine_structure_width = 140.0
        m.suspend_auto_fine_structure_width()
        m.resume_auto_fine_structure_width()
        window = (
            m["C_K"].onset_energy.value
            - m["B_K"].onset_energy.value
            - m._preedge_safe_window_width
        )
        m.enable_fine_structure()
        m.resolve_fine_structure()
        assert window == m["B_K"].fine_structure_width

    def test_disable_fine_structure(self):
        self.m.components.C_K.fine_structure_active = True
        self.m.components.B_K.fine_structure_active = True
        self.m.disable_fine_structure()
        assert not self.m.components.C_K.fine_structure_active
        assert not self.m.components.B_K.fine_structure_active

    def test_get_first_ionization_edge_energy_C_B(self):
        assert (
            self.m._get_first_ionization_edge_energy()
            == self.m["B_K"].onset_energy.value
        )

    def test_get_first_ionization_edge_energy_C(self):
        self.m["B_K"].active = False
        assert (
            self.m._get_first_ionization_edge_energy()
            == self.m["C_K"].onset_energy.value
        )

    def test_get_first_ionization_edge_energy_None(self):
        self.m["B_K"].active = False
        self.m["C_K"].active = False
        assert self.m._get_first_ionization_edge_energy() is None

    def test_two_area_powerlaw_estimation_BC(self):
        self.m.signal.data = 2.0 * self.m.axis.axis ** (-3)  # A= 2, r=3
        # self.m.signal.axes_manager[-1].is_binned = False
        self.m.two_area_background_estimation()
        np.testing.assert_allclose(
            self.m._background_components[0].A.value, 2.1451237089380295
        )
        np.testing.assert_allclose(
            self.m._background_components[0].r.value, 3.0118980767392736
        )

    def test_two_area_powerlaw_estimation_C(self):
        self.m["B_K"].active = False
        self.m.signal.data = 2.0 * self.m.axis.axis ** (-3)  # A= 2, r=3
        # self.m.signal.axes_manager[-1].is_binned = False
        self.m.two_area_background_estimation()
        np.testing.assert_allclose(
            self.m._background_components[0].A.value, 2.3978438900878087
        )
        np.testing.assert_allclose(
            self.m._background_components[0].r.value, 3.031884021065014
        )

    def test_two_area_powerlaw_estimation_no_edge(self):
        self.m["B_K"].active = False
        self.m["C_K"].active = False
        self.m.signal.data = 2.0 * self.m.axis.axis ** (-3)  # A= 2, r=3
        print(self.m.signal.axes_manager[-1].is_binned)
        # self.m.signal.axes_manager[-1].is_binned = False
        self.m.two_area_background_estimation()
        np.testing.assert_allclose(
            self.m._background_components[0].A.value, 2.6598803469440986
        )
        np.testing.assert_allclose(
            self.m._background_components[0].r.value, 3.0494030409062058
        )

    def test_get_start_energy_none(self):
        assert self.m._get_start_energy() == 150

    def test_get_start_energy_above(self):
        assert self.m._get_start_energy(170) == 170

    def test_get_start_energy_below(self):
        assert self.m._get_start_energy(100) == 150

    def test_remove_components(self):
        comp = self.m[1]
        assert len(self.m) == 3
        self.m.remove(comp)
        assert len(self.m) == 2

    def test_fit_wrong_kind(self):
        with pytest.raises(ValueError):
            self.m.fit(kind="wrongkind")

    def test_enable_background(self):
        self.m.components.PowerLaw.active = False
        self.m.enable_background()
        assert self.m.components.PowerLaw.active

    def test_disable_background(self):
        self.m.components.PowerLaw.active = True
        self.m.disable_background()
        assert not self.m.components.PowerLaw.active

    def test_signal1d_property(self):
        assert self.s == self.m.signal
        s_new = EELSSpectrum(np.ones(200))
        s_new.set_microscope_parameters(100, 10, 10)
        self.m.signal = s_new
        assert self.m.signal == s_new

    def test_signal1d_property_wrong_value_setter(self):
        m = self.m
        s = hs.signals.Signal1D(np.ones(200))
        with pytest.raises(ValueError):
            m.signal = s

    def test_remove(self):
        m = self.m
        c_k = m.components.C_K
        assert c_k in m
        m.remove(c_k)
        assert c_k not in m

    def test_quantify(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            self.m.quantify()
        out = f.getvalue()
        assert (
            out
            == "\nAbsolute quantification:\nElem.\tIntensity\nB\t1.000000\nC\t1.000000\n"
        )

    def test_enable_edges(self):
        m = self.m
        m.components.B_K.active = False
        m.components.C_K.active = False
        m.enable_edges(edges_list=[m.components.B_K])
        assert m.components.B_K.active
        assert not m.components.C_K.active
        m.enable_edges()
        assert m.components.B_K.active
        assert m.components.C_K.active

    def test_disable_edges(self):
        m = self.m
        m.components.B_K.active = True
        m.components.C_K.active = True
        m.disable_edges(edges_list=[m.components.B_K])
        assert not m.components.B_K.active
        assert m.components.C_K.active
        m.disable_edges()
        assert not m.components.B_K.active
        assert not m.components.C_K.active

    def test_set_all_edges_intensities_positive(self):
        m = self.m
        m.components.B_K.intensity.ext_force_positive = False
        m.components.B_K.intensity.ext_bounded = False
        m.components.C_K.intensity.ext_force_positive = False
        m.components.C_K.intensity.ext_bounded = False
        m.set_all_edges_intensities_positive()
        assert m.components.B_K.intensity.ext_force_positive
        assert m.components.B_K.intensity.ext_bounded
        assert m.components.C_K.intensity.ext_force_positive
        assert m.components.C_K.intensity.ext_bounded

    def test_unset_all_edges_intensities_positive(self):
        m = self.m
        m.components.B_K.intensity.ext_force_positive = True
        m.components.B_K.intensity.ext_bounded = True
        m.components.C_K.intensity.ext_force_positive = True
        m.components.C_K.intensity.ext_bounded = True
        m.unset_all_edges_intensities_positive()
        assert not m.components.B_K.intensity.ext_force_positive
        assert not m.components.B_K.intensity.ext_bounded
        assert not m.components.C_K.intensity.ext_force_positive
        assert not m.components.C_K.intensity.ext_bounded

    def test_fix_edges(self):
        m = self.m
        m.components.B_K.onset_energy.free = True
        m.components.B_K.intensity.free = True
        m.components.B_K.fine_structure_coeff.free = True
        m.components.C_K.onset_energy.free = True
        m.components.C_K.intensity.free = True
        m.components.C_K.fine_structure_coeff.free = True
        m.fix_edges(edges_list=[m.components.B_K])
        assert not m.components.B_K.onset_energy.free
        assert not m.components.B_K.intensity.free
        assert not m.components.B_K.fine_structure_coeff.free
        assert m.components.C_K.onset_energy.free
        assert m.components.C_K.intensity.free
        assert m.components.C_K.fine_structure_coeff.free
        m.fix_edges()
        assert not m.components.B_K.onset_energy.free
        assert not m.components.B_K.intensity.free
        assert not m.components.B_K.fine_structure_coeff.free
        assert not m.components.C_K.onset_energy.free
        assert not m.components.C_K.intensity.free
        assert not m.components.C_K.fine_structure_coeff.free

    def test_free_edges(self):
        m = self.m
        m.components.B_K.onset_energy.free = False
        m.components.B_K.intensity.free = False
        m.components.B_K.fine_structure_coeff.free = False
        m.components.C_K.onset_energy.free = False
        m.components.C_K.intensity.free = False
        m.components.C_K.fine_structure_coeff.free = False
        m.free_edges(edges_list=[m.components.B_K])
        assert m.components.B_K.onset_energy.free
        assert m.components.B_K.intensity.free
        assert m.components.B_K.fine_structure_coeff.free
        assert not m.components.C_K.onset_energy.free
        assert not m.components.C_K.intensity.free
        assert not m.components.C_K.fine_structure_coeff.free
        m.free_edges()
        assert m.components.B_K.onset_energy.free
        assert m.components.B_K.intensity.free
        assert m.components.B_K.fine_structure_coeff.free
        assert m.components.C_K.onset_energy.free
        assert m.components.C_K.intensity.free
        assert m.components.C_K.fine_structure_coeff.free

    def test_fix_fine_structure(self):
        m = self.m
        m.components.B_K.fine_structure_coeff.free = True
        m.components.C_K.fine_structure_coeff.free = True
        m.fix_fine_structure(edges_list=[m.components.B_K])
        assert not m.components.B_K.fine_structure_coeff.free
        assert m.components.C_K.fine_structure_coeff.free
        m.fix_fine_structure()
        assert not m.components.B_K.fine_structure_coeff.free
        assert not m.components.C_K.fine_structure_coeff.free

    def test_free_fine_structure(self):
        m = self.m
        m.components.B_K.fine_structure_coeff.free = False
        m.components.C_K.fine_structure_coeff.free = False
        m.free_fine_structure(edges_list=[m.components.B_K])
        assert m.components.B_K.fine_structure_coeff.free
        assert not m.components.C_K.fine_structure_coeff.free
        m.free_fine_structure()
        assert m.components.B_K.fine_structure_coeff.free
        assert m.components.C_K.fine_structure_coeff.free


@lazifyTestClass
class TestEELSModelFitting:
    def setup_method(self, method):
        data = np.zeros(200)
        data[25:] = 100
        s = EELSSpectrum(data)
        s.set_microscope_parameters(100, 10, 10)
        s.axes_manager[-1].offset = 150
        s.add_elements(("B",))
        self.m = s.create_model(auto_background=False)

    @pytest.mark.parametrize("kind", ["std", "smart"])
    def test_free_edges(self, kind):
        m = self.m
        m.enable_fine_structure()
        intensity = m.components.B_K.intensity.value
        onset_energy = m.components.B_K.onset_energy.value
        fine_structure_coeff = m.components.B_K.fine_structure_coeff.value
        m.free_edges()
        m.multifit(kind=kind)
        assert intensity != m.components.B_K.intensity.value
        assert onset_energy != m.components.B_K.onset_energy.value
        assert fine_structure_coeff != m.components.B_K.fine_structure_coeff.value

    @pytest.mark.parametrize("kind", ["std", "smart"])
    def test_fix_edges(self, kind):
        m = self.m
        m.enable_fine_structure()
        intensity = m.components.B_K.intensity.value
        onset_energy = m.components.B_K.onset_energy.value
        fine_structure_coeff = m.components.B_K.fine_structure_coeff.value
        m.free_edges()
        m.fix_edges()
        m.multifit(kind=kind)
        assert intensity == m.components.B_K.intensity.value
        assert onset_energy == m.components.B_K.onset_energy.value
        assert fine_structure_coeff == m.components.B_K.fine_structure_coeff.value


@lazifyTestClass
class TestFitBackground:
    def setup_method(self, method):
        s = EELSSpectrum(np.ones(200))
        s.set_microscope_parameters(100, 10, 10)
        s.axes_manager[-1].offset = 150
        CE = elements.C.Atomic_properties.Binding_energies.K.onset_energy_eV
        BE = elements.B.Atomic_properties.Binding_energies.K.onset_energy_eV
        s.isig[BE:] += 1
        s.isig[CE:] += 1
        s.add_elements(("Be", "B", "C"))
        self.m = s.create_model(auto_background=False)
        self.m.append(hs.model.components1D.Offset())

    def test_fit_background_B_C(self):
        self.m.fit_background()
        np.testing.assert_allclose(self.m["Offset"].offset.value, 1)
        assert self.m["B_K"].active
        assert self.m["C_K"].active

    def test_fit_background_C(self):
        self.m["B_K"].active = False
        self.m.fit_background()
        np.testing.assert_allclose(self.m["Offset"].offset.value, 1.7142857)
        assert not self.m["B_K"].active
        assert self.m["C_K"].active

    def test_fit_background_no_edge(self):
        self.m["B_K"].active = False
        self.m["C_K"].active = False
        self.m.fit_background()
        np.testing.assert_allclose(self.m["Offset"].offset.value, 2.14)
        assert not self.m["B_K"].active
        assert not self.m["C_K"].active


@lazifyTestClass
class TestFitBackground2D:
    def setup_method(self):
        pl = hs.model.components1D.PowerLaw()
        data = np.empty((2, 250))
        data[0] = pl.function(np.arange(150, 400))
        pl.r.value = 1.5
        data[1] = pl.function(np.arange(150, 400))
        s = EELSSpectrum(data)
        s.set_microscope_parameters(100, 10, 10)
        s.axes_manager[-1].offset = 150
        self.s = s
        self.m = s.create_model()

    def test_only_current_false(self):
        self.m.fit_background(only_current=False)
        if self.s._lazy and Version(dask.__version__) < Version("2024.12.0"):
            pytest.skip("dask version must be >= 2024.12.0.")
        residual = self.s - self.m.as_signal()
        assert pytest.approx(residual.data) == 0


@lazifyTestClass
class TestEELSFineStructure:
    def setup_method(self, method):
        s = EELSSpectrum(np.zeros((1024)))
        s.axes_manager[0].units = "eV"
        s.axes_manager[0].scale = 0.1
        s.axes_manager[0].offset = 690
        s.add_elements(["Fe"])
        s.set_microscope_parameters(100, 15, 30)

        m = s.create_model(GOS="hydrogenic", auto_background=False)

        self.g1 = hs.model.components1D.GaussianHF(centre=712, height=50, fwhm=3)
        self.g2 = hs.model.components1D.GaussianHF(centre=725, height=30, fwhm=4)
        self.m = m

    def test_fs_components_in_model_update(self):
        self.m.components.Fe_L3.fine_structure_components.update((self.g1, self.g2))
        for component in self.m.components.Fe_L3.fine_structure_components:
            assert component in self.m

    def test_fs_components_in_model_add(self):
        self.m.components.Fe_L3.fine_structure_components.update((self.g1, self.g2))
        for component in (self.g1, self.g2):
            self.m.components.Fe_L3.fine_structure_components.add(component)
            assert component in self.m

    @pytest.mark.parametrize("fine_structure_active", [True, False])
    def test_fs_components_inherit_fs_active(self, fine_structure_active):
        self.m.components.Fe_L3.fine_structure_active = fine_structure_active
        self.m.components.Fe_L3.fine_structure_components.update((self.g1, self.g2))
        for component in self.m.components.Fe_L3.fine_structure_components:
            assert component.active == fine_structure_active
        self.m.components.Fe_L3.fine_structure_active = not fine_structure_active
        for component in self.m.components.Fe_L3.fine_structure_components:
            assert component.active == (not fine_structure_active)

    def test_fine_structure_smoothing(self):
        Fe = self.m.components.Fe_L3
        Fe.fine_structure_active = True
        Fe.fine_structure_smoothing = 0.3
        len_coeff = len(Fe.fine_structure_coeff.value)
        Fe.fine_structure_smoothing = 0.2
        assert len(Fe.fine_structure_coeff) < len_coeff
        Fe.fine_structure_smoothing = 0.4
        assert len(Fe.fine_structure_coeff) > len_coeff
        with pytest.raises(ValueError):
            Fe.fine_structure_smoothing = 3
        with pytest.raises(ValueError):
            Fe.fine_structure_smoothing = -3

    def test_free_fix_fine_structure(self):
        Fe = self.m.components.Fe_L3
        Fe.fine_structure_active = True
        assert Fe.fine_structure_coeff.free
        Fe.fix_fine_structure()
        assert not Fe.fine_structure_coeff.free
        Fe.free_fine_structure()
        assert Fe.fine_structure_coeff.free
        Fe.fine_structure_components.update((self.g1, self.g2))
        self.g1.fwhm.free = False
        self.g2.fwhm.free = False
        Fe.fix_fine_structure()
        for component in (self.g1, self.g2):
            for parameter in component.parameters:
                assert not parameter.free
        Fe.free_fine_structure()
        for component in (self.g1, self.g2):
            for parameter in component.parameters:
                if parameter.name != "fwhm":
                    assert parameter.free
                else:
                    assert not parameter.free

    def test_fine_structure_active_frees_coeff(self):
        Fe = self.m.components.Fe_L3
        Fe.fine_structure_active = True
        assert Fe.fine_structure_coeff.free
        Fe.fine_structure_coeff.free = False
        Fe.fine_structure_active = False
        assert not Fe.fine_structure_coeff.free
        Fe.fine_structure_active = True
        assert not Fe.fine_structure_coeff.free

    def test_fine_structure_spline_active_frees_coeff(self):
        Fe = self.m.components.Fe_L3
        Fe.fine_structure_active = True
        assert Fe.fine_structure_coeff.free
        Fe.fine_structure_spline_active = False
        assert not Fe.fine_structure_coeff.free
        Fe.fine_structure_spline_active = True
        assert Fe.fine_structure_coeff.free
        Fe.fine_structure_coeff.free = False
        Fe.fine_structure_spline_active = False
        assert not Fe.fine_structure_coeff.free
        Fe.fine_structure_spline_active = True
        assert not Fe.fine_structure_coeff.free

    def test_fine_structure_spline(self):
        Fe = self.m.components.Fe_L3
        Fe.fine_structure_active = True
        Fe.fine_structure_spline_active = True
        Fe.fine_structure_width = 30
        axis1 = np.linspace(
            Fe.onset_energy.value,
            Fe.onset_energy.value + Fe.fine_structure_width,
            endpoint=False,
        )
        assert np.all(Fe.function(axis1) == 0)
        Fe.fine_structure_coeff.value = (
            np.arange(len(Fe.fine_structure_coeff.value)) + 1
        )
        assert np.all(Fe.function(axis1) != 0)
        Fe.fine_structure_spline_onset = 10
        Fe.fine_structure_coeff.value = (
            np.arange(len(Fe.fine_structure_coeff.value)) + 1
        )
        axis2 = np.linspace(
            Fe.onset_energy.value,
            Fe.onset_energy.value + Fe.fine_structure_spline_onset,
            endpoint=False,
        )
        axis3 = np.linspace(
            Fe.onset_energy.value + Fe.fine_structure_spline_onset,
            Fe.onset_energy.value + Fe.fine_structure_width,
            endpoint=False,
        )
        assert np.all(Fe.function(axis2) == 0)
        assert np.all(Fe.function(axis3) != 0)

    def test_model_store_restore(self):
        Fe = self.m.components.Fe_L3
        Fe.fine_structure_active = True
        Fe.fine_structure_components.update((self.g1, self.g2))
        Fe.fine_structure_spline_onset = 20
        Fe.fine_structure_coeff.value = (
            np.arange(len(Fe.fine_structure_coeff.value)) + 1
        )
        m = self.m
        m.store()
        mc = m.signal.models.a.restore()
        assert np.array_equal(m._get_current_data(), mc._get_current_data())


class TestModelJacobians:
    def setup_method(self, method):
        s = EELSSpectrum(np.zeros(1))
        m = s.create_model(auto_add_edges=False, auto_background=False)
        self.low_loss = 7.0
        self.weights = 0.3
        m.axis.axis = np.array([1, 0])
        m._channel_switches = np.array([0, 1], dtype=bool)
        m.append(hs.model.components1D.Gaussian())
        m[0].A.value = 1
        m[0].centre.value = 2.0
        m[0].sigma.twin = m[0].centre
        m._low_loss = mock.MagicMock()
        m._low_loss._get_current_data = mock.MagicMock()
        m.low_loss._get_current_data.return_value = self.low_loss
        self.model = m
        m._convolution_axis = np.zeros(2)

    def test_jacobian_convolved(self):
        m = self.model
        m.convolved = True
        m.append(hs.model.components1D.Gaussian())
        m[0].convolved = False
        m[1].convolved = True
        assert m.low_loss._get_current_data() == 7
        jac = m._jacobian((1, 2, 3, 4, 5), None, weights=self.weights)
        np.testing.assert_array_almost_equal(
            jac.squeeze(),
            self.weights
            * np.array(
                [
                    m[0].A.grad(0),
                    m[0].sigma.grad(0) + m[0].centre.grad(0),
                    m[1].A.grad(0) * self.low_loss,
                    m[1].centre.grad(0) * self.low_loss,
                    m[1].sigma.grad(0) * self.low_loss,
                ]
            ),
        )
        assert m[0].A.value == 1
        assert m[0].centre.value == 2
        assert m[0].sigma.value == 2
        assert m[1].A.value == 3
        assert m[1].centre.value == 4
        assert m[1].sigma.value == 5


class TestModelSettingPZero:
    def setup_method(self, method):
        s = EELSSpectrum(np.empty(1))
        m = s.create_model(auto_add_edges=False, auto_background=False)
        self.model = m

    def test_calculating_convolution_axis(self, caplog):
        m = self.model
        # setup
        m.axis.offset = 10
        m.axis.size = 10
        ll_axis = mock.MagicMock()
        ll_axis.size = 7
        ll_axis.value2index.return_value = 3
        m._low_loss = mock.MagicMock()
        m.low_loss.axes_manager.signal_axes = [
            ll_axis,
        ]

        # calculation
        m._set_convolution_axis()

        # tests
        np.testing.assert_array_equal(m._convolution_axis, np.arange(7, 23))
        np.testing.assert_equal(ll_axis.value2index.call_args[0][0], 0)

        with caplog.at_level(logging.WARNING):
            # deprecation warning
            m.set_convolution_axis()

        with caplog.at_level(logging.WARNING):
            # deprecation warning
            convolution_axis = m.convolution_axis.copy()

        with caplog.at_level(logging.WARNING):
            # deprecation warning
            m.convolution_axis = convolution_axis


@lazifyTestClass
class TestConvolveModelSlicing:
    def setup_method(self, method):
        s = EELSSpectrum(np.random.random((10, 10, 600)))
        s.axes_manager[-1].offset = -150.0
        s.axes_manager[-1].scale = 0.5
        m = s.create_model(auto_add_edges=False, auto_background=False)
        m.low_loss = s + 1
        g = hs.model.components1D.Gaussian()
        m.append(g)
        self.m = m

    def test_slicing_low_loss_inav(self):
        m = self.m
        m1 = m.inav[::2]
        assert m1.signal.data.shape == m1.low_loss.data.shape

    def test_slicing_low_loss_isig(self):
        m = self.m
        m1 = m.isig[::2]
        assert m.signal.data.shape == m1.low_loss.data.shape


class TestModelDictionary:
    def setup_method(self, method):
        s = EELSSpectrum(np.array([1.0, 2, 4, 7, 12, 7, 4, 2, 1]))
        m = s.create_model(auto_add_edges=False, auto_background=False)
        m.low_loss = (s + 3.0).deepcopy()
        self.model = m
        self.s = s

        m.append(hs.model.components1D.Gaussian())
        m.append(hs.model.components1D.Gaussian())
        m.append(hs.model.components1D.ScalableFixedPattern(s * 0.3))
        m[0].A.twin = m[1].A
        m.fit()

    def test_to_dictionary(self):
        m = self.model
        d = m.as_dictionary()

        np.testing.assert_allclose(m.low_loss.data, d["low_loss"]["data"])

    def test_load_dictionary(self):
        d = self.model.as_dictionary()
        mn = self.s.create_model()
        mn.append(hs.model.components1D.Lorentzian())
        mn._load_dictionary(d)
        mo = self.model

        np.testing.assert_allclose(mn.low_loss.data, mo.low_loss.data)
        for i in range(len(mn)):
            assert mn[i]._id_name == mo[i]._id_name
            for po, pn in zip(mo[i].parameters, mn[i].parameters):
                np.testing.assert_allclose(po.map["values"], pn.map["values"])
                np.testing.assert_allclose(po.map["is_set"], pn.map["is_set"])

        assert mn[0].A.twin is mn[1].A
