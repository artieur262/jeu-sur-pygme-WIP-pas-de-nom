"""contient les class de block activateur"""

from .class_block import Block  # , ObjetGraphique, pygame, gener_texture


class Interupteur(Block):
    """class d'un interupteur"""

    def __init__(
        self,
        valeur_activation: int,
        coordonnee: tuple[int, int, int],
        taille: tuple[int, int, int],
        color: tuple[int, int, int] = None,
        type_: str = "bouton",
        texture: list[str] = None,
        # collision_: bool = True,
    ):
        super().__init__(coordonnee, taille, color, texture=texture)
        self.type = type_  #  bouton | impulsif | levier
        self._active = False
        self.valeur_activation = valeur_activation
        # self._collision = collision_

    def get_active(self):
        """return self._active"""
        return self._active

    def actualise(self):
        """reset l'activiter du block"""
        if self.type in ("bouton", "impulsif"):
            self._active = False

    def activation(self):
        """permet d'activer le block"""
        if self.type in ("bouton", "impulsif"):
            self._active = True
        elif self.type == "levier":
            self._active = not self._active

    def activate(self, set_activation: set):
        """active le block"""
        if self._active:
            set_activation.add(self.valeur_activation)

    def convert_save(self) -> dict:
        sorti = super().convert_save()
        sorti["id"] = self.valeur_activation
        sorti["type"] = "interupteur"
        sorti["mode"] = self.type
        # sorti["collision"] = self._collision
        return sorti

    @staticmethod
    def convert_load(dic: dict):
        return Interupteur(
            dic["id"],
            dic["coor"],
            dic["taille"],
            dic["color"],
            dic["mode"],
            texture=dic["texture"],
        )


class ZoneActive(Block):
    """class d'une zone activation"""

    def __init__(
        self,
        valeur_activation: int,
        coordonnee: tuple[int, int, int],
        taille: tuple[int, int, int],
        color: tuple[int, int, int] = None,
        type_: str = "bouton",
        texture: list[str] = None,
        # collision_: bool = True,
    ):
        super().__init__(coordonnee, taille, color, texture=texture)
        self.type = type_
        self._active = False
        self.valeur_activation = valeur_activation
        self.memoire_playeur = False
        # self._collision = collision_

    def get_active(self):
        """return self._active"""
        return self._active

    def actualise(self):
        """reset l'activiter du block"""
        if self.type in ("bouton", "impulsif"):
            self._active = False

    def activation(self):
        """permet d'activer le block"""
        if self.type == "impulsif" and not self.memoire_playeur:
            self._active = True
        if self.type == "bouton":
            self._active = True
        elif self.type == "levier" and not self.memoire_playeur:
            self._active = not self._active

    def activate(self, set_activation: set):
        """active le block"""
        if self._active:
            set_activation.add(self.valeur_activation)

    def convert_save(self) -> dict:
        sorti = super().convert_save()
        sorti["id"] = self.valeur_activation
        sorti["type"] = "zone"
        sorti["mode"] = self.type
        return sorti

    @staticmethod
    def convert_load(dic: dict):
        return ZoneActive(
            dic["id"],
            dic["coor"],
            dic["taille"],
            dic["color"],
            dic["mode"],
            texture=dic["texture"],
        )
