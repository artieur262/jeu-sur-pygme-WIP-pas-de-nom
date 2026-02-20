from typing import TYPE_CHECKING

from py.block.activable.activable import Activable
from py.objet.objet_unicolor import ObjetUnicolor3D

if TYPE_CHECKING:
    from py.game.map import Map


class PlatformeMouvante(ObjetUnicolor3D, Activable):
    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int, int],
        couleur: tuple[int, int, int],
        entre: int | tuple[str, int] | tuple[str, int, str],
    ):
        """initialise le bouton"""
        ObjetUnicolor3D.__init__(self, coordonnee, taille, couleur)
        Activable.__init__(self, entre)
        self._active: bool = False

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        self._active = map_.in_signal(self._entre)

    def ajouter_map(self, map_):
        Activable.ajouter_map(self, map_)

    def arriver_fin(self):
        """permet de definir le comportement de la plateforme a la fin du deplacement"""
        pass  # pylint: disable=unnecessary-pass
        # a definir en fonction de la plateforme

    def deplacer(self, map_: "Map") -> None:
        """permet de deplacer la plateforme"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")
