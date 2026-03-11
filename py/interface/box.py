"""
abandonne pour le moment, a revoir plus tard
"""

from typing import TYPE_CHECKING


from py.objet.objet_visuel import ObjetVisuel2D
from py.interface.element_it import ElementInterface

if TYPE_CHECKING:
    import pygame


class Box(ElementInterface):
    """Box est une zone qui a une image et un texte
    Args:
        ObjetVisuel (ObjetVisuel): est la zone de l'objet graphique
    """

    def __init__(
        self,
        pos: tuple[int, int],
        taille: tuple[int, int] = None,
        element: list[ElementInterface | ObjetVisuel2D] = None,
        auto_taille: bool = False,
        parent: ElementInterface = None,
    ):

        super().__init__(pos, taille, auto_taille, parent)
        self._element = element

    def set_pos(self, valu: tuple[int, int]):
        """defini la position de l'objet"""
        decalage = soustract_2_tuple(valu, self.coordonnee)
        super().set_pos(valu)
        for i in self._element:
            i.add_pos(decalage)

    def add_pos(self, valu: tuple[int, int]):
        """ajoute une position a l'objet"""
        super().add_pos(valu)
        for i in self._element:
            i.add_pos(valu)

    def ajouter_element(self, element: ElementInterface) -> None:
        """ajoute un element a la box"""
        self._element.append(element)
        element.set_parent(self)

    def retirer_element(self, element: ElementInterface) -> None:
        """retire un element de la box"""
        self._element.remove(element)
        element.set_parent(None)

    def actualise_taille(self) -> None:
        """actualise la taille de la box en fonction de ses element"""
        raise NotImplementedError(
            "Cette méthode doit être implémentée par les sous-classes."
        )

    def affiche(
        self, decalage: tuple[int, int] = None, surface: "pygame.Surface" | None = None
    ) -> None:
        """affiche la grille sur la surface donnée

        Args:
            surface (pygame.Surface): est la surface sur laquelle afficher la grille
        """
        for element in self._element:
            element.affiche(decalage, surface)


def soustract_2_tuple(
    tuple1: tuple[int, int], tuple2: tuple[int, int]
) -> tuple[int, int]:
    """permet de soustraire 2 tuple

    Args:
        tuple1 (tuple[int, int]): est le premier tuple
        tuple2 (tuple[int, int]): est le second tuple

    Returns:
        tuple[int, int]: le resultat de la soustraction
    """
    return (tuple1[0] - tuple2[0], tuple1[1] - tuple2[1])
