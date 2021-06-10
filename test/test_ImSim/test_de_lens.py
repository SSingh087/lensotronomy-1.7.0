__author__ = 'sibirrer'

import numpy as np
import numpy.testing as npt
import lenstronomy.ImSim.de_lens as DeLens
import pytest


class TestDeLens(object):

    def setup(self):
        self.deLens = DeLens

    def test_get_param_WLS(self):
        A = np.array([[1, 2, 3], [3, 2, 1]]).T
        C_D_inv = np.array([1, 1, 1])
        d = np.array([1, 2, 3])
        result, cov_error, image = self.deLens.get_param_WLS(A, C_D_inv, d)
        npt.assert_almost_equal(result[0], 1, decimal=8)
        npt.assert_almost_equal(result[1], 0, decimal=8)
        npt.assert_almost_equal(image[0], d[0], decimal=8)

        result_new, cov_error_new, image_new = self.deLens.get_param_WLS(A, C_D_inv, d, inv_bool=False)
        npt.assert_almost_equal(result_new[0], result[0], decimal=10)
        npt.assert_almost_equal(result_new[1], result[1], decimal=10)
        npt.assert_almost_equal(image_new[0], image[0], decimal=10)

    def test_wls_stability(self):
        A = np.array([[1, 2, 3], [3, 2, 1]]).T
        C_D_inv = np.array([0, 0, 0])
        d = np.array([1, 2, 3])
        result, cov_error, image = self.deLens.get_param_WLS(A, C_D_inv, d)
        npt.assert_almost_equal(result[0], 0, decimal=8)
        npt.assert_almost_equal(result[1], 0, decimal=8)
        npt.assert_almost_equal(image[0], 0, decimal=8)

        A = np.array([[1, 2, 1], [1, 2, 1]]).T
        d = np.array([1, 2, 3])
        result, cov_error, image = self.deLens.get_param_WLS(A, C_D_inv, d, inv_bool=False)

        npt.assert_almost_equal(result[0], 0, decimal=8)
        npt.assert_almost_equal(result[1], 0, decimal=8)
        npt.assert_almost_equal(image[0], 0, decimal=8)

        C_D_inv = np.array([1, 1, 1])
        A = np.array([[1., 2., 1. + 10**(-8.9)], [1., 2., 1.]]).T
        d = np.array([1, 2, 3])
        result, cov_error, image = self.deLens.get_param_WLS(A, C_D_inv, d, inv_bool=False)
        result, cov_error, image = self.deLens.get_param_WLS(A, C_D_inv, d, inv_bool=True)
        npt.assert_almost_equal(result[0], 0, decimal=8)
        npt.assert_almost_equal(result[1], 0, decimal=8)
        npt.assert_almost_equal(image[0], 0, decimal=8)

    def test_marginalisation_const(self):
        A = np.array([[1,2,3],[3,2,1]]).T
        C_D_inv = np.array([1,1,1])
        d = np.array([1,2,3])
        result, cov_error, image = self.deLens.get_param_WLS(A, C_D_inv, d)
        logL_marg = self.deLens.marginalisation_const(cov_error)
        npt.assert_almost_equal(logL_marg, -2.2821740957339181, decimal=8)

        M_inv = np.array([[1,0],[0,1]])
        marg_const = self.deLens.marginalisation_const(M_inv)
        assert marg_const == 0

    def test_margnialization_new(self):
        M_inv = np.array([[1, -0.5, 1],
                          [-0.5, 3, 0],
                          [1, 0, 2]])
        d_prior = 1000
        m = len(M_inv)
        log_det = DeLens.marginalization_new(M_inv, d_prior=d_prior)
        log_det_old = DeLens.marginalisation_const(M_inv)
        npt.assert_almost_equal(log_det, log_det_old + m/2. * np.log(np.pi/2.) - m * np.log(d_prior), decimal=9)

        M_inv = np.array([[1, 1, 1],
                          [0., 1., 0.],
                          [1., 2., 1.]])
        log_det = DeLens.marginalization_new(M_inv, d_prior=10)
        log_det_old = DeLens.marginalisation_const(M_inv)
        npt.assert_almost_equal(log_det, log_det_old, decimal=9)
        npt.assert_almost_equal(log_det, -10**(15), decimal=10)

        log_det = DeLens.marginalization_new(M_inv, d_prior=None)
        log_det_old = DeLens.marginalisation_const(M_inv)
        npt.assert_almost_equal(log_det, log_det_old, decimal=9)


if __name__ == '__main__':
    pytest.main()
