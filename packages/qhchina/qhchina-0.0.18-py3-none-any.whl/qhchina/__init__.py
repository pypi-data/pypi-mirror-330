# qhchina/__init__.py
__version__ = "0.0.18"

from .analysis import calculate_collocations, cooc_matrix, compare_bows, project_2d, binary_analysis, get_axis
from .preprocessing import split_into_chunks
from .helpers import install_package, load_texts, load_font, set_font, HELPERS_PATH, CJK_FONT_PATH, MPL_FONT_PATH
from .educational import show_vectors

__all__ = [
    'calculate_collocations',
    'cooc_matrix',
    'compare_bows',
    'split_into_chunks',
    'install_package',
    'load_texts',
    'show_vectors',
    'project_2d',
    'binary_analysis',
    'get_axis',
    'load_font',
    'set_font',
    'HELPERS_PATH',
    'CJK_FONT_PATH',
    'MPL_FONT_PATH'
]