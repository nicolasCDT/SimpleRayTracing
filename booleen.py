# coding: utf-8
from utils import *


def tof(contact):
    if is_num(contact):
        return contact
    return contact.t


def inter(a, b):
    """
    Intersection entre deux ensembles
    :param a: liste d'intervalles
    :param b: liste d'intervalles
    :return: Intersection de a et b
    """
    if a is None or b is None:
        return None
    ((a1, a2), qa) = (hd(a), tl(a))
    ((b1, b2), qb) = (hd(b), tl(b))
    assert (tof(a1) <= tof(a2))
    assert (tof(b1) <= tof(b2))
    if tof(a1) > tof(b1):
        return inter(b, a)
    if tof(a2) < tof(b1):
        return inter(qa, b)
    if tof(b2) <= tof(a2):
        return cons((b1, b2), inter(a, qb))
    return cons((b1, a2), inter(qa, b))


def reunion(a, b):
    """
    Union entre deux ensembles
    :param a: liste d'intervalles
    :param b: liste d'intervalles
    :return: Union de a et b
    """
    if a is None:
        return b
    if b is None:
        return a
    (ta, qa) = (hd(a), tl(a))
    (tb, qb) = (hd(b), tl(b))
    (a1, a2) = ta
    (b1, b2) = tb
    assert (tof(a1) <= tof(a2))
    assert (tof(b1) <= tof(b2))
    if tof(a1) > tof(b1):
        return reunion(b, a)
    # ta commence avant tb :
    if tof(a2) < tof(b1):
        # ta finit avant que tb, et donc b commence :
        # print( 'a2 < b1 ')
        return cons(ta, reunion(qa, b))
    if tof(b2) <= tof(a2):
        # tb est inclus dans ta :
        # print( 'b2 <= a2')
        return reunion(a, qb)
    # ordre= a1, b1, a2, b2:
    return reunion(cons((a1, b2), qb), qa)



def differ(a, b):
    """
    Différence entre deux ensembles
    :param a: liste d'intervalles
    :param b: liste d'intervalles
    :return: Différence de a et b
    """
    if a is None:
        return None
    if b is None:
        return a
    (ta, qa) = (hd(a), tl(a))
    (tb, qb) = (hd(b), tl(b))
    (a1, a2) = ta
    (b1, b2) = tb
    assert (tof(a1) <= tof(a2))
    assert (tof(b1) <= tof(b2))
    if tof(b2) <= tof(a1):
        # b1 b2 a1 a2
        return differ(a, qb)
    if tof(a2) <= tof(b1):
        # a1 a2 b1 b2
        return cons(ta, differ(qa, b))
    if tof(b1) <= tof(a1):
        if tof(b2) <= tof(a2):
            # b1 a1 b2 a2
            return differ(cons((b2, a2), qa), qb)
        return differ(qa, b)
    if tof(a2) <= tof(b2):
        # a1 b1 a2 b2
        return differ((cons((a1, b1), qa)), b)
    # a1, b1, b2, a2
    return differ(cons((a1, b1), cons((b2, a2), qa)), qb)


# pour fusionner des intervalles contigus :
def simplifie_intervalles(intervalles):
    """
    Simplifie les intervalles contigus
    :param intervalles: liste d'intervalles
    :return: liste simplifiée
    """
    if None == intervalles or None == tl(intervalles):
        return intervalles
    a = (a1, a2) = hd(intervalles)
    (b1, b2) = hd(tl(intervalles))
    if tof(a2) == tof(b1):
        return simplifie_intervalles(cons((a1, b2), tl(tl(intervalles))))
    return cons(a, simplifie_intervalles(tl(intervalles)))


def intersec(vec1, vec2):
    """
    Intersection de deux vecteurs d'intervalles
    :param va: vecteur
    :param vb: vecteur
    :return: Vecteur intersection
    """
    return ltov(inter(vtol(vec1), vtol(vec2)))


def reunir(va, vb):
    """
    Union de deux vecteurs d'intervalles
    :param va: vecteur
    :param vb: vecteur
    :return: Vecteur union
    """
    return ltov(reunion(vtol(va), vtol(vb)))


def ote(va, vb):
    """
    Différence de deux vecteurs d'intervalles
    :param va: vecteur
    :param vb: vecteur
    :return: Vecteur différence
    """
    return ltov(differ(vtol(va), vtol(vb)))
