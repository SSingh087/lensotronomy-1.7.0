__author__ = 'sibirrer'

import pytest
import numpy as np
import numpy.testing as npt

from lenstronomy.LensModel.lens_model import LensModel


class TestNumerics(object):
    """
    tests the source model routines
    """
    def setup(self):
        self.lensModel = LensModel(['GAUSSIAN'])
        self.kwargs = [{'amp': 1./4., 'sigma_x': 2., 'sigma_y': 2., 'center_x': 0., 'center_y': 0.}]

    def test_kappa(self):
        x, y = 1., 1.
        output = self.lensModel.kappa(x, y, self.kwargs)
        output_num = self.lensModel.kappa(x, y, self.kwargs, diff=0.00001)
        npt.assert_almost_equal(output_num, output, decimal=5)

    def test_gamma(self):
        x, y = 1., 2.
        output1, output2 = self.lensModel.gamma(x, y, self.kwargs)
        output1_num, output2_num = self.lensModel.gamma(x, y, self.kwargs, diff=0.00001)
        npt.assert_almost_equal(output1_num, output1, decimal=5)
        npt.assert_almost_equal(output2_num, output2, decimal=5)

    def test_magnification(self):
        x, y = 1., 1.
        output = self.lensModel.magnification(x, y, self.kwargs)
        output_num = self.lensModel.magnification(x, y, self.kwargs, diff=0.00001)
        npt.assert_almost_equal(output_num, output, decimal=5)

    def test_differentials(self):
        x, y = 1., 1.
        f_xx, f_xy, f_yx, f_yy = self.lensModel.hessian(x, y, self.kwargs)
        f_xx_num, f_xy_num, f_yx_num, f_yy_num = self.lensModel.hessian(x, y, self.kwargs, diff=0.00001)
        assert f_xy_num == f_yx_num
        npt.assert_almost_equal(f_xx_num, f_xx, decimal=5)
        npt.assert_almost_equal(f_xy_num, f_xy, decimal=5)
        npt.assert_almost_equal(f_yx_num, f_yx, decimal=5)
        npt.assert_almost_equal(f_yy_num, f_yy, decimal=5)

    def test_flexion(self):
        lensModel = LensModel(lens_model_list=['FLEXION'])
        g1, g2, g3, g4 = 0.01, 0.02, 0.03, 0.04
        kwargs = [{'g1': g1, 'g2': g2, 'g3': g3, 'g4': g4}]
        f_xxx, f_xxy, f_xyy, f_yyy = lensModel.flexion(x=1., y=1., kwargs=kwargs, diff=0.0001)
        npt.assert_almost_equal(f_xxx, g1, decimal=2)
        npt.assert_almost_equal(f_xxy, g2, decimal=2)
        npt.assert_almost_equal(f_xyy, g3, decimal=2)
        npt.assert_almost_equal(f_yyy, g4, decimal=2)

        f_xxx, f_xxy, f_xyy, f_yyy = lensModel.flexion(x=1., y=1., kwargs=kwargs, diff=0.0001, hessian_diff=0.001)
        npt.assert_almost_equal(f_xxx, g1, decimal=2)
        npt.assert_almost_equal(f_xxy, g2, decimal=2)
        npt.assert_almost_equal(f_xyy, g3, decimal=2)
        npt.assert_almost_equal(f_yyy, g4, decimal=2)


class TestNumericsProfile(object):
    """
    tests the second derivatives of various lens models
    """
    def setup(self):
        pass

    def assert_differentials(self, lens_model, kwargs, potential=True):
        #lensModelNum = NumericLens(lens_model)
        diff = 0.000001
        #x, y = 1., 2.
        x = np.linspace(start=0.1, stop=5.5, num=10)
        y = np.zeros_like(x)
        lensModel = LensModel(lens_model)
        f_xx, f_xy, f_yx, f_yy = lensModel.hessian(x, y, [kwargs])
        f_xx_num, f_xy_num, f_yx_num, f_yy_num = lensModel.hessian(x, y, [kwargs], diff=diff)

        npt.assert_almost_equal(f_xx, f_xx_num, decimal=3)
        npt.assert_almost_equal(f_yy, f_yy_num, decimal=3)
        npt.assert_almost_equal(f_xy, f_xy_num, decimal=3)

        if potential is True:
            f_x, f_y = lensModel.alpha(x, y, [kwargs])
            f_x_num, f_y_num = lensModel.alpha(x, y, [kwargs], diff=diff)

            npt.assert_almost_equal(f_x, f_x_num, decimal=3)
            npt.assert_almost_equal(f_y, f_y_num, decimal=3)

    def test_gaussian(self):
        lens_model = ['GAUSSIAN']
        kwargs = {'amp': 1. / 4., 'sigma_x': 2., 'sigma_y': 2., 'center_x': 0., 'center_y': 0.}
        self.assert_differentials(lens_model, kwargs)
        kwargs = {'amp': 1. / 4., 'sigma_x': 20., 'sigma_y': 20., 'center_x': 0., 'center_y': 0.}
        self.assert_differentials(lens_model, kwargs)
        kwargs = {'amp': 1. / 4., 'sigma_x': 2., 'sigma_y': 2., 'center_x': 2., 'center_y': 2.}
        self.assert_differentials(lens_model, kwargs)

    def test_gausian_kappa(self):
        kwargs = {'amp': 1. / 4., 'sigma': 2., 'center_x': 0., 'center_y': 0.}
        lens_model = ['GAUSSIAN_KAPPA']
        self.assert_differentials(lens_model, kwargs)

    def test_gausian_ellipse_kappa(self):
        kwargs = {'amp': 1., 'sigma': 1., 'e1': 0.1, 'e2': -0.1, 'center_x':
            0., 'center_y': 0.}
        lens_model = ['GAUSSIAN_ELLIPSE_KAPPA']
        self.assert_differentials(lens_model, kwargs)

    def test_gausian_ellipse_potential(self):
        kwargs = {'amp': 1., 'sigma': 2., 'e1': .1, 'e2': -0.1, 'center_x': 0., 'center_y': 0.}
        lens_model = ['GAUSSIAN_ELLIPSE_POTENTIAL']
        self.assert_differentials(lens_model, kwargs)

    def test_external_shear(self):
        kwargs = {'gamma1': 0.1, 'gamma2': -0.1}
        lens_model = ['SHEAR']
        self.assert_differentials(lens_model, kwargs)

    def test_hessian(self):
        kwargs = {'f_xx': 0.1, 'f_yy': -0.1, 'f_xy': 0.1, 'f_yx': 0.1}
        lens_model = ['HESSIAN']
        self.assert_differentials(lens_model, kwargs)

    def test_mass_sheet(self):
        kwargs = {'kappa_ext': 0.1}
        lens_model = ['CONVERGENCE']
        self.assert_differentials(lens_model, kwargs)

    def test_sis(self):
        kwargs = {'theta_E': 0.5}
        lens_model = ['SIS']
        self.assert_differentials(lens_model, kwargs)

    def test_flexion(self):
        kwargs = {'g1': 0.01, 'g2': -0.01, 'g3': 0.001, 'g4': 0}
        lens_model = ['FLEXION']
        self.assert_differentials(lens_model, kwargs)

    def test_nfw(self):
        kwargs = {'alpha_Rs': .1, 'Rs': 5.}
        lens_model = ['NFW']
        self.assert_differentials(lens_model, kwargs)

    def test_tnfw(self):
        kwargs = {'alpha_Rs': .1, 'Rs': 5., 'r_trunc': 7}
        lens_model = ['TNFW']
        self.assert_differentials(lens_model, kwargs)

        kwargs = {'Rs': 2., 'alpha_Rs': 1., 'r_trunc': 7}
        lens_model = ['TNFW']
        self.assert_differentials(lens_model, kwargs)

    def test_nfw_ellipse(self):
        kwargs = {'alpha_Rs': .1, 'Rs': 5., 'e1': 0.04, 'e2': -0.04}
        lens_model = ['NFW_ELLIPSE']
        self.assert_differentials(lens_model, kwargs)

    def test_nfw_ellipse_gauss_dec(self):
        kwargs = {'alpha_Rs': .1, 'Rs': 5., 'e1': 0.04, 'e2': -0.04}
        lens_model = ['NFW_ELLIPSE_GAUSS_DEC']
        self.assert_differentials(lens_model, kwargs)

    def test_ctnfw_gauss_dec(self):
        kwargs = {'rho_s': 5, 'r_s': 5., 'r_trunc': 10., 'r_core': 0.3, 'a': 2}
        lens_model = ['CTNFW_GAUSS_DEC']
        self.assert_differentials(lens_model, kwargs)

    def test_point_mass(self):
        kwargs = {'theta_E': 2.}
        lens_model = ['POINT_MASS']
        self.assert_differentials(lens_model, kwargs)

    def test_sersic(self):
        kwargs = {'n_sersic': .5, 'R_sersic': 1.5, 'k_eff': 0.3}
        lens_model = ['SERSIC']
        self.assert_differentials(lens_model, kwargs)

    def test_sersic_ellipse_gauss_dec(self):
        kwargs = {'n_sersic': 1., 'R_sersic': 2., 'k_eff': 1., 'e1': 0.04,
                  'e2': 0.}
        lens_model = ['SERSIC_ELLIPSE_GAUSS_DEC']
        self.assert_differentials(lens_model, kwargs)

    def test_sersic_ellipse_pot(self):
        kwargs = {'n_sersic': 2., 'R_sersic': 0.5, 'k_eff': 0.3, 'e1': 0.04, 'e2': -0.0}
        lens_model = ['SERSIC_ELLIPSE_POTENTIAL']
        self.assert_differentials(lens_model, kwargs)

    def test_shapelets_pot_2(self):
        kwargs = {'coeffs': [0, 1, 2, 3, 4, 5], 'beta': 0.3}
        lens_model = ['SHAPELETS_CART']
        self.assert_differentials(lens_model, kwargs)

    def test_sis_truncate(self):
        kwargs = {'theta_E': 0.5, 'r_trunc': 2.}
        lens_model = ['SIS_TRUNCATED']
        self.assert_differentials(lens_model, kwargs)

    def test_spep(self):
        kwargs = {'theta_E': 0.5, 'gamma': 1.9, 'e1': 0.04, 'e2': -0.1}
        lens_model = ['SPEP']
        self.assert_differentials(lens_model, kwargs)

    def test_spp(self):
        kwargs = {'theta_E': 0.5, 'gamma': 1.9}
        lens_model = ['SPP']
        self.assert_differentials(lens_model, kwargs)

    def test_PJaffe(self):
        kwargs = {'sigma0': 1., 'Ra': 0.2, 'Rs': 2.}
        lens_model = ['PJAFFE']
        self.assert_differentials(lens_model, kwargs)

    def test_PJaffe_ellipse(self):
        kwargs = {'sigma0': 1., 'Ra': 0.2, 'Rs': 2., 'e1': 0.04, 'e2': -0.0}
        lens_model = ['PJAFFE_ELLIPSE']
        self.assert_differentials(lens_model, kwargs)

    def test_Hernquist(self):
        kwargs = {'sigma0': 1., 'Rs': 1.5}
        lens_model = ['HERNQUIST']
        self.assert_differentials(lens_model, kwargs)

    def test_Hernquist_ellipse(self):
        kwargs = {'sigma0': 1., 'Rs': 1.5, 'e1': 0.04, 'e2': -0.0}
        lens_model = ['HERNQUIST_ELLIPSE']
        self.assert_differentials(lens_model, kwargs)

    def test_NIE(self):
        kwargs = {'theta_E': 2., 'e1': 0.1, 'e2': 0., 's_scale': 0.04}
        lens_model = ['NIE']
        self.assert_differentials(lens_model, kwargs)

    def test_NIE_simple(self):
        kwargs = {'b': 2., 'q': 0.3, 's': 0.04}
        lens_model = ['NIE_SIMPLE']
        self.assert_differentials(lens_model, kwargs)

    def test_EPL(self):
        kwargs = {'theta_E': 2., 'e1': 0.1, 'e2': 0., 'gamma': 2.13}
        lens_model = ['EPL']
        self.assert_differentials(lens_model, kwargs)

    def test_coreBurk(self):
        kwargs={'Rs':2, 'alpha_Rs': 1, 'r_core':0.4}
        lens_model = ['coreBURKERT']
        self.assert_differentials(lens_model, kwargs)
        kwargs = {'Rs': 2, 'alpha_Rs': 1, 'r_core':5}
        self.assert_differentials(lens_model, kwargs)

    def test_cnfw(self):
        kwargs={'Rs': 15.5, 'alpha_Rs': 1., 'r_core': 8.}
        lens_model = ['CNFW']
        self.assert_differentials(lens_model, kwargs, potential=True)

    def test_cnfw_ellipse(self):
        kwargs = {'alpha_Rs': .1, 'Rs': 5., 'r_core': 0.1, 'e1': 0.04, 'e2': -0.04}
        lens_model = ['CNFW_ELLIPSE']
        self.assert_differentials(lens_model, kwargs, potential=True)

    def test_cored_density(self):
        kwargs = {'sigma0': 0.1, 'r_core': 8}
        lens_model = ['CORED_DENSITY']
        self.assert_differentials(lens_model, kwargs)

    def test_cored_density_2(self):
        kwargs = {'sigma0': 0.1, 'r_core': 8}
        lens_model = ['CORED_DENSITY_2']
        self.assert_differentials(lens_model, kwargs)

    def test_cored_density_mst(self):
        kwargs = {'lambda_approx': 1.1, 'r_core': 8}
        lens_model = ['CORED_DENSITY_MST']
        self.assert_differentials(lens_model, kwargs)

    def test_cored_density_2_mst(self):
        kwargs = {'lambda_approx': 1.1, 'r_core': 8}
        lens_model = ['CORED_DENSITY_2_MST']
        self.assert_differentials(lens_model, kwargs)
        
    def test_const_mag_positive(self):
        kwargs = {'mu_r': 1, 'mu_t': 10, 'parity': 1, 'phi_G': 0.1}
        lens_model = ['CONST_MAG']
        self.assert_differentials(lens_model, kwargs)
        
    def test_const_mag_negative(self):
        kwargs = {'mu_r': 1, 'mu_t': 10, 'parity': -1, 'phi_G': 0.1}
        lens_model = ['CONST_MAG']
        self.assert_differentials(lens_model, kwargs)
        
    def test_nie_potential(self):
        kwargs = {'theta_E':2. , 'theta_c':1. , 'e1': 0.1, 'e2': 0.1}
        lens_model = ['NIE_POTENTIAL']
        self.assert_differentials(lens_model, kwargs)
    def test_multipole(self):
        kwargs = {'m':4, 'a_m':0.05, 'phi_m':0.1, 'center_x':0., 'center_y':0.}
        lens_model = ['MULTIPOLE']
        self.assert_differentials(lens_model,kwargs,potential=True)
        kwargs = {'m': 2, 'a_m': 0.1, 'phi_m': 0.05, 'center_x': 0., 'center_y': 0.}
        lens_model = ['MULTIPOLE']
        self.assert_differentials(lens_model, kwargs, potential=True)
        kwargs = {'m': 3, 'a_m': 0.07, 'phi_m': 0., 'center_x': -0.01, 'center_y': -0.5}
        lens_model = ['MULTIPOLE']
        self.assert_differentials(lens_model, kwargs, potential=True)


if __name__ == '__main__':
    pytest.main("-k TestLensModel")
