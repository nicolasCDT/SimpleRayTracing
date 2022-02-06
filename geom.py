# coding=utf−8

from utils import *
import math


class Trfo(object):
    """
    Modélise une transformation
    """
    def __init__(self, direct, inverse):
        self.direct = direct
        self.inverse = inverse


def pscal(u, v):
    assert (len(u) == len(v))
    s = 0
    for i in range(0, len(u), 1):
        s += u[i] * v[i]
    return s


def inter_constant(epsilon, polca):
    assert (1 == len(polca))
    if polca[0] <= 0:
        return cons((epsilon, 1.), None)
    else:
        return None


def inter_lineaire(epsilon, polca):
    assert (2 == len(polca))
    a = polca[1]
    b = polca[0]
    if 0. == a:
        return inter_constant(epsilon, [b])
    else:
        y0 = b
        y1 = a + b
        cas = y0 * y1
        if cas > 0:
            if y0 <= 0.:
                return cons((epsilon, 1.), None)
            else:
                return None
        else:
            # il y a une racine:
            rac = (0. - b) / float(a)
            if y1 <= 0.:
                return cons((rac, 1.), None)
            else:
                return cons((epsilon, rac), None)


# produit matrice vecteur, attention: le vecteur [1, 2, 3...] est un vecteur colonne
def mat_vec(m, v):
    nl = len(m)
    nc = len(m[0])
    assert (nc == len(v))
    return vecteur(nl, (lambda li: sigma(0, nc - 1,
                                         (lambda co: m[li][co] * v[co]))))


def mat_mat(a, b):
    la = len(a)
    lb = len(b)
    ca = len(a[0])
    cb = len(b[0])
    assert (ca == lb)
    return matrice(la, cb, (lambda l, c: sigma(0, ca - 1, (lambda k: a[l][k] * b[k][c]))))


# produit vecteur matrice, attention: le vecteur [1, 2, 3...] est un vecteur ligne
def vec_mat(v, a):
    la = len(a)
    ca = len(a[0])
    assert (len(v) == la)
    return vecteur(ca, (lambda c: sigma(0, la - 1, (lambda k: v[k] * a[k][c]))))


# gestion des transformations 3D
def mat_trans(tx, ty, tz):
    return [[1., 0., 0., tx],
            [0., 1., 0., ty],
            [0., 0., 1., tz],
            [0., 0., 0., 1.]]


# scaling, ou affinite
def mat_affinite(sx, sy, sz):
    assert (not (sx * sy * sz == 0))
    return [[sx, 0., 0., 0.],
            [0., sy, 0., 0.],
            [0., 0., sz, 0.],
            [0., 0., 0., 1.]]


def mat_rota_Oz(theta):
    c = math.cos(theta)
    s = math.sin(theta)
    return [[c, -s, 0., 0.],
            [s, c, 0., 0.],
            [0., 0., 1., 0.],
            [0., 0., 0., 1.]]


def mat_rota_Ox(theta):
    c = math.cos(theta)
    s = math.sin(theta)
    return [[1., 0., 0., 0.],
            [0, c, -s, 0.],
            [0, s, c, 0.],
            [0., 0., 0., 1.]]


def mat_rota_Oy(theta):
    c = math.cos(theta)
    s = math.sin(theta)
    return [[c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]]


def trf_trans(tx, ty, tz):
    return Trfo(mat_trans(tx, ty, tz), mat_trans(-tx, -ty, -tz))


def trf_affinite(x, y, z):
    return Trfo(mat_affinite(x, y, z), mat_affinite(1. / x, 1. / y, 1. / z))


def trf_rota_Oz(theta):
    return Trfo(mat_rota_Oz(theta), mat_rota_Oz(-theta))


def trf_rota_Ox(theta):
    return Trfo(mat_rota_Ox(theta), mat_rota_Ox(-theta))


def trf_rota_Oy(theta):
    return Trfo(mat_rota_Oy(theta), mat_rota_Oy(-theta))


def trf_inverse(transformation):
    return Trfo(transformation.inverse, transformation.direct)
