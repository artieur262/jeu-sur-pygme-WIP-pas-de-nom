from typing import TYPE_CHECKING

from py.block.activable.activable import Activable
from py.objet.objet_unicolor import ObjetUnicolor3D

if TYPE_CHECKING:
    from py.game.map import Map


class PlatformeMouvantee(ObjetUnicolor3D, Activable):
    """PlatformeMouvante est une zone qui a pour but de se deplacer
    Args:
        coordonnee (list[int]): est la coordonnee de l'objet graphique
        taille (tuple[int, int, int]): est la taille de l'objet graphique
        couleur (tuple[int, int, int]): est la couleur de l'objet graphique
        entre (int | tuple[str, int] | tuple[str, int, str]): est l'entree logique de la plateforme
    """

    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int, int],
        couleur: tuple[int, int, int],
        entre: int | tuple[str, int] | tuple[str, int, str],
    ):
        """initialise le bouton"""
        ObjetUnicolor3D.__init__(self, coordonnee, taille, couleur)
        Activable.__init__(self, entre)
        self._active: bool = False

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        self._active = map_.in_signal(self._entre)
        self.mouvoir(map_)

    def ajouter_map(self, map_: "Map") -> None:
        Activable.ajouter_map(self, map_)
        map_.add_colision(self)
        map_.add_afficher(self)

    def retirer_map(self, map_: "Map") -> None:
        Activable.retirer_map(self, map_)
        map_.remove_afficher(self)
        map_.remove_colision(self)

    def arriver_fin(self):
        """permet de definir le comportement de la plateforme a la fin du deplacement"""
        pass  # pylint: disable=unnecessary-pass
        # a definir en fonction de la plateforme

    def mouvoir(self, map_: "Map") -> None:
        """permet de deplacer la plateforme"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")
        # a definir en fonction de la plateforme


class PlatformeMouvanteeOnGo(PlatformeMouvantee):
    """PlatformeMouvanteOnGo est une zone qui a pour but de se deplacer
    quand elle est active
    Args:
        coordonnee (list[int]): est la coordonnee de l'objet graphique
        taille (tuple[int, int, int]): est la taille de l'objet graphique
        couleur (tuple[int, int, int]): est la couleur de l'objet graphique
        parcour (list[tuple[int, int, int]]): est la liste de deplacement de la plateforme
            tuple[int, int, int] : est le mouvement dans un axe
                tuple[0] : est l'axe de mouvement (0, 1 ou 2)
                tuple[1] : est la vitesse de mouvement
                tuple[2] : est la distance de mouvement
        entre (int | tuple[str, int] | tuple[str, int, str]): est l'entree logique de la plateforme
    """

    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int, int],
        couleur: tuple[int, int, int],
        parcour: list[tuple[int, int, int]],
        entre: int | tuple[str, int] | tuple[str, int, str],
    ):
        """initialise le bouton"""
        PlatformeMouvantee.__init__(self, coordonnee, taille, couleur, entre)
        self._parcour: list[tuple[int, int, int]] = parcour
        self._distance_parcourue: int = 0

        if len(self._parcour) == 0:
            self._index_parcour = -2
        else:
            self._index_parcour: int = 0

    def mouvoir(self, map_: "Map") -> None:
        """permet de deplacer la plateforme"""
        if self._active and self._index_parcour != -2:
            if self._index_parcour >= len(self._parcour):
                return None
            axe, vitesse, distance = self._parcour[self._index_parcour]
            vitesse = min(abs(vitesse), abs(distance) - self._distance_parcourue) * (
                1 if vitesse > 0 else -1
            )
            effectuer = self.deplacer_in_axe(
                axe, vitesse, map_.get_colision(), map_.get_poussable()
            )
            self._distance_parcourue += abs(effectuer)
            if self._distance_parcourue >= abs(distance):
                self._distance_parcourue = 0
                self._index_parcour += 1
                if self._index_parcour >= len(self._parcour):
                    self.arriver_fin()


class PlatformeMouvanteeOnGoOffRetour(PlatformeMouvanteeOnGo):
    """PlatformeMouvanteOnGoOffRetour est une zone qui a pour but de se deplacer
    quand elle est active et de revenir a sa position initiale quand elle est desactive
    Args:
        coordonnee (list[int]): est la coordonnee de l'objet graphique
        taille (tuple[int, int, int]): est la taille de l'objet graphique
        couleur (tuple[int, int, int]): est la couleur de l'objet graphique
        parcour (list[tuple[int, int, int]]): est la liste de deplacement de la plateforme
            tuple[int, int, int] : est le mouvement dans un axe
                tuple[0] : est l'axe de mouvement (0, 1 ou 2)
                tuple[1] : est la vitesse de mouvement
                tuple[2] : est la distance de mouvement
        entre (int | tuple[str, int] | tuple[str, int, str]): est l'entree logique de la plateforme
    """

    def mouvoir(self, map_: "Map") -> None:
        super().mouvoir(map_)
        if not self._active and self._index_parcour < 0:
            axe, vitesse, distance = self._parcour[self._index_parcour]
            vitesse = min(abs(vitesse), abs(distance) - self._distance_parcourue) * (
                -1 if vitesse > 0 else 1
            )
            effectuer = self.deplacer_in_axe(
                axe, vitesse, map_.get_colision(), map_.get_poussable()
            )
            self._distance_parcourue += abs(effectuer)
            if self._distance_parcourue >= abs(distance):
                self._distance_parcourue = 0
                self._index_parcour -= 1
                if self._index_parcour < 0:
                    self.arriver_fin()
