import pygame

from py.objet.objetVisuel import ObjetVisuel2D
from py.graphique.image import Image

class ObjetGraphique(ObjetVisuel2D):
    """Objet graphique est une zone qui a une image et un texte
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(
        self,
        coordonnee: list,
        textures: list[str | pygame.Surface | Image | tuple[str|tuple[int,int]]],
        taille: tuple[int, int],
        animation: int = 0,
    ):
        self.texture : list[Image] = []
        for i in textures:
            if isinstance(i, Image):
                self.texture.append(i)
            else:
                textures.append(Image(i))
        super().__init__(coordonnee, taille)
        self.animation = animation

    def image_actuel(self) -> Image:
        """get la texture de l'objet graphique"""
        return self.texture[self.animation]
    
    def get_animation(self) -> int:
        """get l'animation de l'objet graphique"""
        return self.animation
    
    def set_animation(self, animation: int) -> None:
        """set l'animation de l'objet graphique"""
        self.animation = animation

    def imgage_dans_surface(self, pos_surface:tuple[int,int], taille_surface:tuple[int,int]) -> bool:
        """permet de savoir si l'image est dans une surface"""
        return self.image_actuel().if_in_zone(pos_surface, (0, 0), taille_surface)
    
    def redimentione_all_image(self, taille: tuple[int]):
        """redimentionne toute les images"""
        for image in self.texture:
            image.redimentione(taille)


    def afficher(
        self,
        decalage: tuple[int, int] = None,
        surface: pygame.Surface = None,
    ) -> bool:
        """permet de l'affiché sur la sur une surface et de savoir si il est affiché

        Args:
            decalage (tuple[int, int], optional): est le decalage de l'objet. Defaults to None.
            surface (pygame.Surface, optional): est la surface sur laquel afficher. Defaults None.

        if la surface est None alors c'est directement sur l'écran
        """
        if decalage is None:
            decalage = (0, 0)
        # print(self.animation)
        if self.imgage_dans_surface(decalage, surface.get_size()):
            self.texture[self.animation].afficher(
                (self.coordonnee[0] - decalage[0], self.coordonnee[1] - decalage[1]),
                surface,
            )
            return True
        return False
    

    



    