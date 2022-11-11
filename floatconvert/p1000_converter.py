from floatconvert.float_converter import FloatConverter
from math import frexp, ldexp


class P1000Converter(FloatConverter):

    def __init__(self):
        self._tokens = None

    def encode(self, val):
        sign = "+" if val >= 0 else "-"
        mantissa, exponent = frexp(val)
        assert exponent >= -100 and exponent <= 100
        mantissa = "{:.4f}".format(mantissa)[-4:]
        exponent = "E{}".format(exponent)
        return (sign, mantissa, exponent)

    def decode(self, lst):
        assert len(lst) == 3
        assert lst[0] in ["+", "-"]
        sign = 1 if lst[0] == "+" else -1
        mantissa = sign * int(lst[1]) / 1e4
        exponent = int(lst[2][1:])
        return ldexp(mantissa, exponent)

    def tokens(self):
        if self._tokens is None:
            self._tokens = [
                "+", "-",
                *["{:04d}".format(i) for i in range(10000)],
                *["E{}".format(i) for i in range(-100, 101)]
            ]
        return self._tokens
