from floatconvert.float_converter import FloatConverter
from math import frexp, ldexp
import numpy as np

class FP16Converter(FloatConverter):

    def __init__(self):
        self._tokens = None
        self.inf_map = {
            np.nan: "nan",
            np.inf: "inf",
            np.NINF: "-inf"
        }
        self.inv_inf_map = {v: k for k, v in self.inf_map.items()}

    def encode(self, val):
        if val in self.inf_map.keys():
            return (self.inf_map[val])
        sign = "+" if val >= 0 else "-"
        mantissa, exponent = frexp(val)
        assert exponent >= -100 and exponent <= 100
        mantissa = "{:.6f}".format(mantissa)[-6:]
        exponent = "E{}".format(exponent)
        return (f"{sign}{mantissa}{exponent}")

    def decode(self, lst):
        token = lst[0]
        if token in self.inv_inf_map:
            return (self.inv_inf_map[token])
        mantissa_str, exponent_str = token.split("E")
        mantissa = int(mantissa_str) / 1e6
        exponent = int(exponent_str)
        return ldexp(mantissa, exponent)

    def tokens(self):
        if self._tokens is None:
            self._tokens = [
                f"{sign}{mantissa}{exponent}"
                for sign in ["+", "-"]
                for mantissa in ["{:04d}".format(i) for i in range(10000)]
                for exponent in ["E{}".format(i) for i in range(-100, 101)]
            ]
            self._tokens += self.inf_map.values()
        return self._tokens
