"""ce module contient la class Lumiere et ses variantes
elle permet de faire des blocs changeant de couleur en fonction d'un signal d'activation
en realité ce sont des diapos de couleurs
"""

import pygame
from py.block.activable.diapo import (
    Diapo,
    DiapoBoucle,
    DiapoAllerRetour,
    DiapoFin,
)


class Lumiere(Diapo):
    """cette class permet de faire une lumiere qui s'allume et s'eteint"""

    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int, int],
        color_pack: list[tuple[tuple[int, int, int]]],
        entre: str,
    ):
        surface_pack = [
            (
                pygame.Surface((taille[1], taille[2]), pygame.SRCALPHA),
                pygame.Surface((taille[0], taille[2]), pygame.SRCALPHA),
                pygame.Surface((taille[0], taille[1]), pygame.SRCALPHA),
            )
            for _ in color_pack
        ]
        for i, color in enumerate(color_pack):
            for face in range(3):
                surface_pack[i][face].fill(color[face])

        super().__init__(coordonnee, taille, surface_pack, entre)

    def actualise_index_texture(self) -> None:
        """permet de mettre a jour l'index du diapo"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")


class LumiereBoucle(Lumiere):
    """cette class permet de faire une lumiere qui s'allume et s'eteint en boucle"""

    def actualise_index_texture(self):
        DiapoBoucle.actualise_index_texture(self)


class LumiereAllerRetour(Lumiere):
    """cette class permet de faire une lumiere qui s'allume et s'eteint en aller retour"""

    def actualise_index_texture(self):
        DiapoAllerRetour.actualise_index_texture(self)


class LumiereFin(Lumiere):
    """cette class permet de faire une lumiere qui s'allume et s'eteint une seule fois"""

    def actualise_index_texture(self):
        DiapoFin.actualise_index_texture(self)
