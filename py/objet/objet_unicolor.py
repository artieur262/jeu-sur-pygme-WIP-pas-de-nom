"""Module qui gère les objets unicolor (2D et 3D)
elle permet de créer des objets graphique avec une seule couleur

il contient les classes:
- ObjetUnicolor2D
- ObjetUnicolor3D


"""

import pygame

# from py.graphique.graphique import screen
# from py.graphique.image import Image
from py.objet.objet_visuel import ObjetVisuel3D, ObjetVisuel2D


class ObjetUnicolor2D(ObjetVisuel2D):
    """ObjetUnicolor est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(
        self, coordonnee: list, taille: tuple[int, int], couleur: tuple[int, int, int]
    ):
        surface = pygame.Surface(taille)
        surface.fill(couleur)
        self.couleur = couleur
        super().__init__(coordonnee, taille, surface)


class ObjetUnicolor3D(ObjetVisuel3D):
    """ObjetUnicolor est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int, int],
        couleur: tuple[int, int, int],
    ):
        """initialise le bouton"""
        face_graphique = [
            pygame.Surface((taille[1], taille[2]), pygame.SRCALPHA),
            pygame.Surface((taille[0], taille[2]), pygame.SRCALPHA),
            pygame.Surface((taille[0], taille[1]), pygame.SRCALPHA),
        ]
        for i in face_graphique:
            i.fill(couleur)
        super().__init__(coordonnee, taille, face_graphique)
        self.couleur = couleur

    def ajouter_map(self, map_):
        raise NotImplementedError("la fonction n'est pas encore implémenté")
