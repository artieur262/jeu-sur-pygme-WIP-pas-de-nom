""""""

# pylint: disable=no-member
from interface.actualisation_pygame import actualise_event
from graphique import (
    ObjetGraphique,
    pygame,
    gener_texture,
    place_texte_in_texture,
    screen,
)

from class_clavier import Clavier, Souris
from classbouton import Bouton


class YesOrNot:
    """est le menu pour choisir les touches"""

    def __init__(
        self,
        souris: Souris,
        clavier: Clavier,
        texte: str,
        police: str = "monospace",
        police_taille_1: int = 20,
        police_taille_2: int = 35,
    ):
        self.etat = "en cour"
        self.police_1 = pygame.font.SysFont(police, police_taille_1)
        self.police_2 = pygame.font.SysFont(police, police_taille_2)
        self.souris = souris
        self.clavier = clavier
        self.fond = ObjetGraphique((0, 0), [gener_texture((450, 350), (175, 175, 175))])
        self.texte_str = texte
        self.list_bouton: list[Bouton] = [
            Bouton(
                i[0],
                i[1],
                i[2],
                [gener_texture(i[2], (100, 100, 100)) for _ in range(2)],
                [(100, 100, 100), (50, 50, 50)],
                self.police_1,
                (255, 255, 255),
            )
            for i in [
                ("Oui", (0, 300), (225, 50)),
                ("Non", (225, 300), (225, 50)),
            ]
        ]

        self.texte_obj = ObjetGraphique(
            (0, 0), [gener_texture((450, 200), (100, 100, 100))]
        )
        self.texte_obj.images[0] = place_texte_in_texture(
            gener_texture((450, 300), (0, 0, 0, 0)),
            str(self.texte_str),
            self.police_2,
            (0, 0, 0),
        )
        self.actualise_graphique()

    def actualise_graphique(self):
        """actualise l'overlay des boutons et des images"""
        centrage = [
            screen.get_size()[i] // 2
            - self.fond.dimension[i]
            + self.fond.dimension[i] // 2
            for i in range(2)
        ]
        self.souris.get_pos()
        pos_sour = self.souris.get_pos()
        pos_sour_decale = [pos_sour[i] - centrage[i] for i in range(2)]

        for bouton in self.list_bouton:
            if bouton.x_y_dans_objet(pos_sour_decale[0], pos_sour_decale[1]):
                bouton.set_animation(1)
            else:
                bouton.set_animation(0)

    def afficher(self):
        """affiche les objets"""
        centrage = [
            -screen.get_size()[i] // 2 + self.fond.dimension[i] // 2 for i in range(2)
        ]
        self.fond.afficher(centrage)
        self.texte_obj.afficher(centrage)
        for bouton in self.list_bouton:
            bouton.afficher(centrage)

    def clique_bouton(self):
        """actuatise les actions quand on clique sur un truc"""
        if self.souris.get_pression("clique_gauche") == "vien_presser":
            pos_sour = self.souris.get_pos()
            pos_sour_decale = [
                pos_sour[i] - screen.get_size()[i] // 2 + self.fond.dimension[i] // 2
                for i in range(2)
            ]
            for bouton in self.list_bouton:
                if bouton.x_y_dans_objet(pos_sour_decale[0], pos_sour_decale[1]):
                    if bouton.get_text() == "Oui":
                        self.etat = "oui"
                    elif bouton.get_text() == "Non":
                        self.etat = "non"


def selection_oui_non(
    text: str, touche_oui: str | int = None, touche_non: str | int = None
) -> bool:
    """permet de choisir une touche
    et le main de l'interface graphique pour choisir une touche"""
    clock = pygame.time.Clock()
    y_or_n = YesOrNot(Souris(), Clavier(), text)
    while y_or_n.etat in ("en cour"):
        if (
            touche_oui is not None
            and y_or_n.clavier.get_pression(touche_oui) == "vien_presser"
        ):
            y_or_n.etat = "oui"
        elif (
            touche_non is not None
            and y_or_n.clavier.get_pression(touche_non) == "vien_presser"
        ):
            y_or_n.etat = "non"
        actualise_event(y_or_n.clavier, y_or_n.souris)
        clock.tick(30)
        y_or_n.afficher()
        y_or_n.actualise_graphique()
        y_or_n.clique_bouton()
        pygame.display.update()

    return y_or_n.etat == "oui"
