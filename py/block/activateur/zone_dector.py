from typing import TYPE_CHECKING
from py.objet.zone import Zone3D
from py.block.activateur.activateur import Activateur


if TYPE_CHECKING:
    from py.game.map import Map


class TargetDectorZone:
    """classe d'enumération pour les cibles du déctor de zone"""

    POUSSABLE = 2
    NOT_POUSSABLE = -2
    PLAYEUR = 1
    NOT_PLAYEUR = -1


class DectorZone(Zone3D, Activateur):
    """DectorZone est une zone qui a pour but de détecter des objets dans une zone"""

    def __init__(
        self,
        coordonnee: list[int],
        taille: list[int],
        target: list[int],
        detection_mode: str,
        sorti: int | str | tuple[str, int],
    ):
        Zone3D.__init__(self, coordonnee, taille)
        Activateur.__init__(self, sorti)
        self._target: set[int] = set(target)
        self._detection_mode: str = detection_mode

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")

    def methode_dectection(self, zone: Zone3D) -> int:
        """permet de détecter un objet dans la zone"""
        if self._detection_mode == "collision":
            return self.collision_zone(zone)
        elif self._detection_mode == "dans_zone":
            return self.contiens_zone(zone)

    def _dectecter_one(self, list_objet: list[Zone3D]) -> bool:
        """permet de détecter un objet dans la zone"""
        for objet in list_objet:
            if self.methode_dectection(objet):
                return True
        return False

    def _dectecter_all(self, list_objet: list[Zone3D]) -> int:
        """permet de détecter tous les objets dans la zone"""
        count: int = 0
        for objet in list_objet:
            if self.methode_dectection(objet):
                count += 1
        return count

    def get_setarget(self, map_: "Map") -> set[Zone3D]:
        """permet de récupérer la liste des cibles"""
        liste_target: set[Zone3D] = set()
        if TargetDectorZone.PLAYEUR in self._target:
            liste_target.add(map_.get_playeur())
        if TargetDectorZone.POUSSABLE in self._target:
            liste_target = liste_target.union(map_.get_poussable())
        if TargetDectorZone.NOT_PLAYEUR in self._target:
            liste_target.remove(map_.get_playeur())
        if TargetDectorZone.NOT_POUSSABLE in self._target:
            liste_target = liste_target.difference(map_.get_poussable())
        return liste_target

    def ajouter_map(self, map_: "Map") -> None:
        """ajoute la map"""
        Activateur.ajouter_map(self, map_)

    def retirer_map(self, map_):
        Activateur.retirer_map(self, map_)


class DectorZoneCount(DectorZone):
    """DectorZoneCount est une zone qui a pour but de détecter des objets dans une zone
    et de compter le nombre d'objets détectés
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(
        self,
        coordonnee: list[int],
        taille: list[int],
        target: list[int],
        detection_mode: str,
        sorti: str,
    ):
        """initialise le bouton"""
        super().__init__(coordonnee, taille, target, detection_mode, sorti)
        self._sorti = sorti

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        liste_target: set[Zone3D] = self.get_setarget(map_)
        count: int = self._dectecter_all(list(liste_target))
        map_.add_signal((self._sorti, count))

class DectorZoneDifference(DectorZone):
    """DectorZoneDifference est une zone qui a pour but de détecter des objets dans une zone
    et de savoir si le nombre d'objets détectés a changé
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(
        self,
        coordonnee: list[int],
        taille: list[int],
        target: list[int],
        detection_mode: str,
        sorti: int | tuple[str, int],
    ):
        """initialise le bouton"""
        super().__init__(coordonnee, taille, target, detection_mode, sorti)
        self._sorti = sorti
        self._last_count: int = -1

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        liste_target: set[Zone3D] = self.get_setarget(map_)
        count: int = self._dectecter_all(list(liste_target))
        if count != self._last_count:
            map_.add_signal(self._sorti)
            self._last_count = count
