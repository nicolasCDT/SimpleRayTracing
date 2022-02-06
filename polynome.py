from utils import *
from geom import *


# 1 + 2*t + 3*t^2 ==> [1, 2, 3]
def get_coef(a, i):
    """
    Retourne le coef i d'un polynome a
    :param a: polynome
    :param i: coef
    :return: coefficient
    """
    if 0 <= i < len(a):
        return a[i]
    else:
        return 0


def polplus(a, b):
    """
    Ajoute les deux polynomes a et b
    :param a: polynome
    :param b: polynome
    :return: somme des polynomes
    """
    return vecteur(max(len(a), len(b)), (lambda i: get_coef(a, i) + get_coef(b, i)))


def polopp(a):
    """
    Opposé du polynôme a
    :param a: polynôme
    :return: Opposé de a
    """
    return vecteur(len(a), (lambda i: 0 - a[i]))


def polmult(a, b):
    """
    Multiplie deux polynômes a et b
    :param a: polynôme
    :param b: polynôme
    :return: Produit de a et b
    """
    la = len(a)
    lb = len(b)
    da = la - 1
    db = lb - 1
    return vecteur(da + db + 1, (lambda d: sigma(0, da, (lambda i: a[i] * get_coef(b, d - i)))))


def casteljau(polbe):
    """
    Algorithme de casteljau
    :param polbe: polynome dans la base de Bernstein
    :return: Approximation du polynomes
    """
    n = len(polbe)
    d = n - 1
    couches = [None] * n
    couches[0] = polbe
    for c in range(1, n):
        couches[c] = milieux(couches[c - 1])
    return (vecteur(n, (lambda i: couches[i][0])),
            vecteur(n, (lambda i: couches[n - i - 1][i])))


'''
si polynome p est dans la base de bernstein, alors p( [0, 1]) est dans [mintab( p_i), maxtab( p_i)] , les p_i etant les
coefs de p dans la base de bernstein
casterljau( p dans la base de bernstein) rend p1(X: 0..0.5) les coefs de p( 2x) 
et de p2(X:0.5, 1) les coefs de p( 2x-1)
'''


def solve(epsilon, polbe, t1, t2, racines):
    """
    Cherche les racines d'un polynome dans la base de Bernstein
    :param epsilon: Précision
    :param polbe: Polynome
    :param t1: borne
    :param t2: borne
    :param racines: racines trouvées
    :return: Liste des racines
    """
    (mi, ma) = (mintab(polbe), maxtab(polbe))
    if ma < 0 or 0 < mi:
        return racines
    else:
        tm = milieu(t1, t2)
        dt = t2 - t1
        if dt < epsilon:
            return cons(tm, racines)
        else:
            (p1, p2) = casteljau(polbe)
            return solve(epsilon, p1, t1, tm, solve(epsilon, p2, tm, t2, racines))


def binom(k, n):
    """
    Retourne k parmi n : binomial
    :param k: Nombre
    :param n: nombre
    :return: k parmi n
    """
    if k < 0 or n < 0 or k > n:
        return 0
    elif 0 == k:
        return 1
    elif n - k < k:
        return binom(n - k, n)
    else:
        return binom(k - 1, n) * (n - k + 1) / k


def tobernstein(polca):
    """
    Convertie un polynôme dans la base canonique à la base de Bernstein
    :param polca: Polynôme dans la base canonique
    :return: Polynôme dans la base de Bernstein
    """
    n = len(polca)
    d = n - 1
    return vecteur(n, (lambda i: sigma(0, d, (lambda k: polca[k] * binom(k, i) / float(binom(k, d))))))


def solvegt1(epsilon, polca):
    """
    Trouve les racines supérieures à 1 de polca
    :param epsilon: précision
    :param polca: Polynôme en base canonique
    :return: Liste de racines
    """
    n = len(polca)
    d = n - 1
    aux = vecteur(n, (lambda i: polca[d - i]))
    polbe = tobernstein(aux)
    zeros = solve(epsilon, polbe, 0., 1., None)
    zeros = filtrer((lambda x: x > 0.0001), zeros)
    return reverse(my_map((lambda x: 1. / x), zeros))


def racines(eps, polca):
    """
    Cherche les racines d'un polynôme de base canonique
    :param eps: Precision
    :param polca: Polynôme en base canonique
    :return: Racine supérieur à 1
    """
    return solvegt1(eps, polca)


def study_interval(epsilon, polbe, t1, t2, liste_a_droite):
    (mi, ma) = (mintab(polbe), maxtab(polbe))
    if 0. < mi:  # polynome > 0. donc vide
        return liste_a_droite
    elif ma <= 0.:
        return kons((t1, t2), liste_a_droite)
    else:
        dt = t2 - t1
        tm = (t1 + t2) / 2.
        if dt < epsilon:
            return kons((t1, t2), liste_a_droite)
        (pol1, pol2) = casteljau(polbe)
        return study_interval(epsilon, pol1, t1, tm, study_interval(epsilon, pol2, tm, t2, liste_a_droite))


# intervalle (t1, t2) dans [0, 1] --> (1/t2, 1/t1)
def inverse_interval(t1t2):
    (t1, t2) = t1t2
    if 0. == t1:
        return 1. / t2, 1e20
    return 1. / t2, 1. / t1


# inter_polca_01 rend une liste d'intervalle dans [0, 1] où polca est négatif :
def inter_polca_01(epsilon, polca):
    # on elimine les coefficients nuls de bas degre
    polca = ltov(eteter((lambda coeff: abs(coeff) >= 1e-6), vtol(polca)))
    n = len(polca)
    if 0 == n:  # polynome identiquement nul
        return cons((epsilon, 1.), None)
    elif 1 == n:  # cas polynome constant
        return inter_constant(epsilon, polca)
    elif 2 == n:  # cas polynome degre 1: a*t+b
        return inter_lineaire(epsilon, polca)
    else:
        polbe = tobernstein(polca)
        ivals = study_interval(epsilon, polbe, 0., 1., None)
        return ivals


def inter_polca(epsilon, polca):
    n = len(polca)
    polinv = [polca[n - i - 1] for i in range(0, n)]
    ivals = inter_polca_01(epsilon, polinv)
    # les racines sont dans (0, 1), on les inverse :
    ivals = reverse(ivals)  # car 1/x est decroissant
    return my_map(inverse_interval, ivals)
