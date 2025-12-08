from typing import TYPE_CHECKING

from py.block.plateforme import Plateforme

if TYPE_CHECKING:
    from py.game.Map import Map
# from py.game.game import Map


class Activateur:
    """Activateur est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(self, sorti: int):
        """initialise le bouton"""
        self._sorti = sorti
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

    def activer(self, map_: "Map") -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        output: set[int] = map_.get_signal()
        if self._activer:
            output.add(self._sorti)

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
