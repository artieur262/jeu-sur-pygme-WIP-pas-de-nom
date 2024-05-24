"""Créer un crédit"""

from graphique import (
    gener_texture,
    place_texte_in_texture,
    decoupe_texte,
    pygame,
    screen,
)
from class_clavier import Clavier, Souris
from interface.actualisation_pygame import actualise_event, change_fullscreen


class Credit:
    """Créer un crédit

    agrs:
        texte : str : le texte du crédit
        boucle : bool : si le crédit boucle
    """

    def __init__(self, texte, boucle: bool = True):
        taille_police = 50
        police = pygame.font.SysFont("comicsans", taille_police)
        dimention = (
            1000,
            police.get_height() * len(decoupe_texte(texte, 1000, police)),
        )
        self.texture = gener_texture(dimention, (125, 125, 125, 0))
        self.texture = place_texte_in_texture(
            self.texture, texte, police, (255, 255, 255), "centrage_haut"
        )
        self.position = [0, 0]
        self.scroll = screen.get_size()[1]
        self.encours = True
        self.boucle = boucle

    def place_position(self):
        """place le crédit"""
        self.position = [
            screen.get_width() // 2 - self.texture.get_width() // 2,
            self.scroll,
        ]

    def update(self):
        """update le crédit"""
        self.scroll -= 2
        if self.scroll < -self.texture.get_size()[1]:
            self.scroll = screen.get_size()[1]
            if not self.boucle:
                self.encours = False
        if self.scroll > screen.get_size()[1]:
            self.scroll = -self.texture.get_size()[1]
            if not self.boucle:
                self.encours = False

    def affiche(self):
        """affiche le crédit"""
        screen.blit(self.texture, self.position)

    def reset(self):
        """reset le crédit"""
        self.scroll = screen.get_size()[1]
        self.encours = True

    def play(self, clavier: Clavier, souris: Souris):
        """joue le crédit"""
        clock = pygame.time.Clock()
        while self.encours:
            event = actualise_event(clavier, souris)
            if "quitter" in event or clavier.get_pression("echap") == "vien_presser":
                self.encours = False
            if clavier.get_pression("f11") == "vien_presser":
                change_fullscreen()
            if clavier.get_pression("z") == "presser":
                self.scroll -= 6
            if clavier.get_pression("s") == "presser":
                self.scroll += 8
            if clavier.get_pression("maj gauche") == "presser":
                self.scroll -= 6
            self.place_position()
            self.update()
            clock.tick(60)
            screen.fill((0, 0, 0))
            self.affiche()
            pygame.display.update()
