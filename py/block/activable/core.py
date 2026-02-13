from typing import TYPE_CHECKING
from py.objet.objet_visuel import ObjetVisuel3D
from py.block.activable.activable import Activable
from py.block.special import Special


if TYPE_CHECKING:
    from py.game.map import Map
    from py.graphique.image import Image
    from py.block.playeur import Playeur


class Core(ObjetVisuel3D):
    """Classe de base pour les blocs du jeu.



    agrs:
        coordonnee (list[int]): La position du bloc dans l'espace 3D.
        taille (list[int]): Les dimensions du bloc.
        texture (tuple[Image, Image, Image]): Les textures appliquées aux faces du bloc.
        transposition (tuple[int, int, int]): La transposition du bloc. {na:-1, x:0, y:1, z:2}
            un indice pour chaque axe (x, y, z).
            ex: (1, 0, -1) indique une transposition
                quand on est sur l'axe x on sera sur la face y,
                quand on est sur l'axe y on sera sur la face x,
                comme l'axe z est à -1 il n'y a pas de transposition sur cet axe.
    """

    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int, int],
        texture: tuple["Image", "Image", "Image"],
        transposition: tuple[int, int, int],
    ):
        super().__init__(coordonnee, taille, texture)
        self.transposition: tuple[int, int, int] = transposition

    def retourner_player(self, map_: "Map"):
        """Permet de retourner la face du joueur en fonction de la transposition.

        Args:
            face (int): La face actuelle du joueur.

        Returns:
            int: La nouvelle face du joueur après transposition.
        """
        plan = map_.get_game().get_plan()
        new_plan = self.transposition[plan]
        player = map_.get_playeur()
        player_center = player.get_center()
        if new_plan != -1 and self.point_dans_objet(player_center):
            player.set_face(new_plan)
            map_.get_game().set_plan(new_plan)

            player.deplacer_on_point(player_center)

    def ajouter_map(self, map_: "Map") -> None:
        """Ajoute l'objet à la map."""
        map_.add_afficher(self)

    def retirer_map(self, map_: "Map") -> None:
        """Retire l'objet de la map."""
        map_.remove_afficher(self)


class CoreActivable(Core, Activable):
    """Ce Core est activable avec de la logique"""

    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int, int],
        texture: tuple["Image", "Image", "Image"],
        entre: int | tuple[str, int] | tuple[str, int, str],
        transposition: tuple[int, int, int],
    ):
        super().__init__(coordonnee, taille, texture, transposition)
        Activable.__init__(self, entre)

    def activation(self, map_):
        """Méthode d'activation spéciale."""
        raise NotImplementedError(
            "Cette méthode doit être implémentée par les sous-classes."
        )

    def ajouter_map(self, map_: "Map") -> None:
        """Ajoute l'objet à la map."""
        Core.ajouter_map(self, map_)
        Activable.ajouter_map(self, map_)

    def retirer_map(self, map_: "Map") -> None:
        """Retire l'objet de la map."""
        Core.retirer_map(self, map_)
        Activable.retirer_map(self, map_)


class CoreSpecial(Core, Special):
    """Ce Core est un élément spécial activable avec les contrôles"""

    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int, int],
        texture: tuple["Image", "Image", "Image"],
        transposition: tuple[int, int, int],
    ):
        super().__init__(coordonnee, taille, texture, transposition)
        Special.__init__(self, (("interaction", 3),))

    def actualiser(self, map_: "Map") -> None:
        """Méthode d'actualisation spéciale."""
        raise NotImplementedError(
            "Cette méthode doit être implémentée par les sous-classes."
        )

    def ajouter_map(self, map_: "Map") -> None:
        """Ajoute l'objet à la map."""
        Core.ajouter_map(self, map_)
        Special.ajouter_map(self, map_)

    def retirer_map(self, map_: "Map") -> None:
        """Retire l'objet de la map."""
        Core.retirer_map(self, map_)
        Special.retirer_map(self, map_)
