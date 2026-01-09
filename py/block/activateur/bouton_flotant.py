from typing import TYPE_CHECKING

from py.block.activateur.activateur import ActivateurPlatforme
from py.objet.zone import Zone3D

if TYPE_CHECKING:
    from py.game.map import Map
    from py.interface.class_clavier import Clavier


class BoutonFlottant(ActivateurPlatforme):
    """Bouton est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    # def __init__(
    #     self,
    #     coordonnee: list[int],
    #     taille: tuple[int, int, int],
    #     couleur: tuple[int, int, int],
    #     sorti: int,
    # ):
    #     """initialise le bouton"""
    #     super().__init__(coordonnee, taille, couleur, sorti)

    def get_zone_dectect(self) -> Zone3D:
        """permet de récupérer la zone de détection"""
        return self

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")

    def condition_sup(self, map_: "Map") -> bool:  # pylint: disable=unused-argument
        """permet de vérifier la condition supplémentaire"""
        return True


class BoutonFlottantPush(BoutonFlottant):
    """Bouton_push est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    # def __init__(
    #     self,
    #     coordonnee: list[int],
    #     taille: tuple[int, int, int],
    #     couleur: tuple[int, int, int],
    #     sorti: int,
    #     rayon_dectect: int,
    # ):
    #     """initialise le bouton"""
    #     super().__init__(coordonnee, taille, couleur, sorti, rayon_dectect)

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        clavier: Clavier = map_.get_game().clavier
        touche: dict[str, int] = map_.get_game().get_touche()
        joueur: Zone3D = map_.get_playeur()

        if (
            clavier.get_pression(touche["interaction"]) == "presser"
            and self.condition_sup(map_)
            and self.get_zone_dectect().collision(joueur.get_pos(), joueur.get_size())
        ):
            self.set_activer(True)
        else:
            self.set_activer(False)


class BoutonFlottantSwitch(BoutonFlottant):
    """Bouton_switch est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    # def __init__(
    #     self,
    #     coordonnee: list[int],
    #     taille: tuple[int, int, int],
    #     couleur: tuple[int, int, int],
    #     sorti: int,
    #     zone_dectect: Zone3D,
    # ):
    #     """initialise le bouton"""
    #     super().__init__(coordonnee, taille, couleur, sorti, zone_dectect)

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        clavier: Clavier = map_.get_game().clavier
        touche: dict[str, int] = map_.get_game().get_touche()
        joueur: Zone3D = map_.get_playeur()

        if (
            clavier.get_pression(touche["interaction"]) == "vien_presser"
            and self.condition_sup(map_)
            and self.get_zone_dectect().collision(joueur.get_pos(), joueur.get_size())
        ):
            self.set_activer(not self.get_activer())


class BoutonFlottantImpulse(BoutonFlottant):
    """Bouton_impulse est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    # def __init__(
    #     self,
    #     coordonnee: list[int],
    #     taille: tuple[int, int, int],
    #     couleur: tuple[int, int, int],
    #     sorti: int,
    #     zone_dectect: Zone3D,
    # ):
    #     """initialise le bouton"""
    #     super().__init__(coordonnee, taille, couleur, sorti, zone_dectect)

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        clavier: Clavier = map_.get_game().clavier
        touche: dict[str, int] = map_.get_game().get_touche()
        joueur: Zone3D = map_.get_playeur()

        if (
            clavier.get_pression(touche["interaction"]) == "vien_presser"
            and self.condition_sup(map_)
            and self.get_zone_dectect().collision(joueur.get_pos(), joueur.get_size())
        ):
            self.set_activer(True)
        else:
            self.set_activer(False)
