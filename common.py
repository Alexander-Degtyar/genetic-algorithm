class Variant:
    def __init__(self):
        self.a = None
        self.b = None
        self.c = None
        self.d = None

VARIANT = None

def get_variant():
    def ask_variant():
        v = Variant()
        v.a = int(input('a='))
        v.b = int(input('b='))
        v.c = int(input('c='))
        v.d = int(input('d='))

        return v

    def hardcoded_variant():
        v = Variant()
        v.a = 25
        v.b = 10
        v.c = -46
        v.d = 1
        return v

    return ask_variant()
    # return hardcoded_variant()


def range_limits():
    def hardcoded_limits():
        return -10, 53
    return hardcoded_limits()


def extremum_type_name(y: float):
    if y > 0:
        return 'минимум'
    else:
        return 'максимум'


def calc_equation(x: float) -> float:
    v = VARIANT
    return v.a + v.b * x + v.c * x ** 2 + v.d * x ** 3
