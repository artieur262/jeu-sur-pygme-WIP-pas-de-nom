from typing import TYPE_CHECKING
from py.objet.objet_unicolor import ObjetUnicolor3D

if TYPE_CHECKING:
    from py.game.map import Map


class Poussable(ObjetUnicolor3D):
    """Poussable est une zone qui a pour but d'être poussée par le joueur
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def ajouter_map(self, map_: "Map") -> None:
        map_.add_poussable(self)
        map_.add_afficher(self)

    def retirer_map(self, map_: "Map") -> None:
        map_.remove_poussable(self)
        map_.remove_afficher(self)
