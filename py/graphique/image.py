import pygame

from py.graphique.graphique import screen

class Image:
    """class pour gérer les images
    avec des fonctions pour les afficher et les redimentionner

    agrs:
        texture (str or pygame.Surface) : est l'image
        ancre (tuple[int, int]) : est l'ancre de l'image
    """

    def __init__(self, texture: str | pygame.Surface, ancre: tuple[int, int] = None):
        if ancre is None:
            ancre = (0, 0)
        if isinstance(texture, str):
            texture = pygame.image.load(texture)
            texture.convert()
        self.ancre: tuple[int, int] = ancre
        self.texture: pygame.Surface = texture
    
    def get_texture(self) -> pygame.Surface:
        """get la texture de l'image"""
        return self.texture
    
    def get_ancre(self) -> tuple[int, int]:
        """get l'ancre de l'image"""
        return self.ancre

    def set_ancre(self, ancre: tuple[int, int]) -> None:
        """set l'ancre de l'image"""
        self.ancre = ancre
    
    def get_taille(self) -> tuple[int, int]:
        """get la taille de l'image"""
        return self.texture.get_size()
    
    def redimentione(self, taille: tuple[int, int]):
        """redimentionne l'image"""
        self.texture = pygame.transform.scale(self.texture, taille)
    
    def if_in_zone(self, pos_self: tuple, pos_zone: tuple, size_zone: tuple) -> bool:
        """permet de savoir si l'objet est dans une zone

        Args:
            axe_x (tuple): à une longuer de 2 (le premier est le plus petit)
            axe_y (tuple): à une longuer de 2 (le premier est le plus petit)

        Returns:
            bool: si l'objet
        """
        size_self = self.get_size()
        coin_1_self = [pos_self[0] - self.ancre[0], pos_self[1] - self.ancre[1]]
        coin_2_self = [
            pos_self[0] + size_self[0] - self.ancre[0],
            pos_self[1] + size_self[1] - self.ancre[1],
        ]

        coin_1_zone = pos_zone
        coin_2_zone = [pos_zone[0] + size_zone[0], pos_zone[1] + size_zone[1]]

        return (
            coin_1_zone[0] <= coin_1_self[0] < coin_2_zone[0]
            or coin_1_self[0] <= coin_1_zone[0] < coin_2_self[0]
        ) and (
            coin_1_zone[1] <= coin_1_self[1] < coin_2_zone[1]
            or coin_1_self[1] <= coin_1_zone[1] < coin_2_self[1]
        )

    def afficher(self, position, surface: pygame.Surface = None):
        """affiche l'image sur la fenêtre"""
        if surface is None:
            surface = screen
        if self.if_in_zone(position, self.ancre, surface.get_size()):
            emplacement = (position[0] - self.ancre[0], position[1] - self.ancre[1])
            surface.blit(self.texture, emplacement)

    def ajoute_image(self, image: "Image", position: tuple[int, int]):
        """ajoute une image sur l'image"""
        image.afficher(
            (position[0] + self.ancre[0], position[1] + self.ancre[1]), self.texture
        )


   
    @staticmethod
    def genere_list_Image(entre:list[str|tuple[str|tuple[int,int]]])->list['Image']:        
        if isinstance(entre, list):
            sortie=[]
            for i in entre:
                if isinstance(i, str):
                    sortie.append(Image(i))
                elif isinstance(i, tuple):
                    sortie.append(Image(i[0], i[1]))
                elif isinstance(i, pygame.Surface):
                    sortie.append(Image(i))
                elif isinstance(i, Image):
                    sortie.append(i)
        else:
            raise ValueError("entre doit être une list")
        return sortie
