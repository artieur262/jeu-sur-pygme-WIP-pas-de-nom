"""est le jeu"""

# pylint: disable=no-member disable=no-name-in-module


# import save
from graphique import (
    screen,
    gener_texture,
    place_texte_in_texture,
    ObjetGraphique,
    pygame,
)
from block.class_obj import (
    # for the typing
    Block,
    BlockTexte,
    Playeur,
    #
    Interupteur,
    ZoneActive,
    BlockLumiere,
    PlateformeMouvante,
    #
    BlockCore,
    TunelDimensionelBrigitte,
    RedimentioneurPlayer,
    Graviteur,
    #
    Logique,
    LogiqueNot,
    LogiqueTimer,
    LogiqueChangement,
)

from class_clavier import Clavier  # for typing only

# import time


class Game:
    """est le jeu"""

    def __init__(
        self,
        dict_obj: dict[
            str,
            list[
                Block
                | BlockTexte
                | Playeur
                #
                | Interupteur
                | ZoneActive
                | BlockLumiere
                | PlateformeMouvante
                #
                | BlockCore
                | TunelDimensionelBrigitte
                | RedimentioneurPlayer
                | Graviteur
                #
                | Logique
                | LogiqueNot
                | LogiqueTimer
                | LogiqueChangement
            ],
        ],
        face: str,
        valeur_de_fin: int,
        valeur_mort: int,
        controle: dict,
        option: dict,
        clavier: Clavier = None,
        police: str = "monospace",
        taille_police: int = 30,
    ):
        self.etat = "en cour"
        self.dict_obj = dict_obj
        self.face = face  # 0:yz ; 1:xz ; 2:xy
        self.hauteur = 251
        self.clavier = clavier
        self.set_activation = set()
        self.camera = [0, 0]
        self.option = option
        self.valeur_de_fin = valeur_de_fin
        self.valeur_mort = valeur_mort
        self.police = pygame.font.SysFont(police, taille_police)
        self.controle = controle
        self.dict_obj["playeur"][0].actualise_taille_playeur(face)
        self.actualise_camera()
        dimentions = screen.get_size()
        self.face_texte = ObjetGraphique(
            (0, 0), [gener_texture((150, 50), (125, 125, 125)) for _ in range(3)]
        )
        for i, text in enumerate(("face:yz", "face:xz", "face:xy")):
            self.face_texte.images[i].blit(
                place_texte_in_texture(
                    gener_texture(
                        (
                            self.face_texte.dimension[0] - 10,
                            self.face_texte.dimension[1] - 10,
                        ),
                        (50, 50, 50),
                    ),
                    text,
                    self.police,
                    (255, 255, 255),
                ),
                (5, 5),
            )

        largeur_contour = 15
        self.contour: list[ObjetGraphique] = []
        for i in [
            ((255, 0, 0), (0, 0, 255), (largeur_contour, dimentions[1]), (0, 0)),
            (
                (255, 0, 0),
                (0, 0, 255),
                (largeur_contour, dimentions[1]),
                (dimentions[0] - largeur_contour, 0),
            ),
            ((0, 0, 255), (0, 255, 0), (dimentions[0], largeur_contour), (0, 0)),
            (
                (0, 0, 255),
                (0, 255, 0),
                (dimentions[0], largeur_contour),
                (0, dimentions[1] - largeur_contour),
            ),
        ]:
            self.contour.append(
                ObjetGraphique(
                    i[3],
                    [
                        gener_texture(i[2], i[0]),
                        gener_texture(i[2], i[1]),
                    ],
                )
            )
        self.coin = [
            ObjetGraphique(
                i, [gener_texture((largeur_contour, largeur_contour), (255, 255, 255))]
            )
            for i in (
                (0, 0),
                (dimentions[0] - largeur_contour, 0),
                (0, dimentions[1] - largeur_contour),
                (dimentions[0] - largeur_contour, dimentions[1] - largeur_contour),
            )
        ]
        self.actualise_fenetre()
        self.actualise_face()

    def set_option(self, option: dict):
        """change les option"""
        self.option = option

    def set_controle(self, controle: dict):
        """change les controle"""
        self.controle = controle

    def actualise_fenetre(self):
        """actualise les contours"""
        largeur_contour = 15
        dimentions = screen.get_size()
        for obj in zip(
            self.contour,
            (
                (0, 0),
                (dimentions[0] - largeur_contour, 0),
                (0, 0),
                (0, dimentions[1] - largeur_contour),
            ),
            (
                (largeur_contour, dimentions[1]),
                (largeur_contour, dimentions[1]),
                (dimentions[0], largeur_contour),
                (dimentions[0], largeur_contour),
            ),
        ):
            obj[0].coordonnee = obj[1]
            obj[0].redimentione_all_image(obj[2])

        for coin in zip(
            self.coin,
            (
                (0, 0),
                (dimentions[0] - largeur_contour, 0),
                (0, dimentions[1] - largeur_contour),
                (dimentions[0] - largeur_contour, dimentions[1] - largeur_contour),
            ),
        ):
            coin[0].coordonnee = coin[1]
        self.face_texte.coordonnee = (
            dimentions[0] // 2 - self.face_texte.dimension[0] // 2,
            0,
        )

    def actualise_face(self):
        """actualise la face"""
        self.face_texte.animation = self.face
        if self.face == 0:
            self.contour[0].animation = 1
            self.contour[1].animation = 1
            self.contour[2].animation = 1
            self.contour[3].animation = 1

        elif self.face == 1:
            self.contour[0].animation = 0
            self.contour[1].animation = 0
            self.contour[2].animation = 1
            self.contour[3].animation = 1

        else:
            self.contour[0].animation = 0
            self.contour[1].animation = 0
            self.contour[2].animation = 0
            self.contour[3].animation = 0

    def actualise_camera(self, surface: pygame.Surface = None):
        """actualise la camera"""
        if surface is None:
            surface = screen
        taille = surface.get_size()

        self.hauteur = self.dict_obj["playeur"][0].get_centre_objet()[self.face]
        camera = self.dict_obj["playeur"][0].get_centre_objet()
        camera.pop(self.face)
        self.camera = [int(camera[i] - taille[i] // 2) for i in range(2)]
        # print(self.camera)

    def affiche_obj(self, surface: pygame.Surface = None):
        """affiche les objets"""
        # print(self.dict_obj["playeur"][0]._taille)
        if surface is None:
            surface = screen
        for clee_affichable in (
            "block",
            "interupteur",
            "plaforme",
            "lumière",
            "core",
            "redimentioneur",
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
                    surface=surface,
                )
        if "couleur" in self.option["indicateur_face"]:
            for obj in self.contour:
                obj.afficher(surface=surface)
            for obj in self.coin:
                obj.afficher(surface=surface)
        if "text" in self.option["indicateur_face"]:
            self.face_texte.afficher(surface=surface)

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

        for clee_activateur in (
            "plaforme",
            "logique",
            "lumière",
            "core",
            "redimentioneur",
        ):
            for obj in self.dict_obj[clee_activateur]:
                obj.activation(self.set_activation)

        for core in self.dict_obj["core"]:
            core.actualise()
            self.face = core.activate_core(self.face, self.dict_obj["playeur"])
        for redimentioneur in self.dict_obj["redimentioneur"]:
            redimentioneur.activate_redimentioneur(self.dict_obj["playeur"], self.face)
            redimentioneur.actualise()
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

        if self.face == 2:
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

        if any(
            obj.collision(self.dict_obj["playeur"][0])
            for obj in self.dict_obj["tunel_dimensionel"]
        ):

            if self.face == 0:
                if self.clavier.get_pression(self.controle["avancer"]) == "presser":
                    playeur = self.dict_obj["playeur"][0]
                    playeur.deplace(obj_colision, 0, 3)
                if self.clavier.get_pression(self.controle["reculer"]) == "presser":
                    playeur = self.dict_obj["playeur"][0]
                    playeur.deplace(obj_colision, 0, -3)
            elif self.face == 1:
                if self.clavier.get_pression(self.controle["avancer"]) == "presser":
                    playeur = self.dict_obj["playeur"][0]
                    playeur.deplace(obj_colision, 1, -3)
                if self.clavier.get_pression(self.controle["reculer"]) == "presser":
                    playeur = self.dict_obj["playeur"][0]
                    playeur.deplace(obj_colision, 1, 3)

            elif self.face == 2:
                if self.clavier.get_pression(self.controle["avancer"]) == "presser":
                    playeur = self.dict_obj["playeur"][0]
                    playeur.deplace(obj_colision, 2, -3)
                if self.clavier.get_pression(self.controle["reculer"]) == "presser":
                    playeur = self.dict_obj["playeur"][0]
                    playeur.deplace(obj_colision, 2, 3)

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
                    ) and list_interupteur[i].in_axe(self.hauteur, self.face):
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
                    ].in_axe(self.hauteur, self.face):
                        list_interupteur[i].activation()
                # print(list_interupteur[0].get_active())
