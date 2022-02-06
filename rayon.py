# coding=utf−8

from PIL import Image
from expr import *
from booleen import *

last_percent = 0  # Nécessaire pour l'affichage des barres d'avancement


class Obj(object):
    """
    Classe mère des modèles
    """

    def __init__(self):
        pass


class Rayon(object):
    """
    Modélise un rayon par sa source et sa direction
    """

    def __init__(self, source, dir):
        self.source = source
        self.dir = dir


class Contact(object):
    """
    Point de contact entre le rayon et la primitive
    """

    def __init__(self, t, pt, plan, color):
        self.t = t
        self.pt = pt
        self.plan = plan
        self.color = color


class Camera(object):
    """
    Caméra visualisant la scence
    """

    def __init__(self, o, ox, oy, oz, h_size_world, h_size_win, sun, **kwargs):
        self.o = o
        self.ox = ox  # vers la droite du spectateur
        self.oy = oy  # regard du spectateur
        self.oz = oz  # vertical du spectateur
        self.h_size_world = h_size_world
        self.h_size_win = h_size_win
        self.sun = normalize3(sun)
        self.background = None
        self.background_link = None
        if "background" in kwargs:
            self.background = kwargs["background"]
            self.background_link = kwargs["background"]
            if not isinstance(kwargs["background"], tuple):
                self.load_background_image()
        else:
            self.background = (100, 100, 255, 255)
            self.background_link = (100, 100, 255, 255)
        self.nom = "img.png"

    def generate_ray(self, x, z):
        """
        Génération du rayon
        :param x: pixel x
        :param z: pixel z
        :return: Rayon
        """
        (x0, y0, z0) = self.o
        kx = interpole(0., 0., self.h_size_win, self.h_size_world, float(x))
        kz = interpole(0., 0., self.h_size_win, self.h_size_world, float(z))
        return Rayon((x0 + kx * self.ox[0] + kz * self.oz[0],
                      y0 + kx * self.ox[1] + kz * self.oz[1],
                      z0 + kx * self.ox[2] + kz * self.oz[2]),
                     self.oy)

    def load_background_image(self):
        """
        Retourne le fond d'écran : une image, ou un tuple si on ne peut pas charger le fond d'écran
        :rtype: tuple|Image
        """
        try:
            self.background = Image.open(self.background_link)
        except Exception as e:
            print(f"Cannot load the background. Setting default color: {e}")
            self.background = (100, 100, 255, 255)

    def has_background(self):
        """
        Renvoie True ou false selon s'il y a un fond d'écran
        :rtype: bool
        """
        return not isinstance(self.background, tuple)


class Prim(Obj):
    """
    Modélise une primitive
    """

    def __init__(self, fonc_xyz, color):
        super().__init__()
        self.fonc = fonc_xyz
        self.color = color

    def normale(self, xyz):
        (x, y, z) = xyz
        fx = self.fonc.derivee("x")
        fy = self.fonc.derivee("y")
        fz = self.fonc.derivee("z")
        dico = {"x": x, "y": y, "z": z}
        (a, b, c) = (fx.eval(dico), fy.eval(dico), fz.eval(dico))
        return normalize3((a, b, c))

    def creer_contact(self, rayon, t):
        """
        Créer un point de contact
        :param rayon: Rayon
        :param t: t
        :return: Contact
        """
        pt = pt_sur_rayon(rayon, t)
        abc = (a, b, c) = self.normale(pt)
        d = 0 - pscal3(pt, abc)
        plan = (a, b, c, d)
        return Contact(t, pt, plan, self.color)

    def two_contacts(self, rayon, t1t2):
        """
        Créer deux points de contacts
        :param rayon: Rayon
        :param t1t2: tuple de t1, t2
        :return: Paire de contacts
        """
        (t1, t2) = t1t2
        return (self.creer_contact(rayon, t1),
                self.creer_contact(rayon, t2))

    def intersection(self, rayon):
        """
        Calcule les intersections entre l'objet et le rayon
        :param rayon: Rayon
        :return: liste de contacts
        """
        dic = build_dic(rayon)
        expression_en_t = self.fonc.evalsymb(dic)
        pol_t = to_pol_en_t(expression_en_t)
        intervalles = inter_polca(1e-4, pol_t)
        # intervalles= ... remplace: roots = racines( pol_t)
        intervals_contacts = my_map((lambda t1t2: self.two_contacts(rayon, t1t2)), intervalles)
        return intervals_contacts


class TransfObj(Obj):
    """
    Transformation d'objet
    """
    def __init__(self, transformation, obj):
        super().__init__()
        self.transfo = transformation
        self.obj = obj

    def intersection(self, rayon):
        """
        Récupère les points de contacts entre l'objet et le rayon
        :param rayon: Rayon
        :return: Liste des points de contacts
        """
        rayon_aux = transform_ray(trf_inverse(self.transfo), rayon)
        # contacts_aux est une liste de paire de contacts:
        contacts_aux = self.obj.intersection(rayon_aux)
        contacts = my_map((lambda ival:
                           transform_interval(self.transfo, ival)), contacts_aux)
        return contacts


class Union(Obj):
    """
    Union d'objet
    """
    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b

    def intersection(self, rayon):
        """
        Renvoie l'intersection entre un rayon et l'union de a et b
        :param rayon: Rayon
        :return: Intersection d'union
        """
        ia = self.a.intersection(rayon)
        ib = self.b.intersection(rayon)
        return reunion(ia, ib)


class Inter(Obj):
    """
    Intersection de deux objets
    """
    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b

    def intersection(self, rayon):
        """
        Intersection entre un rayon et l'intersection de deux objets
        :param rayon: Rayon
        :return: Points de contacts entre l'intersection de deux objets
        """
        ia = self.a.intersection(rayon)
        if ia is None:
            return None
        else:
            ib = self.b.intersection(rayon)
            return inter(ia, ib)


class Differ(Obj):
    """
    Différence entre deux objets
    """
    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b

    def intersection(self, rayon):
        """
        Intersection entre la différences des objets et le rayon
        :param rayon: Rayon
        :return: Points de contacts entre le rayon et la différence des deux objets
        """
        ia = self.a.intersection(rayon)
        if ia is None:
            return None
        else:
            ib = self.b.intersection(rayon)
            return differ(ia, ib)


def get_color(pt_contact, i):
    """
    Retourne la couleur du pixel en fonction du point de contact
    :param pt_contact: Point de contacte
    :param i: Numéro de l'image pour créer une animation
    :return:
    """
    if len(pt_contact) != 3:
        return 255, 255, 255, 255

    x, y, z = pt_contact
    x = int(x * 10)
    y = int(y * 10)
    if x % 2 == y % 2:
        return 255, 255, 255, 255
    return 20, 20, 20, 255


def transform_interval(transfo, intervalle_contacts):
    (contact1, contact2) = intervalle_contacts
    return transform_contact(transfo, contact1), transform_contact(transfo, contact2)


def to_pol_en_t(e):
    """
    Convertie e en polynome en t
    :param e: expression en t
    :return: list
    """
    return e.polent()


def interpole(x1, y1, x2, y2, x):
    """
    Interpolation linéaire
    :return: int
    """
    x1, y1, x2, y2, x = float(x1), float(y1), float(x2), float(y2), float(x)
    return (x - x2) / (x1 - x2) * y1 + (x - x1) / (x2 - x1) * y2


def milieu(t1, t2):
    """
    Retourne le milieu entre deux points
    :return: (float, float) : Point
    """
    x1, y1 = t1
    x2, y2 = t2
    return float((x1 + x2)) / 2., float((y1 + y2)) / 2.


def normalize3(abc):
    (a, b, c) = abc
    (a, b, c) = (float(a), float(b), float(c))
    n = math.sqrt(a * a + b * b + c * c)
    if n == 0:
        return 0., 0., 0.
    else:
        return a / n, b / n, c / n


def build_dic(rayon):
    """
    Créer le dictionnaire qui contient les équations du rayon
    :param rayon: Rayon
    :return: dict
    """
    return {"x": Nb(rayon.source[0]) + Nb(rayon.dir[0]) * Var("t"),
            "y": Nb(rayon.source[1]) + Nb(rayon.dir[1]) * Var("t"),
            "z": Nb(rayon.source[2]) + Nb(rayon.dir[2]) * Var("t")}


def transform_contact(trf, contact):
    """
    Transforme un contact
    :param trf: Transformation
    :param contact: Contact
    :return: Contact
    """
    if is_num(contact):
        return 1 / 0
    t_pt = vec2xyz(mat_vec(trf.direct, xyz2vec(contact.pt)))
    t_plan = vec2abcd(vec_mat(contact.plan, trf.inverse))
    return Contact(contact.t, t_pt, t_plan, contact.color)


def pscal3(xyz1, xyz2):
    (x1, y1, z1) = xyz1
    (x2, y2, z2) = xyz2
    return x1 * x2 + y1 * y2 + z1 * z2


def clamp(mi, ma, v):
    return min(ma, max(mi, v))


def transform_ray(trf, rayon):
    """
    Applique une transformation à un rayon
    :param trf: Transformation
    :param rayon: Rayon
    :return: Rayon
    """
    t_src = vec2xyz(mat_vec(trf.direct, xyz2vec(rayon.source)))
    t_dir = vec2abc(mat_vec(trf.direct, abc2vec(rayon.dir)))
    return Rayon(t_src, t_dir)


def transform_cam(trf, cam):
    """
    Applique une transformation à une caméra
    :param trf: Transformation
    :param cam: Caméra
    :return: Caméra
    """
    o2 = vec2xyz(mat_vec(trf.direct, xyz2vec(cam.o)))
    ox2 = vec2abc(mat_vec(trf.direct, abc2vec(cam.ox)))
    oy2 = vec2abc(mat_vec(trf.direct, abc2vec(cam.oy)))
    oz2 = vec2abc(mat_vec(trf.direct, abc2vec(cam.oz)))
    return Camera(o2, ox2, oy2, oz2, cam.h_size_world, cam.h_size_win, cam.sun)


def pt_sur_rayon(rayon, t):
    """
    Point sur le rayon à t
    :param rayon: Rayon
    :param t: t
    :return: Point
    """
    (x, y, z) = rayon.source
    (a, b, c) = rayon.dir
    return x + t * a, y + t * b, z + t * c


def progress_bar(i):  # Uniquement en monothread
    """Affiche la barre de progression pour savoir où on en est"""
    global last_percent
    if int(i / 5) != last_percent:
        print(f"\r Progress: [{'#' * int(i / 5)}{' ' * int(20 - (i / 5))}] ", end="")
        last_percent = int(i / 5)


def rendering(cam, contact, i):
    """
    Fait le rendu d'un pixel
    :param cam: Caméra
    :param contact: Point de contact entre le rayon et le modèle
    :param i: Numéro de l'image
    :return: tuple de couleur : (rouge, bleu, vert, brillance)
    """
    if 1.0 == contact.t:
        # l'oeil est "dans la matiere", à l'intérieur d'une primitive
        if contact.color:  # Si l'objet à une couleur
            (r, v, b, ll) = contact.color  # on attribue la bonne couleur
        else:  # Sinon
            (r, v, b, ll) = get_color(contact.pt, i)  # on récupére la couleur génrée (damier)
        return r // 2, v // 2, b // 2, ll

    if contact.color:  # Si l'objet à une couleur
        (rr, vv, bb, ll) = contact.color  # on attribue la bonne couleur
    else:  # Sinon
        (rr, vv, bb, ll) = get_color(contact.pt, i)  # on récupére la couleur génrée (damier)
    (rr, vv, bb, ll) = (float(rr), float(vv), float(bb), float(ll))  # On convertit tout en float
    (a, b, c, d) = contact.plan

    # avec les soustractions, il peut arriver que le plan soit mal orienté, ie la normale ne pointe pas vers
    # l'extérieur de l'objet si le point du contact est vu, alors pscal3( sa normale, cam.oy)<= 0
    if pscal3(cam.oy, (a, b, c)) > 0.:
        (a, b, c, d) = (-a, -b, -c, -d)
    ps = pscal3((a, b, c), cam.sun)
    ps = clamp(-1., 1., ps)
    coef = interpole(-1., 0.5, 1., 1., ps)
    return int(coef * rr), int(coef * vv), int(coef * bb), int(ll)


def raycasting(cam, objet, verbal, i):
    """
    Créer l'image de fin pixel par pixel
    :param cam: Caméra
    :param objet: objet à modéliser
    :param verbal: Afficher les barres etc..
    :param i: Numéro de l'image
    """
    img = Image.new("RGB",  # color mode
                    (2 * cam.h_size_win + 1, 2 * cam.h_size_win + 1),  # size
                    (255, 255, 255) if cam.has_background() else cam.background  # Couleur de fond d'écran
                    )

    if cam.has_background():  # Si l'image à un fond d'écran, on l'applique directement
        background = cam.background
        img_w, img_h = img.size
        bg_w, bg_h = background.size
        offset = ((img_w - bg_w) // 2, (img_h - bg_h) // 2)
        img.paste(background, offset)  # on applique le fond d'écran à l'image à générer

    # On touche ensuite seulement les pixels concernés par l'objet qu'on modélise
    for x_pix in range(-cam.h_size_win, cam.h_size_win + 1, 1):  # Pour tous les pixels en x de l'image
        for z_pix in range(-cam.h_size_win, cam.h_size_win + 1, 1):  # pour tous les pixels en y
            if verbal:  # Si verbal = True, on affiche la barre de progression
                progress_bar(((x_pix + cam.h_size_win) / (cam.h_size_win * 2. + 1.)) * 100)
            rayon = cam.generate_ray(x_pix, z_pix)  # On génère le rayon
            contacts = objet.intersection(rayon)  # On récupère les contacts
            if contacts is not None:  # S'il y a un contact entre le rayon de l'objet à modéliser
                (contact1, contact2) = hd(contacts)  # On récupère le contacte
                (r, v, b, ll) = rendering(cam, contact1, i)  # On fait le rendu du pixel
                # On met à jour le pixel :
                img.putpixel((x_pix + cam.h_size_win, 2 * cam.h_size_win - (z_pix + cam.h_size_win)), (r, v, b, ll))

    # img.show()
    img.save(f"{cam.nom}.png")  # On sauvegarde l'image

    if not verbal:  # Si on n'affiche pas la progression, on affiche tout de même un message de fin
        print(f"{cam.nom} generated")
