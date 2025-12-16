from typing import TYPE_CHECKING
from py.block.activable.activable import Activable
from py.objet.objetVisuel import ObjetVisuel3D


if TYPE_CHECKING:
    from py.game.map import Map


class Diapo(Activable, ObjetVisuel3D):
    def __init__(self, coordonnee: list[int], taille: tuple[int, int, int], couleur: tuple[int, int, int], entre: int):
        """initialise le diapo"""
        Activable.__init__(self, entre)
        
        for i in face_graphique:
            i.fill(couleur)
        ObjetVisuel3D.__init__(self, coordonnee, taille, face_graphique)
        self.couleur = couleur
        
