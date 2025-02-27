import builtins as __builtin__
from sympy import abc as __vars__
import lbdc
import edprompt
import clro
from subpr.lib import __subpr__
__builtin__.v = __vars__
__builtin__.incognito = lambda x : __subpr__(f'start chrome --incognito {x}')
__all__, __version__ = ['__main__', 'confapp'], '0.0.5'
