import pygame

from py.objet.zone import Zone

class ObjetVisuel(Zone):
    """ObjetVisuel est une zone qui a une image et un texte
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(self, coordonnee: list, taille: tuple[int, int]):
        super().__init__(coordonnee, taille)

        
    def afficher(
        self,
        decalage: tuple[int, int] = None,
        surface: pygame.Surface = None,
    ):
        """permet de l'affiché sur la sur une surface et de savoir si il est affiché

        Args:
            decalage (tuple[int, int], optional): est le decalage de l'objet. Defaults to None.
            surface (pygame.Surface, optional): est la surface sur laquel afficher. Defaults None.

        Returns:
            bool: si l'objet est affiché
        """
        pass