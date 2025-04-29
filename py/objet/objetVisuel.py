import pygame

from py.graphique.image import Image
from py.objet.zone import Zone2D, Zone3D

class ObjetVisuel2D(Zone2D):
    """ObjetVisuel est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(self, coordonnee: list, taille: tuple[int, int]):
        super().__init__(coordonnee, taille)

        
    def afficher(
        self,
        decalage: tuple[int, int] = None,
        surface: pygame.Surface = None,
    ):
        """permet de l'affiché sur la sur une surface et de savoir si il est affiché

        Args:
            decalage (tuple[int, int], optional): est le decalage de l'objet. Defaults to None.
            surface (pygame.Surface, optional): est la surface sur laquel afficher. Defaults None.

        Returns:
            bool: si l'objet est affiché
        """
        pass


class ObjetVisuel3D(Zone3D):
    """ObjetVisuel est une zone qui a pour but d'être affiché 
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    LIST_FACE = ("x", "y", "z")

    def __init__(self, coordonnee: list[int], taille: tuple[int, int, int], face: tuple[Image, Image, Image]):
        """initialise le bouton"""
        super().__init__(coordonnee, taille)
        self.face_graphique = face
    
   

    def afficher(
        self,
        face: int|str,
        decalage: tuple[int, int] = None,
        surface: pygame.Surface = None,
    ):
        """permet de l'affiché sur la sur une surface et de savoir si il est affiché

        Args:
            decalage (tuple[int, int], optional): est le decalage de l'objet. Defaults to None.
            surface (pygame.Surface, optional): est la surface sur laquel afficher. Defaults None.

        Returns:
            bool: si l'objet est affiché
        """
        if isinstance(face, str):
            face = self.LIST_FACE.index(face)
        self.face_graphique[face].afficher(decalage, surface)

    
    def afficher_plan(
        self,
        hauteur: int,
        face: int|str,
        decalage: tuple[int, int] = None,
        surface: pygame.Surface = None,
    ):
        """permet de l'affiché sur la sur une surface et de savoir si il est affiché

        Args:
            decalage (tuple[int, int], optional): est le decalage de l'objet. Defaults to None.
            surface (pygame.Surface, optional): est la surface sur laquel afficher. Defaults None.

        Returns:
            bool: si l'objet est affiché
        """
        if isinstance(face, str):
            face = self.LIST_FACE.index(face)
        if self.est_dans_plan(hauteur, face):
            self.afficher(face, decalage, surface)
            
        
