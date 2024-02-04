"""contient les block activable"""

from .class_block import Block, ObjetGraphique, gener_texture


class PlateformeMouvante(Block):
    """class d'une plateforme mouvante"""

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

    def deplace_chemain(self, list_obj):
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


class BlockLumiere(Block):
    """class d'un block lumiere"""

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
                    (self._coordonnee[1:]),  # xy
                    self._texure,
                    self.animation,
                ),
                ObjetGraphique(
                    (self._coordonnee[0], self._coordonnee[2]),  # xz
                    self._texure,
                    self.animation,
                ),
                ObjetGraphique(
                    (self._coordonnee[:2]),  # yz
                    self._texure,
                    self.animation,
                ),
            )
        else:
            self.graphique = (
                ObjetGraphique(
                    (self._coordonnee[1:]),  # xy
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
                    (self._coordonnee[:2]),  # yz
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
        return BlockLumiere(
            dic["coor"],
            dic["taille"],
            dic["color"],
            dic["id"],
            texture=dic["texture"],
        )
