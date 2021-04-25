import numpy as np
from sympy import *
import matplotlib
import matplotlib.pyplot as plt
from common import *


v = get_variant()
VARIANT = v

x = Symbol('x')
y = v.a + v.b * x + v.c * x ** 2 + v.d * x ** 3

print('Целевая функция: f(x) =', y)

yprime = y.diff(x)
print('Первая производная: f\'(x) =', yprime)

coefs = [float(yprime.args[2].args[0]), float(yprime.args[1].args[0]), float(yprime.args[0])]
sq_roots = np.roots(coefs)
print("Корни квадратного уравнения. x1 = {:.3f}, x2 = {:.3f}".format(sq_roots[0],sq_roots[1]))

ysec = yprime.diff(x)
print('Вторая производная: f\'\'(x) =', ysec)

ysec_x = [ysec.args[1].args[0]*root + ysec.args[0] for root in sq_roots]
print('Определение типов экстремумов:',
      "f\'\'({:.3f}) = {:.3f} --> {}, ".format(sq_roots[0], ysec_x[0], extremum_type_name(ysec_x[0])),
      "f\'\'({:.3f}) = {:.3f} --> {}".format(sq_roots[1], ysec_x[1], extremum_type_name(ysec_x[1])))

extremums = [calc_equation(x) for x in sq_roots]
print('Значения функции в точках экстремумов: ',
      "f({:.3f}) = {:.3f}, ".format(sq_roots[0], extremums[0]),
      "f({:.3f}) = {:.3f}".format(sq_roots[1], extremums[1]))

limits_points = [calc_equation(x) for x in range_limits()]
print('Значения функции на границах интервала:',
      "f({:.3f}) = {:.3f}, ".format(range_limits()[0], limits_points[0]),
      "f({:.3f}) = {:.3f}".format(range_limits()[1], limits_points[1]))

y_max = max(extremums+limits_points)
y_min = min(extremums+limits_points)
print("y(max) = {:.3f}, y(min) = {:.3f}".format(y_max, y_min))

# matplotlib.use('TkAgg')  # Uncomment for Windows
xs = range(*range_limits())
ys = [calc_equation(x) for x in xs]
t = np.asarray(xs)
s = np.asarray(ys)

fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='x', ylabel='y',
       title='Classical Optimization Theory')
ax.grid()

plt.show()
