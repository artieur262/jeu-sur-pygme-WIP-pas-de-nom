"""est le jeu"""

# pylint: disable=no-member disable=no-name-in-module


# import save
from block.class_obj import (
    screen,
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

from class_clavier import Clavier  # for typing only

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
