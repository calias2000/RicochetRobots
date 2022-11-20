# -*- coding: utf-8 -*-
"""
Grupo tg04
Bernardo Quinteiro 93692
Diogo Lopes 93700
"""

import numpy as np
from math import log

def I(p, n):

    pp = p / (p + n)
    pn = n / (n + p)
    try:
        return - pp * log(pp, 2) - pn * log(pn, 2)
    except:
        return 0

def rest(t, f, ttl):
    sum_t = sum(t) * 1.0
    sum_f = sum(f) * 1.0
    return sum_t / ttl * I(t[0] / sum_t, t[1] / sum_t) + sum_f / ttl * I(f[0] / sum_f, f[1] / sum_f)


def information_gain(examples, attr, Y):
    t = [0, 0]
    f = [0, 0]
    ex = [x[attr] for x in examples]
    ttl = len(ex)

    for i in range(ttl):
        if ex[i] == 0:
            t[Y[i]] += 1
        else:
            f[Y[i]] += 1

    if t[0] + t[1] == 0:
        return 0
    if f[0] + f[1] == 0:
        return 0

    p = t[0] + f[0]
    n = t[1] + f[1]

    return I(p / (p + n), n / (p + n)) - rest(t, f, ttl)


def dtl(D, attributes, Y, exp_pais, noise):
    if D == []:
        maxi = -1
        soma = -1
        for x in exp_pais:
            current = 0
            for y in exp_pais:
                if int(y) == int(x):
                    current += 1
            if current > soma:
                maxi = int(x)
            soma = current
        return maxi
    else:
        dif = False
        for x in range(len(Y)):
            if int(Y[x]) != int(Y[0]):
                dif = True
        if not dif:
            return int(Y[0])
        elif attributes == [] and noise:
            maxi = -1
            soma = -1
            for x in Y:
                current = 0
                for y in Y:
                    if int(y) == int(x):
                        current += 1
                if current > soma:
                    maxi = int(x)
                soma = current
            return maxi
        else:
            best = 0
            score = -100
            for x in attributes:
                z = information_gain(D, x, Y)
                if z > score:
                    score = z
                    best = x
            tree = [best]
            for x in (0, 1):
                aux_list = []
                new_y = []
                for z in range(len(D)):
                    if D[z][best] == x:
                        aux_list.append(D[z])
                        new_y.append(int(Y[z]))
                att_backup = attributes.copy()
                att_backup.remove(best)
                sub_tree = dtl(aux_list, att_backup, new_y, Y, noise)
                tree.append(sub_tree)
            return tree


def check_equal(Y):
    for x in Y:
        if int(Y[0]) != int(x):
            return False
    return True


def createdecisiontree(D, Y, noise=False):
    if(check_equal(Y)):
        return [0, int(Y[0]), int(Y[0])]

    attributes = []

    for x in range(len(D[0])):
        attributes.append(x)

    y_array = list(Y)
    d_array = list(D)

    return dtl(d_array, attributes, y_array, [], noise)
