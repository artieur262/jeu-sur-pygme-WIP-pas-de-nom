"""Bouton est un objet graphique qui a une image et un texte

class :
    Bouton(ObjetGraphique): Bouton est un objet graphique qui a une image et un texte
    Args:
        ObjetGraphique (ObjetGraphique): est l'objet graphique

"""

from typing import TYPE_CHECKING
from py.graphique.objetGraphique import ObjetGraphique
from py.graphique.graphique import place_texte_in_texture
from py.interface.element_it import ElementInterface


if TYPE_CHECKING:
    import pygame


class Bouton(ObjetGraphique, ElementInterface):
    """Bouton est un objet graphique qui a une image et un texte
    Args:
        ObjetGraphique (ObjetGraphique): est l'objet graphique
    """

    def __init__(
        self,
        coordonnee: list,
        textures: list[str],
        taille: tuple[int, int],
        mode: str = "clique",
        parent: ElementInterface = None,
        action: callable = None,
    ):
        """initialise le bouton"""
        ObjetGraphique.__init__(self, coordonnee, textures, taille)
        ElementInterface.__init__(self, coordonnee, taille, False, parent)
        self.mode = mode
        self.action = action
        self.__actif = False
        self.__clique = False
        self.__survol = False

    def actualise_taille(self):
        pass

    def get_mode(self) -> str:
        """get le mode du bouton"""
        return self.mode

    def set_actif(self, actif: bool) -> None:
        """set l'etat actif du bouton"""
        self.__actif = actif
        self.actualise_animation()

    def get_actif(self) -> bool:
        """get l'etat actif du bouton"""
        return self.__actif

    def actualise_animation(self) -> None:
        """actualise l'animation du bouton"""
        match self.mode:
            case "on/off":
                if self.__actif:
                    if self.__survol:
                        self.set_animation(3)
                    else:
                        self.set_animation(2)
                elif self.__survol:
                    self.set_animation(1)
                else:
                    self.set_animation(0)
            case "clique":
                if self.__survol:
                    self.set_animation(1)
                else:
                    self.set_animation(0)

    def cliquer(self, pos: tuple[int, int]) -> bool:
        """permet de savoir si le bouton est cliqué"""
        self.__clique = self.point_dans_objet(pos)
        return self.__clique

    def get_clique(self) -> bool:
        """get l'etat du bouton"""
        return self.__clique

    def hover(self, pos: tuple[int, int]) -> bool:
        """permet de savoir si le bouton est survolé"""
        self.__survol = self.point_dans_objet(pos)
        self.actualise_animation()
        return self.__survol

    def get_survol(self) -> bool:
        """get l'etat du bouton"""
        return self.__survol

    def play_action(self):
        """permet de passer l'action du bouton"""
        if self.action is not None:
            self.action()


class BoutonRedimentionable(Bouton, ElementInterface):
    """BoutonRedimentionable est un bouton qui peut être redimentionable
    Args:
        Bouton (Bouton): est le bouton de base
    """

    def __init__(
        self,
        coordonnee: list,
        textures: list[str],
        taille: tuple[int, int],
        mode: str = "clique",
        auto_taille: bool = False,
        parent: ElementInterface = None,
        action: callable = None,
    ):
        """initialise le bouton redimentionable"""
        self.intial_texture = textures
        super().__init__(coordonnee, textures, taille, mode, parent, action)
        ElementInterface.__init__(self, coordonnee, taille, auto_taille, parent)

    def actualise_taille(self) -> None:
        """actualise la taille du bouton en fonction de son contenu"""
        pass  # pylint: disable=unnecessary-pass

    def set_size(self, valu):
        super().set_size(valu)
        self.set_texture(self.intial_texture)

    def set_size_in_axe(self, axe: int, valeur: int) -> None:
        super().set_size_in_axe(axe, valeur)
        self.set_texture(self.intial_texture)

    def add_size_in_axe(self, axe: int, valeur: int) -> None:
        super().add_size_in_axe(axe, valeur)
        self.set_texture(self.intial_texture)


class BoutonText(BoutonRedimentionable):
    """BoutonText est un bouton qui a un texte
    Args:
        BoutonRedimentionable (BoutonRedimentionable): est le bouton redimentionable de base
    """

    def __init__(
        self,
        coordonnee: list,
        textures: list[str],
        taille: tuple[int, int],
        textes: str,
        text_police: "pygame.font.Font",
        color_text: tuple[int, int, int] | tuple[int | int | int | int] = None,
        text_mode: str = "center",
        mode: str = "clique",
        auto_taille: bool = False,
        parent: ElementInterface = None,
    ):
        """initialise le bouton text"""
        super().__init__(
            coordonnee, textures, taille, mode, auto_taille, parent, action=None
        )
        self.textes = textes
        self.color_text = color_text
        self.text_mode = text_mode
        self.police = text_police
        self.actualise_text()

    def actualise_text(self) -> None:
        """actualise le texte du bouton"""
        for texture in self.texture:
            place_texte_in_texture(
                texture.texture,
                self.textes,
                self.color_text,
                self.police,
                self.text_mode,
            )


def get_callable(fn, *args, **kwargs) -> callable:
    """get une fonction avec des arguments

    Args:
        fn (callable): est la fonction a appeler
        *args: sont les arguments de la fonction sous forme de tuple
        **kwargs: sont les arguments de la fonction sous forme de dictionnaire


    Returns:
        callable: est la fonction avec les arguments
    """

    def runner():
        return fn(*args, **kwargs)

    return runner
