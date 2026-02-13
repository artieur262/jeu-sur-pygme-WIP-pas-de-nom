from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py.game.map import Map


class Special:
    """Classe de base pour les éléments spéciaux du jeu.

    Args:
        controle (tuple[tuple[str, int], ...]): Un tuple de tuples représentant les contrôles
            associés à cet élément spécial. tuple[touche, action]
            - touche (str): Le nom de la touche qui déclenche l'action.
                le nom de la touche correspond à controle
            - action (int): Le code de l'action à effectuer lorsque la touche est pressée.
                0: laché, 1: relâché, 2: maintenu, 3:vient d'être pressé
                # Note ne pas utiliser la valeur 0 pour les actions car erreur potentielle.
    """

    def __init__(self, controle: tuple[tuple[str, int], ...] = None):
        """initialise l'élément spécial"""
        self.__controle = controle if controle is not None else ()

    def get_controle(self) -> tuple[tuple[str, int], ...]:
        """get le controle de l'élément spécial"""
        return self.__controle

    def active_input(self, controle: tuple[str, int], map_: "Map") -> None:
        """gère les entrées pour l'élément spécial"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")

    def actualiser(self, map_: "Map") -> None:
        """actualise les éléments spéciaux"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")

    def ajouter_map(self, map_: "Map") -> None:
        """ajoute la map"""
        for controle in self.__controle:
            map_.add_special(controle, self)

    def retirer_map(self, map_: "Map") -> None:
        """retire la map"""
        for controle in self.__controle:
            map_.remove_special(controle, self)
