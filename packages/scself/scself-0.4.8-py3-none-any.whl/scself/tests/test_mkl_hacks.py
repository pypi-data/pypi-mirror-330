import os
import unittest
import numpy as np
import numpy.testing as npt

try:
    from scself.sparse.truncated_svd import TruncatedSVDMKL
    MKL_SKIP = False
except ImportError:
    MKL_SKIP = True

from sklearn.decomposition import TruncatedSVD

DATA = np.random.default_rng(100).random((100, 50)).astype(np.float32)


@unittest.skipIf(MKL_SKIP, 'NO MKL')
class TestTruncatedSVDMKL(unittest.TestCase):

    @unittest.skipIf('CI' in os.environ, 'Skip for CI')
    def test_tsvd_mkl(self):

        scaler_old = TruncatedSVD(
            n_components=5,
            algorithm='randomized',
            random_state=50
        )
        scaler_new = TruncatedSVDMKL(
            n_components=5,
            algorithm='randomized',
            random_state=50
        )

        scaler_old.fit(DATA)
        scaler_new.fit(DATA)

        npt.assert_almost_equal(
            scaler_new.components_,
            scaler_old.components_,
            decimal=2
        )

        npt.assert_almost_equal(
            scaler_new.explained_variance_,
            scaler_old.explained_variance_,
            decimal=2
        )
