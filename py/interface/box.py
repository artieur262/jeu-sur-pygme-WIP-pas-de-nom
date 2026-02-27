"""
abandonne pour le moment, a revoir plus tard
"""

from typing import TYPE_CHECKING
import pygame

from py.objet.objet_visuel import ObjetVisuel2D
from py.interface.element_it import ElementInterface


class Box(ObjetVisuel2D, ElementInterface):
    """Box est une zone qui a une image et un texte
    Args:
        ObjetVisuel (ObjetVisuel): est la zone de l'objet graphique
    """

    def __init__(
        self,
        taille: tuple[int, int] = None,
        ellement: list[ObjetVisuel2D] = None,
        parent: ElementInterface = None,
    ):

        if taille is None:
            taille = (0, 0)
            ElementInterface.__init__(self, True, parent)
        else:
            ElementInterface.__init__(self, False, parent)
        super().__init__((0, 0), taille)

        self.ellement = ellement
        self.ecart = 0
        self.ecart_auto = True

    def set_pos(self, valu: tuple[int, int]):
        """defini la position de l'objet"""
        decalage = soustract_2_tuple(valu, self.coordonnee)
        super().set_pos(valu)
        for i in self.ellement:
            i.add_pos(decalage)

    def set_size(self, valu):
        ObjetVisuel2D.set_size(self, valu)

    def ajouter_ellement(self, ellement: ElementInterface) -> None:
        """ajoute un ellement a la box"""
        self.ellement.append(ellement)
        ellement.set_parent(self)

    def retirer_ellement(self, ellement: ElementInterface) -> None:
        """retire un ellement de la box"""
        self.ellement.remove(ellement)
        ellement.set_parent(None)

    def actualise_taille(self) -> None:
        """actualise la taille de la box en fonction de ses ellement"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")


class VBox(Box):
    """VBox est une box qui aligne ses ellement verticalement"""

    def actualise_taille(self) -> None:
        """actualise la taille de la box en fonction de ses ellement"""
        # definir la taille fixe de la box en fonction de ses ellement qui ne change pas de taille
        somme = 0
        nb = 0
        for i in self.ellement:
            if i.get_size() != (0, 0):
                somme += i.get_size()[1]
                nb += 1

        reste = self.get_size()[1] - somme
        part = (reste / (len(self.ellement) - nb)) if len(self.ellement) - nb > 0 else 0


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
