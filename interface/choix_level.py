"""est le menu pour choisir le level"""

import os
from graphique import (
    pygame,
    screen,
    ObjetGraphique,
    gener_texture,
    place_texte_in_texture,
    gener_texture_arc_ciel,
)
from class_clavier import Souris


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
