import pygame
from py.block.activable.diapo import Diapo, DiapoBoucle, DiapoAllerRetour, DiapoFin
from py.graphique.image import Image


class Lumiere(Diapo):
    """cette class permet de faire une lumiere qui s'allume et s'eteint"""

    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int, int],
        color_pack: list[tuple[tuple[int, int, int]]],
        entre: int,
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

    def activation(self, map_):
        raise NotImplementedError("La methode activation doit etre implementée")


class LumiereBoucle(Lumiere):
    """cette class permet de faire une lumiere qui s'allume et s'eteint en boucle"""

    def __init__(self, coordonnee, taille, color_pack, entre):
        Lumiere.__init__(self, coordonnee, taille, color_pack, entre)

    def activation(self, map_):
        DiapoBoucle.activation(self, map_)


class LumiereAllerRetour(Lumiere):
    """cette class permet de faire une lumiere qui s'allume et s'eteint en aller retour"""

    def __init__(self, coordonnee, taille, color_pack, entre):
        Lumiere.__init__(self, coordonnee, taille, color_pack, entre)

    def activation(self, map_):
        DiapoAllerRetour.activation(self, map_)


class LumiereFin(Lumiere):
    """cette class permet de faire une lumiere qui s'allume et s'eteint une seule fois"""

    def __init__(self, coordonnee, taille, color_pack, entre):
        Lumiere.__init__(self, coordonnee, taille, color_pack, entre)

    def activation(self, map_):
        DiapoFin.activation(self, map_)
