"""Constants (like hbar) related to quantum mechanics."""

from __future__ import print_function, division

from sympy.core.numbers import NumberSymbol
from sympy.core.singleton import Singleton
from sympy.printing.pretty.stringpict import prettyForm
import mpmath.libmp as mlib

#-----------------------------------------------------------------------------
# Constants
#-----------------------------------------------------------------------------
class Constants(NumberSymbol, metaclass=Singleton):

    __all__ = [
        'h',
        'PLC',
        'UGC',
        'G',
        'VOL',
        'c',
        'EPS',
        'epsilon0',
        'Ga',
        'g',
        'BOC',
        'k',
        'ELC',
        'qe',
        'EMC',
        'me',
        'alpha',
        'FSC',
        'PIV',
        'mew0',
        'BMC',
        'Bohr',
        'AVC',
        'NA',
        'FAC',
        'F'
    ]
    is_real = True
    is_positive = True
    is_negative = False
    is_irrational = True


class PLC(Constants):
    """Reduced Plank's constant in numerical and symbolic form [1]_.

    Examples
    ========

        >>> from sympy.physics.quantum.constants import hbar
        >>> hbar.evalf()
        1.05457162000000e-34

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Planck_constant
    """

    is_real = True
    is_positive = True
    is_negative = False
    is_irrational = True

    __slots__ = ()

    def _as_mpf_val(self, prec):
        return mlib.from_float(6.62607015e-34, prec)

    def _sympyrepr(self, printer, *args):
        return 'PLC()'

    def _sympystr(self, printer, *args):
        return 'h'

    def _pretty(self, printer, *args):
        if printer._use_unicode:
            return prettyForm('\N{PLANCK CONSTANT OVER TWO PI}')
        return prettyForm('h')

    def _latex(self, printer, *args):
        return r'\h'

# Create an instance for everyone to use.
h = PLC()

class UGC(Constants):
    """
    Universal Gravitational Constant
    """

    is_real = True
    is_positive = True
    is_negative = False
    is_irrational = True

    __slots__ = ()

    def _as_mpf_val(self, prec):
        return mlib.from_float(6.67259e-11, prec)

    def _sympyrepr(self, printer, *args):
        return 'UGC()'

    def _sympystr(self, printer, *args):
        return 'G'

    def _pretty(self, printer, *args):
        if printer._use_unicode:
            return prettyForm('Universal Gravitational Constant')
        return prettyForm('G')

    def _latex(self, printer, *args):
        return r'\G'

# Create an instance for everyone to use.
G = UGC()

class VOL(Constants):
    """
    velocity of light
    """

    is_real = True
    is_positive = True
    is_negative = False
    is_irrational = True

    __slots__ = ()

    def _as_mpf_val(self, prec):
        return mlib.from_float(2.99792458e8, prec)

    def _sympyrepr(self, printer, *args):
        return 'VOL()'

    def _sympystr(self, printer, *args):
        return 'c'

    def _pretty(self, printer, *args):
        if printer._use_unicode:
            return prettyForm('velocity of light')
        return prettyForm('c')

    def _latex(self, printer, *args):
        return r'\c'

# Create an instance for everyone to use.
c = VOL()

class EPS(Constants):
    """
    vacuum dielectric constant
    """

    is_real = True
    is_positive = True
    is_negative = False
    is_irrational = True

    __slots__ = ()

    def _as_mpf_val(self, prec):
        return mlib.from_float(8.85418782e-12, prec)

    def _sympyrepr(self, printer, *args):
        return 'EPS()'

    def _sympystr(self, printer, *args):
        return 'epsilon0'

    def _pretty(self, printer, *args):
        if printer._use_unicode:
            return prettyForm('vacuum dielectric constant')
        return prettyForm('epsilon0')

    def _latex(self, printer, *args):
        return r'\epsilon0'

# Create an instance for everyone to use.
epsilon0 = EPS()

class Ga(Constants):
    """
    Gravitational acceleration
    """

    is_real = True
    is_positive = True
    is_negative = False
    is_irrational = True

    __slots__ = ()

    def _as_mpf_val(self, prec):
        return mlib.from_float(9.80665, prec)

    def _sympyrepr(self, printer, *args):
        return 'Ga()'

    def _sympystr(self, printer, *args):
        return 'g'

    def _pretty(self, printer, *args):
        if printer._use_unicode:
            return prettyForm('Gravitational acceleration')
        return prettyForm('g')

    def _latex(self, printer, *args):
        return r'\g'

# Create an instance for everyone to use.
g = Ga()

class BOC(Constants):
    """
    Boltzmann constant
    """

    is_real = True
    is_positive = True
    is_negative = False
    is_irrational = True

    __slots__ = ()

    def _as_mpf_val(self, prec):
        return mlib.from_float(1.380649e-23, prec)

    def _sympyrepr(self, printer, *args):
        return 'BOC()'

    def _sympystr(self, printer, *args):
        return 'k'

    def _pretty(self, printer, *args):
        if printer._use_unicode:
            return prettyForm('Boltzmann constant')
        return prettyForm('k')

    def _latex(self, printer, *args):
        return r'\k'

# Create an instance for everyone to use.
k = BOC()

class ELC(Constants):
    """
    electron charge
    """

    is_real = True
    is_positive = True
    is_negative = False
    is_irrational = True

    __slots__ = ()

    def _as_mpf_val(self, prec):
        return mlib.from_float(1.60217663e-19, prec)

    def _sympyrepr(self, printer, *args):
        return 'ELC()'

    def _sympystr(self, printer, *args):
        return 'qe'

    def _pretty(self, printer, *args):
        if printer._use_unicode:
            return prettyForm('electron charge')
        return prettyForm('qe')

    def _latex(self, printer, *args):
        return r'\qe'

# Create an instance for everyone to use.
qe = ELC()

class EMC(Constants):
    """
    electron mass
    """

    is_real = True
    is_positive = True
    is_negative = False
    is_irrational = True

    __slots__ = ()

    def _as_mpf_val(self, prec):
        return mlib.from_float(9.10938356e-28, prec)

    def _sympyrepr(self, printer, *args):
        return 'EMC()'

    def _sympystr(self, printer, *args):
        return 'me'

    def _pretty(self, printer, *args):
        if printer._use_unicode:
            return prettyForm('electron mass')
        return prettyForm('me')

    def _latex(self, printer, *args):
        return r'\me'

# Create an instance for everyone to use.
me = EMC()

class FSC(Constants):
    """
    Fine structure constant
    """

    is_real = True
    is_positive = True
    is_negative = False
    is_irrational = True

    __slots__ = ()

    def _as_mpf_val(self, prec):
        return mlib.from_float(7.29927007e-3, prec)

    def _sympyrepr(self, printer, *args):
        return 'FSC()'

    def _sympystr(self, printer, *args):
        return 'alpha'

    def _pretty(self, printer, *args):
        if printer._use_unicode:
            return prettyForm('Fine structure constant')
        return prettyForm('alpha')

    def _latex(self, printer, *args):
        return r'\alpha'

# Create an instance for everyone to use.
alpha = FSC()

class PIV(Constants):
    """
    permeability in vacuum
    """

    is_real = True
    is_positive = True
    is_negative = False
    is_irrational = True

    __slots__ = ()

    def _as_mpf_val(self, prec):
        return mlib.from_float(1.25663706e-6, prec)

    def _sympyrepr(self, printer, *args):
        return 'PIV()'

    def _sympystr(self, printer, *args):
        return 'mew0'

    def _pretty(self, printer, *args):
        if printer._use_unicode:
            return prettyForm('permeability in vacuum')
        return prettyForm('mew0')

    def _latex(self, printer, *args):
        return r'\mew0'

# Create an instance for everyone to use.
mew0 = PIV()

class BMC(Constants):
    """
    Bohr magneton
    """

    is_real = True
    is_positive = True
    is_negative = False
    is_irrational = True

    __slots__ = ()

    def _as_mpf_val(self, prec):
        return mlib.from_float(9.27401007e-24, prec)

    def _sympyrepr(self, printer, *args):
        return 'BMC()'

    def _sympystr(self, printer, *args):
        return 'Bohr'

    def _pretty(self, printer, *args):
        if printer._use_unicode:
            return prettyForm('Bohr magneton')
        return prettyForm('Bohr')

    def _latex(self, printer, *args):
        return r'\Bohr'

# Create an instance for everyone to use.
Bohr = BMC()

class AVC(Constants):
    """
    Avogadro constant
    """

    is_real = True
    is_positive = True
    is_negative = False
    is_irrational = True

    __slots__ = ()

    def _as_mpf_val(self, prec):
        return mlib.from_float(6.02214076e23, prec)

    def _sympyrepr(self, printer, *args):
        return 'AVC()'

    def _sympystr(self, printer, *args):
        return 'NA'

    def _pretty(self, printer, *args):
        if printer._use_unicode:
            return prettyForm('Avogadro constant')
        return prettyForm('NA')

    def _latex(self, printer, *args):
        return r'\NA'

# Create an instance for everyone to use.
NA = AVC()

class FAC(Constants):
    """
    Faraday constant
    """

    is_real = True
    is_positive = True
    is_negative = False
    is_irrational = True

    __slots__ = ()

    def _as_mpf_val(self, prec):
        return mlib.from_float(9.64853329e4, prec)

    def _sympyrepr(self, printer, *args):
        return 'FAC()'

    def _sympystr(self, printer, *args):
        return 'F'

    def _pretty(self, printer, *args):
        if printer._use_unicode:
            return prettyForm('Faraday constant')
        return prettyForm('F')

    def _latex(self, printer, *args):
        return r'\F'

# Create an instance for everyone to use.
F = FAC()
