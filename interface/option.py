"""est le module pour les interfaces graphiques"""

# pylint: disable=no-member disable=no-name-in-module
import os
from block.class_obj import (
    screen,
    pygame,
    ObjetGraphique,
    gener_texture,
    gener_texture_arc_ciel,
    place_texte_in_texture,
)
from class_clavier import Clavier, Souris



class FichierDossier:
    """est un fichier ou un dossier"""

    def __init__(
        self,
        name: str,
        coordonnee: list[int, int],
        type_: str,
        couleur1: tuple[int, int, int],
        couleur2: tuple[int, int, int],
        couleur3: tuple[int, int, int],
        police: str = "monospace",
        taille_police: int = 15,
    ):
        arc_enciel = name in ("cat", "chaton", "chat", "charançon")
        self.visible = True
        self.police = pygame.font.SysFont(police, taille_police)
        self.type = type_
        self.name = name
        self._coordonnee = coordonnee
        self.taille = [125, 50]
        if arc_enciel:
            self.graphique = ObjetGraphique(
                coordonnee,
                [
                    gener_texture_arc_ciel(self.taille),
                    gener_texture_arc_ciel(self.taille, 4),
                ],
            )
            for image in self.graphique.images:
                image = place_texte_in_texture(image, name, self.police, [0, 0, 0])

        else:
            self.graphique = ObjetGraphique(
                coordonnee,
                [
                    gener_texture(self.taille, couleur1),
                    gener_texture(self.taille, couleur1),
                ],
            )
            self.graphique.images[0].blit(
                place_texte_in_texture(
                    gener_texture([self.taille[0] - 10, self.taille[1] - 10], couleur2),
                    name,
                    self.police,
                    [255, 255, 255],
                ),
                (5, 5),
            )
            self.graphique.images[1].blit(
                place_texte_in_texture(
                    gener_texture([self.taille[0] - 10, self.taille[1] - 10], couleur3),
                    name,
                    self.police,
                    [255, 255, 255],
                ),
                (5, 5),
            )

    def get_coordonnee(self):
        """get la coordonnée"""
        return self._coordonnee

    def set_coordonnee(self, value):
        """set la coordonnée"""
        self._coordonnee = value
        self.graphique.set_coordonnee(value)

    def affiche(self):
        """affiche l'objet"""
        self.graphique.afficher()

    def x_y_dans_objet(self, x, y):
        """dit si les coordonnées sont dans l'objet"""
        return self.graphique.x_y_dans_objet(x, y)


class ChoisirLevel:
    """est le menu pour choisir le level"""

    def __init__(
        self, contexte: str = "", police: str = "monospace", police_taille: int = 20
    ):
        self.etat = "encour"
        self.debut_lien = "map/"
        self.suite_lien = []
        self.contexte = contexte
        self.page = 0
        self.page_max = 0
        self.police = pygame.font.SysFont(police, police_taille)
        taille_retour = (90, 110)
        self.retour = ObjetGraphique(
            (0, 0), [gener_texture(taille_retour, (100, 100, 100))]
        )

        self.retour.images: list[pygame.Surface]
        self.retour.images[0].blit(
            place_texte_in_texture(
                gener_texture(
                    (taille_retour[0] - 10, taille_retour[1] - 10), (50, 50, 50)
                ),
                "retour",
                self.police,
                (255, 255, 255),
            ),
            (5, 5),
        )
        taille_home = (90, 110)
        self.home = ObjetGraphique(
            (0, 0), [gener_texture(taille_home, (100, 100, 100))]
        )
        self.home.images[0].blit(
            place_texte_in_texture(
                gener_texture((taille_home[0] - 10, taille_home[1] - 10), (50, 50, 50)),
                "home",
                self.police,
                (255, 255, 255),
            ),
            (5, 5),
        )
        taille_precedent = (60, 80)
        self.precedent = ObjetGraphique(
            (0, 0), [gener_texture(taille_precedent, (100, 100, 100))]
        )
        self.precedent.images: list[pygame.Surface]
        self.precedent.images[0].blit(
            place_texte_in_texture(
                gener_texture(
                    (taille_precedent[0] - 10, taille_precedent[1] - 10), (50, 50, 50)
                ),
                "-",
                self.police,
                (255, 255, 255),
            ),
            (5, 5),
        )
        taille_suivant = (60, 80)
        self.suivant = ObjetGraphique(
            (0, 0), [gener_texture(taille_suivant, (100, 100, 100))]
        )
        self.suivant.images: list[pygame.Surface]
        self.suivant.images[0].blit(
            place_texte_in_texture(
                gener_texture(
                    (taille_suivant[0] - 10, taille_suivant[1] - 10), (50, 50, 50)
                ),
                "+",
                self.police,
                (255, 255, 255),
            ),
            (5, 5),
        )
        taille_graf = (80, 80)
        self.graf_page = ObjetGraphique(
            (0, 0), [gener_texture(taille_graf, (100, 100, 100))]
        )
        self.actualise_element_dossier()

    def actualise_element_dossier(self):
        """actualise les éléments du dossier"""
        suite_lien = ""
        for i in self.suite_lien:
            suite_lien += i
        dossier_os = os.listdir(self.debut_lien + suite_lien)
        # print("355 cat", dossier_os)
        dossiers = []
        for element in dossier_os:
            if os.path.isdir(self.debut_lien + suite_lien + element):
                dossiers.append(element)
        fichiers = []
        for element in dossier_os:
            if (
                os.path.isfile(self.debut_lien + suite_lien + element)
                and len(element) > 4
                and element[-5:] == ".json"
            ):
                fichiers.append(element[:-5])
        # print("364 cat", fichiers, dossiers)
        self.fichier_dossier: list[FichierDossier] = []
        for dossier in dossiers:
            self.fichier_dossier.append(
                FichierDossier(
                    dossier,
                    [0, 0],
                    "dossier",
                    (125, 75, 0),
                    (255, 125, 0),
                    (225, 95, 0),
                )
            )
        for fichier in fichiers:
            self.fichier_dossier.append(
                FichierDossier(
                    fichier,
                    [0, 0],
                    "level",
                    (0, 0, 255),
                    (100, 100, 255),
                    (70, 70, 225),
                )
            )
        self.fichier_dossier: list[FichierDossier]
        self.actualise_possition()

    def actualise_possition(self):
        """actualise la possition des objets"""
        size_screen = screen.get_size()
        limite = [
            (size_screen[0] - 200) // 150,
            (size_screen[1] - 150) // 100,
        ]
        if limite[0] < 1:
            limite[0] = 1
        if limite[1] < 1:
            limite[1] = 1
        # print("374 cat is so cute", self.fichier_dossier)
        self.page_max = len(self.fichier_dossier) // (limite[1] * limite[0]) - (
            0 if len(self.fichier_dossier) % (limite[1] * limite[0]) else 1
        )
        if self.page >= self.page_max:
            self.page = self.page_max
        if self.page < 0:
            self.page = 0
        for i, level_dossier in enumerate(self.fichier_dossier):
            if (
                self.page * limite[1] * limite[0]
                <= i
                < limite[1] * limite[0] + limite[1] * limite[0] * self.page
            ):
                level_dossier.set_coordonnee(
                    [
                        100 + (i % limite[0]) * 150,
                        150 + ((i % (limite[1] * limite[0])) // limite[0]) * 100,
                    ]
                )
                level_dossier.visible = True
            else:
                level_dossier.visible = False
            # print(fichier_dossier.get_coordonnee())
        self.graf_page.images[0].blit(
            place_texte_in_texture(
                gener_texture(
                    (
                        self.graf_page.dimension[0] - 30,
                        self.graf_page.dimension[1] - 30,
                    ),
                    (50, 50, 50),
                ),
                str(self.page + 1),
                self.police,
                (255, 255, 255),
            ),
            (15, 15),
        )
        self.home.set_coordonnee([size_screen[0] - self.home.dimension[0], 0])
        self.graf_page.set_coordonnee(
            [size_screen[0] // 2 - self.graf_page.dimension[0] // 2, 0]
        )
        self.precedent.set_coordonnee(
            [
                size_screen[0] // 2
                - self.precedent.dimension[0]
                - self.graf_page.dimension[0] // 2,
                0,
            ]
        )
        self.suivant.set_coordonnee(
            [
                size_screen[0] // 2
                # + self.suivant.dimension[0]
                + self.graf_page.dimension[0] // 2,
                0,
            ]
        )

    def actualise_animation(self, souris: Souris):
        """actualise les animations de quand la souris passe dessus"""
        pos_sour = souris.get_pos()
        for i, level_dossier in enumerate(self.fichier_dossier):
            # print(fichier_dossier)
            # print(
            #     fichier_dossier.x_y_dans_objet(pos_sour[0], pos_sour[1]),
            #     fichier_dossier.visible,
            # )
            if (
                level_dossier.x_y_dans_objet(pos_sour[0], pos_sour[1])
                and level_dossier.visible
            ):
                self.fichier_dossier[i].graphique.animation = 1
                # print("cat")
            else:
                self.fichier_dossier[i].graphique.animation = 0

    def affiche(self):
        """affiche les objets"""
        self.retour.afficher()
        self.home.afficher()
        self.graf_page.afficher()
        self.precedent.afficher()
        self.suivant.afficher()
        for level_dossier in self.fichier_dossier:
            if level_dossier.visible:
                level_dossier.affiche()

    def clique_sur_chose(self, souris: Souris):
        """actualise les actions quand on clique sur un truc"""
        pos_sour = [souris.get_pos()[0], souris.get_pos()[1]]
        if souris.get_pression("clique_gauche") == "vien_presser":
            if self.retour.x_y_dans_objet(pos_sour[0], pos_sour[1]):
                if len(self.suite_lien) > 0:
                    self.suite_lien.pop()
                    self.actualise_element_dossier()
            if self.precedent.x_y_dans_objet(pos_sour[0], pos_sour[1]):
                if self.page > 0:
                    self.page -= 1

            if self.suivant.x_y_dans_objet(pos_sour[0], pos_sour[1]):
                if self.page < self.page_max:
                    self.page += 1
            if self.home.x_y_dans_objet(pos_sour[0], pos_sour[1]):
                self.etat = "home"

            for level_dossier in self.fichier_dossier:
                if level_dossier.x_y_dans_objet(pos_sour[0], pos_sour[1]):
                    if level_dossier.visible and level_dossier.type == "dossier":
                        self.suite_lien.append(level_dossier.name + "/")
                        self.actualise_element_dossier()
                    elif level_dossier.visible and level_dossier.type == "level":
                        self.etat = "fini"
                        self.suite_lien.append(level_dossier.name + ".json")
                        # print("484cat")


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
            [i[0], ObjetGraphique(i[1], [gener_texture(i[2], (100, 100, 100))])]
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
            else:
                bouton[1].images[0].blit(
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
