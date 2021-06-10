import numpy as np
import numpy.testing as npt
import pytest
import matplotlib.pyplot as plt


import lenstronomy.Plots.plot_util as plot_util


class TestPlotUtil(object):

    def setup(self):
        pass

    def test_sqrt(self):
        image = np.random.randn(10, 10)
        image_rescaled = plot_util.sqrt(image)
        npt.assert_almost_equal(np.min(image_rescaled), 0)

    def test_scale_bar(self):
        f, ax = plt.subplots(1, 1, figsize=(4, 4))
        plot_util.scale_bar(ax, 3, dist=1, text='1"', flipped=True)
        plt.close()
        f, ax = plt.subplots(1, 1, figsize=(4, 4))
        plot_util.text_description(ax, d=3, text='test', color='w', backgroundcolor='k', flipped=True)
        plt.close()

    def test_source_position_plot(self):
        from lenstronomy.PointSource.point_source import PointSource
        from lenstronomy.LensModel.lens_model import LensModel
        lensModel = LensModel(lens_model_list=['SIS'])
        ps = PointSource(point_source_type_list=['UNLENSED', 'LENSED_POSITION', 'SOURCE_POSITION'], lensModel=lensModel)
        kwargs_lens = [{'theta_E': 1., 'center_x': 0, 'center_y': 0}]
        kwargs_ps = [{'ra_image': [1., 1.], 'dec_image': [0, 1], 'point_amp': [1, 1]},
                          {'ra_image': [1.], 'dec_image': [1.], 'point_amp': [10]},
                          {'ra_source': 0.1, 'dec_source': 0, 'point_amp': 1.}]
        ra_source, dec_source = ps.source_position(kwargs_ps, kwargs_lens)
        from lenstronomy.Data.coord_transforms import Coordinates
        coords_source = Coordinates(transform_pix2angle=np.array([[1, 0], [0, 1]])* 0.1,
                                    ra_at_xy_0=-2,
                                    dec_at_xy_0=-2)

        f, ax = plt.subplots(1, 1, figsize=(4, 4))
        plot_util.source_position_plot(ax, coords_source, ra_source, dec_source)
        plt.close()

    def test_result_string(self):
        x = np.random.normal(loc=1, scale=0.1, size=10000)
        string =plot_util.result_string(x, weights=None, title_fmt=".2f", label='test')
        print(string)
        assert string == str('test = ${1.00}_{-0.10}^{+0.10}$')


if __name__ == '__main__':
    pytest.main()
