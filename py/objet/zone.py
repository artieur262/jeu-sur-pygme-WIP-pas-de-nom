class Zone2D:
    """class pour gérer les zones"""

    def __init__(self, coordonnee: list[int, int], taille: list[int, int]):
        self.coordonnee = coordonnee
        self.__taille = taille

    def dans_plan(self, hauteur: int, plan: int) -> bool:
        """permet de savoir si l'objet est dans un plan"""
        return (
            self.coordonnee[plan]
            <= hauteur
            < self.coordonnee[plan] + self.get_size()[plan]
        )

    def get_pos(self) -> tuple[int, int] | int:
        """renvoi les coordonées de l'objet
        Args:
            axe (int, optional): {0= axe x, 1= axe y}. Defaults to None."""

        return self.coordonnee

    def set_pos(self, valu: list[int, int]):
        """defini les coordonées de l'objet"""
        self.coordonnee = valu

    def add_pos(self, valu: tuple[int, int]):
        """ajoute des coordonées à l'objet"""
        self.coordonnee = [self.coordonnee[i] + valu[i] for i in range(2)]

    def get_size(self) -> tuple[int, int] | int:
        """renvoi la taille de l'objet"""
        return self.__taille

    def get_center(self) -> tuple[float, float]:
        """renvoi le centre de l'objet"""
        return (
            self.coordonnee[0] + self.__taille[0] / 2,
            self.coordonnee[1] + self.__taille[1] / 2,
        )

    def set_size(self, valu: tuple[int, int]):
        """defini la taille de l'objet"""
        self.__taille = valu

    def point_dans_objet(self, point: tuple[int, int]) -> bool:
        """pour savoir si un point est dans l'objet

        entre :
            point (tuple[int, int]) : est le point à tester

        retun (bool) : si le point est dans l'objet

        """
        return (
            self.coordonnee[0] <= point[0] < self.coordonnee[0] + self.get_size()[0]
        ) and (self.coordonnee[1] <= point[1] < self.coordonnee[1] + self.get_size()[1])

    def contiens_in_axe(self, obj_pos: int, obj_size: int, axe: int) -> bool:
        """pemet de voir si un objet est contenu sur un plan

        Args:
            obj_pos (int): est la position de l'objet sur l'axe
            obj_size (int): est la taille de l'objet sur l'axe
            axe (int): {1= axe x, 2= axe y}

        Returns: (bool)
        """
        coin_1_self = self.get_pos()[axe]
        coin_2_self = self.get_pos()[axe] + self.get_size()[axe]

        coin_1_obj = obj_pos
        coin_2_obj = obj_pos + obj_size

        return coin_1_self <= coin_1_obj and coin_2_obj <= coin_2_self

    def contiens(self, obj_pos: tuple[int], obj_size: tuple[int]) -> bool:
        """pemet savoir l'objet est contenu dans un autre objet dans l'espace
        args:
            obj_pos (tuple[int]) : est la position de l'objet
            obj_size (tuple[int]) : est la taille de l'objet
        """
        return self.contiens_in_axe(
            obj_pos[0], obj_size[0], 0
        ) and self.contiens_in_axe(obj_pos[1], obj_size[1], 1)

    def collision_in_axe(self, obj_pos: int, obj_size: int, axe: int) -> bool:
        """pemet de voir si un objet a une colisiont sur un plan

        Args:
            obj_pos (int): est la position de l'objet sur l'axe
            obj_size (int): est la taille de l'objet sur l'axe
            axe (int): {1= axe x, 2= axe y}

        Returns: (bool)
        """
        coin_1_self = self.get_pos()[axe]
        coin_2_self = self.get_pos()[axe] + self.get_size()[axe]

        coin_1_obj = obj_pos
        coin_2_obj = obj_pos + obj_size

        return (
            coin_1_obj <= coin_1_self < coin_2_obj
            or coin_1_self <= coin_1_obj < coin_2_self
        )

    def collision(self, obj_pos: tuple[int], obj_size: tuple[int]) -> bool:
        """pemet savoir l'objet à une colision avec un autre objet dans l'espace
        args:
            obj_pos (tuple[int]) : est la position de l'objet
            obj_size (tuple[int]) : est la taille de l'objet
        """
        return self.collision_in_axe(
            obj_pos[0], obj_size[0], 0
        ) and self.collision_in_axe(obj_pos[1], obj_size[1], 1)

    def collision_zone(self, zone: "Zone2D") -> bool:
        """pemet savoir l'objet à une colision avec un autre objet dans l'espace
        args:
            zone (Zone3D) : est la zone à tester
        """
        return self.collision(
            zone.get_pos(),
            zone.get_size(),
        )

    def collision_list_zone(self, list_zone: list["Zone2D"]) -> bool:
        """pemet savoir l'objet à une colision avec un autre objet dans une liste
        args:
            list_zone (list[Zone3D]) : est la liste des zones à tester
        """
        for i in list_zone:
            if self != i and self.collision_zone(i):
                return True
        return False

    def objet_dans_zone(self, pos_zone: tuple, size_zone: tuple) -> bool:
        """permet de savoir si un bojet est dans une zone

        Args:
            axe_x (tuple): à une longuer de 2 (le premier est le plus petit)
            axe_y (tuple): à une longuer de 2 (le premier est le plus petit)

        Returns:
            bool: si l'objet
        """
        coin_1_self = self.coordonnee
        coin_2_self = [self.get_pos()[i] + self.get_size()[i] for i in range(2)]

        coin_1_zone = pos_zone
        coin_2_zone = [pos_zone[0] + size_zone[0], pos_zone[1] + size_zone[1]]

        return (
            coin_1_zone[0] <= coin_1_self[0] < coin_2_zone[0]
            or coin_1_self[0] <= coin_1_zone[0] < coin_2_self[0]
        ) and (
            coin_1_zone[1] <= coin_1_self[1] < coin_2_zone[1]
            or coin_1_self[1] <= coin_1_zone[1] < coin_2_self[1]
        )

    def calcul_distace_au_carre(self, zone: "Zone2D") -> float:
        """calcule la distance au carre entre 2 zones"""
        return (self.get_center()[0] - zone.get_center()[0]) ** 2 + (
            self.get_center()[1] - zone.get_center()[1]
        ) ** 2

    def calcul_distace(self, zone: "Zone2D") -> float:
        """calcule la distance entre 2 zones"""
        return self.calcul_distace_au_carre(zone) ** 0.5

    def set_pos_in_axe(self, axe: int, valeur: int) -> None:
        """defini les coordonées de l'objet dans un axe"""
        self.coordonnee[axe] = valeur

    def add_pos_in_axe(self, axe: int, valeur: int) -> None:
        """deplace l'objet dans un axe"""
        self.coordonnee[axe] += valeur

    def set_size_in_axe(self, axe: int, valeur: int) -> None:
        """defini la taille de l'objet dans un axe"""
        self.__taille[axe] = valeur

    def add_size_in_axe(self, axe: int, valeur: int) -> None:
        """change la taille de l'objet dans un axe"""
        self.__taille[axe] += valeur

    def distance_entre_in_axe(self, zone: "Zone2D", axe: int) -> float:
        """calcule la distance entre 2 zones dans un axe
        il calcule la distance en regardant l'espace vide entre les 2 zones dans l'axe,
        si les zones se chevauchent dans l'axe alors la distance est de -1
        """
        coin_1_self = self.coordonnee[axe]
        coin_2_self = self.coordonnee[axe] + self.get_size()[axe]

        coin_1_zone = zone.get_pos()[axe]
        coin_2_zone = zone.get_pos()[axe] + zone.get_size()[axe]

        if coin_1_self < coin_1_zone:
            if coin_2_self <= coin_1_zone:
                return coin_1_zone - coin_2_self
            else:
                return -1
        else:
            if coin_2_zone <= coin_1_self:
                return coin_1_self - coin_2_zone
            else:
                return -1

    def new_zone_agrandi_axe(self, axe: int, valeur: int) -> "Zone2D":
        """renvoi une nouvelle zone agrandi dans un axe"""
        new_zone = Zone2D([i for i in self.get_pos()], [i for i in self.get_size()])
        new_zone.add_size_in_axe(axe, valeur)
        if valeur < 0:
            new_zone.add_pos_in_axe(axe, valeur)
        return new_zone

    def pre_deplacer_in_axe(
        self,
        axe: int,
        valeur: int,
        list_collision: set["Zone2D"] = None,
        list_poussable: set["Zone2D"] = None,
        list_collision_poussable: set["Zone2D"] = None,
    ) -> int:
        """deplace l'objet dans un axe"""
        if list_collision is None:
            list_collision = set()
        if list_poussable is None:
            list_poussable = set()
        if list_collision_poussable is None:
            list_collision_poussable = list_collision

        zonne_collision = self.new_zone_agrandi_axe(axe, valeur)
        toucher = False
        objet_plus_proche: Zone2D | None = None
        for i in list_collision:
            if i != self and zonne_collision.collision_zone(i):
                toucher = True
                if objet_plus_proche is None or (
                    self.distance_entre_in_axe(i, axe)
                    < self.distance_entre_in_axe(objet_plus_proche, axe)
                ):
                    objet_plus_proche = i

        direction = valeur
        if toucher:
            if objet_plus_proche.distance_entre_in_axe(self, axe) <= 0:
                direction = 0
            elif valeur > 0:
                new_pos = objet_plus_proche.get_pos()[axe] - self.get_size()[axe]
                direction = new_pos - self.coordonnee[axe]
            else:
                new_pos = (
                    objet_plus_proche.get_pos()[axe] + objet_plus_proche.get_size()[axe]
                )
                direction = new_pos - self.coordonnee[axe]

        zonne_collision = self.new_zone_agrandi_axe(axe, direction)
        for i in list_poussable:
            if i != self and zonne_collision.collision_zone(i):
                distance = self.distance_entre_in_axe(i, axe)
                new_direction = direction + (distance if direction < 0 else -distance)
                if (new_direction < 0) != (direction < 0):
                    # pour éviter les erreurs de calcul qui font
                    # que l'objet se déplace dans le mauvais sens
                    new_direction = 0
                temp = i.pre_deplacer_in_axe(
                    axe,
                    new_direction,
                    list_collision_poussable,
                    list_poussable,
                )
                temp -= distance if temp < 0 else -distance
                if abs(temp) < abs(direction):
                    direction = temp
                    zonne_collision = self.new_zone_agrandi_axe(axe, direction)

        return direction

    def deplacer_in_axe(
        self,
        axe: int,
        valeur: int,
        list_collision: set["Zone2D"] = None,
        list_poussable: set["Zone2D"] = None,
        list_collision_poussable: set["Zone2D"] = None,
    ) -> int:
        """deplace l'objet dans un axe
        en prenant en compte les collisions avec les objets de la liste de collision et
        en poussant les objets de la liste de poussable
        """
        direction = self.pre_deplacer_in_axe(
            axe, valeur, list_collision, list_poussable, list_collision_poussable
        )

        self.deplacer_pousser_in_axe(axe, direction, list_poussable)
        return direction

    def deplacer_pousser_in_axe(
        self, axe: int, valeur: int, list_poussable: set["Zone2D"] = None
    ) -> None:
        """deplace l'objet dans un axe en poussant les objets de la liste de poussable"""
        if list_poussable is None or len(list_poussable) == 0:
            self.add_pos_in_axe(axe, valeur)
            return None
        dict_deplacement: dict["Zone2D", int] = dict()
        self.__deplacer_pousser_recursif_in_axe(
            axe, valeur, list_poussable, dict_deplacement
        )
        for key, value in dict_deplacement.items():
            key.add_pos_in_axe(axe, value)
        self.add_pos_in_axe(axe, valeur)

    def __deplacer_pousser_recursif_in_axe(
        self,
        axe: int,
        valeur: int,
        list_poussable: set["Zone2D"],
        dict_deplacement: dict["Zone2D", int],
    ) -> int:
        """deplace l'objet dans un axe
        en poussant les objets de la liste de poussable
        """
        zonne_collision = self.new_zone_agrandi_axe(axe, valeur)
        for i in list_poussable:
            if i != self and zonne_collision.collision_zone(i):

                distance = self.distance_entre_in_axe(i, axe)
                temp = valeur + (distance if valeur < 0 else -distance)

                if i not in dict_deplacement:
                    dict_deplacement[i] = temp
                elif abs(dict_deplacement[i]) < abs(temp):
                    dict_deplacement[i] = temp
                i.__deplacer_pousser_recursif_in_axe(  # pylint: disable=protected-access
                    axe,
                    temp,
                    list_poussable,
                    dict_deplacement,
                )

        return valeur

    def deplacer_indepant_axe(
        self,
        valeur: tuple[int, int],
        list_collision: set["Zone2D"] = None,
        list_poussable: set["Zone2D"] = None,
    ) -> None:
        """deplace l'objet dans un axe"""
        if len(valeur) != 2:
            raise ValueError("la valeur doit etre de la forme (x,y)")
        if valeur[0]:
            self.deplacer_in_axe(0, valeur[0], list_collision, list_poussable)
        if valeur[1]:
            self.deplacer_in_axe(1, valeur[1], list_collision, list_poussable)


class Zone3D(Zone2D):
    """class pour gérer les zones en 3D"""

    LIST_FACE = ("yz", "xz", "xy")
    LIST_AXE = ("x", "y", "z")

    def __init__(self, coordonnee: list[int, int, int], taille: list[int, int, int]):
        super().__init__(coordonnee, taille)

    def get_pos(self) -> tuple[int, int, int] | int:
        """renvoi les coordonées de l'objet
        Args:
            axe (int, optional): {0= axe x, 1= axe y}. Defaults to None."""

        return self.coordonnee

    def set_pos(self, valu: list[int, int, int]):
        """defini les coordonées de l'objet"""
        self.coordonnee = list(valu)

    def add_pos(self, valu: tuple[int, int, int]):
        """ajoute des coordonées à l'objet"""
        self.coordonnee = [self.coordonnee[i] + valu[i] for i in range(3)]

    def get_size(self) -> tuple[int, int, int] | int:
        """renvoi la taille de l'objet"""
        return super().get_size()

    def set_size(self, valu: tuple[int, int, int]):
        """defini la taille de l'objet"""
        super().set_size(valu)

    def new_zone_agrandi_axe(self, axe: int, valeur: int) -> "Zone3D":
        """renvoi une nouvelle zone agrandi dans un axe"""
        new_zone = Zone3D([i for i in self.get_pos()], [i for i in self.get_size()])
        new_zone.add_size_in_axe(axe, valeur)
        if valeur < 0:
            new_zone.add_pos_in_axe(axe, valeur)
        return new_zone

    def get_center(self) -> tuple[float, float, float]:
        """renvoi le centre de l'objet"""
        return (
            self.coordonnee[0] + self.__taille[0] / 2,
            self.coordonnee[1] + self.__taille[1] / 2,
            self.coordonnee[2] + self.__taille[2] / 2,
        )

    def point_dans_objet(self, point: tuple[int, int, int]) -> bool:
        """pour savoir si un point est dans l'objet

        entre :
            point (tuple[int, int, int]) : est le point à tester

        retun (bool) : si le point est dans l'objet

        """
        return (
            (self.coordonnee[0] <= point[0] < self.coordonnee[0] + self.get_size()[0])
            and (
                self.coordonnee[1] <= point[1] < self.coordonnee[1] + self.get_size()[1]
            )
            and (
                self.coordonnee[2] <= point[2] < self.coordonnee[2] + self.get_size()[2]
            )
        )

    def deplacer_on_point(self, point: tuple[int, int, int]) -> None:
        """deplace l'objet pour que son centre soit sur un point"""
        self.coordonnee = [point[i] - self.get_size()[i] / 2 for i in range(3)]

    def contiens_zone(self, zone: "Zone3D") -> bool:
        """pemet savoir l'objet est contenu dans un autre objet dans l'espace
        args:
            zone (Zone3D) : est la zone à tester
        """
        return self.contiens(zone.get_pos(), zone.get_size())

    def contiens(self, obj_pos, obj_size):
        return super().contiens(obj_pos, obj_size) and self.contiens_in_axe(
            obj_pos[2], obj_size[2], 2
        )

    def collision(self, obj_pos, obj_size):
        return (
            self.collision_in_axe(obj_pos[0], obj_size[0], 0)
            and self.collision_in_axe(obj_pos[1], obj_size[1], 1)
            and self.collision_in_axe(obj_pos[2], obj_size[2], 2)
        )

    def collision_zone(self, zone: "Zone3D") -> bool:
        return super().collision_zone(zone)

    def collision_list_zone(self, list_zone: list["Zone3D"]) -> bool:
        """pemet savoir l'objet à une colision avec un autre objet dans une liste
        args:
            list_zone (list[Zone3D]) : est la liste des zones à tester
        """
        return super().collision_list_zone(list_zone)

    def objet_dans_zone(self, pos_zone: tuple, size_zone: tuple) -> bool:
        """permet de savoir si un bojet est dans une zone

        Args:
            axe_x (tuple): à une longuer de 2 (le premier est le plus petit)
            axe_y (tuple): à une longuer de 2 (le premier est le plus petit)
        """
        coin_1_self = self.coordonnee
        coin_2_self = [self.get_pos()[i] + self.get_size()[i] for i in range(3)]

        coin_1_zone = pos_zone
        coin_2_zone = [
            pos_zone[0] + size_zone[0],
            pos_zone[1] + size_zone[1],
            pos_zone[2] + size_zone[2],
        ]

        return (
            (
                coin_1_zone[0] <= coin_1_self[0] < coin_2_zone[0]
                or coin_1_self[0] <= coin_1_zone[0] < coin_2_self[0]
            )
            and (
                coin_1_zone[1] <= coin_1_self[1] < coin_2_zone[1]
                or coin_1_self[1] <= coin_1_zone[1] < coin_2_self[1]
            )
            and (
                coin_1_zone[2] <= coin_1_self[2] < coin_2_zone[2]
                or coin_1_self[2] <= coin_1_zone[2] < coin_2_self[2]
            )
        )

    def calcul_distace_au_carre(self, zone: "Zone3D") -> float:
        """calcule la distance au carre entre 2 zones"""
        return (
            (self.get_center()[0] - zone.get_center()[0]) ** 2
            + (self.get_center()[1] - zone.get_center()[1]) ** 2
            + (self.get_center()[2] - zone.get_center()[2]) ** 2
        )

    def calcul_distace(self, zone: "Zone3D") -> float:
        """calcule la distance entre 2 zones"""
        return self.calcul_distace_au_carre(zone) ** 0.5

    def est_dans_plan(self, hauteur: float, plan: int | str) -> bool:
        """permet de savoir si l'objet est dans un plan"""
        if isinstance(plan, str):
            plan = self.LIST_FACE.index(plan)
        return (
            self.coordonnee[plan]
            <= hauteur
            < self.coordonnee[plan] + self.get_size()[plan]
        )

    def distance_entre_in_axe(self, zone: "Zone3D", axe: int) -> float:
        return super().distance_entre_in_axe(zone, axe)

    def deplacer_in_axe(
        self,
        axe: int,
        valeur: int,
        list_collision: set["Zone3D"] = None,
        list_poussable: set["Zone3D"] = None,
    ) -> int:
        return super().deplacer_in_axe(axe, valeur, list_collision, list_poussable)

    def deplacer_indepant_axe(
        self,
        valeur: tuple[int, int, int],
        list_collision: set["Zone3D"] = None,
        list_poussable: set["Zone3D"] = None,
    ) -> None:
        """deplace l'objet dans un axe"""
        if len(valeur) != 3:
            raise ValueError("la valeur doit etre de la forme (x,y,z)")
        if valeur[0]:
            self.deplacer_in_axe(0, valeur[0], list_collision, list_poussable)
        if valeur[1]:
            self.deplacer_in_axe(1, valeur[1], list_collision, list_poussable)
        if valeur[2]:
            self.deplacer_in_axe(2, valeur[2], list_collision, list_poussable)

    def ajouter_map(self, map_):
        """ajoute la zone à la map"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")

    def retirer_map(self, map_):
        """retire la zone de la map"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")
