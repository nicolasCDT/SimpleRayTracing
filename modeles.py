# coding: utf-8
from expr import *
import math

#############################################################
#
# List des objets pouvant être modélisés
#


def boule(centre, r):
    """
    Expression d'une sphère
    :param centre: Point centre
    :param r: rayon
    :return: Expression
    """
    (cx, cy, cz) = centre
    x = Var("x")
    y = Var("y")
    z = Var("z")
    return (x - Nb(cx)) * (x - Nb(cx)) + (y - Nb(cy)) * (y - Nb(cy)) + (z - Nb(cz)) * (z - Nb(cz)) - Nb(r * r)


def tore(r1, r2):
    """
    Expression d'un tore
    :param r1: int
    :param r2: int
    :return: Expression
    """
    x = Var("x")
    y = Var("y")
    z = Var("z")
    tmp = x * x + y * y + z * z + Nb(r2 * r2 - r1 * r1)
    return tmp * tmp - Nb(4. * r2 * r2) * (x * x + z * z)


def steiner2():
    """
    Expression d'une surface de steiner
    :return: Expression
    """
    x = Var("x")
    y = Var("y")
    z = Var("z")
    return x * x * y * y - x * x * z * z + y * y * z * z - x * y * z


def steiner4():
    """
    Expression d'une surface de steiner
    :return: Expression
    """
    x = Var("x")
    y = Var("y")
    z = Var("z")
    return y * y - Nb(2.) * x * y * y - x * z * z + x * x * y * y + x * x * z * z - z * z * z * z


def roman():
    """
    Expression d'une surface de roman
    :return: Expression
    """
    x = Var("x")
    y = Var("y")
    z = Var("z")
    return x * x * y * y + x * x * z * z + y * y * z * z - Nb(2.) * x * y * z


def cone(alpha):
    """
    Expression d'un cône
    :param alpha: angle
    :return: Expression
    """
    x = Var("x")
    y = Var("y")
    z = Var("z")
    return x * x + y * y - (z * z * Nb((math.tan(alpha))))


def hyperboloide_2nappes():
    """
    Expression d'une hyperboloide à 2 nappes
    :return: Expression
    """
    x = Var("x")
    y = Var("y")
    z = Var("z")
    return Nb(0.) - (z * z - (x * x + y * y + Nb(0.1)))


def hyperboloide_1nappe():
    """
    Expression d'une hyperboloide à 1 nappes
    :return: Expression
    """
    x = Var("x")
    y = Var("y")
    z = Var("z")
    return Nb(0.) - (z * z - (x * x + y * y - Nb(0.1)))

