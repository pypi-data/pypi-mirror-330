__version__ = '0.4.8'

from ._mcv import (
    mcv,
    mcv_r2_per_cell
)
from ._noise2self import (
    noise2self,
    multimodal_noise2self
)
from .scaling import (
    TruncRobustScaler,
    TruncStandardScaler,
    TruncMinMaxScaler
)
from .utils.dot_product import (
    dot,
    sparse_dot_patch
)
from .utils import standardize_data
from ._denoise import denoise_data
from ._modules import (
    get_correlation_modules,
    get_correlation_submodules,
    module_score,
    score_all_modules,
    score_all_submodules
)