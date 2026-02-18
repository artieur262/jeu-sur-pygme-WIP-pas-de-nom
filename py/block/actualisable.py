from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py.game.map import Map


class Actualisable:
    """Classe de base pour les éléments qui nécessitent une actualisation régulière.
    Les éléments qui héritent de cette classe doivent implémenter la méthode `actualiser`.
    """

    def actualiser(self, map_: "Map") -> None:
        """Actualise l'état de l'élément en fonction de la map.
        Cette méthode doit être implémentée par les sous-classes.
        """
        raise NotImplementedError("La méthode 'actualiser' doit être implémentée.")

    def ajouter_map(self, map_: "Map") -> None:
        """ajoute la map"""
        map_.add_actualisable(self)

    def retirer_map(self, map_: "Map") -> None:
        """retire la map"""
        map_.remove_actualisable(self)
