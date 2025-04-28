"""cette parti est la pour gérer l'interface graphique du jeu

il y a 2 class:
    - Image : class pour gérer les images
    - ObjetGraphique : class pour gérer les objet graphique

il y a 6 fonctions:
    - gener_texture : permet de générer une texture rectangulaire
    - gener_texture_arc_ciel : permet de générer une texture arc en ciel
    - decoupe_texte : permet de découper un texte en plusieur ligne
    - place_texte_in_texture : permet de mettre du texte sur une image
    - vider_affichage : permet de vider l'affichage
    - quitter : permet de quitter
    
et 1 variable:
    - screen : est la fenêtre du jeu
"""

# pylint: disable=no-member

import os
import pygame
import numpy as nup
from py.autre import save

       
        
    


def surfaces_egales(surface1 :pygame.Surface, surface2:pygame.Surface) -> bool:
    if surface1.get_size() != surface2.get_size():
        return False
    # Conversion des surfaces en tableaux de pixels
    pixels1 = pygame.surfarray.array3d(surface1)
    pixels2 = pygame.surfarray.array3d(surface2)
    
    return nup.array_equal(pixels1, pixels2)

def genere_texture(taille: tuple[int, int], color: tuple) -> pygame.Surface:
    """génere une texture rectangulaire

    Args:
        taile (tuple[int]): (x,y) est la taille de la texture
        color (tuple[int]): (Red,Green,Blue,trasparence "optionel") est la couleur de l'image

    Returns:
        Surface: est l'image généré
    """

    if len(color) == 3:  # permet de pas forcer de metre des couleurs
        # print(taille)
        image = pygame.Surface(taille)
        image.fill(color)
    elif len(color) == 4:
        image = pygame.Surface(taille, pygame.SRCALPHA)
        image.fill(color)
    return image


def decoupe_texte(
    texte: str, longueur_ligne: int, police: pygame.font.Font
) -> list[str]:
    """decoupe un texte en plusieur ligne
    en sorte que chaque ligne ne dépasse pas la longueur donnée

    Args:
        texte (str): est le texte à découper
        taille (int): est la taille de la ligne
        police (pygame.font.Font): est la police du texte

    Returns:
        list[str]: est le texte découpé
    """
    texte = texte.split("\n")
    texte_decoupe = []
    for fragment in texte:
        fragment = fragment.split(" ")
        ligne = ""
        for i in fragment:
            if police.size(ligne + i)[0] < longueur_ligne:
                ligne += i + " "
            elif len(ligne) > 0:
                texte_decoupe.append(ligne[:-1])
                ligne = i + " "
            else:
                texte_decoupe.append(i)
        if len(ligne) > 0:
            texte_decoupe.append(ligne[:-1])

    return texte_decoupe


def place_texte_in_texture(
    image: pygame.Surface,
    texte: str,
    police: pygame.font.Font,
    color: tuple[int],
    mode: str = "centrage",
) -> pygame.Surface:
    """ajoute du texte sur une image
    la fonction gère les saut de ligne quand le texte est trop long ou qu'il y a des "\\n"

    Args:
        image (pygame.Surface): est l'image qui recevera le texte
        texte (str): est le texte rajouter
        police (pygame.font.Font): est la police du texte
        color (tuple[int]): est la couleur du texte
        mode (str, optional): est le mode de placement du texte. Defaults to "centrage".
                ("centrage", "haut_gauche", "gauche_centre", "haut_droit", "centrage_haut")
    Returns:
        image (pygame.Surface): est image avec son texte
    """
    # print(type(image))
    dimention_image = image.get_size()
    texte_decoupe = decoupe_texte(texte, dimention_image[0], police)
    match mode:
        case "centrage":
            for i, ligne in enumerate(texte_decoupe):
                dimention_ligne = police.size(ligne)
                image.blit(
                    police.render(ligne, 2, color),
                    (
                        (dimention_image[0] - dimention_ligne[0]) // 2,
                        (dimention_image[1] - dimention_ligne[1] * len(texte_decoupe))
                        // 2
                        + i * dimention_ligne[1],
                    ),
                )
        case "haut_gauche":
            for i, ligne in enumerate(texte_decoupe):
                dimention_ligne = police.size(ligne)
                image.blit(
                    police.render(ligne, 2, color),
                    (0, i * dimention_ligne[1]),
                )
        case "haut_droit":
            for i, ligne in enumerate(texte_decoupe):
                dimention_ligne = police.size(ligne)
                image.blit(
                    police.render(ligne, 2, color),
                    (
                        dimention_image[0] - dimention_ligne[0],
                        i * dimention_ligne[1],
                    ),
                )
        case "centrage_haut":
            for i, ligne in enumerate(texte_decoupe):
                dimention_ligne = police.size(ligne)
                image.blit(
                    police.render(ligne, 2, color),
                    (
                        (dimention_image[0] - dimention_ligne[0]) // 2,
                        i * dimention_ligne[1],
                    ),
                )
        case "gauche_centre":
            for i, ligne in enumerate(texte_decoupe):
                dimention_ligne = police.size(ligne)
                image.blit(
                    police.render(ligne, 2, color),
                    (
                        0,
                        (dimention_image[1] - dimention_ligne[1] * len(texte_decoupe))
                        // 2
                        + i * dimention_ligne[1],
                    ),
                )
        case _:
            print("mode inconnu :", mode)
    return image


def vider_affichage(couleur_du_fond: tuple | int = 0):
    """permet de vider l'affichage
    donc de tout retire et met la couleur qui est entre en fond

    Args:
        couleur_du_fond (tuple or int): bref c'est une couleur RGB (red, green, blue)
    """
    screen.fill(couleur_du_fond)


def quitter():
    """permet de quitter"""
    pygame.quit()
    exit()


pygame.init()
screen = pygame.display.set_mode((1200, 600), pygame.RESIZABLE)
screen.fill((200, 200, 200))

if __name__ == "__main__":
    pygame.display.set_caption("projet")
