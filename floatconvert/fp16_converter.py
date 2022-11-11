from floatconvert.float_converter import FloatConverter
from math import frexp, ldexp
import numpy as np

class FP16Converter(FloatConverter):

    def __init__(self):
        self._tokens = None

    def encode(self, val):
        if np.isnan(val):
            return ("nan")
        sign = "+" if val >= 0 else "-"
        if np.isinf(val):
            return (f"{sign}inf")
        mantissa, exponent = frexp(val)
        if exponent < -25:
            return ("-inf")
        elif exponent > 24:
            return ("+inf")
        else:
            mantissa = "{:.2f}".format(mantissa)[-2:]
            exponent = "E{}".format(exponent)
            return (f"{sign}{mantissa}{exponent}")

    def decode(self, lst):
        token = lst[0]
        if token == "nan":
            return np.nan
        elif token == "+inf":
            return np.inf
        elif token == "-inf":
            return np.NINF
        else:
            mantissa_str, exponent_str = token.split("E")
            mantissa = int(mantissa_str) / 100
            exponent = int(exponent_str)
            return ldexp(mantissa, exponent)

    def tokens(self):
        if self._tokens is None:
            self._tokens = [
                f"{sign}{mantissa}{exponent}"
                for sign in ["+", "-"]
                for mantissa in ["{:02d}".format(i) for i in range(100)]
                for exponent in ["E{}".format(i) for i in range(-25, 25)]
            ]
            self._tokens += ["nan", "+inf", "-inf"]
        return self._tokens
