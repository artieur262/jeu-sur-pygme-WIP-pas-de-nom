"""est le module qui contient les classes de block"""

# pylint : missing-module-docstring
from graphique import *  # pylint: disable=unused-wildcard-import wildcard-import

# import traceback
# from IPython import embed


class Vec:
    """est un vecteur"""

    def __init__(
        self,
        vitesse: tuple[float, float, float],
        aceleration: tuple[float, float, float],
    ):
        self._vitesse = vitesse
        self._aceleration = aceleration

    def get_vitesse(self) -> tuple[float, float, float]:
        """renvoi la vitesse"""
        return self._vitesse

    def set_vitesse(self, vitesse: tuple[float, float, float]):
        """permet de definir la vitesse"""
        self._vitesse = vitesse

    def get_aceleration(self) -> tuple[float, float, float]:
        """renvoi l'aceleration"""
        return self._aceleration

    def set_aceleration(self, aceleration: tuple[float, float, float]):
        """permet de definir l'aceleration"""
        self._aceleration = aceleration

    def actualise_vitesse(self):
        """actualise la vitesse en fonction de l'aceleration"""
        self._vitesse = tuple(x + y for x, y in zip(self._vitesse, self._aceleration))


class Block:
    """est un block"""

    def __init__(
        self,
        coordonnee: tuple[int, int, int],
        taille: tuple[int, int, int],
        color: tuple[int, int, int] = None,
        animation: int = 0,
        texture: list[str] = None,
    ):
        self._texure_active = True
        if color is None:
            color = (0, 0, 0)
        if texture is None:
            texture = []
            self._texure_active = False
        self._color = color  # color : (int,int,int)
        self._coordonnee = coordonnee  # coordonnee : (x,y,z)
        self.vecteur = Vec((0, 0, 0), (0, 0, 0))
        self._taille = taille  # taille : (x,y,z)
        self.animation = animation  # int correspond a quelle image sera afficher
        self._texure = texture
        self.genere_graphique()

    def genere_graphique(self):
        """pemet de actualiser les faces du pave"""
        if self._texure_active:
            self.graphique = (
                ObjetGraphique(
                    (self._coordonnee[1:]),  # yz
                    self._texure,
                    self.animation,
                ),
                ObjetGraphique(
                    (self._coordonnee[0], self._coordonnee[2]),  # xz
                    self._texure,
                    self.animation,
                ),
                ObjetGraphique(
                    (self._coordonnee[:2]),  # xy
                    self._texure,
                    self.animation,
                ),
            )  # graphique les façaces sont les plans  : ([x,y],[x,z],[y,z])
            for i, image in enumerate(self.graphique[2].images):
                self.graphique[0].images[i] = pygame.transform.scale(
                    image, self._taille[1:]
                )
            for i, image in enumerate(self.graphique[1].images):
                self.graphique[1].images[i] = pygame.transform.scale(
                    image, (self._taille[0], self._taille[2])
                )
            for i, image in enumerate(self.graphique[0].images):
                self.graphique[2].images[i] = pygame.transform.scale(
                    image, self._taille[:2]
                )

            # print("cat")
        else:
            self.graphique = (
                ObjetGraphique(
                    (self._coordonnee[1:]),  # yz
                    [gener_texture(self._taille[1:], self._color)],
                    self.animation,
                ),
                ObjetGraphique(
                    (self._coordonnee[0], self._coordonnee[2]),  # xz
                    [gener_texture((self._taille[0], self._taille[2]), self._color)],
                    self.animation,
                ),
                ObjetGraphique(
                    (self._coordonnee[:2]),  # xy
                    [gener_texture(self._taille[:2], self._color)],
                    self.animation,
                ),
            )  # graphique les façaces sont les plans  : ([x,y],[x,z],[y,z])

    # def __getattribute__(self, name):
    #     if name == "_coordonnee":
    #         st = traceback.extract_stack(limit=2)
    #         print(f"Line {st[0][1]} in {st[0][2]}: {st[0][3]}")
    #     return super().__getattribute__(name)

    def actualise_graphique_animation(self):
        """permet de actualisé les animations graphique"""
        self.graphique[0].animation = self.animation
        self.graphique[1].animation = self.animation
        self.graphique[2].animation = self.animation

    def actualise_coord_graph(self):
        """actualise la position des objet graphique"""
        self.graphique[0].coordonnee = self._coordonnee[1:]
        self.graphique[1].coordonnee = (self._coordonnee[0], self._coordonnee[2])
        self.graphique[2].coordonnee = self._coordonnee[:2]

    def get_color(self) -> tuple[int]:
        """renvoi la couleur"""
        return self._color

    def get_coordonnee(self, index: int = None):
        """return les coordonees ou coordonees[index]"""
        if index is None:
            return self._coordonnee
        return self._coordonnee[index]

    def get_taille(self, index: int = None):
        """return la taille ou taille[index]"""
        if index is None:
            return self._taille
        return self._taille[index]

    def get_centre_objet(self):
        """return le centre de l'objet"""
        cord = self.get_coordonnee()
        tail = self.get_taille()
        return [cord[i] + tail[i] / 2 for i in range(3)]

    def set_coordonnee(self, valeur: list[int] | tuple[int, int, int]):
        """permet de modifier les coordonnees"""
        self._coordonnee = tuple(valeur)
        self.actualise_coord_graph()

    def set_aceleration(self, valeur: list[float] | tuple[float, float, float]):
        """permet de modifier l'aceleration"""
        self.vecteur.set_aceleration(valeur)

    def set_vitesse(self, valeur: list[float] | tuple[float, float, float]):
        """permet de modifier la vitesse"""
        self.vecteur.set_vitesse(valeur)

    def modif_coordonnee(
        self,
        value: list[int] | tuple[int, int, int],
        mode: str = "=",
        index: int = None,
    ):
        """permet de modifier les coordonnees

        Args:
            value (list[int] | tuple[int, int, int]):
            mode (str("+" | "=" | "-")): permet de faire +, - ou =
            index (int): permet de selectioner l'index de coordonneee

        """
        if index is None:
            if not isinstance(value, (list, tuple)):
                raise ValueError(
                    "error : la valeur n'est pas une liste ou"
                    + " une tuple alors que un index n'a pas été donné"
                )
            if mode == "=":
                self._coordonnee = value
            else:
                raise ValueError('error : index is None and mode != "=" ')
        else:
            if not isinstance(value, int):
                raise ValueError("la valeur n'est pas un int")
            coordonnee = list(self._coordonnee)
            if mode == "=":
                coordonnee[index] = value

            elif mode == "+":
                coordonnee[index] += value

            elif mode == "-":
                coordonnee[index] -= value

            else:
                raise ValueError("error : mode not in ('=','+','-')")
            self._coordonnee = tuple(coordonnee)
            self._coordonnee: tuple[int, int, int]
        self.actualise_coord_graph()

    def ajoute_screen(
        self,
        face: int,
        cord_face: int,
        decalage: tuple = None,
        taille: tuple = None,
        surface=None,
    ):
        """affiche l'objet sur la fenêtre

        Args:
            face (int): {0:"xy", 1:"xz", 2:"yz"}
            cord_face (int): _description_
            decalage (tuple, optional): _description_. Defaults to None.
            taille (tuple, optional): _description_. Defaults to None.
        """

        if self.in_axe(cord_face, face):
            self.graphique[face].afficher(decalage, taille, surface)

    def in_axe(self, point, axe):
        """verfie si un point est sur le même allignement de l'objet sur un axe"""
        coin_1_self = self.get_coordonnee(axe)
        coin_2_self = self.get_coordonnee(axe) + self.get_taille(axe)
        return (
            coin_1_self <= point <= coin_2_self
        )  # or coin_1_self == point == coin_2_self

    def collision_in_axe(self, obj, axe: int) -> bool:
        """pemet de voir si un objet a une colisiont sur un plan

        Args:
            obj (Pave)
            axe (int): {1= axe x, 2= axe y, 3= axe z}

        Returns: (bool)
        """
        # if not (
        #     isinstance(obj, self.__class__)
        #     or bool(set(obj.__class__.__bases__) & set(self.__class__.__bases__))
        # ):
        #     raise ValueError("obj n'a pas d'ancetre commun (pas un pavé)")
        coin_1_self = self.get_coordonnee(axe)
        coin_2_self = self.get_coordonnee(axe) + self.get_taille(axe)

        coin_1_obj = obj.get_coordonnee(axe)
        coin_2_obj = obj.get_coordonnee(axe) + obj.get_taille(axe)

        return (
            coin_1_obj <= coin_1_self < coin_2_obj
            or coin_1_self <= coin_1_obj < coin_2_self
        )

    def collision(self, obj):
        """pemet savoir l'objet à une colision avec un autre objet dans l'espace
        obj: (Playeur | Block)
        """
        return (
            self.collision_in_axe(obj, 0)
            and self.collision_in_axe(obj, 1)
            and self.collision_in_axe(obj, 2)
        )

    def si_touche_obj(self, obj, axe: int):
        """teste si un objet touche un autre objet sur un axe"""
        obj: Block
        sorti = True
        for i in range(3):
            if i == axe:
                if not (
                    self.get_coordonnee(i) + self.get_taille(i) == obj.get_coordonnee(i)
                    or obj.get_coordonnee(i) + obj.get_taille(i)
                    == self.get_coordonnee(i)
                ):
                    sorti = False
            elif not self.collision_in_axe(obj, i):
                sorti = False
        # print(sorti)
        return sorti

    def trouve_obj_autour(self, list_obj: list):
        """permet de trouver les objets sous self

        Args:
            list_obj (list): est la liste des objet qui vont être testé

        Returns:
            list: est la liste de indide des block qui sont dessou self
        """
        list_obj: list[Block]
        sorti = []
        for i, obj in enumerate(list_obj):
            if (
                self.si_touche_obj(obj, 0)
                or self.si_touche_obj(obj, 1)
                or self.si_touche_obj(obj, 2)
            ):
                sorti.append(i)
        return sorti

    def deplace(self, list_block: list, axe: int, distance: int):
        """fait déplacer le block en evitant les colisions

        Args:
            list_block (list[Block]): _description_
            axe (int): {0 : axe x, 1 : axe y, 2 : axe z}
            vecteur (int):

        Returns:
            bool: est la réponce de si un obstacle a gené le dépacment du block
        """
        # print([self.collision(x) for x in list_block])
        self.modif_coordonnee(distance, "+", axe)
        if any(self.collision(x) for x in list_block):
            # self._coordonnee[2] -= chute
            # self.actualise_coord_graph()
            self.modif_coordonnee(distance, "-", axe)
            self.actualise_coord_graph()
            for i in range(distance * (-1 if distance < 0 else 1)):  # anti-niggatif
                self.modif_coordonnee(1 * (-1 if distance < 0 else 1), "+", axe)
                if any(self.collision(x) for x in list_block):
                    self.modif_coordonnee(1 * (-1 if distance < 0 else 1), "-", axe)
                    self.actualise_coord_graph()
                    return distance - i * (-1 if distance < 0 else 1)

        self.actualise_coord_graph()
        return 0

    def convert_save(self) -> dict:
        """pemet de convetir le bloque en un format pour le mettre dans json"""
        sorti = {
            "type": "block",
            "taille": self._taille,
            "coor": self._coordonnee,
            "color": self._color,
        }
        if self._texure_active:
            sorti["texture"] = self._texure
        else:
            sorti["texture"] = None
        return sorti

    def __str__(self) -> str:
        return f"pos{self._coordonnee},taille{self._taille},color{self._color}"

    @staticmethod
    def convert_load(dic: dict):
        """pemet de convetir un dic en un block"""
        return Block(dic["coor"], dic["taille"], dic["color"], texture=dic["texture"])
