# coding: utf-8
from PIL import Image
import glob
import os


def make_gif(**kwargs):
    """
    Génère un gif avec les images se trouvant dans le 'path'
    :param kwargs: dict -> path, duration, deleted_images
    :return: None
    """
    # Liste des images
    frames = []

    # On liste toutes les images se trouvant dans le dossier
    if "path" in kwargs:
        imgs = glob.glob(f"{kwargs['path']}*.png")
    else:
        imgs = glob.glob("*.png")

    # S'il n'y a pas d'image
    if len(imgs) == 0:
        print("Cannot find an image.")
        return

    # On crée une un objet image et on lui ajoute toutes les images
    for img in imgs:
        new_frame = Image.open(img)
        frames.append(new_frame)

    # On enregistre l'image
    # Le temps d'affichage de chaque image se modifie avec le paramètre 'duration'
    frames[0].save(f"{kwargs['path'] if 'path' in kwargs else ''}render.gif",
                   format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=kwargs.get("duration", 80),
                   loop=0,
                   quality=5)

    # On supprime les images si deleted_images est défini
    if "deleted_images" in kwargs:
        if kwargs["deleted_images"]:
            for img in imgs:
                if os.path.exists(img):
                    os.remove(img)


# Si on lance le fichier de manière unitaire
if __name__ == "__main__":
    make_gif(path="output/steiner4/")
