"""module pour le menu pause"""

from graphique import ObjetGraphique, gener_texture, place_texte_in_texture, pygame
from class_clavier import Souris


class MenuPause:
    """est le menu pause"""

    def __init__(
        self,
        contexte: str = "nul",
        police: str = "monospace",
        taile_police_bouton: int = 20,
        taile_police_titre: int = 30,
    ):
        self.etat = "null"
        self.contexte = contexte
        self.police_titre = pygame.font.SysFont(police, taile_police_titre)
        self.police_bouton = pygame.font.SysFont(police, taile_police_bouton)
        dimension_fond = (310, 580)
        self.image_fond = ObjetGraphique(
            (0, 0),
            [gener_texture(dimension_fond, (100, 100, 100))],
        )

        self.image_fond.images[0].blit(
            gener_texture(
                (dimension_fond[0] - 10, dimension_fond[1] - 10), (50, 50, 50)
            ),
            (5, 5),
        )
        dimension_bouton = (250, 75)
        self.image_fond.images[0].blit(
            place_texte_in_texture(
                gener_texture((dimension_fond[0], 75), (50, 50, 50, 0)),
                "pause",
                self.police_titre,
                [255, 255, 255],
            ),
            (0, 0),
        )

        self.bouton: list[list[str | ObjetGraphique]] = [
            [
                j,
                ObjetGraphique(
                    [
                        dimension_fond[0] // 2 - dimension_bouton[0] // 2,
                        75 + i * 100,
                    ],
                    [
                        gener_texture(dimension_bouton, (100, 100, 100))
                        for _ in range(2)
                    ],
                ),
            ]
            for i, j in enumerate(
                ("reprendre", "level", "redémarrer", "option", "quitter")
            )
        ]

        for bouton in self.bouton:
            bouton[1].images[0].blit(
                place_texte_in_texture(
                    gener_texture(
                        (dimension_bouton[0] - 10, dimension_bouton[1] - 10),
                        (50, 50, 50),
                    ),
                    bouton[0],
                    self.police_bouton,
                    (255, 255, 255),
                ),
                (5, 5),
            )
            bouton[1].images[1].blit(
                place_texte_in_texture(
                    gener_texture(
                        (dimension_bouton[0] - 10, dimension_bouton[1] - 10),
                        (25, 25, 25),
                    ),
                    bouton[0],
                    self.police_bouton,
                    (255, 255, 255),
                ),
                (5, 5),
            )

    def affiche(self):
        """affiche les objets"""
        self.image_fond.afficher()
        for bouton in self.bouton:
            bouton[1].afficher()

    def actualise_bouton(self, souris: Souris):
        """actualise les bouton"""
        pos_sour = souris.get_pos()
        for bouton in self.bouton:
            if bouton[1].x_y_dans_objet(pos_sour[0], pos_sour[1]):
                bouton[1].animation = 1
            else:
                bouton[1].animation = 0

    def clique_bouton(self, souris: Souris):
        """actualise les actions quand on clique sur un truc"""
        self.etat = "null"
        sour_pos = souris.get_pos()
        # print(souris.get_pression("clique_gauche"))
        if souris.get_pression("clique_gauche") == "vien_presser":
            # print("cat :", sour_pos)
            for bouton in self.bouton:
                if bouton[1].x_y_dans_objet(sour_pos[0], sour_pos[1]):
                    self.etat = bouton[0]
