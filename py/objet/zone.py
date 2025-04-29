class Zone2D:
    """class pour gérer les zones"""

    def __init__(self, coordonnee: list[int, int], taille: list[int,int]):
        self.coordonnee = coordonnee
        self.__taille = taille

    def get_pos(self) -> tuple[int, int] | int:
        """renvoi les coordonées de l'objet
        Args:
            axe (int, optional): {0= axe x, 1= axe y}. Defaults to None."""

        return self.coordonnee

    def set_pos(self, valu:list[int, int]):
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

    def calcul_distace_au_carre(self,zone:"Zone2D")->float:
        """calcule la distance au carre entre 2 zones"""
        return ((self.get_center()[0]-zone.get_center()[0])**2 +
                (self.get_center()[1]-zone.get_center()[1])**2)
    
    def calcul_distace(self,zone:"Zone2D")->float:
        """calcule la distance entre 2 zones"""
        return self.calcul_distace_au_carre(zone)**0.5


class Zone3D(Zone2D):
    """class pour gérer les zones en 3D"""

    LIST_FACE = ("x", "y", "z")

    def __init__(self, coordonnee: list[int,int,int], taille: list[int,int,int]):
        super().__init__(coordonnee, taille)
     
    def get_pos(self) -> tuple[int, int, int] | int:
        """renvoi les coordonées de l'objet
        Args:
            axe (int, optional): {0= axe x, 1= axe y}. Defaults to None."""

        return self.coordonnee

    def set_pos(self, valu:list[int, int, int]):
        """defini les coordonées de l'objet"""
        self.coordonnee = valu
    
    def add_pos(self, valu: tuple[int, int, int]):
        """ajoute des coordonées à l'objet"""
        self.coordonnee = [self.coordonnee[i] + valu[i] for i in range(3)]
    
    def get_size(self) -> tuple[int, int, int] | int:
        """renvoi la taille de l'objet"""
        return self.__taille

    def set_size(self, valu: tuple[int, int, int]):
        """defini la taille de l'objet"""
        self.__taille = valu
    
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
            point (tuple[int, int]) : est le point à tester

        retun (bool) : si le point est dans l'objet

        """
        return (
            self.coordonnee[0] <= point[0] < self.coordonnee[0] + self.get_size()[0]
        ) and (self.coordonnee[1] <= point[1] < self.coordonnee[1] + self.get_size()[1]
        ) and (self.coordonnee[2] <= point[2] < self.coordonnee[2] + self.get_size()[2])

    def collision(self, obj_pos, obj_size):
        return super().collision(obj_pos, obj_size) and self.collision_in_axe(self.coordonnee[2], self.__taille[2], 2)
    
    def objet_dans_zone(self, pos_zone: tuple, size_zone: tuple) -> bool:
        """permet de savoir si un bojet est dans une zone

        Args:
            axe_x (tuple): à une longuer de 2 (le premier est le plus petit)
            axe_y (tuple): à une longuer de 2 (le premier est le plus petit)
        """
        coin_1_self = self.coordonnee
        coin_2_self = [self.get_pos()[i] + self.get_size()[i] for i in range(3)]

        coin_1_zone = pos_zone
        coin_2_zone = [pos_zone[0] + size_zone[0], pos_zone[1] + size_zone[1], pos_zone[2] + size_zone[2]]

        return (
            coin_1_zone[0] <= coin_1_self[0] < coin_2_zone[0]
            or coin_1_self[0] <= coin_1_zone[0] < coin_2_self[0]
        ) and (
            coin_1_zone[1] <= coin_1_self[1] < coin_2_zone[1]
            or coin_1_self[1] <= coin_1_zone[1] < coin_2_self[1]
        ) and (
            coin_1_zone[2] <= coin_1_self[2] < coin_2_zone[2]
            or coin_1_self[2] <= coin_1_zone[2] < coin_2_self[2]
        )
    
    def calcul_distace_au_carre(self,zone:"Zone3D")->float:
        """calcule la distance au carre entre 2 zones"""
        return ((self.get_center()[0]-zone.get_center()[0])**2 +
                (self.get_center()[1]-zone.get_center()[1])**2 +
                (self.get_center()[2]-zone.get_center()[2])**2)

    def calcul_distace(self,zone:"Zone3D")->float:
        """calcule la distance entre 2 zones"""
        return self.calcul_distace_au_carre(zone)**0.5

    def est_dans_plan(self, hauteur:float, plan:int|str)->bool:
        """permet de savoir si l'objet est dans un plan"""
        if isinstance(plan, str):
            plan = self.LIST_FACE.index(plan)
        return self.coordonnee[plan] <= hauteur < self.coordonnee[plan] + self.__taille[plan]

       