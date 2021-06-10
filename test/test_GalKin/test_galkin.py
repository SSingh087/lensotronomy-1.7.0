"""
Tests for `galkin` module.
"""
import pytest
import unittest
import numpy.testing as npt
import numpy as np
import scipy.integrate as integrate
from lenstronomy.GalKin.galkin import Galkin
from lenstronomy.GalKin.light_profile import LightProfile
from lenstronomy.GalKin.analytic_kinematics import AnalyticKinematics
import lenstronomy.Util.param_util as param_util


class TestGalkin(object):

    def setup(self):
        np.random.seed(42)

    def test_log_linear_integral(self):
        # light profile
        light_profile_list = ['HERNQUIST']
        Rs = .5
        kwargs_light = [{'Rs':  Rs, 'amp': 1.}]  # effective half light radius (2d projected) in arcsec
        # 0.551 *
        # mass profile
        mass_profile_list = ['SPP']
        theta_E = 1.2
        gamma = 2.
        kwargs_profile = [{'theta_E': theta_E, 'gamma': gamma}]  # Einstein radius (arcsec) and power-law slope

        # anisotropy profile
        anisotropy_type = 'OM'
        r_ani = 2.
        kwargs_anisotropy = {'r_ani': r_ani}  # anisotropy radius [arcsec]

        # aperture as slit
        aperture_type = 'slit'

        psf_fwhm = 0.7  # Gaussian FWHM psf
        kwargs_cosmo = {'d_d': 1000, 'd_s': 1500, 'd_ds': 800}
        kwargs_numerics_linear = {'interpol_grid_num': 500, 'log_integration': False,
                           'max_integrate': 10, 'min_integrate': 0.001}
        kwargs_numerics_log = {'interpol_grid_num': 500, 'log_integration': True,
                           'max_integrate': 10, 'min_integrate': 0.001}
        kwargs_aperture = {'width': 1, 'length': 1., 'aperture_type': aperture_type}
        kwargs_psf = {'psf_type': 'GAUSSIAN', 'fwhm': psf_fwhm}
        kwargs_model = {'mass_profile_list': mass_profile_list,
                        'light_profile_list': light_profile_list,
                        'anisotropy_model': anisotropy_type}
        galkin_linear = Galkin(kwargs_model=kwargs_model, kwargs_aperture=kwargs_aperture,
                               kwargs_psf=kwargs_psf, kwargs_cosmo=kwargs_cosmo, kwargs_numerics=kwargs_numerics_linear)
        galkin_log = Galkin(kwargs_model=kwargs_model, kwargs_aperture=kwargs_aperture,
                            kwargs_psf=kwargs_psf, kwargs_cosmo=kwargs_cosmo, kwargs_numerics=kwargs_numerics_log)
        R = np.linspace(0.05, 1, 100)
        lin_I_R = np.zeros_like(R)
        log_I_R = np.zeros_like(R)
        for i in range(len(R)):
            lin_I_R[i] = galkin_linear.numerics._I_R_sigma2(R[i], kwargs_profile, kwargs_light, kwargs_anisotropy)
            log_I_R[i] = galkin_log.numerics._I_R_sigma2(R[i], kwargs_profile, kwargs_light, kwargs_anisotropy)
        print(log_I_R/lin_I_R)
        for i in range(len(R)):
            npt.assert_almost_equal(log_I_R[i] / lin_I_R[i], 1, decimal=2)

    def test_log_vs_linear_integral(self):
        # light profile
        light_profile_list = ['HERNQUIST']
        Rs = .5
        kwargs_light = [{'Rs':  Rs, 'amp': 1.}]  # effective half light radius (2d projected) in arcsec
        # 0.551 *
        # mass profile
        mass_profile_list = ['SPP']
        theta_E = 1.2
        gamma = 2.
        kwargs_profile = [{'theta_E': theta_E, 'gamma': gamma}]  # Einstein radius (arcsec) and power-law slope

        # anisotropy profile
        anisotropy_type = 'OM'
        r_ani = 2.
        kwargs_anisotropy = {'r_ani': r_ani}  # anisotropy radius [arcsec]

        # aperture as slit
        aperture_type = 'slit'
        length = 3.8
        width = 0.9
        kwargs_aperture = {'aperture_type': aperture_type, 'length': length, 'width': width, 'center_ra': 0, 'center_dec': 0, 'angle': 0}

        psf_fwhm = 0.7  # Gaussian FWHM psf
        kwargs_cosmo = {'d_d': 1000, 'd_s': 1500, 'd_ds': 800}
        kwargs_numerics_log = {'interpol_grid_num': 500, 'log_integration': True,
                           'max_integrate': 10}
        kwargs_numerics_linear = {'interpol_grid_num': 500, 'log_integration': False,
                           'max_integrate': 10}
        kwargs_psf = {'psf_type': 'GAUSSIAN', 'fwhm': psf_fwhm}
        kwargs_model = {'mass_profile_list': mass_profile_list,
                        'light_profile_list': light_profile_list,
                        'anisotropy_model': anisotropy_type}
        galkin_linear = Galkin(kwargs_model=kwargs_model, kwargs_aperture=kwargs_aperture, kwargs_psf=kwargs_psf,
                               kwargs_cosmo=kwargs_cosmo, kwargs_numerics=kwargs_numerics_linear)

        sigma_v = galkin_linear.dispersion(kwargs_profile, kwargs_light, kwargs_anisotropy, sampling_number=1000)
        galkin_log = Galkin(kwargs_model=kwargs_model, kwargs_aperture=kwargs_aperture, kwargs_psf=kwargs_psf,
                            kwargs_cosmo=kwargs_cosmo, kwargs_numerics=kwargs_numerics_log)
        sigma_v2 = galkin_log.dispersion(kwargs_profile, kwargs_light, kwargs_anisotropy, sampling_number=1000)
        print(sigma_v, sigma_v2, 'sigma_v linear, sigma_v log')
        print((sigma_v/sigma_v2)**2)

        npt.assert_almost_equal(sigma_v/sigma_v2, 1, decimal=1)

    def test_compare_power_law(self):
        """
        compare power-law profiles analytical vs. numerical
        :return:
        """
        # light profile
        light_profile_list = ['HERNQUIST']
        r_eff = 1.5
        kwargs_light = [{'Rs':  0.551 * r_eff, 'amp': 1.}]  # effective half light radius (2d projected) in arcsec
        # 0.551 *
        # mass profile
        mass_profile_list = ['SPP']
        theta_E = 1.2
        gamma = 2.
        kwargs_profile = [{'theta_E': theta_E, 'gamma': gamma}]  # Einstein radius (arcsec) and power-law slope

        # anisotropy profile
        anisotropy_type = 'OM'
        r_ani = 2.
        kwargs_anisotropy = {'r_ani': r_ani}  # anisotropy radius [arcsec]

        # aperture as slit
        aperture_type = 'slit'
        length = 1.
        width = 0.3
        kwargs_aperture = {'aperture_type': aperture_type, 'length': length, 'width': width, 'center_ra': 0, 'center_dec': 0, 'angle': 0}

        psf_fwhm = 1.  # Gaussian FWHM psf
        kwargs_cosmo = {'d_d': 1000, 'd_s': 1500, 'd_ds': 800}
        kwargs_numerics = {'interpol_grid_num': 500, 'log_integration': True,
                           'max_integrate': 100}
        kwargs_model = {'mass_profile_list': mass_profile_list,
                        'light_profile_list': light_profile_list,
                        'anisotropy_model': anisotropy_type}
        kwargs_psf = {'psf_type': 'GAUSSIAN', 'fwhm': psf_fwhm}
        galkin = Galkin(kwargs_model=kwargs_model, kwargs_aperture=kwargs_aperture, kwargs_psf=kwargs_psf,
                        kwargs_cosmo=kwargs_cosmo, kwargs_numerics=kwargs_numerics)
        sigma_v = galkin.dispersion(kwargs_profile, kwargs_light, kwargs_anisotropy, sampling_number=1000)

        kwargs_numerics = {'interpol_grid_num': 500, 'log_integration': False, 'max_integrate': 10}

        galkin = Galkin(kwargs_model=kwargs_model, kwargs_aperture=kwargs_aperture, kwargs_psf=kwargs_psf,
                        kwargs_cosmo=kwargs_cosmo, kwargs_numerics=kwargs_numerics, analytic_kinematics=False)
        sigma_v_lin = galkin.dispersion(kwargs_profile, kwargs_light, kwargs_anisotropy, sampling_number=1000)

        los_disp = Galkin(kwargs_model=kwargs_model, kwargs_aperture=kwargs_aperture, kwargs_psf=kwargs_psf,
                        kwargs_cosmo=kwargs_cosmo, kwargs_numerics=kwargs_numerics, analytic_kinematics=True)
        sigma_v2 = los_disp.dispersion(kwargs_mass={'gamma': gamma, 'theta_E': theta_E}, kwargs_light={'r_eff': r_eff},
                                       kwargs_anisotropy={'r_ani':r_ani}, sampling_number=1000)
        print(sigma_v, sigma_v_lin, sigma_v2, 'sigma_v Galkin (log and linear), sigma_v los dispersion')
        npt.assert_almost_equal(sigma_v2/sigma_v, 1, decimal=2)

    def test_projected_light_integral_hernquist(self):
        """

        :return:
        """
        light_profile_list = ['HERNQUIST']
        Rs = 1.
        kwargs_light = [{'Rs': Rs, 'amp': 1.}]  # effective half light radius (2d projected) in arcsec
        lightProfile = LightProfile(light_profile_list)
        R = 2
        light2d = lightProfile.light_2d(R=R, kwargs_list=kwargs_light)
        out = integrate.quad(lambda x: lightProfile.light_3d(np.sqrt(R**2+x**2), kwargs_light), 0, 100)
        npt.assert_almost_equal(light2d, out[0]*2, decimal=3)

    def test_projected_light_integral_hernquist_ellipse(self):
        """

        :return:
        """
        light_profile_list = ['HERNQUIST_ELLIPSE']
        Rs = 1.
        phi, q = 1, 0.8
        e1, e2 = param_util.phi_q2_ellipticity(phi, q)
        kwargs_light = [{'Rs': Rs, 'amp': 1.,'e1': e1, 'e2': e2}]  # effective half light radius (2d projected) in arcsec
        lightProfile = LightProfile(light_profile_list)
        R = 2
        light2d = lightProfile.light_2d(R=R, kwargs_list=kwargs_light)
        out = integrate.quad(lambda x: lightProfile.light_3d(np.sqrt(R**2+x**2), kwargs_light), 0, 10)
        npt.assert_almost_equal(light2d, out[0]*2, decimal=3)

    def test_projected_light_integral_pjaffe(self):
        """

        :return:
        """
        light_profile_list = ['PJAFFE']
        kwargs_light = [{'Rs': .5, 'Ra': 0.01, 'amp': 1.}]  # effective half light radius (2d projected) in arcsec
        lightProfile = LightProfile(light_profile_list)
        R = 0.01
        light2d = lightProfile.light_2d(R=R, kwargs_list=kwargs_light)
        out = integrate.quad(lambda x: lightProfile.light_3d(np.sqrt(R**2+x**2), kwargs_light), 0, 100)
        print(out, 'out')
        npt.assert_almost_equal(light2d/(out[0]*2), 1., decimal=3)

    def test_realistic_0(self):
        """
        realistic test example
        :return:
        """
        light_profile_list = ['HERNQUIST']
        kwargs_light = [{'Rs': 0.10535462602138289, 'center_x': -0.02678473951679429, 'center_y': 0.88691126347462712, 'amp': 3.7114695634960109}]
        lightProfile = LightProfile(light_profile_list)
        R = 0.01
        light2d = lightProfile.light_2d(R=R, kwargs_list=kwargs_light)
        out = integrate.quad(lambda x: lightProfile.light_3d(np.sqrt(R**2+x**2), kwargs_light), 0, 100)
        print(out, 'out')
        npt.assert_almost_equal(light2d/(out[0]*2), 1., decimal=3)

    def test_realistic_1(self):
        """
        realistic test example
        :return:
        """
        light_profile_list = ['HERNQUIST_ELLIPSE']
        phi, q = 0.74260706384506325, 0.46728323131925864
        e1, e2 = param_util.phi_q2_ellipticity(phi, q)
        kwargs_light = [{'Rs': 0.10535462602138289, 'e1': e1, 'e2': e2, 'center_x': -0.02678473951679429, 'center_y': 0.88691126347462712, 'amp': 3.7114695634960109}]
        lightProfile = LightProfile(light_profile_list)
        R = 0.01
        light2d = lightProfile.light_2d(R=R, kwargs_list=kwargs_light)
        out = integrate.quad(lambda x: lightProfile.light_3d(np.sqrt(R**2+x**2), kwargs_light), 0, 100)
        print(out, 'out')
        npt.assert_almost_equal(light2d/(out[0]*2), 1., decimal=3)

    def test_realistic(self):
        """
        realistic test example
        :return:
        """
        light_profile_list = ['HERNQUIST_ELLIPSE', 'PJAFFE_ELLIPSE']
        phi, q = 0.74260706384506325, 0.46728323131925864
        e1, e2 = param_util.phi_q2_ellipticity(phi, q)

        phi2, q2 = -0.33379268413794494, 0.66582356813012267
        e12, e22 = param_util.phi_q2_ellipticity(phi2, q2)
        kwargs_light = [{'Rs': 0.10535462602138289, 'e1': e1, 'e2': e2, 'center_x': -0.02678473951679429, 'center_y': 0.88691126347462712, 'amp': 3.7114695634960109},
                        {'Rs': 0.44955054610388684, 'e1': e12, 'e2': e22, 'center_x': 0.019536801118136753, 'center_y': 0.0218888643537157, 'Ra': 0.0010000053334891974, 'amp': 967.00280526319796}]
        lightProfile = LightProfile(light_profile_list)
        R = 0.01
        light2d = lightProfile.light_2d(R=R, kwargs_list=kwargs_light)
        out = integrate.quad(lambda x: lightProfile.light_3d(np.sqrt(R**2+x**2), kwargs_light), 0, 100)
        print(out, 'out')
        npt.assert_almost_equal(light2d/(out[0]*2), 1., decimal=3)

    def test_dispersion_map(self):
        """
        tests whether the old and new version provide the same answer
        """
        # light profile
        light_profile_list = ['HERNQUIST']
        r_eff = 1.5
        kwargs_light = [{'Rs': r_eff, 'amp': 1.}]  # effective half light radius (2d projected) in arcsec
        # 0.551 *
        # mass profile
        mass_profile_list = ['SPP']
        theta_E = 1.2
        gamma = 2.
        kwargs_mass = [{'theta_E': theta_E, 'gamma': gamma}]  # Einstein radius (arcsec) and power-law slope

        # anisotropy profile
        anisotropy_type = 'OM'
        r_ani = 2.
        kwargs_anisotropy = {'r_ani': r_ani}  # anisotropy radius [arcsec]

        # aperture as shell
        #aperture_type = 'shell'
        #kwargs_aperture_inner = {'r_in': 0., 'r_out': 0.2, 'center_dec': 0, 'center_ra': 0}

        #kwargs_aperture_outer = {'r_in': 0., 'r_out': 1.5, 'center_dec': 0, 'center_ra': 0}

        # aperture as slit
        r_bins = np.linspace(0, 2, 3)
        kwargs_ifu = {'r_bins': r_bins, 'center_ra': 0, 'center_dec': 0, 'aperture_type': 'IFU_shells'}
        kwargs_aperture = {'aperture_type': 'shell', 'r_in': r_bins[0], 'r_out': r_bins[1], 'center_ra': 0,
                           'center_dec': 0}

        psf_fwhm = 1.  # Gaussian FWHM psf
        kwargs_cosmo = {'d_d': 1000, 'd_s': 1500, 'd_ds': 800}
        kwargs_numerics = {'interpol_grid_num': 500, 'log_integration': True,
                           'max_integrate': 100}
        kwargs_model = {'mass_profile_list': mass_profile_list,
                        'light_profile_list': light_profile_list,
                        'anisotropy_model': anisotropy_type}
        kwargs_psf = {'psf_type': 'GAUSSIAN', 'fwhm': psf_fwhm}

        galkinIFU = Galkin(kwargs_aperture=kwargs_ifu, kwargs_psf=kwargs_psf, kwargs_cosmo=kwargs_cosmo,
                           kwargs_model=kwargs_model, kwargs_numerics=kwargs_numerics, analytic_kinematics=True)
        sigma_v_ifu = galkinIFU.dispersion_map(kwargs_mass={'theta_E': theta_E, 'gamma': gamma}, kwargs_light={'r_eff': r_eff},
                                               kwargs_anisotropy=kwargs_anisotropy, num_kin_sampling=1000)
        galkin = Galkin(kwargs_model, kwargs_aperture, kwargs_psf, kwargs_cosmo, kwargs_numerics,
                        analytic_kinematics=True)
        sigma_v = galkin.dispersion(kwargs_mass={'theta_E': theta_E, 'gamma': gamma}, kwargs_light={'r_eff': r_eff},
                                    kwargs_anisotropy=kwargs_anisotropy, sampling_number=1000)
        npt.assert_almost_equal(sigma_v, sigma_v_ifu[0], decimal=-1)


class TestRaise(unittest.TestCase):

    def test_raise(self):
        with self.assertRaises(ValueError):
            kwargs_model = {'anisotropy_model': 'const'}
            kwargs_aperture = {'center_ra': 0, 'width': 1, 'length': 1, 'angle': 0, 'center_dec': 0,
                               'aperture_type': 'slit'}
            kwargs_cosmo = {'d_d': 1000, 'd_s': 1500, 'd_ds': 800}
            kwargs_psf = {'psf_type': 'GAUSSIAN', 'fwhm': 1}
            Galkin(kwargs_model, kwargs_aperture, kwargs_psf, kwargs_cosmo, kwargs_numerics={},
                   analytic_kinematics=True)


if __name__ == '__main__':
    pytest.main()
