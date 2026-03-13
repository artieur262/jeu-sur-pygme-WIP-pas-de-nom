import pygame

from py.interface.element_it import ElementInterface
from py.interface.box import Box
from py.objet.objet_visuel import ObjetVisuel2D


class Iframe(ObjetVisuel2D, Box):
    """Iframe est une interface qui affiche un objet graphique

    Args:
        objet (ObjetVisuel2D): est l'objet graphique à afficher dans l'iframe
    """

    def __init__(
        self,
        pos: tuple[int, int],
        taille: tuple[int, int],
        element: list[ElementInterface] = None,
        parent: ElementInterface = None,
        auto_actualise: bool = True,
    ):
        image = pygame.Surface(taille)
        image.fill((0, 0, 0, 0))
        ObjetVisuel2D.__init__(self, pos, taille, image)
        Box.__init__(self, pos, taille, element, False, parent)
        self._auto_actualise = auto_actualise

    def actualise_taille(self):
        """actualise la taille de l'iframe en fonction de ses elements"""
        self.actualise_graphique()

    def actualise_graphique(self):
        """actualise la surface de l'iframe en fonction de ses elements"""
        self.texture.texture.fill((0, 0, 0, 0))
        for element in self._element:
            element.actualise_taille()
            element.afficher(
                (-self.get_pos()[0], -self.get_pos()[1]), self.texture.texture
            )

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
        if decalage is None:
            decalage = (0, 0)
        if surface is None:
            surface = pygame.display.get_surface()
        if self._auto_actualise:
            self.actualise_graphique()
        if self.texture.if_in_zone((0, 0), (0, 0), surface.get_size()):
            self.texture.afficher(
                (self.coordonnee[0] + decalage[0], self.coordonnee[1] + decalage[1]),
                surface,
            )
            return True
        return False
