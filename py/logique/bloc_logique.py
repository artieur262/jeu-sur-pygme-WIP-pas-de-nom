"""contient les different bloc logique"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py.game.map import Map


class Logique:
    """classe mere des blocs logique"""

    def __init__(self, entre, sorti: int | tuple[str, int]):
        """initialise le bloc logique"""
        self.entre = entre
        self.sorti = sorti

    def get_activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")

    def ajouter_map(self, map_: "Map") -> None:
        """ajoute la map"""
        map_.add_logique(self)

    def retirer_map(self, map_: "Map") -> None:
        """retire la map"""
        map_.remove_logique(self)
