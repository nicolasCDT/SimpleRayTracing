# coding=utf-8
from make_gif import make_gif
from rayon import *
from booleen import *
import math

pi = 4. * math.atan(1.)


def cylindre_Oz(z0, z1, radius, coul):
    assert (z0 <= z1)
    x = Var('x')
    y = Var('y')
    z = Var('z')
    equation = x * x + y * y - Nb(radius * radius)
    return Inter(Prim(equation, coul),
                 Inter(Prim(z - Nb(z1), coul), Prim(Nb(z0) - z, coul)))


def cylindre_Ox(x0, x1, radius, coul):
    assert (x0 <= x1)
    x = Var('x')
    y = Var('y')
    z = Var('z')
    equation = y * y + z * z - Nb(radius * radius)
    return Inter(Prim(equation, coul),
                 Inter(Prim(x - Nb(x1), coul), Prim(Nb(x0) - x, coul)))


def cylindre_Oy(y0, y1, radius, coul):
    assert (y0 <= y1)
    x = Var('x')
    y = Var('y')
    z = Var('z')
    equation = x * x + z * z - Nb(radius * radius)
    return Inter(Prim(equation, coul),
                 Inter(Prim(y - Nb(y1), coul), Prim(Nb(y0) - y, coul)))


def bloc(x1x2, y1y2, z1z2, coul):
    (x1, x2) = x1x2
    (y1, y2) = y1y2
    (z1, z2) = z1z2
    x = Var('x')
    y = Var('y')
    z = Var('z')
    return Inter(Prim(x - Nb(x2), coul),
                 Inter(Prim(y - Nb(y2), coul),
                       Inter(Prim(z - Nb(z2), coul),
                             Inter(Prim(Nb(x1) - x, coul),
                                   Inter(Prim(Nb(y1) - y, coul),
                                         Prim(Nb(z1) - z, coul))))))


def voutes():
    """
    Modélise une architecture
    :return: expression de l'architecture
    """
    maille = 10.
    hsize = 3 * maille / 2.
    radius = maille / 2.
    epais = 0.5
    gradius = radius + epais
    sradius = radius - epais
    coul = (255, 255, 0, 255)
    hauteur = maille * 1.414
    toit = Differ(
        Union(cylindre_Ox(-hsize - epais, hsize + epais, gradius, coul),
              cylindre_Oy(-hsize - epais, hsize + epais, gradius, coul)),
        Union(bloc((-1.2 * hsize, 1.2 * hsize), (-1.2 * hsize, 1.2 * hsize), (-1.2 * hsize, 0), coul),
              Union(cylindre_Ox(-hsize - 1, hsize + 1, sradius, coul),
                    cylindre_Oy(-hsize - 1, hsize + 1, sradius, coul))))
    poteau = cylindre_Oz(-hauteur, 0, epais, coul)
    delta = maille / 2.
    poteau0 = TransfObj(trf_trans(-delta, -delta, 0.), poteau)
    piles = None
    for xx in range(-1, 3):
        for yy in range(-1, 3):
            if (xx - 0.5) * (xx - 0.5) + (yy - 0.5) * (yy - 0.5) < 2.7:
                piles = cons(TransfObj(trf_trans(xx * maille, yy * maille, 0), poteau0), piles)
    les_piliers = foldl((lambda accu, obj: Union(accu, obj)), hd(piles), tl(piles))
    archi = Union(toit, les_piliers)
    archi = Union(archi, bloc((-3. * maille, 3. * maille), (-3. * maille, 3. * maille), (-2 * hauteur, -hauteur),
                              (150, 75, 75, 255)))
    return archi
