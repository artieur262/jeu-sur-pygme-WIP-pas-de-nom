"""ce module contient la classe Activable qui est la classe de base des blocs logique activable"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py.game.map import Map


class Activable:
    """Activateur est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(self, entre: int):
        """initialise le bouton"""
        self._entre = entre
        self._activer = False

    def get_activer(self) -> bool:
        """permet de savoir si le bloc logique est actif"""
        return self._activer

    def set_activer(self, activer: bool) -> None:
        """permet de changer l'etat du bloc logique"""
        self._activer = activer

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")

    def ajouter_map(self, map_: "Map") -> None:
        """ajoute la map"""
        map_.add_activateur(self)
