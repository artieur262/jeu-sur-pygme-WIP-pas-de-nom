"""module qui contient la classe Playeur"""

from .class_block import Block


class Playeur(Block):
    """est le joueur"""

    def __init__(
        self,
        coordonnee: tuple[int, int, int],
        taille: int,
        color: tuple[int, int, int] = None,
        texture: list[str] = None,
    ):
        self._taille_int = taille
        self.vie = "en vie"
        self.etat = "tombe"
        super().__init__(coordonnee, (taille, taille, taille), color, texture=texture)

    def get_taille_int(self) -> int:
        """retourne la taille du joueur"""
        return self._taille_int

    def set_taille_int(self, taille: int, face: int):
        """change la taille du joueur"""
        self._taille_int = taille
        self.actualise_taille_playeur(face)

    def actualise_taille_playeur(self, face: str):
        """actualise la taille du joueur en fonction de la face"""
        if face == 0:
            self._taille = [1, self._taille_int, self._taille_int]
        elif face == 1:
            self._taille = [self._taille_int, 1, self._taille_int]
        elif face == 2:
            self._taille = [self._taille_int, self._taille_int, 1]

        else:
            raise ValueError(f"la face n'est pas reconnu : face = {face}")

    def deplace(self, list_block: list, axe: int, distance: int):
        """fait déplacer le joueur en evitant les colisions
        et change l'état du joueur en fonction de son déplacement
        """
        deplacemment = super().deplace(list_block, axe, distance)
        if axe == 2 and distance > 0:
            self.etat = "par terre" if deplacemment else "tombe"
            # print(f"cat {self.etat}")

        elif axe == 2 and distance < 0:
            self.etat = "saute"

            # print(f"cat {self.etat}")
        return deplacemment

    def convert_save(self) -> dict:
        """Convertit l'état du joueur en un dictionnaire pour sauvegarde.
        """
        sorti = super().convert_save()
        sorti["type"] = "player"
        sorti["taille"] = self._taille_int
        return sorti

    @staticmethod
    def convert_load(dic: dict):
        """Convertit un dictionnaire en un joueur.
        """
        return Playeur(dic["coor"], dic["taille"], dic["color"], texture=dic["texture"])
