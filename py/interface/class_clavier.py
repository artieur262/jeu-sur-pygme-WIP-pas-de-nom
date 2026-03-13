"""ce module contien les class pour la souris et le clavier

il y a 2 class:
    - Clavier : class pour gérer le clavier
    - Souris : class pour gérer la souris

et 2 dictionnaire:
    - key_names : dictionnaire pour les noms des touches
    - mouse_names : dictionnaire pour les noms des cliques de la souris
"""

from typing import Literal

import pygame
import enum


class ClickStatut(enum.Enum):
    """enum pour les états de clique"""
    LACHER = 0
    VIEN_LACHER = 1
    PRESSER = 2
    VIEN_PRESSER = 3


class Peripherique:
    """classe de base pour les périphériques (clavier, souris, manette, etc.)"""

    CLICK_NAMES = [
        "lacher",
        "vien_lacher",
        "presser",
        "vien_presser",
    ]

    def __init__(self):
        self.dict_touches: dict[int, int] = {}

    def reset(self):
        """reset la pression de toute les touches
        pour les mettre a lacher
        """
        self.dict_touches = {}

    def lacher_tout(self):
        """met toute les touches a lacher"""
        for clee, value in self.dict_touches.items():
            if value != 0:
                self.dict_touches[clee] = 1

    def update_all_key(self):
        """actualise toute les touches"""
        clee_a_supprimer = []
        for clee, touche in self.dict_touches.items():
            if touche == 4:
                self.dict_touches[clee] = 3
            elif touche <= 1:
                clee_a_supprimer.append(clee)
        for clee in clee_a_supprimer:
            del self.dict_touches[clee]

    def get_pression(self, clee: int) -> Literal[3, 2, 1, 0]:
        """get la pression d'une touche

        retrun : Literal[3, 2, 1, 0]
            0 : lacher
            1 : vien_lacher
            2 : presser
            3 : vien_presser
        """
        if clee in self.dict_touches:
            return self.dict_touches[clee]
        else:
            return 0

    def set_pression(self, clee: int, value: Literal[3, 2, 1, 0]) -> None:
        """change la pression d'une touche
        args:
            clee (int): est la clee de la touche
            value (Literal[3, 2, 1, 0]): est la nouvelle valeur de la touche
                0 : lacher
                1 : vien_lacher
                2 : presser
                3 : vien_presser
        """
        self.dict_touches[clee] = value

    def __str__(self) -> str:
        res = "-{"
        for clee, value in self.dict_touches.items():
            res += f"{clee}:{self.CLICK_NAMES[value]},"
        res += "}-"
        return res


class Clavier(Peripherique):
    """cette class permet de gérer le clavier
    et de savoir si une touche est presser ou lacher
    """

    KEY_NAMES = {
        "en": {
            8: "backspace",
            9: "tab",
            13: "return",
            27: "escape",
            32: "space",
            127: "delete",
            1073741881: "caps lock",
            1073741903: "right",
            1073741904: "left",
            1073741905: "down",
            1073741906: "up",
            1073742048: "left ctrl",
            1073742049: "left shift",
            1073742050: "left alt",
            1073742051: "left windows",
            1073742052: "right ctrl",
            1073742053: "right shift",
            1073742054: "right alt",
            1073742055: "right windows",
        },
        "fr": {
            8: "retour arrière",
            9: "tabulation",
            13: "entrée",
            27: "échap",
            32: "espace",
            127: "suppr",
            1073741881: "verr maj",
            1073741903: "droite",
            1073741904: "gauche",
            1073741905: "bas",
            1073741906: "haut",
            1073742048: "ctrl gauche",
            1073742049: "shift gauche",
            1073742050: "alt gauche",
            1073742051: "windows gauche",
            1073742052: "ctrl droit",
            1073742053: "shift droit",
            1073742054: "alt droit",
            1073742055: "windows droit",
        },
    }


class Souris(Peripherique):
    """cette class permet de gérer la souris
    peremet de savoir la position de la souris
    et permet de savoir si un clique est vien_presser, presser, vien_lacher ou lacher
    """

    CLICK_NAMES = {
        "en": {1: "left click", 2: "wheel click", 3: "right click"},
        "fr": {1: "clique gauche", 2: "clique molette", 3: "clique droit"},
    }

    def __init__(self):
        super().__init__()
        self.update_pos()

    def get_pos(self):
        """get la position de la souris"""
        return self.pos

    def update_pos(self):
        """actualise la position de la souris"""
        self.pos = pygame.mouse.get_pos()
