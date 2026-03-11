from typing import TYPE_CHECKING

from py.interface.box import Box


if TYPE_CHECKING:
    import pygame
    from py.interface.element_it import ElementInterface


class Grid(Box):
    """Grid est une box qui aligne ses element sur une grille encré par le coin haut gauche"""

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        espacement: tuple[int, int],
        element: list["ElementInterface"] | None = None,
        parent: "ElementInterface" = None,
    ) -> None:
        if element is None:
            element = []

        super().__init__(position, size, True, parent)
        self._espacement = espacement
        self._element: list["ElementInterface"] = element

    def get_espacement(self) -> tuple[int, int]:
        """get l'espacement entre les éléments de la grille"""
        return self._espacement

    def get_element(self) -> list["ElementInterface"]:
        """get les éléments de la grille"""
        return self._element

    def add_element(self, element: "ElementInterface") -> None:
        """ajoute un élément à la grille

        Args:
            element (elementInterface): élément à ajouter
        """
        self._element.append(element)

    def actualise_taille(self) -> None:
        """actualise la taille de la box en fonction de ses element"""
        for element in self._element:
            element.actualise_taille()

        nb_ligne_max = self.get_size()[0] // self._espacement[0]

        for i, element in enumerate(self._element):
            element.set_parent(self)
            if nb_ligne_max == 0:
                element.set_pos((0, 0))
            else:
                element.set_pos(
                    (
                        (i % nb_ligne_max) * self._espacement[0] + self.get_pos()[0],
                        (i // nb_ligne_max) * self._espacement[1] + self.get_pos()[1],
                    )
                )


class GridCenter(Grid):
    """GridCenter est une box qui aligne ses element sur une grille encré par le centre"""

    def actualise_taille(self) -> None:
        """actualise la taille de la box en fonction de ses element"""
        for element in self._element:
            element.actualise_taille()

        nb_ligne_max = self.get_size()[0] // self._espacement[0]

        for i, element in enumerate(self._element):
            element.set_parent(self)
            if nb_ligne_max == 0:
                element.set_pos((0, 0))
            else:
                element.set_pos(
                    (
                        (i % nb_ligne_max) * self._espacement[0]
                        + self.get_pos()[0]
                        - ((self.get_size()[0] + self._espacement[0]) // 2),
                        (i // nb_ligne_max) * self._espacement[1]
                        + self.get_pos()[1]
                        - ((self.get_size()[1] + self._espacement[1]) // 2),
                    )
                )
