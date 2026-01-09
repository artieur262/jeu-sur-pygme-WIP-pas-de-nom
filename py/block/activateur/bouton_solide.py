from typing import TYPE_CHECKING

from py.block.activateur.activateur import ActivateurPlatforme
from py.objet.zone import Zone3D

# from py.interface.class_clavier import Clavier
from py.block.activateur.bouton_flotant import (
    BoutonFlottantPush,
    BoutonFlottantSwitch,
    BoutonFlottantImpulse,
)

if TYPE_CHECKING:
    from py.game.map import Map
    from py.interface.class_clavier import Clavier


class BoutonSolid(ActivateurPlatforme):
    """Bouton est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int, int],
        couleur: tuple[int, int, int],
        sorti: int | tuple[str, int],
        rayon_dectect: int,
    ):
        """initialise le bouton"""
        super().__init__(coordonnee, taille, couleur, sorti)
        self.__rayon_dectect = rayon_dectect
        self.__zone_dectect: Zone3D = self.genere_zone_dectect()

    def get_zone_dectect(self) -> Zone3D:
        """permet de récupérer la zone de détection"""
        return self.__zone_dectect

    def genere_zone_dectect(self) -> Zone3D:
        """permet de générer la zone de détection
        Args:
            axe (int, optional):
                axe de la zone de détection. Defaults to -1, ce qui signifie que la zone de
                détection est dans les 3 axes. La valeur de axe correspond à l'axe qui ne sera
                pas pris en compte pour la zone de détection.
                axe = 0 pour l'axe x, axe = 1 pour l'axe y, axe = 2 pour l'axe z.


        """
        pos = []
        taille = []
        for i in range(3):
            pos.append(self.get_pos()[i] - self.__rayon_dectect)
            taille.append(self.get_size()[i] + self.__rayon_dectect * 2)

    def condition_sup(self, map_: "Map") -> bool:
        """permet de vérifier la condition supplémentaire"""
        return self.dans_plan(map_.get_game().get_hauteur(), map_.get_game().get_plan())
        # autre possibilité avec la collision mais optimisation moins bonne
        # playeur = map_.get_playeur()
        # plan = map_.get_game().get_plan()
        # return self.collision_in_axe(
        #     playeur.get_pos()[plan], playeur.get_size()[plan], plan
        # )

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")


class BoutonSolidPush(BoutonSolid):
    """Bouton_push est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        BoutonFlottantPush.activation(self, map_)


class BoutonSolidSwitch(BoutonSolid):
    """Bouton_switch est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int, int],
        couleur: tuple[int, int, int],
        sorti: int | tuple[str, int],
        rayon_dectect: int,
    ):
        """initialise le bouton"""
        super().__init__(coordonnee, taille, couleur, sorti, rayon_dectect)
        self.activer: bool = False

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        BoutonFlottantSwitch.activation(self, map_)


class BoutonSolidImpulse(BoutonSolid):
    """Bouton_impulse est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        BoutonFlottantImpulse.activation(self, map_)
