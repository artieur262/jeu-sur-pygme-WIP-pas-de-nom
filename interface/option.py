"""est le module pour les interfaces graphiques"""

# pylint: disable=no-member disable=no-name-in-module

from block.class_obj import (
    screen,
    pygame,
    ObjetGraphique,
    gener_texture,
    place_texte_in_texture,
)
from class_clavier import Clavier, Souris


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
        self.list_bouton: list[str | ObjetGraphique] = [
            [
                i[0],
                ObjetGraphique(
                    i[1], [gener_texture(i[2], (100, 100, 100)) for _ in range(2)]
                ),
            ]
            for i in [
                ("anuler", (0, 300), (150, 50)),
                ("valider", (300, 300), (150, 50)),
                ("changer", (150, 300), (150, 50)),
            ]
        ]
        for bouton in self.list_bouton:
            bouton[1].images[0].blit(
                place_texte_in_texture(
                    gener_texture(
                        (bouton[1].dimension[0] - 10, bouton[1].dimension[1] - 10),
                        (75, 75, 75),
                    ),
                    bouton[0],
                    self.police_1,
                    (255, 255, 255),
                ),
                (5, 5),
            )

            bouton[1].images[1].blit(
                place_texte_in_texture(
                    gener_texture(
                        (bouton[1].dimension[0] - 10, bouton[1].dimension[1] - 10),
                        (50, 50, 50),
                    ),
                    bouton[0],
                    self.police_1,
                    (255, 255, 255),
                ),
                (5, 5),
            )

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
        """actualise les boutons"""
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
            if bouton[1].x_y_dans_objet(pos_sour_decale[0], pos_sour_decale[1]):
                bouton[1].animation = 1
            else:
                bouton[1].animation = 0

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
            bouton[1].afficher(centrage)

    def clique_bouton(self):
        """actuatise les actions quand on clique sur un truc"""
        if self.souris.get_pression("clique_gauche") == "vien_presser":
            pos_sour = self.souris.get_pos()
            pos_sour_decale = [
                pos_sour[i] - screen.get_size()[i] // 2 + self.fond.dimension[i] // 2
                for i in range(2)
            ]
            for bouton in self.list_bouton:
                if bouton[1].x_y_dans_objet(pos_sour_decale[0], pos_sour_decale[1]):
                    if bouton[0] == "anuler":
                        self.etat = "anuler"
                    elif bouton[0] == "valider":
                        self.etat = "valider"
                    elif bouton[0] == "changer":
                        self.etat = "changer"


def selection_touche(c_t: ChoixTouche):
    """permet de choisir une touche"""
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
        contexte: set[str],
        police: str = "monospace",
        police_taille: int = 20,
    ):
        self.touche_selectioner = None
        self.clavier = clavier
        self.souris = souris
        self.contexte = contexte
        self.page = "graphique"  # "graphique", "controle"
        self.police = pygame.font.SysFont(police, police_taille)
        self.etat = "encour"
        # print(option)
        self.option = option
        self.control = controle
        self.list_bouton = [
            [
                i[0],
                ObjetGraphique(
                    i[1],
                    [gener_texture(i[2], (125, 125, 125))],
                ),
                i[3],
                i[4],
            ]
            for i in [
                (
                    "couleur",
                    (325, 100),
                    (150, 100),
                    "indicateur_face_couleur",
                    "graphique",
                ),
                ("text", (475, 100), (150, 100), "indicateur_face_text", "graphique"),
                ("activer", (325, 200), (150, 100), "plein_ecran", "graphique"),
                ("graphique", (50, 0), (150, 50), "page_graphique", "all"),
                ("controle", (200, 0), (150, 50), "page_controle", "all"),
                ("anuler", (0, 0), (150, 50), "anuler", "all"),
                ("valider", (0, 0), (150, 50), "valider", "all"),
                ("reset", (0, 0), (150, 50), "reset", "all"),
            ]
        ]
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
                [(25, 100), (300, 100), "indicateur de face", "graphique"],
                [(25, 200), (300, 100), "plein écran", "graphique"],
            ]
        ]
        self.list_bouton: list[list[str | ObjetGraphique]]
        for i, key_value in enumerate(self.control.items()):
            self.list_bouton.append(
                [
                    key_value[1],
                    ObjetGraphique(
                        (175 + 275 * (i % 2), 100 + (i // 2) * 100),
                        [gener_texture((125, 100), (125, 125, 125))],
                    ),
                    "control" + key_value[0],
                    "controle",
                ]
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
        """actualise les controles et les touches"""
        for bouton in self.list_bouton:
            if bouton[2][0:7] == "control":
                bouton[0] = self.control[bouton[2][7:]]

    def actualise_bouton(self):
        """actualise les boutons"""
        dimension = screen.get_size()
        pos_sour = self.souris.get_pos()
        for bouton in self.list_bouton:
            if bouton[3] == self.page or bouton[3] == "all":
                bouton[1].visible = True
            else:
                bouton[1].visible = False
            if bouton[2] == "valider":
                bouton[1].set_coordonnee([dimension[0] - bouton[1].dimension[0], 0])
            elif bouton[2] == "anuler":
                bouton[1].set_coordonnee(
                    [dimension[0] - bouton[1].dimension[0] - 300, 0]
                )
            elif bouton[2] == "reset":
                bouton[1].set_coordonnee(
                    [dimension[0] - bouton[1].dimension[0] - 150, 0]
                )

            if bouton[2] == "plein_ecran":
                if self.option["plein_écran"]:
                    bouton[1].images[0].blit(
                        place_texte_in_texture(
                            gener_texture(
                                (
                                    bouton[1].dimension[0] - 10,
                                    bouton[1].dimension[1] - 10,
                                ),
                                (50, 200, 50),
                            ),
                            bouton[0],
                            self.police,
                            (255, 255, 255),
                        ),
                        (5, 5),
                    )
                else:
                    bouton[1].images[0].blit(
                        place_texte_in_texture(
                            gener_texture(
                                (
                                    bouton[1].dimension[0] - 10,
                                    bouton[1].dimension[1] - 10,
                                ),
                                (200, 50, 50),
                            ),
                            bouton[0],
                            self.police,
                            (255, 255, 255),
                        ),
                        (5, 5),
                    )
            if bouton[2] in {
                "indicateur_face_text",
                "indicateur_face_couleur",
            }:

                if bouton[0] in self.option["indicateur_face"]:
                    bouton[1].images[0].blit(
                        place_texte_in_texture(
                            gener_texture(
                                (
                                    bouton[1].dimension[0] - 10,
                                    bouton[1].dimension[1] - 10,
                                ),
                                (50, 200, 50),
                            ),
                            bouton[0],
                            self.police,
                            (255, 255, 255),
                        ),
                        (5, 5),
                    )
                else:
                    bouton[1].images[0].blit(
                        place_texte_in_texture(
                            gener_texture(
                                (
                                    bouton[1].dimension[0] - 10,
                                    bouton[1].dimension[1] - 10,
                                ),
                                (200, 50, 50),
                            ),
                            bouton[0],
                            self.police,
                            (255, 255, 255),
                        ),
                        (5, 5),
                    )
            elif (
                bouton[2]
                in {"page_graphique", "page_controle", "anuler", "valider", "reset"}
                or bouton[2][0:7] == "control"
            ):
                if bouton[1].x_y_dans_objet(pos_sour[0], pos_sour[1]):
                    bouton[1].images[0].blit(
                        place_texte_in_texture(
                            gener_texture(
                                (
                                    bouton[1].dimension[0] - 10,
                                    bouton[1].dimension[1] - 10,
                                ),
                                (50, 50, 50),
                            ),
                            bouton[0],
                            self.police,
                            (255, 255, 255),
                        ),
                        (5, 5),
                    )
                else:
                    bouton[1].images[0].blit(
                        place_texte_in_texture(
                            gener_texture(
                                (
                                    bouton[1].dimension[0] - 10,
                                    bouton[1].dimension[1] - 10,
                                ),
                                (100, 100, 100),
                            ),
                            bouton[0],
                            self.police,
                            (255, 255, 255),
                        ),
                        (5, 5),
                    )

        for objet_text in self.objet_texts:
            if objet_text[1] == self.page or objet_text[1] == "all":
                objet_text[0].visible = True
            else:
                objet_text[0].visible = False

    def clique_bouton(self):
        """teste si un bouton est presser et exécute sont action"""
        pos_sour = self.souris.get_pos()
        if self.souris.get_pression("clique_gauche") == "vien_presser":
            for bouton in self.list_bouton:
                if bouton[1].visible and bouton[1].x_y_dans_objet(
                    pos_sour[0], pos_sour[1]
                ):
                    if bouton[2] == "indicateur_face_couleur":
                        if bouton[0] in self.option["indicateur_face"]:
                            self.option["indicateur_face"].remove(bouton[0])
                        else:
                            self.option["indicateur_face"].append(bouton[0])

                    elif bouton[2] == "indicateur_face_text":
                        if bouton[0] in self.option["indicateur_face"]:
                            self.option["indicateur_face"].remove(bouton[0])
                        else:
                            self.option["indicateur_face"].append(bouton[0])

                    elif bouton[2] == "page_graphique":
                        self.page = "graphique"
                    elif bouton[2] == "page_controle":
                        self.page = "controle"
                    elif bouton[2][0:7] == "control":
                        self.touche_selectioner = bouton[2][7:]
                        c_t = ChoixTouche(
                            self.souris,
                            self.clavier,
                            self.control[self.touche_selectioner],
                        )
                        selection_touche(c_t)
                        if c_t.etat == "valider" and c_t.touche is not None:
                            self.control[self.touche_selectioner] = c_t.touche
                            bouton[0] = c_t.touche
                        c_t = None  # détruit la variable
                    elif bouton[2] == "plein_ecran":
                        active_f11("vien_presser", self.option)

                    elif bouton[2] == "anuler":
                        self.etat = "anuler"
                    elif bouton[2] == "valider":
                        self.etat = "valider"
                    elif bouton[2] == "reset":
                        self.etat = "reset"

    def affiche(self):
        """affiche l'interface graphique"""
        for bouton in self.list_bouton:
            if bouton[1].visible:
                bouton[1].afficher()
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


def actualise_event(clavier: Clavier, souris: Souris):
    """actualise les événement"""
    souris.actualise_position()
    souris.actualise_all_clique()
    clavier.actualise_all_touche()
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            # cat[event.unicode] = event.key
            # print(event)
            if event.key in clavier.dict_touches:
                clavier.change_pression(event.key, "vien_lacher")

        elif event.type == pygame.KEYDOWN:
            # print(event)
            if event.key in clavier.dict_touches:
                clavier.change_pression(event.key, "vien_presser")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in souris.dict_clique:
                souris.change_pression(event.button, "vien_presser")

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button in souris.dict_clique:
                souris.change_pression(event.button, "vien_lacher")


def active_f11(touche_f11: str, option: dict):
    """active le mode plein écran"""
    global screen  # pylint: disable=global-statement
    if touche_f11 == "vien_presser":
        if screen.get_flags() & pygame.FULLSCREEN:
            screen = pygame.display.set_mode((1200, 600), pygame.RESIZABLE)
            screen = pygame.display.set_mode((1200, 600), pygame.RESIZABLE)
            # pour une raison inconnue il faut le faire deux fois
            option["plein_écran"] = False
        else:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            option["plein_écran"] = True
        # pygame.display.update()
