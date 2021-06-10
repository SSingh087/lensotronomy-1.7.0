import pytest
import numpy.testing as npt
import numpy as np
from lenstronomy.GalKin import velocity_util


class TestVelocityUtil(object):
    """

    """

    def setup(self):
        pass

    def test_sample_gaussian(self):
        np.random.seed(41)
        n = 1000
        FWHM = 1
        pos_x, pos_y = [], []
        for i in range(n):
            x, y = velocity_util.displace_PSF_gaussian(0, 0, FWHM)
            pos_x.append(x)
            pos_y.append(y)

        sigma = FWHM / (2 * np.sqrt(2 * np.log(2)))
        sigma_x = np.std(pos_x)
        npt.assert_almost_equal(sigma, sigma_x, decimal=1)

    def test_sample_moffat(self):
        np.random.seed(41)
        n = 10000
        FWHM = 1
        beta = 2.6
        r_list = []
        for i in range(n):
            r = velocity_util.draw_moffat_r(FWHM, beta)
            r_list.append(r)
        x_array = np.linspace(0, 4 * FWHM, num=100)
        r_hist, bins = np.histogram(r_list, bins=x_array, density=True)
        alpha = velocity_util.moffat_fwhm_alpha(FWHM, beta)

        x_ = x_array[1:] - x_array[1] + x_array[0]
        f_moffat = velocity_util.moffat_r(x_, alpha=alpha, beta=beta) * x_
        #import matplotlib.pyplot as plt
        #plt.plot(x_, f_moffat, label='moffat')
        #plt.plot(x_, r_hist, label='sampled')
        #plt.legend()
        #plt.show()
        npt.assert_almost_equal(r_hist, f_moffat, decimal=1)

    def test_displace_PSF_moffat(self):
        FWHM = 1
        beta = 2.6
        np.random.seed(41)
        x, y = 0, 0
        x_d, y_d = velocity_util.displace_PSF_moffat(x, y, FWHM, beta)
        assert x_d != x
        assert y_d != y






if __name__ == '__main__':
    pytest.main()
