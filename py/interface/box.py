"""
abandonne pour le moment, a revoir plus tard
"""

from typing import TYPE_CHECKING


# from py.objet.objet_visuel import ObjetVisuel2D
from py.interface.element_it import ElementInterface
from py.graphique.actualisation_pygame import screen

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
        element: list[ElementInterface] = None,
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
        print(self._element)
        for i in self._element:
            print("add pos", valu)
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

    def afficher(
        self,
        decalage: tuple[int, int] = None,
        surface: "pygame.Surface" = screen,
    ) -> None:
        """affiche la grille sur la surface donnée

        Args:
            surface (pygame.Surface): est la surface sur laquelle afficher la grille
        """
        for element in self._element:
            element.afficher(decalage, surface)


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


class HBox(Box):
    """HBox est une box qui aligne ses element horizontalement"""

    def __init__(
        self,
        pos: list[int],
        taille: tuple[int, int] = None,
        espacement: int = None,
        element=None,
        auto_taille=False,
        parent=None,
        centrer=False,
    ):
        super().__init__(pos, taille, element, auto_taille, parent)
        self._espacement = espacement
        self._axe = 0
        self._centrer = centrer
        if self._espacement is None and self._taille_auto:
            raise ValueError(
                "L'espacement doit être défini si la taille est automatique"
            )

    def actualise_taille(self) -> None:
        """actualise la taille de la box en fonction de ses element"""
        for element in self._element:
            element.actualise_taille()

        nextpos = [self.get_pos()[0], self.get_pos()[1]]
        if self._centrer:
            nextpos[1 - self._axe] += self.get_size()[1 - self._axe] // 2

        if self._taille_auto:
            for element in self._element:
                element.set_pos(
                    [
                        nextpos[0],
                        nextpos[1],
                    ]
                )
                nextpos[self._axe] += element.get_size()[self._axe] + self._espacement
                if self._centrer:
                    element.add_pos_in_axe(
                        1 - self._axe,
                        element.get_size()[1 - self._axe] // 2,
                    )
            self.set_size_in_axe(
                self._axe,
                nextpos[self._axe] - self.get_pos()[self._axe] - self._espacement,
            )
        else:
            somme_taille = sum(
                element.get_size()[self._axe] for element in self._element
            )
            self._espacement = (self.get_size()[self._axe] - somme_taille) // (
                len(self._element) - 1
            )
            for element in self._element:
                element.set_pos(
                    [
                        nextpos[0],
                        nextpos[1],
                    ]
                )
                nextpos[self._axe] += element.get_size()[self._axe] + self._espacement
                if self._centrer:
                    element.add_pos_in_axe(
                        1 - self._axe,
                        element.get_size()[1 - self._axe] // 2,
                    )


class VBox(HBox):
    """VBox est une box qui aligne ses element verticalement"""

    def __init__(
        self,
        pos: list[int],
        taille: tuple[int, int] = None,
        espacement: int = None,
        element=None,
        auto_taille=False,
        parent=None,
        centrer=False,
    ):
        super().__init__(pos, taille, espacement, element, auto_taille, parent, centrer)
        self._axe = 1
