"""ce module contient la classe Activable qui est la classe de base des blocs logique activable"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py.game.map import Map


class Activable:
    """Activateur est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(self, entre: str | int | tuple[str, int] | tuple[str, int, str]):
        """initialise le bouton"""
        self._entre = entre

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")

    def ajouter_map(self, map_: "Map") -> None:
        """ajoute la map"""
        map_.add_activateur(self)

    def retirer_map(self, map_: "Map") -> None:
        """retire la map"""
        map_.remove_activateur(self)
