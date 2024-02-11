"""est le module pour les interfaces graphiques"""

# pylint: disable=no-member disable=no-name-in-module
from classbouton import Bouton
from graphique import (
    screen,
    pygame,
    ObjetGraphique,
    gener_texture,
    place_texte_in_texture,
)
from class_clavier import Clavier, Souris
from interface.actualisation_pygame import (
    actualise_event,
    get_fullscreen,
    change_fullscreen,
)


class ChoixTouche:
    """est le menu pour choisir les touches"""

    def __init__(
        self,
        souris: Souris,
        clavier: Clavier,
        touche: str | None = None,
        police: str = "monospace",
        police_taille_1: int = 20,
        police_taille_2: int = 35,
    ):
        self.etat = "en cour"
        self.touche = touche
        self.police_1 = pygame.font.SysFont(police, police_taille_1)
        self.police_2 = pygame.font.SysFont(police, police_taille_2)
        self.souris = souris
        self.clavier = clavier
        self.fond = ObjetGraphique((0, 0), [gener_texture((450, 350), (200, 200, 200))])

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
                ("anuler", (0, 300), (150, 50)),
                ("valider", (300, 300), (150, 50)),
                ("changer", (150, 300), (150, 50)),
            ]
        ]

        self.graf_touche = ObjetGraphique(
            (0, 0), [gener_texture((450, 200), (100, 100, 100))]
        )
        self.avetissement_changement = ObjetGraphique(
            (0, 0),
            [
                place_texte_in_texture(
                    gener_texture((450, 75), (100, 100, 100, 0)),
                    "appuyer sur une touche\npour la changer la touche",
                    self.police_1,
                    (255, 0, 0),
                )
            ],
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

        self.graf_touche.images[0] = place_texte_in_texture(
            gener_texture((450, 300), (100, 100, 100, 0)),
            str(self.touche),
            self.police_2,
            (0, 0, 0),
        )
        # self.graf_touche.set_coordonnee(centrage)
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
        self.graf_touche.afficher(centrage)
        if self.etat == "changer":
            self.avetissement_changement.afficher(centrage)
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
                    if bouton.get_text() == "anuler":
                        self.etat = "anuler"
                    elif bouton.get_text() == "valider":
                        self.etat = "valider"
                    elif bouton.get_text() == "changer":
                        self.etat = "changer"


def selection_touche(c_t: ChoixTouche):
    """permet de choisir une touche
    et le main de l'interface graphique pour choisir une touche"""
    while c_t.etat in ("en cour", "changer"):
        if c_t.etat == "changer":
            for event in pygame.event.get(pygame.KEYDOWN):
                if event.key in c_t.clavier.alphabet_clee.values():
                    inver_alphabet_clee = {
                        value: key for key, value in c_t.clavier.alphabet_clee.items()
                    }
                    c_t.touche = inver_alphabet_clee[event.key]
                else:
                    c_t.touche = event.key
                c_t.etat = "en cour"
                # cat is so cute
        actualise_event(c_t.clavier, c_t.souris)
        c_t.afficher()
        c_t.actualise_graphique()
        c_t.clique_bouton()
        pygame.display.update()


class SelectOption:
    """est le menu pour choisir les options"""

    def __init__(
        self,
        controle: dict[str, str],
        option: dict,
        souris: Souris,
        clavier: Clavier,
        contexte: set[str] = None,
        police: str = "monospace",
        police_taille: int = 20,
    ):
        if contexte is None:
            contexte = set()

        self.control = controle
        self.option = option
        self.souris = souris
        self.clavier = clavier
        self.police = pygame.font.SysFont(police, police_taille)

        self.touche_selectioner = None
        self.contexte = contexte
        self.page = "graphique"  # "graphique", "controle"
        self.etat = "encour"

        self.list_bouton: list[Bouton] = [
            Bouton(
                i[0],
                i[1],
                i[2],
                [gener_texture(i[2], (125, 125, 125)) for _ in range(2)],
                [(100, 100, 100), (50, 50, 50)],
                self.police,
                (255, 255, 255),
                [i[3], i[4], False],  # [donnee, contexte, visible]
            )
            for i in [
                ("graphique", (50, 0), (150, 50), "page_graphique", "all"),
                ("controle", (200, 0), (150, 50), "page_controle", "all"),
                ("anuler", (0, 0), (150, 50), "anuler", "all"),
                ("valider", (0, 0), (150, 50), "valider", "all"),
                ("reset", (0, 0), (150, 50), "reset", "all"),
            ]  # est la liste pour les boutons
        ]
        for i in [
            ("démarage", (325, 100), (150, 100), "plein_ecran", "graphique"),
            ("activer", (475, 100), (150, 100), "plein_ecran", "graphique"),
            ("couleur", (325, 200), (150, 100), "indicateur_face", "graphique"),
            ("text", (475, 200), (150, 100), "indicateur_face", "graphique"),
        ]:
            self.list_bouton.append(
                Bouton(
                    i[0],
                    i[1],
                    i[2],
                    [gener_texture(i[2], (125, 125, 125)) for _ in range(2)],
                    [(200, 50, 50), (50, 200, 50)],
                    self.police,
                    (255, 255, 255),
                    [i[3], i[4], False],  # [donnee, contexte, visible]
                )
            )

        self.objet_texts: list[str | ObjetGraphique] = [
            [
                ObjetGraphique(
                    i[0],
                    [
                        place_texte_in_texture(
                            gener_texture(i[1], (125, 125, 125)),
                            i[2],
                            self.police,
                            (255, 255, 255),
                        ),
                    ],
                ),
                i[3],
            ]
            for i in [
                [(25, 100), (300, 100), "plein écran", "graphique"],
                [(25, 200), (300, 100), "indicateur de face", "graphique"]
            ]  # est la liste pour les textes
        ]

        for i, key_value in enumerate(self.control.items()):
            self.list_bouton.append(
                Bouton(
                    key_value[1],
                    (175 + 275 * (i % 2), 100 + (i // 2) * 100),
                    (125, 100),
                    [(125, 125, 125), (125, 125, 125)],
                    [(100, 100, 100), (50, 50, 50)],
                    self.police,
                    (255, 255, 255),
                    ["control" + key_value[0], "controle", False],
                    # [donnee, contexte, visible]
                )
            )
            self.objet_texts.append(
                [
                    ObjetGraphique(
                        (25 + 275 * (i % 2), 100 + (i // 2) * 100),
                        [
                            place_texte_in_texture(
                                gener_texture((150, 100), (125, 125, 125)),
                                key_value[0],
                                self.police,
                                (255, 255, 255),
                            ),
                        ],
                    ),
                    "controle",
                ]
            )

        self.actualise_bouton()

    def actualise_control(self):
        """actualise les boutons du type controle"""
        for bouton in self.list_bouton:
            if bouton.donnee[0][:7] == "control":
                bouton.set_text(self.control[bouton.donnee[0][7:]])

    def actualise_bouton(self):
        """actualise l'overlay, la position et la visiblilité des boutons"""
        dimension = screen.get_size()
        pos_sour = self.souris.get_pos()
        for bouton in self.list_bouton:
            # actualise la visibilité des boutons
            if bouton.donnee[1] == self.page or bouton.donnee[1] == "all":
                bouton.donnee[2] = True
            else:
                bouton.donnee[2] = False

            # actualise la position des boutons
            if bouton.donnee[0] == "valider":
                bouton.set_pos([dimension[0] - bouton.get_taille(0), 0])
            elif bouton.donnee[0] == "anuler":
                bouton.set_pos([dimension[0] - bouton.get_taille(0) - 300, 0])
            elif bouton.donnee[0] == "reset":
                bouton.set_pos([dimension[0] - bouton.get_taille(0) - 150, 0])

            # actualise l'animation d'activation des boutons
            elif bouton.donnee[0] == "plein_ecran" and bouton.get_text() == "activer":
                if get_fullscreen():
                    bouton.set_animation(1)
                else:
                    bouton.set_animation(0)
            elif bouton.donnee[0] == "plein_ecran" and bouton.get_text() == "démarage":
                if self.option["plein_écran"]:
                    bouton.set_animation(1)
                else:
                    bouton.set_animation(0)
            elif bouton.donnee[0] == "indicateur_face":
                if bouton.get_text() in self.option["indicateur_face"]:
                    bouton.set_animation(1)
                else:
                    bouton.set_animation(0)

            # actualise l'overlay des boutons
            if (
                bouton.donnee[0]
                in {"page_graphique", "page_controle", "anuler", "valider", "reset"}
                or bouton.donnee[1][0:7] == "control"
            ):
                if bouton.x_y_dans_objet(pos_sour[0], pos_sour[1]):
                    bouton.set_animation(1)
                else:
                    bouton.set_animation(0)

        for objet_text in self.objet_texts:
            # actualise la visibilité des textes
            if objet_text[1] == self.page or objet_text[1] == "all":
                objet_text[0].visible = True
            else:
                objet_text[0].visible = False

    def clique_bouton(self):
        """teste si un bouton est presser et exécute sont action"""
        pos_sour = self.souris.get_pos()
        if self.souris.get_pression("clique_gauche") == "vien_presser":
            for bouton in self.list_bouton:
                if bouton.donnee[2] and bouton.x_y_dans_objet(pos_sour[0], pos_sour[1]):
                    if bouton.donnee[0] == "page_graphique":
                        self.page = "graphique"
                    elif bouton.donnee[0] == "page_controle":
                        self.page = "controle"
                    elif bouton.donnee[0][:7] == "control":
                        # active le menu pour changer la touche
                        self.touche_selectioner = bouton.donnee[0][7:]
                        c_t = ChoixTouche(
                            self.souris,
                            self.clavier,
                            self.control[self.touche_selectioner],
                        )
                        selection_touche(c_t)
                        if c_t.etat == "valider" and c_t.touche is not None:
                            self.control[self.touche_selectioner] = c_t.touche
                            bouton.set_text(c_t.touche)

                        c_t = None  # détruit la variable

                    elif (
                        bouton.donnee[0] == "plein_ecran"
                        and bouton.get_text() == "activer"
                    ):
                        change_fullscreen("vien_presser")
                    elif (
                        bouton.donnee[0] == "plein_ecran"
                        and bouton.get_text() == "démarage"
                    ):
                        self.option["plein_écran"] = not self.option["plein_écran"]
                    elif bouton.donnee[0] == "indicateur_face":

                        if bouton.get_text() in self.option["indicateur_face"]:
                            self.option["indicateur_face"].remove(bouton.get_text())
                        else:
                            self.option["indicateur_face"].append(bouton.get_text())

                    elif bouton.donnee[0] == "anuler":
                        self.etat = "anuler"
                    elif bouton.donnee[0] == "valider":
                        self.etat = "valider"
                    elif bouton.donnee[0] == "reset":
                        self.etat = "reset"

    def affiche(self):
        """affiche l'interface graphique"""
        for bouton in self.list_bouton:
            if bouton.donnee[2]:
                bouton.afficher()
        for objet_text in self.objet_texts:
            if objet_text[0].visible:
                objet_text[0].afficher()

    def set_option(self, value: list[str]):
        """set l'indicateur face"""
        self.option = value

    def get_option(self) -> list[str]:
        """get l'indicateur face"""
        return self.option

    def set_control(self, value: dict[str, str]):
        """set le control"""
        self.control = value

    def get_control(self) -> dict[str, str]:
        """get le control"""
        return self.control

    def set_contexte(self, value: set[str]):
        """set le contexte"""
        self.contexte = value

    def get_contexte(self) -> set[str]:
        """get le contexte"""
        return self.contexte
