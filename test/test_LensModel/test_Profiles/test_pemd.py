__author__ = 'sibirrer'


import numpy as np
import pytest
import numpy.testing as npt
import lenstronomy.Util.param_util as param_util

try:
    import fastell4py
    fastell4py_bool = True
except:
    print("Warning: fastell4py not available, tests will be trivially fulfilled without giving the right answer!")
    fastell4py_bool = False


class TestSPEMD(object):
    """
    tests the Gaussian methods
    """
    def setup(self):
        from lenstronomy.LensModel.Profiles.pemd import PEMD
        from lenstronomy.LensModel.Profiles.spep import SPEP
        self.PEMD = PEMD(suppress_fastell=True)
        self.SPEP = SPEP()

    def test_function(self):
        phi_E = 1.
        gamma = 1.9
        q = 0.9
        phi_G = 1.
        e1, e2 = param_util.phi_q2_ellipticity(phi_G, q)
        x = np.array([1.])
        y = np.array([2])
        a = np.zeros_like(x)
        values = self.PEMD.function(x, y, phi_E, gamma, e1, e2)
        if fastell4py_bool:
            assert values == 2.1567297115381039
        else:
            assert values == 0
        a += values
        x = np.array(1.)
        y = np.array(2.)
        a = np.zeros_like(x)
        values = self.PEMD.function(x, y, phi_E, gamma, e1, e2)
        print(x, values)
        a += values
        if fastell4py_bool:
            assert values == 2.1567297115381039
        else:
            assert values == 0
        assert type(x) == type(values)

        x = np.array([2, 3, 4])
        y = np.array([1, 1, 1])
        values = self.PEMD.function(x, y, phi_E, gamma, e1, e2)
        if fastell4py_bool:
            npt.assert_almost_equal(values[0], 2.1798076611034141, decimal=7)
            npt.assert_almost_equal(values[1], 3.209319798597186, decimal=7)
            npt.assert_almost_equal(values[2], 4.3105937398856398, decimal=7)
        else:
            npt.assert_almost_equal(values[0], 0, decimal=7)
            npt.assert_almost_equal(values[1], 0, decimal=7)
            npt.assert_almost_equal(values[2], 0, decimal=7)

    def test_derivatives(self):
        x = np.array([1])
        y = np.array([2])
        phi_E = 1.
        gamma = 1.9
        q = 0.9
        phi_G = 1.
        e1, e2 = param_util.phi_q2_ellipticity(phi_G, q)
        f_x, f_y = self.PEMD.derivatives(x, y, phi_E, gamma, e1, e2)
        if fastell4py_bool:
            npt.assert_almost_equal(f_x[0], 0.46663367437984204, decimal=7)
            npt.assert_almost_equal(f_y[0], 0.95307422686028065, decimal=7)
        else:
            npt.assert_almost_equal(f_x[0], 0, decimal=7)
            npt.assert_almost_equal(f_y[0], 0, decimal=7)

        x = np.array([1., 3, 4])
        y = np.array([2., 1, 1])
        a = np.zeros_like(x)
        values = self.PEMD.derivatives(x, y, phi_E, gamma, e1, e2)
        if fastell4py_bool:
            npt.assert_almost_equal(values[0][0], 0.46663367437984204, decimal=7)
            npt.assert_almost_equal(values[1][0], 0.95307422686028065, decimal=7)
            npt.assert_almost_equal(values[0][1], 1.0722152681324291, decimal=7)
            npt.assert_almost_equal(values[1][1], 0.31400298272329669, decimal=7)
        else:
            npt.assert_almost_equal(values[0][0], 0, decimal=7)
            npt.assert_almost_equal(values[1][0], 0, decimal=7)
            npt.assert_almost_equal(values[0][1], 0, decimal=7)
            npt.assert_almost_equal(values[1][1], 0, decimal=7)
        a += values[0]
        x = 1.
        y = 2.
        phi_E = 1.
        gamma = 1.9
        q = 0.9
        phi_G = 1.
        e1, e2 = param_util.phi_q2_ellipticity(phi_G, q)
        f_x, f_y = self.PEMD.derivatives(x, y, phi_E, gamma, e1, e2)
        if fastell4py_bool:
            npt.assert_almost_equal(f_x, 0.46663367437984204, decimal=7)
            npt.assert_almost_equal(f_y, 0.95307422686028065, decimal=7)
        else:
            npt.assert_almost_equal(f_x, 0, decimal=7)
            npt.assert_almost_equal(f_y, 0, decimal=7)
        x = 0.
        y = 0.
        f_x, f_y = self.PEMD.derivatives(x, y, phi_E, gamma, e1, e2)
        assert f_x == 0.
        assert f_y == 0.

    def test_hessian(self):
        x = np.array([1])
        y = np.array([2])
        phi_E = 1.
        gamma = 1.9
        q = 0.9
        phi_G = 1.
        e1, e2 = param_util.phi_q2_ellipticity(phi_G, q)
        f_xx, f_yy,f_xy = self.PEMD.hessian(x, y, phi_E, gamma, e1, e2)
        if fastell4py_bool:
            npt.assert_almost_equal(f_xx, 0.41789957732890953, decimal=7)
            npt.assert_almost_equal(f_yy, 0.14047593655054141, decimal=7)
            npt.assert_almost_equal(f_xy, -0.18560737698052343, decimal=7)
        else:
            npt.assert_almost_equal(f_xx, 0, decimal=7)
            npt.assert_almost_equal(f_yy, 0, decimal=7)
            npt.assert_almost_equal(f_xy, 0, decimal=7)

        x = 1.
        y = 2.
        phi_E = 1.
        gamma = 1.9
        q = 0.9
        phi_G = 1.
        e1, e2 = param_util.phi_q2_ellipticity(phi_G, q)
        a = np.zeros_like(x)
        f_xx, f_yy,f_xy = self.PEMD.hessian(x, y, phi_E, gamma, e1, e2)
        if fastell4py_bool:
            npt.assert_almost_equal(f_xx, 0.41789957732890953, decimal=7)
            npt.assert_almost_equal(f_yy, 0.14047593655054141, decimal=7)
            npt.assert_almost_equal(f_xy, -0.18560737698052343, decimal=7)
        else:
            npt.assert_almost_equal(f_xx, 0, decimal=7)
            npt.assert_almost_equal(f_yy, 0, decimal=7)
            npt.assert_almost_equal(f_xy, 0, decimal=7)
        a += f_xx
        x = np.array([1,3,4])
        y = np.array([2,1,1])
        values = self.PEMD.hessian(x, y, phi_E, gamma, e1, e2)
        print(values, 'values')
        if fastell4py_bool:
            npt.assert_almost_equal(values[0][0], 0.41789957732890953, decimal=7)
            npt.assert_almost_equal(values[1][0], 0.14047593655054141, decimal=7)
            npt.assert_almost_equal(values[2][0], -0.18560737698052343, decimal=7)
            npt.assert_almost_equal(values[0][1], 0.068359818958208918, decimal=7)
            npt.assert_almost_equal(values[1][1], 0.32494089371516482, decimal=7)
            npt.assert_almost_equal(values[2][1], -0.097845438684594374, decimal=7)
        else:
            npt.assert_almost_equal(values[0][0], 0, decimal=7)

    def test_spep_spemd(self):
        x = np.array([1])
        y = np.array([0])
        phi_E = 1.
        gamma = 2.
        q = 1.
        phi_G = 1.
        e1, e2 = param_util.phi_q2_ellipticity(phi_G, q)
        f_x, f_y = self.PEMD.derivatives(x, y, phi_E, gamma, e1, e2)
        f_x_spep, f_y_spep = self.SPEP.derivatives(x, y, phi_E, gamma, e1, e2)
        if fastell4py_bool:
            npt.assert_almost_equal(f_x[0], f_x_spep[0], decimal=2)
        else:
            pass

        theta_E = 2.
        gamma = 2.
        q = 1.
        phi_G = 1.
        e1, e2 = param_util.phi_q2_ellipticity(phi_G, q)
        f_x, f_y = self.PEMD.derivatives(x, y, theta_E, gamma, e1, e2)
        f_x_spep, f_y_spep = self.SPEP.derivatives(x, y, theta_E, gamma, e1, e2)
        if fastell4py_bool:
            npt.assert_almost_equal(f_x[0], f_x_spep[0], decimal=2)
        else:
            pass

        theta_E = 2.
        gamma = 1.7
        q = 1.
        phi_G = 1.
        e1, e2 = param_util.phi_q2_ellipticity(phi_G, q)
        f_x, f_y = self.PEMD.derivatives(x, y, theta_E, gamma, e1, e2)
        f_x_spep, f_y_spep = self.SPEP.derivatives(x, y, theta_E, gamma, e1, e2)
        if fastell4py_bool:
            npt.assert_almost_equal(f_x[0], f_x_spep[0], decimal=4)

    def test_bounds(self):
        from lenstronomy.LensModel.Profiles.spemd import SPEMD
        profile = SPEMD(suppress_fastell=True)
        compute_bool = profile._parameter_constraints(q_fastell=-1, gam=-1, s2=-1, q=-1)
        assert compute_bool is False

    def test_is_not_empty(self):
        func = self.PEMD.spemd_smooth.is_not_empty

        assert func(0.1, 0.2)
        assert func([0.1], [0.2])
        assert func((0.1, 0.3), (0.2, 0.4))
        assert func(np.array([0.1]), np.array([0.2]))
        assert not func([], [])
        assert not func(np.array([]), np.array([]))

    def test_density_lens(self):
        r = 1
        kwargs = {'theta_E': 1, 'gamma': 2, 'e1': 0, 'e2': 0}
        rho = self.PEMD.density_lens(r, **kwargs)
        rho_spep = self.SPEP.density_lens(r, **kwargs)
        npt.assert_almost_equal(rho, rho_spep, decimal=7)


if __name__ == '__main__':
    pytest.main()
