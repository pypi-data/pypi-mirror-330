# -*- coding: utf-8 -*-
# Copyright 2007-2024 The HyperSpy developers
#
# This file is part of HyperSpy.
#
# HyperSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HyperSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HyperSpy. If not, see <https://www.gnu.org/licenses/#GPL>.


import numpy as np
import pytest

import hyperspy.api as hs
from hyperspy.decorators import lazifyTestClass
from hyperspy.misc.hist_tools import histogram


def generate_bad_toy_data():
    """
    Use a deliberately bad dataset here, as per
    https://github.com/hyperspy/hyperspy/issues/784,
    which previously caused a MemoryError when
    using the Freedman-Diaconis rule.
    """
    ax1 = np.exp(-np.abs(np.arange(-30, 100, 0.05)))
    s1 = hs.signals.Signal1D(ax1)
    s1 = hs.stack([s1] * 2)
    return s1


@pytest.mark.parametrize("bins", [10, np.linspace(1, 20, num=11)])
def test_types_of_bins(bins):
    s1 = generate_bad_toy_data()
    out = s1.get_histogram(bins)
    assert out.data.shape == (10,)
    s2 = generate_bad_toy_data().as_lazy()
    out = s2.get_histogram(bins)
    assert out.data.shape == (10,)


def test_knuth_bad_data_set():
    s1 = generate_bad_toy_data()
    with pytest.warns(UserWarning, match="Capping the number of bins"):
        out = s1.get_histogram("knuth")

    assert out.data.shape == (250,)


def test_bayesian_blocks_warning():
    s1 = generate_bad_toy_data()
    with np.errstate(divide="ignore"):  # Required here due to dataset
        with pytest.warns(
            UserWarning, match="is not fully supported in this version of HyperSpy"
        ):
            s1.get_histogram(bins="blocks")


def test_unsupported_lazy():
    s1 = generate_bad_toy_data().as_lazy()
    with pytest.raises(ValueError, match="Unrecognized 'bins' argument"):
        s1.get_histogram(bins="sturges")


@pytest.mark.parametrize("density", (True, False))
@pytest.mark.parametrize("lazy", (True, False))
def test_histogram_metadata(lazy, density):
    s1 = generate_bad_toy_data()
    if lazy:
        s1 = s1.as_lazy()
    s1.metadata.Signal.quantity = "Intensity (Count)"
    out = s1.get_histogram(bins=200, density=density)
    assert out.axes_manager[-1].name == "Intensity"
    assert out.axes_manager[-1].units == "Count"
    quantity = "Probability density" if density else "Count"
    assert out.metadata.Signal.quantity == quantity


@lazifyTestClass
class TestHistogramBinMethodsBadDataset:
    def setup_method(self, method):
        self.s1 = generate_bad_toy_data()

    def test_fd_logger_warning(self):
        with pytest.warns(UserWarning, match="Capping the number of bins"):
            out = self.s1.get_histogram()

        assert out.data.shape == (250,)

    def test_int_bins_logger_warning(self):
        with pytest.warns(UserWarning, match="Capping the number of bins"):
            out = self.s1.get_histogram(bins=251)

        assert out.data.shape == (250,)

    @pytest.mark.parametrize("bins, size", [("scott", (58,)), (10, (10,))])
    def test_working_bins(self, bins, size):
        out = self.s1.get_histogram(bins=bins)
        assert out.data.shape == size

    def test_range_bins(self):
        # when falling back to capping the number of bins to 250, make sure
        # that the kwargs are passed correctly
        with pytest.warns(UserWarning, match="Capping the number of bins"):
            out = self.s1.get_histogram(range_bins=[1e-10, 0.5])

        axis = out.axes_manager[-1].axis
        np.testing.assert_allclose(axis[0], 1e-10)
        np.testing.assert_allclose(axis[-1], 0.498)


def test_histogram_dask_array_fallback():
    s = generate_bad_toy_data().as_lazy()
    out, bins = histogram(s.data, bins=10)
    assert bins.shape == (11,)
    np.testing.assert_allclose(out, [5014, 56, 32, 24, 20, 12, 12, 12, 8, 10])
