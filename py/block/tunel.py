from typing import TYPE_CHECKING
from py.objet.objet_unicolor import ObjetUnicolor3D
from py.block.special import Special

if TYPE_CHECKING:
    from py.game.map import Map


class TunelSimple(ObjetUnicolor3D, Special):
    """classe qui gere les tunel dimentionelle
    il permet de deplacer le playeur entre les different plans de facon parallele
    """

    def __init__(
        self,
        position: tuple[int, int, int],
        taille: tuple[int, int, int],
        couleur: tuple[int, int, int],
        plan_deplassable: int,
    ):
        """initialise le tunel dimentionelle"""
        super().__init__(position, taille, couleur)
        Special.__init__(self, (("deplacer_plan_plus", 2), ("deplacer_plan_moins", 2)))
        self.__plan_deplassable = plan_deplassable

    def get_plan_deplassable(self) -> set[int]:
        """get les plan deplassable"""
        return self.__plan_deplassable

    def _plan_deplacable(self, plan: int) -> bool:
        """verifie si le tunel est dans le plan"""
        return plan == self.__plan_deplassable

    def active_input(self, controle: tuple[str, int], map_: "Map") -> None:
        self.deplacer_playeur(controle, map_)

    def deplacer_playeur(
        self,
        touche: tuple[str, int],
        map_: "Map",
    ):
        """deplace le playeur dans le plan si il est dans le plan ou on peut deplacer"""
        player = map_.get_playeur()
        plan_actuel = map_.get_game().get_plan()
        if (
            self._plan_deplacable(plan_actuel)
            and touche[1] == 2
            and self.contiens_zone(player)
        ):
            player_mouvement = player.get_pos()[plan_actuel]
            if touche[0] == "deplacer_plan_plus":
                player.deplacer_in_axe(plan_actuel, 2, map_.get_colision())
            elif touche[0] == "deplacer_plan_moins":
                player.deplacer_in_axe(plan_actuel, -2, map_.get_colision())
            else:
                raise ValueError(
                    "la touche doit etre deplacer_plan_plus ou deplacer_plan_moins"
                )
            player_mouvement = player.get_pos()[plan_actuel] - player_mouvement
            map_.get_game().set_hauteur(
                map_.get_game().get_hauteur() + player_mouvement
            )

    def ajouter_map(self, map_: "Map") -> None:
        map_.add_special(self)
        map_.add_afficher(self)

    def retirer_map(self, map_: "Map") -> None:
        map_.remove_special(self)
        map_.remove_afficher(self)


class TunelMulti(TunelSimple):
    """classe qui gere les tunel dimentionelle
    il permet de deplacer le playeur entre les different plans de facon parallele
    """

    def __init__(
        self,
        position: tuple[int, int, int],
        taille: tuple[int, int, int],
        couleur: tuple[int, int, int],
        plan_deplassable: set[int],
    ):
        """initialise le tunel dimentionelle"""
        super().__init__(position, taille, couleur, -1)
        self.__plan_deplassable = plan_deplassable

    def get_plan_deplassable(self) -> set[int]:
        """get les plan deplassable"""
        return self.__plan_deplassable

    def _plan_deplacable(self, plan: int) -> bool:
        """verifie si le tunel est dans le plan"""
        return plan in self.__plan_deplassable
