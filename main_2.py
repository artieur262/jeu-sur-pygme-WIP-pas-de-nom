"""est le main du jeu"""

# pylint: disable=no-member disable=no-name-in-module
import os

import save
from block.class_obj import (
    screen,
    pygame,
    ObjetGraphique,
    genere_obj,
    vider_affichage,
    gener_texture,
    gener_texture_arc_ciel,
    place_texte_in_texture,
    # for the typing
    Block,
    BlockLumiere,
    BlockCore,
    Interupteur,
    ZoneActive,
    Playeur,
    Logique,
    LogiqueTimer,
)
from class_clavier import Clavier, Souris

# import time


class Game:
    """est le jeu"""

    def __init__(
        self,
        dict_obj: dict[
            str,
            list[
                Logique
                | LogiqueTimer
                | Block
                | Interupteur
                | BlockLumiere
                | Playeur
                | BlockCore
                | ZoneActive
            ],
        ],
        face: str,
        valeur_de_fin: int,
        controle: dict,
        option: dict,
        clavier: Clavier = None,
    ):
        self.etat = "en cour"
        self.dict_obj = dict_obj
        self.face = face  # 0:xy ; 1:xz ; 2:yz
        self.hauteur = 251
        self.clavier = clavier
        self.set_activation = set()
        self.camera = [0, 0]
        self.option = option
        self.valeur_de_fin = valeur_de_fin
        self.controle = controle
        self.dict_obj["playeur"][0].actualise_taille_playeur(face)
        self.actualise_camera()

    def actualise_camera(self):
        """actualise la camera"""
        self.hauteur = self.dict_obj["playeur"][0].get_centre_objet()[2 - self.face]

        camera = self.dict_obj["playeur"][0].get_centre_objet()
        camera.pop(2 - self.face)
        taille = screen.get_size()
        self.camera = [int(camera[i] - taille[i] // 2) for i in range(2)]
        # print(self.camera)

    def affiche_obj(self):
        """affiche les objets"""
        # print(self.dict_obj["playeur"][0]._taille)
        for clee_affichable in (
            "block",
            "interupteur",
            "plaforme",
            "lumière",
            "core",
            "tunel_dimensionel",
            "texte",
            "playeur",
            "zone_acitve",
        ):
            for obj in self.dict_obj[clee_affichable]:
                obj.ajoute_screen(
                    self.face,
                    self.hauteur,
                    self.camera,
                )

    def actualise_obj(self):
        """actualise les objets"""
        for clee_actualisable in ("lumière",):
            for obj in self.dict_obj[clee_actualisable]:
                obj.actualise()
        obj_colision = self.dict_obj["playeur"]
        for obj in self.dict_obj["plaforme"]:
            obj.deplace_chemain(obj_colision)

    def activate(self):
        """active les objets"""
        self.set_activation = set()
        for obj in self.dict_obj["zone_acitve"]:
            # print("cat", obj.collision(self.dict_obj["playeur"][0]))
            if obj.collision(self.dict_obj["playeur"][0]):
                obj.activation()
                obj.memoire_playeur = True
            else:
                obj.memoire_playeur = False

        for clee_activateur in ("interupteur", "logique", "zone_acitve"):
            for obj in self.dict_obj[clee_activateur]:
                obj.activate(self.set_activation)
                obj.actualise()

        for clee_activateur in ("plaforme", "logique", "lumière", "core"):
            for obj in self.dict_obj[clee_activateur]:
                obj.activation(self.set_activation)

        for core in self.dict_obj["core"]:
            core.actualise()
            self.face = core.activate_core(self.face, self.dict_obj["playeur"])

        if self.valeur_de_fin in self.set_activation:
            self.etat = "victoire"

    def depacle_playeur(self):
        """déplace le playeur"""
        obj_colision = (
            self.dict_obj["block"]
            + self.dict_obj["plaforme"]
            + self.dict_obj["interupteur"]
        )
        if self.face == 0:
            if self.clavier.get_pression(self.controle["haut"]) == "presser":
                for playeur in self.dict_obj["playeur"]:
                    playeur.deplace(obj_colision, 1, -3)
            if self.clavier.get_pression(self.controle["bas"]) == "presser":
                for playeur in self.dict_obj["playeur"]:
                    playeur.deplace(obj_colision, 1, 3)
        else:
            if self.clavier.get_pression(self.controle["bas"]) == "presser":
                for playeur in self.dict_obj["playeur"]:
                    playeur.deplace(obj_colision, 2, 3)
            if self.clavier.get_pression(self.controle["haut"]) == "presser":
                for playeur in self.dict_obj["playeur"]:
                    playeur.deplace(obj_colision, 2, -3)

        if self.face == 2:
            if self.clavier.get_pression(self.controle["droite"]) == "presser":
                for playeur in self.dict_obj["playeur"]:
                    playeur.deplace(obj_colision, 1, 3)
            if self.clavier.get_pression(self.controle["gauche"]) == "presser":
                for playeur in self.dict_obj["playeur"]:
                    playeur.deplace(obj_colision, 1, -3)
        else:
            if self.clavier.get_pression(self.controle["droite"]) == "presser":
                for playeur in self.dict_obj["playeur"]:
                    playeur.deplace(obj_colision, 0, 3)
            if self.clavier.get_pression(self.controle["gauche"]) == "presser":
                for playeur in self.dict_obj["playeur"]:
                    playeur.deplace(obj_colision, 0, -3)

        if any(
            obj.collision(self.dict_obj["playeur"][0])
            for obj in self.dict_obj["tunel_dimensionel"]
        ):
            if self.face == 0:
                if self.clavier.get_pression(self.controle["avancer"]) == "presser":
                    playeur = self.dict_obj["playeur"][0]
                    playeur.deplace(obj_colision, 2, -3)
                if self.clavier.get_pression(self.controle["reculer"]) == "presser":
                    playeur = self.dict_obj["playeur"][0]
                    playeur.deplace(obj_colision, 2, 3)
            if self.face == 1:
                if self.clavier.get_pression(self.controle["avancer"]) == "presser":
                    playeur = self.dict_obj["playeur"][0]
                    playeur.deplace(obj_colision, 1, -3)
                if self.clavier.get_pression(self.controle["reculer"]) == "presser":
                    playeur = self.dict_obj["playeur"][0]
                    playeur.deplace(obj_colision, 1, 3)
            if self.face == 2:
                if self.clavier.get_pression(self.controle["avancer"]) == "presser":
                    playeur = self.dict_obj["playeur"][0]
                    playeur.deplace(obj_colision, 0, 3)
                if self.clavier.get_pression(self.controle["reculer"]) == "presser":
                    playeur = self.dict_obj["playeur"][0]
                    playeur.deplace(obj_colision, 0, -3)

    def acvite_block(self):
        """active les block"""
        if self.clavier.get_pression(self.controle["interagir"]) == "vien_presser":
            for joueur in self.dict_obj["playeur"]:
                list_interupteur = self.dict_obj["interupteur"]
                tac = joueur.trouve_obj_autour(list_interupteur)
                # print(tac)
                # print(list_interupteur[0].get_active())
                for i in tac:
                    # print(i)
                    if list_interupteur[i].type in (
                        "levier",
                        "impulsif",
                    ) and list_interupteur[i].in_axe(self.hauteur, 2 - self.face):
                        list_interupteur[i].activation()
                # print(list_interupteur[0].get_active())

        if self.clavier.get_pression(self.controle["interagir"]) == "presser":
            for joueur in self.dict_obj["playeur"]:
                list_interupteur = self.dict_obj["interupteur"]
                tac = joueur.trouve_obj_autour(list_interupteur)
                # print(tac)
                # print(list_interupteur[0].get_active())
                for i in tac:
                    if list_interupteur[i].type == "bouton" and list_interupteur[
                        i
                    ].in_axe(self.hauteur, 2 - self.face):
                        list_interupteur[i].activation()
                # print(list_interupteur[0].get_active())


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
                        place_texte_in_texture(
                            gener_texture(dimension_bouton, (100, 100, 100)),
                            j,
                            self.police_bouton,
                            (255, 255, 255),
                        )
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

    def affiche(self):
        """affiche les objets"""
        self.image_fond.afficher()
        for bouton in self.bouton:
            bouton[1].afficher()

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


def main():
    """est le main"""
    lien_fichier_map = "map/"
    lien_map = "tuto_5.json"  # "tuto_1_troll.json"  # "map_teste.json"  # "tuto_1.json"
    lien_controle = "option/control.json"
    lien_control_default = "option/control_default.json"
    lien_option = "option/option.json"
    lien_option_default = "option/option_default.json"

    controle = save.open_json(lien_controle)
    option = save.open_json(lien_option)
    # rule, map_ = save.open_json(LIEN_FICHIER_MAP + lien_map)
    # controle = save.open_json(lien_controle)
    # map_ = genere_obj(map_)

    clavier = Clavier()
    souris = Souris()
    # jeu = game(map_, rule["face"], rule["valeur_de_fin"], controle, clavier)

    menu_pause = MenuPause()
    selection_level = ChoisirLevel()
    menu_option = SelectOption(controle, option, souris, clavier, {})
    clock = pygame.time.Clock()
    action = (
        "choix_level"  # "choix_level"  # "chargement_map"  # "pause" # "option_demare"
    )
    # monospace = pygame.font.SysFont("monospace", 30)
    pygame.display.set_gamma(200, 200, 200)
    # pygame.display.se
    while action != "fin":
        if action == "home":
            pass
        if action == "option_demare":
            menu_option.set_option(option)
            menu_option.set_control(controle)
            action = "option"
        if action == "option":
            screen.fill((175, 175, 175))
            actualise_event(clavier, souris)
            active_f11(clavier.get_pression("f11"), option)
            menu_option.clique_bouton()
            menu_option.actualise_bouton()
            menu_option.affiche()
            # print(menu_option.indicateur_face)
            pygame.display.update()
            clock.tick(30)
            if menu_option.etat == "anuler":
                if "menu" in menu_option.contexte:
                    action = "menu"
                elif "pause" in menu_option.contexte:
                    action = "pause"
                menu_option.etat = "en cour"
            elif menu_option.etat == "valider":
                # print("cat")
                option = menu_option.get_option()
                controle = menu_option.get_control()
                save.save_json(lien_option, option)
                save.save_json(lien_controle, controle)
                menu_option.etat = "en cour"
                if "menu" in menu_option.contexte:
                    action = "menu"
                elif "pause" in menu_option.contexte:
                    action = "pause"
            elif menu_option.etat == "reset":
                if menu_option.page == "graphique":
                    option = save.open_json(lien_option_default)
                    menu_option.set_option(option["indicateur_face"])
                elif menu_option.page == "controle":
                    controle = save.open_json(lien_control_default)
                    menu_option.set_control(controle)
                    menu_option.actualise_control()
                menu_option.etat = "en cour"

        if action == "choix_level":
            actualise_event(clavier, souris)
            active_f11(clavier.get_pression("f11"), option)
            screen.fill((0, 0, 0))
            selection_level.actualise_possition()
            selection_level.actualise_animation(souris)
            selection_level.clique_sur_chose(souris)
            selection_level.affiche()
            pygame.display.update()
            clock.tick(30)

            if selection_level.etat == "fini":
                lien_map = ""
                for i in selection_level.suite_lien:
                    lien_map += i
                action = "chargement_map"
                selection_level.suite_lien.pop()
        elif action == "chargement_map":
            rule, map_ = save.open_json(lien_fichier_map + lien_map)
            map_ = genere_obj(map_)
            jeu = Game(
                map_, rule["face"], rule["valeur_de_fin"], controle, option, clavier
            )
            action = "enjeu"
        elif action == "enjeu":
            pygame.display.update()
            screen.fill((0, 0, 0))

            actualise_event(clavier, souris)
            clock.tick(60)
            jeu.affiche_obj()
            jeu.depacle_playeur()
            jeu.actualise_obj()
            jeu.acvite_block()
            jeu.actualise_camera()
            jeu.activate()
            if clavier.get_pression(jeu.controle["debug1"]) == "vien_presser":
                print(jeu.dict_obj["playeur"][0].get_coordonnee())
            active_f11(clavier.get_pression("f11"), option)
            # print(jeu.set_activation)
            # print(jeu.etat, jeu.set_activation, jeu.valeur_de_fin)

            if jeu.etat == "victoire":
                vider_affichage()
                ObjetGraphique(
                    [300, 200],
                    [
                        place_texte_in_texture(
                            gener_texture((500, 300), (125, 125, 125)),
                            "vous avez réussi le niveau",
                            pygame.font.SysFont("monospace", 30),
                            (255, 255, 255),
                        ),
                    ],
                ).afficher()
                pygame.display.update()
                # time.sleep(1.5)

            # print(jeu.dict_obj nvhcfdtst["plaforme"][0].active)
            if clavier.get_pression("\x1b") == "vien_presser":
                # "\x1b" = la touche échape
                action = "pause"
                # quit()
        elif action == "pause":
            # print("cat")

            actualise_event(clavier, souris)
            active_f11(clavier.get_pression("f11"), option)
            menu_pause.clique_bouton(souris)
            screen.fill((0, 0, 0))
            jeu.affiche_obj()
            menu_pause.affiche()
            pygame.display.update()
            clock.tick(20)

            if clavier.get_pression("\x1b") == "vien_presser":
                # "\x1b" = la touche échape
                action = "enjeu"
            # print(menu_pause.etat)

            if menu_pause.etat == "quitter":
                quit()
            elif menu_pause.etat == "reprendre":
                action = "enjeu"
            if menu_pause.etat == "option":
                action = "option_demare"
                menu_option.set_contexte({"pause"})
            elif menu_pause.etat == "redémarrer":
                action = "chargement_map"
            elif menu_pause.etat == "level":
                action = "choix_level"
                selection_level.etat = True


main()
