"""parti grapfique de mon jeu
"""

# pylint: disable= no-member
import pygame


pygame.init()


screen = pygame.display.set_mode((1200, 600), pygame.RESIZABLE)
pygame.display.set_caption("jeu 2D dans monde 3D")
screen.fill((200, 200, 200))
# deplace_map = [0, 0]


class ObjetGraphique:
    """est Objet Graphique qui a le but d'etre affiché"""

    def __init__(self, coordonnee: tuple[int] = None, images: list = None, animation=0):
        if coordonnee is None:
            coordonnee = (0, 0)
            print("error (niveau 1): coordoonnee non prédéfini definition à [0,0]")
        if images is None:
            images = []
            print("error (niveau 1): aucune image défini")
        images_converti = []
        for image in images:  # converti les liens d'images en format Surface
            if isinstance(image, str):
                image = pygame.image.load(image)
                image.convert()
            images_converti.append(image)

        self.coordonnee = coordonnee
        self.images = images_converti
        self.animation = animation
        self.actualise_dimension()
        self.coordonnee: tuple[int]
        self.animation: int
        self.images: list

    def set_coordonnee(self, valu):
        """defini"""
        self.coordonnee = valu

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
        return (self.coordonnee[0] <= x <= self.coordonnee[0] + self.dimension[0]) and (
            self.coordonnee[1] <= y <= self.coordonnee[1] + self.dimension[1]
        )

    def objet_dans_zone(self, axe_x: tuple, axe_y: tuple) -> bool:
        """permet de savoir si un bojet est dans une zone

        Args:
            axe_x (tuple): à une longuer de 2 (le premier est le plus petit)
            axe_y (tuple): _description_

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
        #     axe_x[0] <= self.coordonnee[0] <= axe_x[1] + self.dimension[0]
        #     and axe_y[0] <= self.coordonnee[1] <= axe_y[1] + self.dimension[1]
        # )

    def afficher(self, decalage=None, taille=None):
        """permet de l'affiché sur la fenêtre"""
        # print("tac")
        if taille is None:
            taille = screen.get_size()
        if decalage is not None:
            if self.objet_dans_zone(
                (decalage[0], decalage[0] + taille[0]),
                (decalage[1], decalage[1] + taille[1]),
            ):
                screen.blit(
                    self.image_actuel(),
                    (
                        self.coordonnee[0] - decalage[0],
                        self.coordonnee[1] - decalage[1],
                    ),
                )
        elif self.objet_dans_zone(
            (0, taille[0]),
            (0, taille[1]),
        ):
            # print("chaton")
            screen.blit(self.image_actuel(), self.coordonnee)


def gener_texture(taille: tuple[int], color: tuple[int] = False) -> pygame.Surface:
    """génere une texture rectangulaire

    Args:
        taile (tuple[int]): (x,y) est la taille de la texture
        color (tuple[int]): (Red,Green,Blue,trasparence "optionel") est la couleur de l'image

    Returns:
        Suface: est l'image généré
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
    """génere une texture arc en ciel"""
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


def place_texte_in_texture(
    image: pygame.Surface,
    texte: str,
    police: pygame.font.Font,
    color: tuple[int],
) -> pygame.Surface:
    """ajoute du texte sur une image

    Args:
        image (pygame.Surface): est l'image qui ressevera le texte
        texte (str): est le texte rajouter

    Returns:
        image (pygame.Surface): est image avec son texte
    """
    dimention_image = image.get_size()
    texte_img = police.render(texte, 2, color)
    dimention_texte = texte_img.get_size()
    # print(dimention_texte[1])
    if "\n" in texte:
        frag_texte = texte.split("\n")
        frag_texte_img: list[pygame.Surface] = []
        for i in frag_texte:
            frag_texte_img.append(police.render(i, 2, color))
        position = (17 * len(frag_texte)) // 2
        for i, j in enumerate(frag_texte_img):
            j_taille = j.get_size()
            image.blit(
                j,
                (
                    dimention_image[0] // 2 - j_taille[0] // 2,
                    dimention_image[1] // 2 - position + 17 * i,
                ),
            )

    elif (
        dimention_texte[0] <= dimention_image[0] or len(texte.split(" ")) == 1
    ):  # le texte rentre dans l'image
        image.blit(
            texte_img,
            (
                dimention_image[0] // 2 - dimention_texte[0] // 2,
                dimention_image[1] // 2 - dimention_texte[1] // 2,
            ),
        )
    else:  # sinon on coupe le texte est on place dans l'image
        frag_texte = texte.split(" ")
        frag_texte_img: list[pygame.Surface] = []
        for i in frag_texte:
            frag_texte_img.append(police.render(i, 2, color))
        position = (17 * len(frag_texte)) // 2
        for i, j in enumerate(frag_texte_img):
            j_taille = j.get_size()
            image.blit(
                j,
                (
                    dimention_image[0] // 2 - j_taille[0] // 2,
                    dimention_image[1] // 2 - position + 17 * i,
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


# def gestion_mobiliter_fentre(event: pygame.event.Event):
#     """permet de géreré la mobilité de la fenètre

#     Args:
#         event (pygame.event.Event): _description_
#     """
#     if event.type == pygame.QUIT:
#         # detecte quand on clique sur la croix pour quiter
#         quitter()
