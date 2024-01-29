from graphique import pygame


class Clavier:
    def __init__(self) -> None:
        self.alphabet_clee = {
            "\x08": 8,
            "\t": 9,
            "\r": 13,
            "\x1b": 27,
            "space": 32,
            ")": 41,
            "0": 48,
            "1": 49,
            "2": 50,
            "3": 51,
            "4": 52,
            "5": 53,
            "6": 54,
            "7": 55,
            "8": 56,
            "9": 57,
            "a": 97,
            "b": 98,
            "c": 99,
            "d": 100,
            "e": 101,
            "f": 102,
            "g": 103,
            "h": 104,
            "i": 105,
            "j": 106,
            "k": 107,
            "l": 108,
            "m": 109,
            "n": 110,
            "o": 111,
            "p": 112,
            "q": 113,
            "r": 114,
            "s": 115,
            "t": 116,
            "u": 117,
            "v": 118,
            "w": 119,
            "x": 120,
            "y": 121,
            "z": 122,
            "²": 178,
            "ctrl": 1073742048,
            "maj gauche": 1073742049,
            "alt": 1073742050,
            "maj droit": 1073742053,
            "alt gr": 1073742054,
            "ver maj": 1073741881,
            "f1": 1073741882,
            "f2": 1073741883,
            "f3": 1073741884,
            "f4": 1073741885,
            "f5": 1073741886,
            "f6": 1073741887,
            "f7": 1073741888,
            "f8": 1073741889,
            "f9": 1073741890,
            "f10": 1073741891,
            "f11": 1073741892,
            "f12": 1073741893,
            "fleche droite": 1073741903,
            "fleche gauche": 1073741904,
            "fleche bas": 1073741905,
            "fleche haut": 1073741906,
        }

        # lettre_alphabet = "abcdefghijklmnopqrstuvwxyz 0123456789"
        # print(lettre_alphabet)
        self.dict_touches = {}
        for key in self.alphabet_clee.values():
            self.dict_touches[key] = "lacher"

    def actualise_all_touche(self):
        """actualise toute les touches"""
        for clee, touche in self.dict_touches.items():
            if touche == "vien_presser":
                self.dict_touches[clee] = "presser"
            elif touche == "vien_lacher":
                self.dict_touches[clee] = "lacher"

    def change_pression(self, clee: str, value: str):
        """change la pression d'une touche"""
        self.dict_touches[clee] = value

    def get_pression(self, clee: str | int):
        """get la pression d'une touche"""
        # print([clee])
        if isinstance(clee, str):  # c'est équivalen de type(clee)==str
            return self.dict_touches[self.convert_touche_key(clee)]
        else:
            return self.dict_touches[clee]

    def convert_touche_key(self, touche: str) -> int:
        """converti une touche en key
        exemple 't' -> 116
        """
        return self.alphabet_clee[touche]

    def __str__(self) -> str:
        res = "-{"
        for clee, value in self.dict_touches.items():
            res += f"{clee}:{value},"
        res += "}-"
        return res


class Souris:
    def __init__(self):
        self.actualise_position()
        self.clique_clee = {"clique_gauche": 1, "clique_droit": 3}
        self.dict_clique = {}
        for key in self.clique_clee.values():
            self.dict_clique[key] = "lacher"

    def change_pression(self, clee: str, value: str):
        """change la pression d'une touche"""
        self.dict_clique[clee] = value

    def get_pos(self):
        return self.pos

    def get_pression(self, clee: str | int):
        """get la pression d'une touche"""
        # print([clee])
        if isinstance(clee, str):  # c'est équivalen de type(clee)==str
            return self.dict_clique[self.convert_clique_key(clee)]
        else:
            return self.dict_clique[clee]

    def actualise_position(self):
        self.pos = pygame.mouse.get_pos()

    def convert_clique_key(self, touche: str) -> int:
        """converti une touche en key
        exemple 't' -> 116
        """
        return self.clique_clee[touche]

    def actualise_all_clique(self):
        """actualise toute les touches"""
        for clee, touche in self.dict_clique.items():
            if touche == "vien_presser":
                self.dict_clique[clee] = "presser"
            elif touche == "vien_lacher":
                self.dict_clique[clee] = "lacher"

    def __str__(self) -> str:
        res = "-{"
        for clee, value in self.dict_clique.items():
            res += f"{clee}:{value},"
        res += "}-"
        return res
