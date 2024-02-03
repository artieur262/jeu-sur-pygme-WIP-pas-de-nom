"""module qui contient la classe BlockTexte"""

from .class_block import Block, pygame, place_texte_in_texture


class BlockTexte(Block):
    """est un block qui affiche du texte"""

    def __init__(
        self,
        coordonnee: tuple[int, int, int],
        taille: tuple[int, int, int],
        color: tuple[int, int, int],
        texte_color: tuple[int, int, int],
        texte,
        police: pygame.font.Font,
        taille_police: int,
        animation: int = 0,
        texture=None,
    ):
        self._police_name = police
        self._police = pygame.font.SysFont(self._police_name, taille_police)
        self._texte = texte
        self._texte_color = texte_color
        super().__init__(
            coordonnee,
            taille,
            color,
            animation,
            texture,
        )

    def genere_graphique(self):
        super().genere_graphique()
        for face_graphique in self.graphique:
            for image in face_graphique.images:
                place_texte_in_texture(
                    image, self._texte, self._police, self._texte_color
                )

    def convert_save(self) -> dict:
        sortie = super().convert_save()
        sortie["type"] = "texte"
        sortie["texte"] = self._texte
        sortie["texte_color"] = self._texte_color
        sortie["police_name"] = self._police_name
        sortie["police_taille"] = self._police.get_height()
        return sortie

    @staticmethod
    def convert_load(dic: dict):
        return BlockTexte(
            dic["coor"],
            dic["taille"],
            dic["color"],
            dic["texte_color"],
            dic["texte"],
            dic["police_name"],
            dic["police_taille"],
            texture=dic["texture"],
        )
