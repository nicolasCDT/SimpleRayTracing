from polynome import *


class M(object):
    """
    Classe mère des DAG
    """
    def __init__(self):
        pass

    def __add__(self, b):
        """
        Définition de l'opérateur +
        """
        return Plus(self, b)

    def __mul__(self, b):
        """
        Définition de l'opérateur *
        """
        return Mult(self, b)

    def __sub__(self, b):
        """
        Définition de l'opérateur -
        """
        return Plus(self, Opp(b))


class Opp(M):
    """
    Modélise l'opposé
    """
    def __init__(self, a):
        super().__init__()  # Initialisation de M
        self.a = a  # Expression

    def eval(self, dico):
        """
        Evaluation
        :param dico: dictionnaire
        :return: Retourne l'opposé de l'évaluation
        """
        return 0. - self.a.eval(dico)

    def evalsymb(self, dico):
        """
        Evaluation des symboles
        :param dico: dictionnaire
        :return: Retourne l'opposé de l'évaluation des symboles
        """
        return Opp(self.a.evalsymb(dico))

    def polent(self):
        """
        Polynome en t
        :return: retourne l'opposé du polynôme
        """
        return polopp(self.a.polent())

    def derivee(self, name):
        """
        Derive le polynome
        :param name: nom de la variable à deriver
        :return: L'opposé de la dérivée en fonction de name
        """
        return Opp(self.a.derivee(name))


class Plus(M):
    """
    Modélise l'addition
    """
    def __init__(self, a, b):
        super().__init__()  # Initialisation de M
        self.a = a  # Nombre a
        self.b = b  # Nombre b

    def eval(self, dico):
        """
        Evaluation de l'addition
        :param dico: Dictionnaire
        :return: Retourne la somme des évaluations
        """
        return self.a.eval(dico) + self.b.eval(dico)

    def evalsymb(self, dico):
        """
        Evaluation des symboles
        :param dico: dictionnaire
        :return: Retourne a somme de des évaluations des symboles
        """
        # return Plus( self.a.evalsymb( dico), self.b.evalsymb( dico))
        return self.a.evalsymb(dico) + self.b.evalsymb(dico)

    def polent(self):
        """
        Somme des polynomes en t
        :return: retourne la somme des polynomes en t
        """
        return polplus(self.a.polent(), self.b.polent())

    def derivee(self, name):
        """
        Dervie le polynome en fonction d'une variable
        :param name: nom de la variable
        :return: Dérivée de l'addition
        """
        # (u+v)' = u'+v'
        return self.a.derivee(name) + self.b.derivee(name)


class Mult(M):
    """
    Modélisation de la multiplication
    """
    def __init__(self, a, b):
        super().__init__()  # Initialisation de M
        self.a = a  # Premier nombre
        self.b = b  # Deuxième nombre

    def eval(self, dico):
        """
        Evaluation
        :param dico: dictionnaire
        :return: retourne la multiplication des évaluations
        """
        return self.a.eval(dico) * self.b.eval(dico)

    def evalsymb(self, dico):
        """
        Evalue le symbole
        :param dico: dictionnaire
        :return: retourne la multiplication des évalutions des symboles
        """
        # return Mult( self.a.evalsymb( dico), self.b.evalsymb( dico))
        return self.a.evalsymb(dico) * self.b.evalsymb(dico)

    def polent(self):
        """
        Polynome en t
        :return: mutliplie les deux polybnomes en t
        """
        return polmult(self.a.polent(), self.b.polent())

    def derivee(self, name):
        """
        Derive le produit
        :param name: Nom de la variable à dériver
        :return: Dérivée du produit
        """
        # (uv)' = u'v + uv'
        return self.a.derivee(name) * self.b + self.a * self.b.derivee(name)


class Nb(M):
    """
    Modélise un nombre
    """
    def __init__(self, n):
        super().__init__()  # Initialisation de M
        self.nb = n  # Nombre

    def eval(self, dico):
        """
        Evaluation du nombre
        :param dico: inutilisé
        :return: retourne le nombre lui-même
        """
        return self.nb

    def evalsymb(self, dico):
        """
        Evalue les symboles
        :param dico: inutilisés
        :return: Retourne l'instance
        """
        return self

    def polent(self):
        """
        Polynome en t
        :return: Retourne le nombre
        """
        return [self.nb]

    def derivee(self, _name):
        """
        Dérive
        :param _name: inutilisé
        :return: Retourne la dérivée d'une constante : 0
        """
        return Nb(0)


class Var(M):
    """
    Modélise une variable dans les expressions
    """
    def __init__(self, nom):
        super().__init__()  # On Initialisation de M
        self.nom = nom  # Nom de la variable

    def eval(self, dico):
        """
        Evaluation du dico
        :param dico: dictionnaire
        :return: évaluation
        """
        if self.nom in dico:  # if dico.has_key( self.nom )
            return dico[self.nom]
        else:
            print('erreur dans Var.eval: indefini :' + self.nom)
            return 1 / 0

    def evalsymb(self, dico):
        """
        Evaluation du symbole
        :param dico: dictionnaire
        :return: évaluation
        """
        if self.nom in dico:  # if dico.has_key( self.nom )
            return dico[self.nom]
        else:
            return self

    def polent(self):
        """
        Polynome en t
        :return: intervalle
        """
        if self.nom == 't':
            return [0, 1]
        else:
            print('erreur dans Var.polent: pas t mais ' + self.nom)

    def derivee(self, name):
        """
        Derive la variable
        :param name: nom de la variable à partir de laquelle on dérive
        :return: Dérivée
        """
        if name == self.nom:
            return Nb(1.)
        else:
            return Nb(0.)
