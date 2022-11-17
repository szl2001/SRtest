from floatconvert.float_converter import FloatConverter
import numpy as np

class FP16Base10Converter(FloatConverter):

    def __init__(self):
        self._tokens = None
 

    def encode(self, val):
        assert val >= -1e10 and val < 1e10
        return f"{val:.6E}"

    def decode(self, lst):
        token = lst[0]
        return float(token)

    def tokens(self):
        if self._tokens is None:
            self._tokens = [
                f"{sign}{mantissa}{exponent}"
                for sign in ["+", "-"]
                for mantissa in ["{:04d}".format(i) for i in range(10000)]
                for exponent in ["E{}".format(i) for i in range(-100, 101)]
            ]
        return self._tokens
