from typing import TYPE_CHECKING
from py.objet.objet_unicolor import ObjetUnicolor3D

if TYPE_CHECKING:
    from py.game.map import Map


class Plateforme(ObjetUnicolor3D):
    """Plateforme est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    # def __init__(
    #     self,
    #     coordonnee: list[int],
    #     taille: tuple[int, int, int],
    #     couleur: tuple[int, int, int],
    # ):
    #     """initialise le bouton"""
    #     super().__init__(coordonnee, taille, couleur)

    def ajouter_map(self, map_: "Map") -> None:
        map_.add_colision(self)
        map_.add_afficher(self)

    def retirer_map(self, map_: "Map") -> None:
        map_.remove_colision(self)
        map_.remove_afficher(self)
