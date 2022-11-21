from floatconvert.float_converter import FloatConverter


class FP16Base10Converter(FloatConverter):

    def __init__(self):
        self._tokens = None
 
    def encode(self, val):
        assert val >= -1e2 and val <= 1e2
        return f"{val:.2E}"

    def decode(self, lst):
        token = lst[0]
        return float(token)

    def tokens(self):
        if self._tokens is None:
            self._tokens = [
                self.encode(sign * mantissa / 1e3 * pow(10, exponent))
                for sign in [-1, 1]
                for mantissa in range(1000)
                for exponent in range(-2, 3)
            ]
        return self._tokens
