"""contient la classe MenuPrincipale"""

from graphique import (
    ObjetGraphique,
    gener_texture,
    place_texte_in_texture,
    pygame,
    screen,
)
from class_clavier import Souris


class MenuPrincipale:
    """est le menu principale"""

    def __init__(
        self, souris: Souris, police: str = "monospace", taille_police: int = 30
    ):
        self.police = pygame.font.SysFont(police, taille_police)
        self.etat = "en cour"
        self.souris = souris
        taille_bouton = (200, 50)
        self.declage = (0, 0)
        self.fond = ObjetGraphique((0, 0), [gener_texture((300, 280), (50, 50, 125))])
        self._list_bouton: list[tuple[int, ObjetGraphique]] = [
            (
                texte,
                ObjetGraphique(
                    (self.fond.dimension[0] // 2 - taille_bouton[0] // 2, 45 + 70 * i),
                    [gener_texture(taille_bouton, (125, 125, 125)) for _ in range(2)],
                ),
            )
            for i, texte in enumerate(
                (
                    "commencer",
                    "option",
                    "quitter",
                )
            )
        ]
        for bouton in self._list_bouton:
            for i, couleur in enumerate(((125, 125, 125), (100, 100, 100))):
                bouton[1].images[i].blit(
                    place_texte_in_texture(
                        gener_texture(
                            (
                                bouton[1].dimension[0] - 10,
                                bouton[1].dimension[1] - 10,
                            ),
                            couleur,
                        ),
                        bouton[0],
                        self.police,
                        (255, 255, 255),
                    ),
                    (5, 5),
                )
            self.actualise_fenetre()

    def actualise_bouton(self):
        """actualise le menu"""
        pos_sour = self.souris.get_pos()
        for bouton in self._list_bouton:
            if bouton[1].x_y_dans_objet(
                pos_sour[0] + self.declage[0], pos_sour[1] + self.declage[1]
            ):
                bouton[1].animation = 1
            else:
                bouton[1].animation = 0

    def actualise_fenetre(self):
        """actualise la fenetre"""
        dimention = screen.get_size()
        self.declage = [
            -dimention[i] // 2 + self.fond.dimension[i] // 2 for i in range(2)
        ]

    def affiche(self):
        """affiche le menu"""
        self.fond.afficher(self.declage)
        for bouton in self._list_bouton:
            bouton[1].afficher(self.declage)

    def clique_bouton(self):
        """clique sur un bouton"""
        pos_sour = self.souris.get_pos()
        if self.souris.get_pression("clique_gauche") == "vien_presser":
            for bouton in self._list_bouton:
                if bouton[1].x_y_dans_objet(
                    pos_sour[0] + self.declage[0], pos_sour[1] + self.declage[1]
                ):
                    self.etat = bouton[0]
