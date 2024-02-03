"""module de block special"""

from .class_block import Block, ObjetGraphique, pygame
from .playeur import Playeur  # for the typing


class BlockCore(Block):
    """class d'un block core"""

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
        """permet d'activer le core"""
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
        return BlockCore(
            dic["coor"],
            dic["taille"],
            dic["id"],
            dic["texture"],
            dic["change face"],
            dic["tick"],
        )


class TunelDimensionelBrigitte(Block):
    """class d'un tunel dimensionel"""

    # def __init__(
    #     self,
    #     coordonnee: tuple[int, int, int],
    #     taille: tuple[int, int, int],
    #     color: tuple[int, int, int] = None,
    #     animation: int = 0,
    #     texture: list[str] = None,
    # ):
    #     super().__init__(coordonnee, taille, color, animation, texture)

    def convert_save(self) -> dict:
        sorti = super().convert_save()
        sorti["type"] = "tunel_dimensionel"
        return sorti

    @staticmethod
    def convert_load(dic: dict):
        return TunelDimensionelBrigitte(
            dic["coor"],
            dic["taille"],
            dic["color"],
            texture=dic["texture"],
        )


class RedimentioneurPlayer(Block):
    """class d'un redimentioneur de playeur"""

    def __init__(
        self,
        coordonnee: tuple[int, int, int],
        taille: tuple[int, int, int],
        dict_taille: dict[int, int],
        id_activation: int,
        color: tuple[int, int, int] = None,
        animation: int = 0,
        texture: list[str] = None,
    ):
        self.active = False
        self._id = id_activation
        self.dict_taille = dict_taille
        super().__init__(coordonnee, taille, color, animation, texture)

    def actualise(self):
        """actualise le block"""
        self.active = False

    def activation(self, set_activation: set):
        """permet d'activer le block si l'id correspode à l'une du block"""
        if self._id in set_activation:
            self.active = True

    def activate_redimentioneur(self, playeur: Playeur, face: int):
        """permet de changer la taille du playeur"""
        if self.active:
            playeur.set_taille_int(self.dict_taille[face], face)

    def convert_save(self) -> dict:
        sorti = super().convert_save()
        sorti["type"] = "redimentioneur"
        sorti["dict_taille"] = self.dict_taille
        sorti["id_activation"] = self._id
        return sorti

    @staticmethod
    def convert_load(dic: dict):
        return RedimentioneurPlayer(
            dic["coor"],
            dic["taille"],
            {int(key): value for key, value in dic["dict_taille"].items()},
            dic["color"],
            texture=dic["texture"],
        )


class Graviteur(Block):
    """permet de changer la graviter du jeu"""

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
        """convertie le block en dictionnaire"""
        sorti = super().convert_save()
        sorti["type"] = "graviteur"
        return sorti

    @staticmethod
    def convert_load(dic: dict):
        """convertie un dictionnaire en block"""
        return Graviteur(
            dic["coor"],
            dic["taille"],
            dic["color"],
            texture=dic["texture"],
        )
