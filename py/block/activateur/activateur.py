from typing import TYPE_CHECKING

from py.block.plateforme import Plateforme

if TYPE_CHECKING:
    from py.game.map import Map


class Activateur:
    """Activateur est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(self, sorti: int | str | tuple[str, int]):
        """initialise le bouton"""
        self._sorti: int | str = sorti

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")

    def ajouter_map(self, map_: "Map") -> None:
        """ajoute la map"""
        map_.add_activateur(self)


class ActivateurPlatforme(Plateforme, Activateur):
    """Activateur est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int, int],
        couleur: tuple[int, int, int],
        sorti: int,
    ):
        """initialise le bouton"""
        Plateforme.__init__(self, coordonnee, taille, couleur)
        Activateur.__init__(self, sorti)

    def ajouter_map(self, map_: "Map") -> None:
        Activateur.ajouter_map(self, map_)
        Plateforme.ajouter_map(self, map_)

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")
