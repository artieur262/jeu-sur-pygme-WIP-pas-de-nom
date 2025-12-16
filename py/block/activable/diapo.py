from typing import TYPE_CHECKING
from py.block.activable.activable import Activable
from py.objet.objet_visuel import ObjetVisuel3D
from py.graphique.image import Image


if TYPE_CHECKING:
    from py.game.map import Map


class Diapo(Activable, ObjetVisuel3D):
    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int, int],
        texture_pack: list[tuple[Image, Image, Image]],
        entre: int,
    ):
        """initialise le diapo"""
        Activable.__init__(self, entre)
        ObjetVisuel3D.__init__(
            self, coordonnee, taille, [img[0] for img in texture_pack]
        )
        self._texture_pack = [
            Image.genere_list_image(texture) for texture in texture_pack
        ]
        self._index_texture = 0
        self.etat_precedent = False

    def ajouter_map(self, map_: "Map") -> None:
        """ajoute la map"""
        map_.add_activable(self)

    def retirer_map(self, map_: "Map") -> None:
        """retire la map"""
        map_.remove_activable(self)

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")

    def actualiser_image(self) -> None:
        """permet de mettre a jour l'image en fonction de l'etat"""
        self._set_image_list(self._texture_pack[self._index_texture])

