import pygame


class TextureGenerateur:

    def __init__(self, algorithme: callable, *args, **kwargs):
        self.algorithme = algorithme
        self.args = args
        self.kwargs = kwargs

    def generer_texture(self, taille: tuple[int, int]) -> pygame.Surface:
        """Génère une texture à partir de l'algorithme donné"""
        return self.algorithme(taille, *self.args, **self.kwargs)


def rectange_avec_bordure(
    taille: tuple[int, int], couleur: tuple[int, int, int], bordure: int
):
    """Génère une texture de bordure"""
    surface = pygame.Surface(taille)
    surface.fill((0, 0, 0))
    pygame.draw.rect(surface, couleur, (0, 0, taille[0], taille[1]), bordure)
    return surface


FONCTIONS = {
    "rectange_avec_bordure": rectange_avec_bordure,
}
