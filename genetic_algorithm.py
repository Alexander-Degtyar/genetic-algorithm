import common as task
import numpy as np
from sympy import *
import random
import matplotlib
import matplotlib.pyplot as plt


class Individual:
    CHROMOSOME_LENGTH = 6
    PHENOTYPE_DIFF = 10

    def __init__(self, objective_function, value=None):
        lfrom, lto = task.range_limits()
        if value is None:
            self.value = random.randint(lfrom + self.PHENOTYPE_DIFF,
                                        lto + self.PHENOTYPE_DIFF + 1)
        else:
            self.value = value
        self.objective_function = objective_function

    def __str__(self):
        return "Representation: {val:6b} ({val:2}); Phenotype: {ph:2}; Obj. func. value: {ofv}".format(
            val=self.value,
            ph=self.phenotype,
            ofv=self.objective_function_value
        )

    # def __hash__(self):
    #     return hash(self.phenotype)

    def mutate(self):
        shift = random.randint(0, self.CHROMOSOME_LENGTH)
        self.value ^= 1 << shift

    def cross(self, partner):
        f = self.value ^ 0b111000 + partner.value ^ 0b000111
        s = partner.value ^ 0b111000 + self.value ^ 0b000111

        return Individual(self.objective_function, value=f), \
               Individual(self.objective_function, value=s)

    @property
    def phenotype(self) -> int:
        return self.value - self.PHENOTYPE_DIFF

    @property
    def objective_function_value(self):
        return self.objective_function(self.phenotype)


class Population:
    SIZE = 4
    CROSSES = 2
    MUTATIONS = 1

    def __init__(self, objective_function):
        self.individuals = []
        for i in range(self.SIZE):
            self.individuals.append(Individual(objective_function))

    def __str__(self):
        s = ''
        for i in self.individuals:
            s += str(i) + '\n'
        return s

    def cross(self):
        res = []
        for i in range(self.CROSSES):
            l = random.choice(self.individuals)
            self.individuals.remove(l)
            r = random.choice(self.individuals)
            self.individuals.append(l)

            print("Cross ({:6b}) with ({:6b})".format(l.value, r.value))
            sres = l.cross(r)
            print("Result: ", *sres)
            res.extend(sres)
        return res

    @classmethod
    def mutate(cls, indivs):
        for i in range(cls.MUTATIONS):
            chosen_one = random.choice(indivs)
            chosen_one.mutate()

    def add(self, indivs):
        self.individuals.extend(indivs)

    def reduction(self, increasing: bool):
        # Filter invalid phenotypes
        lfrom, lto = task.range_limits()

        def is_in_limit(indiv):
            return lfrom <= indiv.phenotype <= lto
        removed = [i for i in self.individuals if not is_in_limit(i)]
        for ind in removed:
            print("{:6b} removed due to range limits".format(ind.value))
        with_duplications = [ind for ind in self.individuals if is_in_limit(ind)]

        # Filter duplications
        without_duplications = []
        # phenotypes_without_duplications = (i.phenotype for i in without_duplications)
        for ind in with_duplications:
            duplicate = False
            for j in without_duplications:
                if ind.phenotype == j.phenotype:
                    duplicate = True
            if not duplicate:
                without_duplications.append(ind)

        # Find best
        self.individuals = sorted(without_duplications,
                                  key=lambda i: i.objective_function_value,
                                  reverse=increasing)[:self.SIZE]

    def best(self, increasing: bool):
        return sorted(self.individuals,
                      key=lambda i: i.objective_function_value,
                      reverse=increasing)[0]


v = task.get_variant()
task.VARIANT = v

x = Symbol('x')
y = v.a + v.b * x + v.c * x ** 2 + v.d * x ** 3
print('Целевая функция: f(x) =', y)

# matplotlib.use('TkAgg')  # Uncomment for Windows

p = Population(task.calc_equation)
print("Population at the beginning:\n", p)

best_per_iter = {}

for increasing in (True, False):
    best_per_iter[increasing] = {}
    for i in range(10):
        children = p.cross()
        print("Children before mutation:", *children, sep="\n", end='\n\n')
        p.mutate(children)
        print("Children after mutation:", *children, sep="\n", end='\n\n')
        p.add(children)
        print("Population after children add:\n", p)
        p.reduction(increasing=increasing)
        print("Population after reduction:\n", p)
        best = p.best(increasing=increasing)
        print("Current best in population: [{}]".format(best))
        best_per_iter[increasing][i] = best.objective_function_value


fig, ax = plt.subplots()

ax.plot(np.asarray(list(best_per_iter[True].keys())),
        np.asarray(list(best_per_iter[True].values())),
        label='max')
ax.plot(np.asarray(list(best_per_iter[False].keys())),
        np.asarray(list(best_per_iter[False].values())),
        label='min')

ax.set(xlabel='iteration', ylabel='best f(x)',
       title='Genetic Algorithm')
ax.legend()
ax.grid()

plt.show()
