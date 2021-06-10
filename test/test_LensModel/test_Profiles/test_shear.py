__author__ = 'sibirrer'


from lenstronomy.LensModel.Profiles.shear import Shear, ShearGammaPsi
from lenstronomy.LensModel.lens_model import LensModel
from lenstronomy.Util import param_util

import numpy as np
import numpy.testing as npt
import pytest


class TestShear(object):
    """
    tests the Gaussian methods
    """
    def setup(self):
        self.extShear = Shear()

        gamma1, gamma2 = 0.1, 0.1
        self.kwargs_lens = {'gamma1': gamma1, 'gamma2': gamma2}

    def test_function(self):
        x = np.array([1])
        y = np.array([2])
        values = self.extShear.function(x, y, **self.kwargs_lens)
        npt.assert_almost_equal(values[0], 0.05, decimal=5)
        x = np.array([0])
        y = np.array([0])
        values = self.extShear.function(x, y, **self.kwargs_lens)
        npt.assert_almost_equal(values[0], 0, decimal=5)

        x = np.array([2, 3, 4])
        y = np.array([1, 1, 1])
        values = self.extShear.function(x, y, **self.kwargs_lens)
        npt.assert_almost_equal(values[0],  0.35, decimal=5)
        npt.assert_almost_equal(values[1], 0.7, decimal=5)

    def test_derivatives(self):
        x = np.array([1])
        y = np.array([2])
        f_x, f_y = self.extShear.derivatives(x, y, **self.kwargs_lens)
        npt.assert_almost_equal(f_x[0], 0.3, decimal=5)
        npt.assert_almost_equal(f_y[0], -0.1, decimal=5)

        x = np.array([1, 3, 4])
        y = np.array([2, 1, 1])
        values = self.extShear.derivatives(x, y, **self.kwargs_lens)
        npt.assert_almost_equal(values[0][0], 0.3, decimal=5)
        npt.assert_almost_equal(values[1][0], -0.1, decimal=5)

    def test_hessian(self):
        x = np.array([1])
        y = np.array([2])

        f_xx, f_yy, f_xy = self.extShear.hessian(x, y, **self.kwargs_lens)
        npt.assert_almost_equal(f_xx, 0.1, decimal=5)
        npt.assert_almost_equal(f_yy, -0.1, decimal=5)
        npt.assert_almost_equal(f_xy, 0.1, decimal=5)

        x = np.array([1,3,4])
        y = np.array([2,1,1])
        values = self.extShear.hessian(x, y, **self.kwargs_lens)
        npt.assert_almost_equal(values[0], 0.1, decimal=5)
        npt.assert_almost_equal(values[1], -0.1, decimal=5)
        npt.assert_almost_equal(values[2], 0.1, decimal=5)

        gamma1, gamma2 = 0.1, -0.1
        kwargs = {'gamma1': gamma1, 'gamma2': gamma2}
        lensModel = LensModel(['SHEAR'])
        gamma1, gamma2 = lensModel.gamma(x, y, [kwargs])
        npt.assert_almost_equal(gamma1, gamma1, decimal=9)
        npt.assert_almost_equal(gamma2, gamma2, decimal=9)


class TestShearGammaPsi(object):

    def setup(self):
        self.shear_e1e2 = Shear()
        self.shear = ShearGammaPsi()

    def test_function(self):
        x = np.array([1, 3, 4])
        y = np.array([2, 1, 1])
        gamma, psi = 0.1, 0.5
        gamma1, gamma2 = param_util.shear_polar2cartesian(phi=psi, gamma=gamma)
        values = self.shear.function(x, y, gamma, psi)
        values_e1e2 = self.shear_e1e2.function(x, y, gamma1, gamma2)
        npt.assert_almost_equal(values, values_e1e2, decimal=5)

    def test_derivatives(self):
        x = np.array([1, 3, 4])
        y = np.array([2, 1, 1])
        gamma, psi = 0.1, 0.5
        gamma1, gamma2 = param_util.shear_polar2cartesian(phi=psi, gamma=gamma)
        values = self.shear.derivatives(x, y, gamma, psi)
        values_e1e2 = self.shear_e1e2.derivatives(x, y, gamma1, gamma2)
        npt.assert_almost_equal(values, values_e1e2, decimal=5)

    def test_hessian(self):
        x = np.array([1, 3, 4])
        y = np.array([2, 1, 1])
        gamma, psi = 0.1, 0.5
        gamma1, gamma2 = param_util.shear_polar2cartesian(phi=psi, gamma=gamma)
        values = self.shear.hessian(x, y, gamma, psi)
        values_e1e2 = self.shear_e1e2.hessian(x, y, gamma1, gamma2)
        npt.assert_almost_equal(values, values_e1e2, decimal=5)


if __name__ == '__main__':
    pytest.main()
