from block.class_obj import *
import save
import os
from class_clavier import Clavier, Souris
import time


class game:
    def __init__(
        self,
        dict_obj: dict[
            str,
            list[
                Logique
                | Logique_Timer
                | Block
                | Interupteur
                | Block_lumiere
                | Playeur
                | Block_core
                | Zone_acitve
            ],
        ],
        face: str,
        valeur_de_fin: int,
        controle: dict,
        clavier: Clavier = None,
    ):
        self.etat = "en cour"
        self.dict_obj = dict_obj
        self.face = face  # 0:xy ; 1:xz ; 2:yz
        self.hauteur = 251
        self.clavier = clavier
        self.set_activation = set()

        self.valeur_de_fin = valeur_de_fin
        self.controle = controle
        self.dict_obj["playeur"][0].actualise_taille_playeur(face)
        self.actualise_camera()

    def actualise_camera(self):
        self.hauteur = self.dict_obj["playeur"][0].get_centre_objet()[2 - self.face]

        camera = self.dict_obj["playeur"][0].get_centre_objet()
        camera.pop(2 - self.face)
        taille = screen.get_size()
        self.camera = [int(camera[i] - taille[i] // 2) for i in range(2)]
        # print(self.camera)

    def affiche_obj(self):
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
        for clee_actualisable in ("lumière",):
            for obj in self.dict_obj[clee_actualisable]:
                obj.actualise()
        obj_colision = self.dict_obj["playeur"]
        for obj in self.dict_obj["plaforme"]:
            obj.deplace(obj_colision)

    def activate(self):
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


class Menu_pause:
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
                ("reprendre", "level", "redémarrer", "option (WIP)", "quitter")
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
        self.image_fond.afficher()
        for bouton in self.bouton:
            bouton[1].afficher()

    def clique_bouton(self, souris: Souris):
        self.etat = "null"
        sour_pos = souris.get_pos()
        # print(souris.get_pression("clique_gauche"))
        if souris.get_pression("clique_gauche") == "vien_presser":
            # print("cat :", sour_pos)
            for bouton in self.bouton:
                if bouton[1].x_y_dans_objet(sour_pos[0], sour_pos[1]):
                    self.etat = bouton[0]


class fichier_dossier:
    def __init__(
        self,
        name: str,
        coordonnee: list[int, int],
        type: str,
        couleur1: tuple[int, int, int],
        couleur2: tuple[int, int, int],
        couleur3: tuple[int, int, int],
        police: str = "monospace",
        taille_police: int = 15,
    ):
        arc_enciel = name in ("cat", "chaton", "chat", "charançon")
        self.visible = True
        self.police = pygame.font.SysFont(police, taille_police)
        self.type = type
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
        return self._coordonnee

    def set_coordonnee(self, value):
        self._coordonnee = value
        self.graphique.set_coordonnee(value)

    def affiche(self):
        self.graphique.afficher()

    def x_y_dans_objet(self, x, y):
        return self.graphique.x_y_dans_objet(x, y)


class choisir_level:
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
        self.fichier_dossier: list[fichier_dossier] = []
        for dossier in dossiers:
            self.fichier_dossier.append(
                fichier_dossier(
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
                fichier_dossier(
                    fichier,
                    [0, 0],
                    "level",
                    (0, 0, 255),
                    (100, 100, 255),
                    (70, 70, 225),
                )
            )
        self.fichier_dossier: list[fichier_dossier]
        self.actualise_possition()

    def actualise_possition(self):
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
        for i, fichier_dossier in enumerate(self.fichier_dossier):
            if (
                self.page * limite[1] * limite[0]
                <= i
                < limite[1] * limite[0] + limite[1] * limite[0] * self.page
            ):
                fichier_dossier.set_coordonnee(
                    [
                        100 + (i % limite[0]) * 150,
                        150 + ((i % (limite[1] * limite[0])) // limite[0]) * 100,
                    ]
                )
                fichier_dossier.visible = True
            else:
                fichier_dossier.visible = False
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
        pos_sour = souris.get_pos()
        for i, fichier_dossier in enumerate(self.fichier_dossier):
            # print(fichier_dossier)
            # print(
            #     fichier_dossier.x_y_dans_objet(pos_sour[0], pos_sour[1]),
            #     fichier_dossier.visible,
            # )
            if (
                fichier_dossier.x_y_dans_objet(pos_sour[0], pos_sour[1])
                and fichier_dossier.visible
            ):
                self.fichier_dossier[i].graphique.animation = 1
                # print("cat")
            else:
                self.fichier_dossier[i].graphique.animation = 0

    def affiche(self):
        self.retour.afficher()
        self.home.afficher()
        self.graf_page.afficher()
        self.precedent.afficher()
        self.suivant.afficher()
        for fichier_dossier in self.fichier_dossier:
            if fichier_dossier.visible:
                fichier_dossier.affiche()

    def clique_sur_chose(self, souris: Souris):
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

            for fichier_dossier in self.fichier_dossier:
                if fichier_dossier.x_y_dans_objet(pos_sour[0], pos_sour[1]):
                    if fichier_dossier.visible and fichier_dossier.type == "dossier":
                        self.suite_lien.append(fichier_dossier.name + "/")
                        self.actualise_element_dossier()
                    elif fichier_dossier.visible and fichier_dossier.type == "level":
                        self.etat = "fini"
                        self.suite_lien.append(fichier_dossier.name + ".json")
                        # print("484cat")


def actualise_event(clavier: Clavier, souris: Souris):
    souris.actualise_position()
    souris.actualise_all_clique()
    clavier.actualise_all_touche()
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:  # pylint: disable=no-member
            # cat[event.unicode] = event.key
            # print(event)
            if event.key in clavier.dict_touches:
                clavier.change_pression(event.key, "vien_lacher")

        elif event.type == pygame.KEYDOWN:  # pylint: disable=no-member
            # print(event)
            if event.key in clavier.dict_touches:
                clavier.change_pression(event.key, "vien_presser")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in souris.dict_clique:
                souris.change_pression(event.button, "vien_presser")

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button in souris.dict_clique:
                souris.change_pression(event.button, "vien_lacher")


def active_f11(touche_f11: str):
    global screen
    if touche_f11 == "vien_presser":
        if screen.get_flags() & pygame.FULLSCREEN:
            screen = pygame.display.set_mode((1200, 600), pygame.RESIZABLE)
            screen = pygame.display.set_mode((1200, 600), pygame.RESIZABLE)
        else:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # pygame.display.update()


def main():
    LIEN_FICHIER_MAP = "map/"
    lien_map = "tuto_5.json"  # "tuto_1_troll.json"  # "map_teste.json"  # "tuto_1.json"
    lien_controle = "control.json"
    # save.save_json(lien_controle,{"droite": "d", "gauche": "q", "haut": "z", "bas": "s", "interagir": "y"},)

    # rule, map_ = save.open_json(LIEN_FICHIER_MAP + lien_map)
    # controle = save.open_json(lien_controle)
    # map_ = genere_obj(map_)

    clavier = Clavier()
    souris = Souris()
    # jeu = game(map_, rule["face"], rule["valeur_de_fin"], controle, clavier)
    menu_pause = Menu_pause()
    selection_level = choisir_level()

    clock = pygame.time.Clock()
    action = "choix_level"  # "choix_level"  # "chargement_map"  # "pause"
    # monospace = pygame.font.SysFont("monospace", 30)
    pygame.display.set_gamma(200, 200, 200)
    # pygame.display.se
    while action != "fin":
        if action == "choix_level":
            actualise_event(clavier, souris)
            active_f11(clavier.get_pression("f11"))
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
            rule, map_ = save.open_json(LIEN_FICHIER_MAP + lien_map)
            controle = save.open_json(lien_controle)
            map_ = genere_obj(map_)
            jeu = game(map_, rule["face"], rule["valeur_de_fin"], controle, clavier)
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
            active_f11(clavier.get_pression("f11"))
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
            active_f11(clavier.get_pression("f11"))
            menu_pause.clique_bouton(souris)
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
            elif menu_pause.etat == "redémarrer":
                action = "chargement_map"
            elif menu_pause.etat == "level":
                action = "choix_level"
                selection_level.etat = True


main()
