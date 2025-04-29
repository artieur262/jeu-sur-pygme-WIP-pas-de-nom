import pygame
from py.graphique.graphique import screen
from py.graphique.image import Image
from py.objet.objetVisuel import ObjetVisuel3D, ObjetVisuel2D

class ObjetUnicolor2D(ObjetVisuel2D):
    """ObjetUnicolor est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(self, coordonnee: list, taille: tuple[int, int], couleur: tuple[int, int, int]):
        super().__init__(coordonnee, taille)
        self.couleur = couleur
        self.surface = pygame.Surface(taille)
        self.surface.fill(couleur)


    def afficher(
        self,
        decalage: tuple[int, int] = None,
        surface: pygame.Surface = None,
    ) -> bool:
        """permet de l'affiché sur la sur une surface et de savoir si il est affiché

        Args:
            decalage (tuple[int, int], optional): est le decalage de l'objet. Defaults to None.
            surface (pygame.Surface, optional): est la surface sur laquel afficher. Defaults None.

        Returns:
            bool: si l'objet est affiché
        """
        if surface is None:
            surface = screen
        if decalage is None:
            decalage = (0, 0)
        surface.blit(self.surface, (self.coordonnee[0] + decalage[0], self.coordonnee[1] + decalage[1]))
               


class ObjetUnicolor3D(ObjetVisuel3D):
    """ObjetUnicolor est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(self, coordonnee: list[int], taille: tuple[int, int, int], couleur: tuple[int, int, int]):
        """initialise le bouton"""
        face_graphique = [Image(pygame.surface((taille[1], taille[2]), pygame.SRCALPHA)),
                Image(pygame.surface((taille[0], taille[2]), pygame.SRCALPHA)),
                Image(pygame.surface((taille[0], taille[1]), pygame.SRCALPHA)),
                ]
        for i in face_graphique:
            i.texture.fill(couleur)
        super().__init__(coordonnee, taille, face_graphique)
        self.couleur = couleur