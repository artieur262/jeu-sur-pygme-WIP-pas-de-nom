"""module contenant la classe Bouton"""

from graphique import ObjetGraphique, gener_texture, place_texte_in_texture, pygame


class Bouton:
    """est un bouton"""

    def __init__(
        self,
        texte: str,
        position: tuple[int, int],
        taille: tuple[int, int],
        texture: list[tuple[int, int, int] | str | pygame.Surface],
        couleur_interieur: list[tuple[int, int, int]],
        police: pygame.font.Font,
        couleur_texte: tuple[int, int, int],
        donnee=None,
    ):
        self.donnee = donnee
        self._pos = position
        self._texte = texte
        self._texture = texture
        self._taille = taille
        self._couleur_interieur = couleur_interieur
        self.police = police
        self.couleur_texte = couleur_texte
        self.genere_texture()

    def genere_texture(self):
        """genere les textures du bouton"""
        self.objet = ObjetGraphique(
            self._pos,
            [
                (gener_texture(self._taille, i) if isinstance(i, tuple | list) else i)
                for i in self._texture
            ],
        )
        self.objet.redimentione_all_image(self._taille)
        for image, couleur in zip(self.objet.images, self._couleur_interieur):
            image.blit(
                place_texte_in_texture(
                    gener_texture(
                        (self._taille[0] - 10, self._taille[1] - 10), couleur
                    ),
                    str(self._texte),
                    self.police,
                    self.couleur_texte,
                ),
                (5, 5),
            )

    def set_animation(self, animation: int):
        """set l'animation du bouton"""
        self.objet.animation = animation

    def get_text(self) -> str:
        """get le texte du bouton"""
        return self._texte

    def set_text(self, value: str):
        """set le texte du bouton"""
        self._texte = value
        self.genere_texture()

    def get_pos(self) -> tuple[int, int]:
        """get la position du bouton"""
        return self._pos

    def set_pos(self, value: tuple[int, int]):
        """set la position du bouton"""
        self._pos = value
        self.objet.set_coordonnee(value)

    def get_taille(self, idex=None) -> tuple[int, int]:
        """get la taille du bouton"""
        if idex is None:
            return self._taille
        else:
            return self._taille[idex]

    def set_taille(self, value: tuple[int, int]):
        """set la taille du bouton"""
        self._taille = value
        self.genere_texture()

    def x_y_dans_objet(self, x, y):
        """teste si un point est dans le bouton"""
        return self.objet.x_y_dans_objet(x, y)

    def afficher(
        self,
        decalage: list[int] = None,
        debut: list[int] = None,
        taille: tuple[int, int] = None,
    ):
        """affiche le bouton"""
        self.objet.afficher(decalage, debut, taille)
