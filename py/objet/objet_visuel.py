import pygame

from py.graphique.image import Image
from py.graphique.texture_generateur import TextureGenerateur
from py.graphique.builder_image import genere_image
from py.objet.zone import Zone2D, Zone3D


class ObjetVisuel2D(Zone2D):
    """ObjetVisuel est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(
        self,
        coordonnee: list,
        taille: tuple[int, int],
        texture: (
            Image
            | str
            | tuple[str, tuple[int, int]]
            | pygame.Surface
            | TextureGenerateur
        ),
    ):
        Zone2D.__init__(self, coordonnee, taille)
        self._texture = genere_image(texture, taille)

    def afficher(
        self,
        decalage: tuple[int, int] = None,
        surface: pygame.Surface = None,
    ) -> bool:
        """permet de l'affiché sur la sur une surface et de savoir si il est affiché

        Args:
            decalage (tuple[int, int], optional): est le decalage de l'objet. Defaults to None.
            surface (pygame.Surface, optional): est la surface sur laquel afficher. Defaults None.

        Returns:
            bool: si l'objet est affiché
        """
        if decalage is None:
            decalage = (0, 0)
        if surface is None:
            surface = pygame.display.get_surface()
        # Vérifie si l'objet est dans la surface
        pos_surface = (0, 0)
        taille_surface = surface.get_size()
        if self._texture.if_in_zone(pos_surface, (0, 0), taille_surface):
            self._texture.afficher(
                (self.coordonnee[0] + decalage[0], self.coordonnee[1] + decalage[1]),
                surface,
            )
            return True
        return False


class ObjetVisuel3D(Zone3D):
    """ObjetVisuel est une zone qui a pour but d'être affiché
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    LIST_FACE = ("x", "y", "z")

    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int, int],
        face: tuple[
            Image | str | TextureGenerateur | pygame.Surface,
            Image | str | TextureGenerateur | pygame.Surface,
            Image | str | TextureGenerateur | pygame.Surface,
        ],
    ):
        """initialise le bouton"""
        Zone3D.__init__(self, coordonnee, taille)
        taille_face = (
            (taille[1], taille[2]),
            (taille[0], taille[2]),
            (taille[0], taille[1]),
        )
        self.face_graphique = tuple(
            genere_image(face[i], taille_face[i]) for i in range(3)
        )

    def afficher(
        self,
        face: int | str,
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
        if decalage is None:
            decalage = (0, 0)
        if isinstance(face, str):
            face = self.LIST_FACE.index(face)
        match face:
            case 0:
                coordonnee = self.coordonnee[1:3]
            case 1:
                coordonnee = (self.coordonnee[0], self.coordonnee[2])
            case 2:
                coordonnee = self.coordonnee[0:2]
        self.face_graphique[face].afficher(
            (coordonnee[0] + decalage[0], coordonnee[1] + decalage[1]), surface
        )

    def _set_image_list(self, face: tuple[Image, Image, Image]):
        """permet de set la liste des images des faces

        Args:
            face (tuple[Image, Image, Image]): est la liste des images des faces
        """
        self.face_graphique = face

    def afficher_plan(
        self,
        hauteur: int,
        face: int | str,
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

    def ajouter_map(self, map_):
        raise NotImplementedError("Cette méthode n'est pas encore implémentée")
