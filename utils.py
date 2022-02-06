# coding: utf-8


def sigma(i1, i2, f):
    """
    Retourne la somme de f(i) pour i allant de i1 à i2
    :param i1: Borne inférieur
    :param i2: Borne supérieur
    :param f: Fonction f
    :return: Somme
    """
    if i1 == i2:
        return f(i1)
    else:
        return f(i1) + sigma(i1 + 1, i2, f)


def vecteur(n, f):
    """
    Créer un vecteur en appliquant la fonction f aux nombres de 0 à n
    :param n: Nombre d'éléments
    :param f: Fonction
    :return: Vecteur
    """
    return [f(i) for i in range(0, n)]


def cons(t, q):
    """
    Créer une paire
    :param t: Element
    :param q: Element
    :return: Paire des deux éléments
    """
    return t, q


def hd(l):
    """
    Retourne la tête d'une liste
    :param l: Liste
    :return: Tête
    """
    assert (l is not None)  # None  != l
    (t, q) = l
    return t


def tl(l):
    """
    Retourne la queue d'une liste
    :param l: Liste
    :return: Queue
    """
    assert (None != l)  # None  != l
    (t, q) = l
    return q


def my_map(f, l):
    """
    Applique la fonction f à chaque élément de la liste l
    :param f: Fonction
    :param l: Liste
    :return: Liste modifiée par f
    """
    if l is None:
        return None
    else:
        return cons(f(hd(l)), my_map(f, tl(l)))


def reverse(l):
    """
    Retourne la liste l à l'envers
    :param l: Liste
    :return: liste retournée
    """
    pile = None
    while neq(None, l):
        pile = cons(hd(l), pile)
        l = tl(l)
    return pile


def eteter(predicat_keep, l):
    """
    Trouve le premier element d'une liste validant la condition predicat_keep
    :param predicat_keep: Condition
    :param l: liste
    :return: élement vérifiant la condition
    """
    if l is None or predicat_keep(hd(l)):
        return l
    else:
        return eteter(predicat_keep, tl(l))


def filtrer(pred, l):
    """
    Applique un filtre à une liste
    :param pred: Filtre
    :param l: Liste
    :return: liste filtrée
    """
    if l is None:
        return None
    elif pred(hd(l)):
        return cons(hd(l), filtrer(pred, tl(l)))
    else:
        return filtrer(pred, tl(l))


def milieu(a, b):
    """
    Retourne le milieu de a et b
    :param a: Nombre
    :param b: Nombre
    :return: Milieu
    """
    return (a + b) / 2.


def milieux(v):
    """
    Retourne le nombre du milieu d'un vecteur
    :param v: vecteur
    :return: Milieu
    """
    return vecteur(len(v) - 1, (lambda i: milieu(v[i], v[i + 1])))


def mintab(tab):
    """
    Retourne le minimum d'un tableau
    :param tab: Tableau
    :return: Minimum
    """
    mi = tab[0]
    for i in range(1, len(tab)):
        mi = min(mi, tab[i])
    return mi


def maxtab(tab):
    """
    Retourne le maximum d'un tableu
    :param tab: Tableau
    :return: Maximum
    """
    ma = tab[0]
    for i in range(1, len(tab)):
        ma = max(ma, tab[i])
    return ma


def kons(t1t2, liste):
    (t1, t2) = t1t2
    if liste is None:
        return cons((t1, t2), liste)
    else:
        ((t3, t4), q) = (hd(liste), tl(liste))
        if t2 == t3:
            return cons((t1, t4), q)
        else:
            return cons((t1, t2), liste)


def neq(a, b):
    """
    Inégalité
    :param a: Element
    :param b: Element
    :return: a différent de b
    """
    return not (a == b)


# convertir vecteur v en liste:
def vtol(v):
    """
    Convertit un vecteur en liste
    :param v: Vecteur
    :return: Liste
    """
    l = None
    for i in range(len(v) - 1, -1, -1):
        l = cons(v[i], l)
    return l


# convertir liste en vecteur:
def lgrliste(l):
    """
    Convertir une liste en vecteur
    :param l: Liste
    :return: Vecteur/Tableau
    """
    n = 0
    while not (l is None):
        n += 1
        l = tl(l)
    return n


def ltov(l):
    n = lgrliste(l)
    v = [None] * n
    for i in range(0, n, 1):
        v[i] = hd(l)
        l = tl(l)
    return v


def is_num(v):
    """
    Si le nombre v est un float ou un int
    :param v: Nombre
    :return: Booléen
    """
    return (type(v) is float) or (type(v) is int)


def matrice(nl, nc, f):
    return vecteur(nl, (lambda l: vecteur(nc, (lambda c: f(l, c)))))


def plus_vect(u, v):
    """
    Additionne deux vecteurs de même taille
    :param u: vecteur
    :param v: vecteur
    :return: somme des vecteurs
    """
    assert (len(u) == len(v))
    return [u[i] + v[i] for i in range(0, len(u), 1)]


def moins_vect(u, v):
    """
    Soustrait deux vccteurs de même taille
    :param u: Vecteur
    :param v: Vecteur
    :return: Différence des deux vecteurs
    """
    assert (len(u) == len(v))
    return [u[i] - v[i] for i in range(0, len(u), 1)]


def vec2xyz(v):
    """
    Depack un vecteur de 3 valeurs
    :param v: Vecteur
    :return: triplet
    """
    assert (len(v) == 4 and v[3] == 1)
    return v[0], v[1], v[2]


def vec2abc(v):
    """
    Depack un vecteur de 3 valeurs
    :param v: Vecteur
    :return: triplet
    """
    assert (len(v) == 4 and v[3] == 0)
    return v[0], v[1], v[2]


def vec2abcd(v):
    """
    Depack un vecteur de 4 valeurs
    :param v: Vecteur
    :return: quadruplet
    """
    assert (len(v) == 4)
    return v[0], v[1], v[2], v[3]


def xyz2vec(pt):
    """
    Renvoie un vecteur de 4 éléments à partir d'un triplet
    :param pt: Triplet
    :return: Vecteur
    """
    (x, y, z) = pt
    return [x, y, z, 1]


def abc2vec(abc):
    """
    Renvoie à vecteur à partir d'un triplet
    :param abc: Triplet
    :return: Vecteur
    """
    (a, b, c) = abc
    return [a, b, c, 0]


def abcd2vec(abcd):
    """
    Renvoie un vecteur à partir d'un quadruplet
    :param abcd: quadruplet
    :return: Vecteur
    """
    (a, b, c, d) = abcd
    return [a, b, c, d]


def foldl(operation, si_liste_vide, liste):
    """
    Applique une opération sur une liste
    :param operation: Opération
    :param si_liste_vide: Variable interne
    :param liste: Liste
    :return: Nouvelle liste
    """
    if liste is None:
        return si_liste_vide
    else:
        return foldl(operation, operation(si_liste_vide, hd(liste)), tl(liste))


def lgr(liste):
    """
    Retourne la longueur d'une liste
    :param liste: Liste
    :return: Longueur de la liste
    """
    return foldl((lambda n, li: n + 1), 0, liste)
