from class_block import Block, ObjetGraphique, pygame, gener_texture


class PlateformeMouvante(Block):
    def __init__(
        self,
        coordonnee: tuple[int, int, int],
        taille: tuple[int, int, int],
        id_: int,
        list_trajet_all: list[list[tuple[int, int, int]]] = None,
        color: tuple[int, int, int] = None,
        texture: list[str] = None,
        lethal: bool = False,
    ):
        if list_trajet_all is None:
            list_trajet_all = []
        super().__init__(coordonnee, taille, color, texture=texture)
        self.list_trajet_all = (
            list_trajet_all  # [[(axe,distance,nombre de reption), ...], ...]
        )
        self.lethal = lethal
        self.trajet = 0
        self.pos = 0
        self.repetition = 0
        self.active = False  # revien False à la fin du trajet
        self.sens = 1
        self.ditance_restante = 0
        self._id = id_

    def reset_activite(self):
        """remet l'activité à false"""
        self.active = False

    def get_id(self):
        """return id"""
        return self._id

    def get_nex_action(self):
        """return la prochaine action"""
        return self.list_trajet_all[self.trajet][self.pos]

    def activation(self, set_activation):
        """si l'objet peut etre activer avec l'id"""
        if self._id in set_activation:
            self.active = True

    def deplace(self, list_obj):
        """depace le block"""
        if self.active:
            action = self.get_nex_action()
            if self.ditance_restante == 0:
                # print(action)
                self.ditance_restante = action[1]

            # self.modif_coordonnee(self.ditance_restante, "+", action[0])
            self.ditance_restante = super().deplace(
                list_obj, action[0], self.ditance_restante
            )
            if self.ditance_restante == 0:
                self.repetition += 1
            # else:
            #     print(f"{self.ditance_restante} cat {action[1]}")
            if self.repetition >= action[2]:
                # print("cat")
                self.pos += 1
                self.repetition = 0
            if self.pos >= len(self.list_trajet_all[self.trajet]):
                self.pos = 0
                self.repetition = 0
                self.trajet = (self.trajet + 1) % len(self.list_trajet_all)
                self.active = False

        self.actualise_coord_graph()

    def convert_save(self) -> dict:
        sorti = super().convert_save()
        sorti["type"] = "plaforme"
        sorti["id"] = self._id
        sorti["trajet"] = self.list_trajet_all
        sorti["lethal"] = self.lethal
        return sorti

    @staticmethod
    def convert_load(dic: dict):
        return PlateformeMouvante(
            dic["coor"],
            dic["taille"],
            dic["id"],
            dic["trajet"],
            dic["color"],
            texture=dic["texture"],
            lethal=dic["lethal"],
        )


class Block_lumiere(Block):
    def __init__(
        self,
        coordonnee: tuple[int, int, int],
        taille: tuple[int, int, int],
        list_color: list[tuple[int, int, int]],
        set_id: set[int],
        animation: int = 0,
        texture: list[str] = None,
    ):
        self.animation = animation
        self._list_color = list_color
        self.actualise_color()
        self._set_id = set(set_id)
        self._active = 0
        super().__init__(coordonnee, taille, self._color, texture=texture)

    def actualise_color(self):
        """permet de actualiser"""
        self._color = self._list_color[self.animation]

    def actualise_animation(self):
        """actualise animation"""
        self.animation = self._active
        self.actualise_graphique_animation()

    def genere_graphique(self):
        if self._texure_active:
            self.graphique = (
                ObjetGraphique(
                    (self._coordonnee[:2]),  # xy
                    self._texure,
                    self.animation,
                ),
                ObjetGraphique(
                    (self._coordonnee[0], self._coordonnee[2]),  # xz
                    self._texure,
                    self.animation,
                ),
                ObjetGraphique(
                    (self._coordonnee[1:]),  # yz
                    self._texure,
                    self.animation,
                ),
            )
        else:
            self.graphique = (
                ObjetGraphique(
                    (self._coordonnee[:2]),  # xy
                    [
                        gener_texture(self._taille[:2], color)
                        for color in self._list_color
                    ],
                    self.animation,
                ),
                ObjetGraphique(
                    (self._coordonnee[0], self._coordonnee[2]),  # xz
                    [
                        gener_texture((self._taille[0], self._taille[2]), color)
                        for color in self._list_color
                    ],
                    self.animation,
                ),
                ObjetGraphique(
                    (self._coordonnee[1:]),  # yz
                    [
                        gener_texture(self._taille[1:], color)
                        for color in self._list_color
                    ],
                    self.animation,
                ),
            )

    def actualise(self):
        """reste l'activation"""
        self._active = 0
        self.actualise_animation()

    def activation(self, set_activation: set):
        """permet d'activer le block si l'id correspode à l'une du block"""
        self._active = len(self._set_id & set_activation)
        self.actualise_animation()

    def convert_save(self) -> dict:
        sorti = super().convert_save()
        sorti["type"] = "lumière"
        sorti["id"] = list(self._set_id)
        sorti["color"] = self._list_color
        return sorti

    @staticmethod
    def convert_load(dic: dict):
        return Block_lumiere(
            dic["coor"],
            dic["taille"],
            dic["color"],
            dic["id"],
            texture=dic["texture"],
        )


class Block_core(Block):
    def __init__(
        self,
        coordonnee: tuple[int, int, int],
        taille: tuple[int, int, int],
        id_: int,
        texture: list[str],
        change_face: dict[str],
        tick: int = 60,
    ):
        self.en_cour_active = False
        self.active = False
        self.etat = "en attente"

        self._tick = tick
        self._time = tick
        self.change_face = change_face

        self._id = id_
        super().__init__(coordonnee, taille, (0, 0, 0), texture=texture)
        self.animation = 0

    def actualise(self):
        """actualise le block"""
        # if self.etat != "en attente":
        #     print(self.etat)
        if self.etat == "demarage":
            if self._time <= 0:
                self._time = self._tick
                self.animation = 2
                self.etat = "chargement"
                self.actualise_graphique_animation()

            else:
                self._time -= 1
        elif self.etat == "chargement":
            if self._time <= 0:
                self.etat = "en fonction"
                self._time = self._tick
            else:
                self._time -= 1

        elif self.etat == "dechargement":
            if self._time <= 0:
                self._time = self._tick
                self.animation = 1
                self.etat = "arret"
                self.actualise_graphique_animation()
            else:
                self._time -= 1
        elif self.etat == "arret":
            if self._time <= 0:
                self._time = self._tick
                self.animation = 0
                self.etat = "en attente"
                self.actualise_graphique_animation()
            else:
                self._time -= 1

    def genere_graphique(self):
        if self._texure_active:
            self.graphique = (
                ObjetGraphique(
                    (self._coordonnee[:2]),  # xy
                    self._texure,
                    self.animation,
                ),
                ObjetGraphique(
                    (self._coordonnee[0], self._coordonnee[2]),  # xz
                    self._texure,
                    self.animation,
                ),
                ObjetGraphique(
                    (self._coordonnee[1:]),  # yz
                    self._texure,
                    self.animation,
                ),
            )
            for i, image in enumerate(self.graphique[0].images):
                self.graphique[0].images[i] = pygame.transform.scale(
                    image, self._taille[:2]
                )
            for i, image in enumerate(self.graphique[1].images):
                self.graphique[1].images[i] = pygame.transform.scale(
                    image, (self._taille[0], self._taille[2])
                )
            for i, image in enumerate(self.graphique[2].images):
                self.graphique[2].images[i] = pygame.transform.scale(
                    image, self._taille[1:]
                )

    def activation(self, set_activation: set):
        """permet d'activer le block si l'id correspode à l'une du block"""
        if self._id in set_activation:
            self.etat = "demarage"
            self.animation = 1
            self.actualise_graphique_animation()

    def activate_core(self, face: str, list_playeur: list[Block]):
        if self.etat == "en fonction":
            # print("cat 260", face, self.change_face)
            if str(face) in self.change_face.keys():
                playeur = list_playeur[0]
                # print("cat 270")

                if self.collision(playeur):
                    # print("cat 290")
                    face = int(self.change_face[str(face)])
                    playeur.actualise_taille_playeur(face)
                    # print("cat 280", self.collision(playeur))

                    # print("cat 300")

                    core_cord = self.get_coordonnee()
                    core_tail = self.get_taille()
                    pl_tail = playeur.get_taille()

                    playeur.set_coordonnee(
                        [
                            core_cord[i] + core_tail[i] // 2 - pl_tail[i] // 2
                            for i in range(3)
                        ]
                    )
            self.etat = "dechargement"
            # print(self.etat)

        return face

    def convert_save(self) -> dict:
        sorti = super().convert_save()
        sorti["type"] = "core"
        sorti["id"] = self._id
        sorti["tick"] = self._tick
        sorti["change face"] = self.change_face
        return sorti

    @staticmethod
    def convert_load(dic: dict):
        return Block_core(
            dic["coor"],
            dic["taille"],
            dic["id"],
            dic["texture"],
            dic["change face"],
            dic["tick"],
        )


class Tunel_dimensionel_Brigitte(Block):
    def __init__(
        self,
        coordonnee: tuple[int, int, int],
        taille: tuple[int, int, int],
        color: tuple[int, int, int] = None,
        animation: int = 0,
        texture: list[str] = None,
    ):
        super().__init__(coordonnee, taille, color, animation, texture)

    def convert_save(self) -> dict:
        sorti = super().convert_save()
        sorti["type"] = "tunel_dimensionel"
        return sorti

    @staticmethod
    def convert_load(dic: dict):
        return Tunel_dimensionel_Brigitte(
            dic["coor"],
            dic["taille"],
            dic["color"],
            texture=dic["texture"],
        )
