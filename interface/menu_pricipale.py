"""contient la classe MenuPrincipale"""

from graphique import (
    ObjetGraphique,
    gener_texture,
    pygame,
    screen,
)
from class_clavier import Souris
from classbouton import Bouton


class MenuPrincipale:
    """est le menu principale"""

    def __init__(
        self, souris: Souris, police: str = "monospace", taille_police: int = 30
    ):
        self.souris = souris
        self.police = pygame.font.SysFont(police, taille_police)

        self.etat = "en cour"
        self.declage = (0, 0)
        taille_bouton = (200, 50)

        self.fond = ObjetGraphique((0, 0), [gener_texture((300, 280), (50, 50, 125))])
        self._list_bouton: list[Bouton] = [
            Bouton(
                texte,
                (self.fond.dimension[0] // 2 - taille_bouton[0] // 2, 45 + 70 * i),
                taille_bouton,
                [(125, 125, 125), (125, 125, 125)],
                [(125, 125, 125), (100, 100, 100)],
                self.police,
                (255, 255, 255),
            )
            for i, texte in enumerate(
                (
                    ("commencer"),
                    ("option"),
                    ("quitter"),
                )
            )
        ]
        self.actualise_fenetre()

    def actualise_bouton(self):
        """actualise l'ovelay des bouton"""
        pos_sour = self.souris.get_pos()
        for bouton in self._list_bouton:
            if bouton.x_y_dans_objet(
                pos_sour[0] + self.declage[0], pos_sour[1] + self.declage[1]
            ):
                bouton.set_animation(1)
            else:
                bouton.set_animation(0)

    def actualise_fenetre(self):
        """actualise la position des élents de l'interface"""
        dimention = screen.get_size()
        self.declage = [
            -dimention[i] // 2 + self.fond.dimension[i] // 2 for i in range(2)
        ]

    def affiche(self):
        """affiche le menu"""
        self.fond.afficher(self.declage)
        for bouton in self._list_bouton:
            bouton.afficher(self.declage)

    def clique_bouton(self):
        """gère les clique sur les bouton"""
        pos_sour = self.souris.get_pos()
        if self.souris.get_pression("clique_gauche") == "vien_presser":
            for bouton in self._list_bouton:
                if bouton.x_y_dans_objet(
                    pos_sour[0] + self.declage[0], pos_sour[1] + self.declage[1]
                ):
                    self.etat = bouton.get_text()
