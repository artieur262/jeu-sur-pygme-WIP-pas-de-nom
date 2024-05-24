"""est un trop vieux main pour le jeu"""

import time
from block.class_obj import *  # pylint: disable=unused-wildcard-import disable=wildcard-import
from class_clavier import Clavier

monospace = pygame.font.SysFont("monospace", 15)
# print(monospace.get_ascent())
# print(monospace.get_descent())
# print(monospace.get_height())
# print(monospace.get_underline())
# print(monospace.get_italic())
# print(monospace.get_linesize())
# print(monospace.get_bold())

vider_affichage()
joueur = Playeur((0, 0, 0), 20, (255, 255, 255))
list_block: list[Block] = []
face = 1  # pylint: disable=invalid-name
clock = pygame.time.Clock()
for i in ((50, 0, 0), (100, 0, 0), (0, 50, 0), (0, 0, 50), [50, 0, 75], [125, 0, 50]):
    list_block.append(Block(i, (50, 50, 25), (125, 125, 125)))


for i, j in enumerate(list_block):
    j.ajoute_screen(face, 0)
    pygame.display.update()
    # time.sleep(1)

convet_face_int = {"xy": 0, "xz": 1, "yz": 2}
joueur.ajoute_screen(face, 0)
pygame.display.update()
time_a = time.time()
time_saut = time.time() - 5
clavier = Clavier()
deplacement = "rien"
list_logique = [Logique([1], 3, "and"), LogiqueTimer(20, 6, 7)]
list_logique: list[Logique | LogiqueNot | LogiqueTimer]
list_lumiere = [
    BlockLumiere((0, 0, 0), (10, 10, 10), [(255, 0, 0), (0, 255, 0)], [1]),
    BlockLumiere(
        (10, 0, 0), (10, 10, 10), [(255, 0, 0), (0, 255, 0), (0, 0, 255)], [1, 5]
    ),
    BlockLumiere(
        (20, 0, 0),
        (10, 10, 10),
        [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)],
        [1, 5, 6, 7],
    ),
    BlockLumiere((175, 0, 50), (10, 10, 10), [(255, 0, 0), (0, 255, 0)], [5]),
]
list_texte = [
    BlockTexte(
        [0, 0, 100],
        (250, 50, 50),
        (255, 255, 255, 0),
        (255, 255, 255),
        "les chats sont trop cool",
        "monospace",
        15,
    )
]
list_platforme_mouvente = [
    PlateformeMouvante(
        (50, 0, 50),
        [30, 30, 30],
        2,
        [[(0, 3, 8)], [(2, -3, 8)], [(0, -3, 8), (2, 3, 8)]],
        [0, 0, 255],
    ),
    PlateformeMouvante(
        (125, 0, 25),
        [30, 30, 30],
        1,
        [[(2, 3, 10)], [(2, -3, 10)]],
        [0, 0, 255],
    ),
]
list_interupteur = [
    Interupteur(1, (100, 0, 50), (25, 25, 25), [0, 255, 255]),
    Interupteur(6, (75, 0, 50), (25, 25, 25), [0, 125, 125], "impulsif"),
    Interupteur(1, (0, 20, 0), (50, 50, 50), (0, 255, 255)),
    Interupteur(5, (175, 0, 50), (25, 25, 25), (0, 255, 255), "levier"),
]

set_activation = set()
while True:
    clavier.actualise_all_touche()
    for lumiere in list_lumiere:
        lumiere.actualise()
    for interupteur in list_interupteur:
        interupteur.actualise()
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:  # pylint: disable=no-member
            # cat[event.unicode] = event.key
            # print(event)
            if event.key in clavier.dict_touches:
                clavier.set_pression(event.key, "vien_lacher")

        if event.type == pygame.KEYDOWN:  # pylint: disable=no-member
            # print(event)
            if event.unicode == "\x1b":
                quit()
            elif event.key in clavier.dict_touches:
                clavier.set_pression(event.key, "vien_presser")

    if face == 1:
        if clavier.get_pression("d") == "presser":
            deplacement = "devant"
        elif clavier.get_pression("q") == "presser":
            deplacement = "deriere"
        else:
            deplacement = "rien"

        if clavier.get_pression("z") == "vien_presser" and joueur.etat == "par terre":
            # print("cat")
            time_saut = time.time()
    if clavier.get_pression("r") == "vien_presser":
        list_platforme_mouvente[0].active = True

    if clavier.get_pression("y") == "vien_presser":
        tac = joueur.trouve_obj_autour(list_interupteur)
        # print(tac)
        for i in tac:
            # print(i)
            if list_interupteur[i].type in ("levier", "impulsif") and list_interupteur[
                i
            ].in_axe(0, face):
                list_interupteur[i].activation()

    if clavier.get_pression("y") == "presser":
        tac = joueur.trouve_obj_autour(list_interupteur)
        # print(tac)
        for i in tac:
            # print(i)
            if list_interupteur[i].type == "bouton" and list_interupteur[i].in_axe(
                0, face
            ):
                list_interupteur[i].activation()

    clock.tick(60)
    for interupteur in list_interupteur:
        interupteur.activate(set_activation)

    for logi in list_logique:
        if logi.active:
            logi.activate(set_activation)
    for obj in list_platforme_mouvente:
        obj.activation(set_activation)
    for obj in list_lumiere:
        obj.activation(set_activation)
    for obj in list_logique:
        obj.activation(set_activation)
    for logi in list_logique:
        logi.actualise()
    set_activation = set()

    # print(clavier)
    if time.time() - time_saut < 0.75:
        joueur.deplace(list_block + list_platforme_mouvente + list_interupteur, 2, -1)
    else:
        joueur.deplace(list_block + list_platforme_mouvente + list_interupteur, 2, 1)
    if deplacement == "devant":
        joueur.deplace(list_block + list_platforme_mouvente + list_interupteur, 0, 1)
    if deplacement == "deriere":
        joueur.deplace(list_block + list_platforme_mouvente + list_interupteur, 0, -1)

    for platf in list_platforme_mouvente:
        platf.deplace_chemain([joueur])

    # print(joueur.etat)
    time_a = time.time()
    screen.fill(0)

    for j in list_block:
        j.ajoute_screen(face, 0)

    for i in list_interupteur:
        i.ajoute_screen(face, 0)

    for i in list_platforme_mouvente:
        i.ajoute_screen(face, 0)
    for i in list_lumiere:
        i.ajoute_screen(face, 0)
    for i in list_texte:
        i.ajoute_screen(face, 0)
    joueur.ajoute_screen(face, 0)

    pygame.display.update()
