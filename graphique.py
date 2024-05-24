"""cette parti est la pour gérer l'interface graphique du jeu

il y a une class:
    ObjetGraphique : est un objet graphique qui a le but d'etre affiché

il y a des fonctions:
    - gener_texture : génere une texture rectangulaire
    - gener_texture_arc_ciel : génere une texture arc en ciel
    - decoupe_texte : découpe un texte en plusieur ligne
    - place_texte_in_texture : ajoute du texte sur une image
    - vider_affichage : permet de vider l'affichage
    - quitter : permet de quitter


"""

# pylint: disable=no-member
import pygame


pygame.init()


screen = pygame.display.set_mode((1200, 600), pygame.RESIZABLE)
pygame.display.set_caption("projet")
screen.fill((200, 200, 200))


class ObjetGraphique:
    """est Objet Graphique qui a le but d'etre affiché

    agrs:
        coordonnee : tuple[int, int] : coordonnée de l'objet
        images : list[str | pygame.Surface] : liste des images de l'objet
        animation : int : l'animation actuel de l'objet
    """

    def __init__(
        self,
        coordonnee: tuple[int],
        images: list[str | pygame.Surface],
        animation=0,
    ):
        images_converti: list[pygame.Surface] = []
        for image in images:  # converti les liens d'images en format Surface
            if isinstance(image, str):
                image = pygame.image.load(image)
                image.convert()
            images_converti.append(image)
        self.visible = True
        self.coordonnee = coordonnee
        self.images = images_converti
        self.animation = animation
        self.actualise_dimension()
        self.coordonnee: tuple[int]
        self.animation: int
        self.images: list[pygame.Surface]

    def get_coordonnee(self, axe: int = None) -> tuple[int, int] | int:
        """renvoi les coordonées de l'objet
        Args:
            axe (int, optional): {0= axe x, 1= axe y}. Defaults to None."""
        if axe is None:
            return self.coordonnee
        else:
            return self.coordonnee[axe]

    def set_coordonnee(self, valu):
        """defini les coordonées de l'objet"""
        self.coordonnee = valu

    def get_taille(self, axe: int = None) -> tuple[int, int] | int:
        """renvoi la taille de l'objet"""
        if axe is None:
            return self.dimension
        else:
            return self.dimension[axe]

    def get_center(self) -> tuple[float, float]:
        """renvoi le centre de l'objet"""
        return (
            self.coordonnee[0] + self.dimension[0] / 2,
            self.coordonnee[1] + self.dimension[1] / 2,
        )

    def image_actuel(self) -> pygame.Surface:
        """donne l'image actuel"""
        return self.images[self.animation]

    def redimentione_all_image(self, taille: tuple[int]):
        """redimentionne toute les images"""
        for i, image in enumerate(self.images):
            self.images[i] = pygame.transform.scale(image, taille)
        self.actualise_dimension()

    def actualise_dimension(self):
        """actualise les dimensions"""
        self.dimension = (
            self.images[self.animation].get_width(),
            self.images[self.animation].get_height(),
        )
        self.dimension: tuple[int, int]

    def x_y_dans_objet(self, x: int, y: int):
        """pour savoir si un point est dans l'objet

        entre :
            x (int) : est les coordonees du point sur l'axe x
            y (int) : est les coordonees du point sur l'axe y

        retun (bool) : si le point est dans l'objet

        """
        return (self.coordonnee[0] <= x < self.coordonnee[0] + self.dimension[0]) and (
            self.coordonnee[1] <= y < self.coordonnee[1] + self.dimension[1]
        )

    def collision_in_axe(self, obj_pos: int, obj_size: int, axe: int) -> bool:
        """pemet de voir si un objet a une colisiont sur un plan

        Args:
            obj_pos (int): est la position de l'objet sur l'axe
            obj_size (int): est la taille de l'objet sur l'axe
            axe (int): {1= axe x, 2= axe y}

        Returns: (bool)
        """
        coin_1_self = self.get_coordonnee(axe)
        coin_2_self = self.get_coordonnee(axe) + self.get_taille(axe)

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

    def objet_dans_zone(self, axe_x: tuple, axe_y: tuple) -> bool:
        """permet de savoir si un bojet est dans une zone

        Args:
            axe_x (tuple): à une longuer de 2 (le premier est le plus petit)
            axe_y (tuple): à une longuer de 2 (le premier est le plus petit)

        Returns:
            bool: si l'objet
        """
        coin_1_self = self.coordonnee
        coin_2_self = [self.coordonnee[i] + self.dimension[i] for i in range(2)]

        coin_1_zone = [axe_x[0], axe_y[0]]
        coin_2_zone = [axe_x[1], axe_y[1]]

        return (
            coin_1_zone[0] <= coin_1_self[0] < coin_2_zone[0]
            or coin_1_self[0] <= coin_1_zone[0] < coin_2_self[0]
        ) and (
            coin_1_zone[1] <= coin_1_self[1] < coin_2_zone[1]
            or coin_1_self[1] <= coin_1_zone[1] < coin_2_self[1]
        )
        # return (
        #     axe_x[0] <= self.coordonnee[0] < axe_x[1] + self.dimension[0]
        #     and axe_y[0] <= self.coordonnee[1] < axe_y[1] + self.dimension[1]
        # )

    def afficher(
        self,
        decalage_camera: tuple[int, int] = None,
        debut: tuple[int, int] = None,
        surface: pygame.Surface = None,
    ) -> bool:
        """permet de l'affiché sur la fenêtre et de savoir si il est affiché

        Args:
            decalage_camera (optional): permet de décaler l'objet par rapport à la camera
            debut (optional): permet de définir le début de la zone d'affichage
            taille (optional): permet de définir la taille de la zone d'affichage
        """
        if surface is None:
            surface = screen
        if debut is None:
            debut = (0, 0)
        taille = surface.get_size()

        if decalage_camera is not None:
            if self.objet_dans_zone(
                (decalage_camera[0], decalage_camera[0] + taille[0]),
                (decalage_camera[1], decalage_camera[1] + taille[1]),
            ):
                surface.blit(
                    self.image_actuel(),
                    (
                        self.coordonnee[0] - decalage_camera[0] + debut[0],
                        self.coordonnee[1] - decalage_camera[1] + debut[1],
                    ),
                )
                return True
            else:
                return False
        elif self.objet_dans_zone(
            (0, taille[0]),
            (0, taille[1]),
        ):
            surface.blit(
                self.image_actuel(),
                (self.coordonnee[0] + debut[0], self.coordonnee[1] + debut[1]),
            )
            return True
        else:
            return False


def gener_texture(taille: tuple[int], color: tuple[int] = False) -> pygame.Surface:
    """génere une texture rectangulaire

    Args:
        taile (tuple[int]): (x,y) est la taille de la texture
        color (tuple[int]): (Red,Green,Blue,trasparence "optionel") est la couleur de l'image

    Returns:
        Surface: est l'image généré
    """

    if len(color) == 3:  # permet de pas forcer de metre des couleurs
        # print(taille)
        image = pygame.Surface(taille)
        image.fill(color)
    elif len(color) == 4:
        image = pygame.Surface(taille, pygame.SRCALPHA)
        image.fill(color)
    return image


def gener_texture_arc_ciel(taille: list[int], decalage: int = 0):
    """génere une texture arc en ciel

    agrs:
        taille (list[int]) : est la taille de l'image
        decalage (int) : est le décalage de l'arc en ciel
    """
    couleur = [
        (255, 0, 0),
        (255, 125, 0),
        (255, 255, 0),
        (0, 255, 0),
        (0, 255, 255),
        (0, 0, 255),
        (125, 0, 255),
    ]
    min_taille = 0
    if taille[0] < taille[1]:
        min_taille = taille[0]
    else:
        min_taille = taille[1]
        texture = gener_texture(taille, couleur[0 + decalage])
    for i in range(1, min_taille // 10):
        texture.blit(
            gener_texture(
                [taille[0] - 10 * i, taille[1] - i * 10],
                couleur[(i + decalage) % len(couleur)],
            ),
            (i * 5, i * 5),
        )
    return texture


def decoupe_texte(
    texte: str, longueur_ligne: int, police: pygame.font.Font
) -> list[str]:
    """decoupe un texte en plusieur ligne
    en sorte que chaque ligne ne dépasse pas la longueur donnée

    Args:
        texte (str): est le texte à découper
        taille (int): est la taille de la ligne
        police (pygame.font.Font): est la police du texte

    Returns:
        list[str]: est le texte découpé
    """
    texte = texte.split("\n")
    texte_decoupe = []
    for fragment in texte:
        fragment = fragment.split(" ")
        ligne = ""
        for i in fragment:
            if police.size(ligne + i)[0] < longueur_ligne:
                ligne += i + " "
            elif len(ligne) > 0:
                texte_decoupe.append(ligne[:-1])
                ligne = i + " "
            else:
                texte_decoupe.append(i)
        if len(ligne) > 0:
            texte_decoupe.append(ligne[:-1])

    return texte_decoupe


def place_texte_in_texture(
    image: pygame.Surface,
    texte: str,
    police: pygame.font.Font,
    color: tuple[int],
    mode: str = "centrage",
) -> pygame.Surface:
    """ajoute du texte sur une image
    la fonction gère les saut de ligne quand le texte est trop long ou qu'il y a des "\\n"

    Args:
        image (pygame.Surface): est l'image qui recevera le texte
        texte (str): est le texte rajouter
        police (pygame.font.Font): est la police du texte
        color (tuple[int]): est la couleur du texte
        mode (str, optional): est le mode de placement du texte. Defaults to "centrage".
                              ("centrage", "haut_gauche")
    Returns:
        image (pygame.Surface): est image avec son texte
    """
    dimention_image = image.get_size()
    texte_decoupe = decoupe_texte(texte, dimention_image[0], police)
    if mode == "centrage":
        for i, ligne in enumerate(texte_decoupe):
            dimention_ligne = police.size(ligne)
            image.blit(
                police.render(ligne, 2, color),
                (
                    (dimention_image[0] - dimention_ligne[0]) // 2,
                    (dimention_image[1] - dimention_ligne[1] * len(texte_decoupe)) // 2
                    + i * dimention_ligne[1],
                ),
            )
    elif mode == "haut_gauche":
        for i, ligne in enumerate(texte_decoupe):
            dimention_ligne = police.size(ligne)
            image.blit(
                police.render(ligne, 2, color),
                (0, i * dimention_ligne[1]),
            )
    elif mode == "centrage_haut":
        for i, ligne in enumerate(texte_decoupe):
            dimention_ligne = police.size(ligne)
            image.blit(
                police.render(ligne, 2, color),
                (
                    (dimention_image[0] - dimention_ligne[0]) // 2,
                    i * dimention_ligne[1],
                ),
            )
    return image


def vider_affichage(couleur_du_fond: list | int = 0):
    """permet de vider l'affichage
    donc de tout retire et met la couleur qui est entre en fond
    
    Args:
        couleur_du_fond (list or tuple or int): bref c'est une couleur RGB (red, green, blue)
    """
    screen.fill(couleur_du_fond)


def quitter():
    """permet de quitter"""
    pygame.quit()
    exit()
