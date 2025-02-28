"""
hyyap
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Author: Huang Yiyi
Version:0.0.3
"""

from .Install.mingw import MinGWInstaller
from .Install.innosetup import InnoSetupInstaller
from .Install.chrome import ChromeInstaller
from .Install.vscode import VSCodeInstaller
from .Install.vscpp import VS_CPP_Installer
from .Install.watttoolkit import SteamPlusPlusInstaller
from .Install.geek import GeekInstaller
from .Install.quark import QuarkProductInstaller
from .Install.huorong import HuorongInstaller

from .core.A import (
    ExcelXlsx,
    WordDocx,
    PPTGenerator,
)

from .core.Z import CompressionHandler
from .core.B import HBytes
from .core.S import (
    pptx,
    word,
    xlsx,
    TRUE,
    FALSE,
)

from .core.XH import Xmlhtml
from .core.DI import DLLImageProcessor
from .core.C import (
    factorial,
    floor,
    combination,
    cos,
    cosh,
    cot,
    cwd,
    home,
    absolute_value,
    tan,
    tanh,
    sin,
    sinh,
    sqrt,
    system,
    ctrlc,
    dependencies,
    ComplexNumber,
)

from .core.SY import *
from .utils import HPopen