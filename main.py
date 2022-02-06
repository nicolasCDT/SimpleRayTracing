# coding: utf-8
from rayon import *
import copy
from modeles import *  # Liste des modèles à modéliser (roman, tore, etc...)
from make_gif import make_gif  # Permet de générer un gif sans programme externe
from architecture import voutes

# Activer ou non le multiThreading
# Génération plus rapide, mais qui demande plus de ressource au processeur
MULTI_THREADING = False

if MULTI_THREADING:
    from multiprocessing import Process


def rotaz(theta, pt):
    """
    Rotation d'un angle theta d'un angle par rapport à l'origine
    :param theta: Angle
    :param pt: Point (x, y, z)
    :return: Nouveau point (x, y, z)
    """
    (x, y, z) = pt
    c = math.cos(theta)
    s = math.sin(theta)
    x2 = c * x - s * y
    y2 = s * x + c * y
    return x2, y2, z


def rotation(cam, objet, i, nb):
    """
    Effectue une rotation sur la caméra
    :param cam: Caméra
    :param objet: Objet à modéliser
    :param i: Numéro de l'image
    :param nb: Nombre d'image total
    :return: Scene modifiée
    """
    theta = math.pi * 2. * float(i) / float(nb)
    o2 = rotaz(theta, cam.o)
    ox2 = rotaz(theta, cam.ox)
    oy2 = rotaz(theta, cam.oy)
    oz2 = rotaz(theta, cam.oz)
    cam2 = Camera(o2, ox2, oy2, oz2, cam.h_size_world, cam.h_size_win, cam.sun, background=cam.background_link)
    return cam2, objet


def new_animation(cam, objet, i, nb):
    """
    Animation pour tore
    :param cam: Camera
    :param objet: Tore
    :param i: Ième image
    :param nb: nb images à générer
    :return: Caméra et objet modifiés
    """
    if i < (nb / 2):
        objet = Prim(tore(0.4 - ((0.4 / nb) * i), 1), objet.color)
    else:
        objet = Prim(tore(((0.4 / nb) * i), 1), objet.color)
    return cam, objet


def animation_multi_threads(cam, objet, nb, nom, anim="rota"):
    """
    Génère une animation en faisant tourner la caméra autours de l'objet en nb étapes
    Méthode multithreads : Exploite à 100% le processeur.
    :param cam: Caméra
    :param objet: Objet à modéliser
    :param nb: Nombre d'étapes
    :param nom: Nom du fichier
    :param anim: Nom de la rotation a effectuer, par défaut c'est une rotation
    """
    threads = []
    print("Making images...")
    for i in range(0, nb):  # Pour créer nb images
        if anim == "animation_tore":
            cam2, objet = new_animation(cam, objet, i, nb)
        else:
            cam2, objet = rotation(cam, objet, i, nb)

        cam2.nom = nom + str(i).zfill(4)

        # Génération On copie cam2 car on va le remodifier par la suite pour l'image suivante
        threads.append(Process(target=raycasting, args=(copy.copy(cam2), objet, False, i)))

    for p in threads:  # On lance les threads
        p.start()

    for p in threads:  # On attend la fin de tous les threads
        p.join()
    print("Done.")
    m_gif(f"{'/'.join(nom.split('/')[:2])}/")


def animation_mono_thread(cam, objet, nb, nom, anim="rota"):
    """
    Génère une animation en faisant tourner la caméra autours de l'objet en nb étapes
    Méthode monothread: N'utilise qu'un seul processus, plus long mais plus économique en ressource.
    :param cam: Caméra
    :param objet: Objet à modéliser
    :param nb: Nombre d'étapes
    :param nom: Nom du fichier
    :param anim: Nom de la rotation a effectuer, par défaut c'est une rotation
    """
    print("Making images...")
    for i in range(0, nb):  # Pour créer nb images
        if anim == "animation_tore":
            cam2, objet = new_animation(cam, objet, i, nb)
        else:
            cam2, objet = rotation(cam, objet, i, nb)

        cam2.nom = nom + str(i).zfill(4)

        print(f"Image ({i + 1}/{nb}) ")
        # Génération
        raycasting(cam2, objet, True, i)
        print("Done.")
    m_gif(f"{'/'.join(nom.split('/')[:2])}/")


def m_gif(path):
    # Création du GIF :
    print("making animation...")
    make_gif(
        path=path,
        deleted_images=False,
        duration=120
    )


def animation(cam, objet, nb, nom, anim="rota"):
    if MULTI_THREADING:
        animation_multi_threads(cam, objet, nb, nom, anim)
    else:
        animation_mono_thread(cam, objet, nb, nom, anim)


if __name__ == "__main__":
    # Configuration de l'emplacement
    # caméra par défaut :
    oeil = (0.001, -4., 0.003)
    droite = (1., 0., 0.)
    regard = (0., 1., 0.)
    vertical = (0., 0., 1.)
    camera = Camera(oeil, droite, regard, vertical, 1.5, 100, normalize3((0., -1., 2.)), background="assets"
                                                                                                    "/background.jpg")

    ##########################################
    # Primitives usuelles avec animation
    #

    # Surface de roman sans l'aspect damier :
    # animation(camera, Prim(roman(), (0, 255, 255, 255)), 1, "output/roman/roman_anime_")

    # Steiner 4
    # animation(camera, Prim(steiner4(), (0, 255, 255, 255)), 15, "output/steiner4/steiner_")

    # Steiner 2
    # animation(camera, Prim(steiner2(), (0, 255, 255, 255)), 15, "output/steiner2/steiner_")

    # Hyperboloide1
    # animation(camera, Prim(hyperboloide_1nappe(), (0, 255, 255, 255)), 15, "output/hyperboloide1/hyperboloide_")

    # Hyperboloide2
    # animation(camera, Prim(hyperboloide_2nappes(), (0, 255, 255, 255)), 15, "output/hyperboloide2/hyperboloide_")

    # Tore
    animation(camera, Prim(tore(0.4, 1), (0, 255, 255, 255)), 15, "output/tore/tore_")

    # Cone
    # animation(camera, Prim(cone(0.4), (0, 255, 255, 255)), 15, "output/cone/cone_")

    # Autre animation tore
    # animation(camera, Prim(tore(0.4, 1), (0, 255, 255, 255)), 11, "output/tore2/tore_", "animation_tore")

    ##########################################
    # Booléen
    #
    # Animation differ en forme de lune :
    # animation(camera, Differ(Prim(boule((0, 0., 0.), 1), (255, 0, 0, 255)),
    #                         Prim(boule((0.5, 0., 0.), 1), (0, 255, 255, 255))), 20, "output/differ/differ")

    # Architecture avec sa caméra :
    camera_architecture = Camera(
        (0.001, -2.001, 0.001), (1., 0., 0.), (0., 1., 0.), (0., 0., 1.),
        1.5, 50, normalize3((0., -1., 2.)))
    camera_architecture.o = (0., -50., 0.)
    camera_architecture.h_size_world = 25.
    camera.h_size_win = 100
    camera_architecture = transform_cam(trf_rota_Ox(-math.pi / 10.), camera_architecture)

    # Architecture :
    # animation(camera_architecture, voutes(), 36, "output/archi/archi")

    ##########################################
    # Phase 4 : pièce découpée dans un plateau d'écheque
    #

    # Surface de Roman animé taillée dans un damier
    # animation(camera, Prim(roman(), None), 15, "output/roman/roman_anime_")
