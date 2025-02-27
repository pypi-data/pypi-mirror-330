import ctypes
import platform
from .affine import *
from .apply_cmap import *
from .apply_lut import *
from .basic import *
from .blend import *
from .circular_qualifier import *
from .cmaps import *
from .color_mixer import *
from .compand import *
from .comps import *
from .contrast import *
from .space_convert import *
from .delta_e_1976 import *
from .delta_e_1994 import *
from .delta_e_2000 import *
from .file_io import *
from .filters import *
from .hist import *
from .lerp import *
from .lib_convert import *
from .linear_qualifier import *
from .make_cmap import *
from .neutral_lut import *
from .photos import *
from .rect_sdf import *
from .sig import *
from .space_convert import *
from .swap import *
from .tex import *
from .type_convert import *
from .util import *

if platform.system() == 'Windows':
	ctypes.windll.shcore.SetProcessDpiAwareness(1)