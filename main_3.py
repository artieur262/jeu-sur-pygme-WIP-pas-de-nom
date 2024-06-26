"""est le main"""

# pylint: disable=no-member
import copy
import save
from block.class_obj import genere_obj, vider_affichage
from interface.option import (
    SelectOption,
    change_fullscreen,
    actualise_event,
    pygame,
    screen,
    ObjetGraphique,
    place_texte_in_texture,
    gener_texture,
)
from interface.menu_oui_non import selection_oui_non
from interface.choix_level import ChoisirLevel
from interface.pause import MenuPause
from interface.menu_pricipale import MenuPrincipale
from game import Game
from class_clavier import Clavier, Souris


def main():
    """est le main"""
    global screen  # pylint: disable=global-statement
    lien_fichier_map = "map/"
    lien_map = (
        "tuto/tuto_5.json"  # "tuto_1_troll.json"  # "map_teste.json"  # "tuto_1.json"
    )
    lien_controle = "option/control.json"
    lien_control_default = "option/control_default.json"
    lien_option = "option/option.json"
    lien_option_default = "option/option_default.json"

    controle = save.open_json(lien_controle)
    option = save.open_json(lien_option)
    if option["plein_écran"]:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    clavier = Clavier()
    souris = Souris()
    for i in controle.values():
        if isinstance(i, int):
            clavier.ajoute_touche(i)
    rule, map_ = save.open_json(lien_fichier_map + lien_map)
    map_ = genere_obj(map_)
    jeu = Game(
        map_,
        rule["face"],
        rule["valeur_de_fin"],
        rule["valeur_mort"],
        controle,
        option,
        clavier,
    )
    home = MenuPrincipale(souris)
    menu_pause = MenuPause()
    selection_level = ChoisirLevel()
    menu_option = SelectOption(controle, option, souris, clavier, {})
    clock = pygame.time.Clock()
    action = "home"  # "home" # "choix_level"  # "chargement_map"  # "pause" # "option_demare"
    # monospace = pygame.font.SysFont("monospace", 30)

    # pygame.display.se

    while action != "fin":
        if action == "home":
            home.actualise_bouton()
            home.clique_bouton()
            screen.fill((0, 0, 0))
            home.affiche()
            home.actualise_fenetre()
            pygame.display.update()
            event = actualise_event(clavier, souris)
            clock.tick(30)
            if clavier.get_pression("f11") == "vien_presser":
                change_fullscreen()
            if (
                clavier.get_pression("echap") == "vien_presser" or "quitter" in event
            ) and selection_oui_non(
                souris, clavier, "Voulez-vous\nvraiment quitter ?", "entrer", "echap"
            ):
                action = "fin"
            if home.etat == "quitter":
                if selection_oui_non(
                    souris,
                    clavier,
                    "Voulez-vous\nvraiment quitter ?",
                    "entrer",
                    "echap",
                ):
                    action = "fin"
                home.etat = "en cour"
            elif home.etat == "option":
                action = "option_demare"
                home.etat = "en cour"
                menu_option.set_contexte({"home"})
            elif home.etat == "commencer":
                action = "choix_level"
                home.etat = "en cour"
                selection_level.etat = True
        elif action == "option_demare":
            menu_option.set_option(copy.deepcopy(option))
            menu_option.set_control(copy.deepcopy(controle.copy()))
            menu_option.actualise_control()
            action = "option"
        elif action == "option":
            screen.fill((175, 175, 175))
            event = actualise_event(clavier, souris)
            if clavier.get_pression("f11") == "vien_presser":
                change_fullscreen()
            menu_option.clique_bouton()
            menu_option.actualise_bouton()
            menu_option.affiche()
            pygame.display.update()
            clock.tick(30)
            if menu_option.etat == "anuler":
                if "home" in menu_option.contexte:
                    action = "home"

                elif "pause" in menu_option.contexte:
                    action = "pause"
                menu_option.etat = "en cour"
            elif menu_option.etat == "valider":
                # print("cat")
                option = menu_option.get_option()
                controle = menu_option.get_control()
                save.save_json(lien_option, option)
                save.save_json(lien_controle, controle)
                for i in controle.values():
                    if isinstance(i, int):
                        clavier.set_pression(i, "lacher")
                menu_option.etat = "en cour"
                if "home" in menu_option.contexte:
                    action = "home"
                elif "pause" in menu_option.contexte:
                    action = "pause"
                    jeu.set_option(option)
                    jeu.set_controle(controle)

            elif menu_option.etat == "reset":
                if menu_option.page == "graphique":

                    menu_option.set_option(
                        copy.deepcopy(save.open_json(lien_option_default))
                    )
                elif menu_option.page == "controle":

                    menu_option.set_control(save.open_json(lien_control_default))
                    menu_option.actualise_control()
                    for i in controle:
                        if isinstance(controle[i], int):
                            clavier.ajoute_touche(i)
                menu_option.etat = "en cour"

        elif action == "choix_level":
            event = actualise_event(clavier, souris)
            if clavier.get_pression("f11") == "vien_presser":
                change_fullscreen()
            if (
                clavier.get_pression("echap") == "vien_presser" or "quitter" in event
            ) and selection_oui_non(
                souris, clavier, "Voulez-vous\nvraiment quitter ?", "entrer", "echap"
            ):
                action = "fin"
            screen.fill((0, 0, 0))
            selection_level.actualise_possition()
            selection_level.actualise_animation(souris)
            selection_level.clique_sur_chose(souris)
            selection_level.affiche()
            pygame.display.update()
            clock.tick(30)

            if selection_level.etat == "fini":
                lien_map = ""
                for i in selection_level.suite_lien:
                    lien_map += i
                action = "chargement_map"
                selection_level.suite_lien.pop()
            elif selection_level.etat == "home":
                action = "home"

        elif action == "chargement_map":
            rule, map_ = save.open_json(lien_fichier_map + lien_map)
            map_ = genere_obj(map_)
            jeu = Game(
                map_,
                rule["face"],
                rule["valeur_de_fin"],
                rule["valeur_mort"],
                controle,
                option,
                clavier,
            )
            action = "enjeu"
        elif action == "enjeu":
            pygame.display.update()
            screen.fill((0, 0, 0))

            event = actualise_event(clavier, souris)
            clock.tick(60)
            jeu.actualise_face()
            jeu.actualise_fenetre()
            jeu.affiche_obj()
            jeu.depacle_playeur()
            jeu.actualise_obj()
            jeu.acvite_block()
            jeu.actualise_camera()
            jeu.activate()
            if clavier.get_pression(jeu.controle["debug1"]) == "vien_presser":
                print(jeu.dict_obj["playeur"][0].get_coordonnee())
            if clavier.get_pression("f11") == "vien_presser":
                change_fullscreen()

            # print(jeu.set_activation)
            # print(jeu.etat, jeu.set_activation, jeu.valeur_de_fin)

            if jeu.etat == "victoire":
                vider_affichage()
                ObjetGraphique(
                    [300, 200],
                    [
                        place_texte_in_texture(
                            gener_texture((500, 300), (125, 125, 125)),
                            "vous avez réussi le niveau",
                            pygame.font.SysFont("monospace", 30),
                            (255, 255, 255),
                        ),
                    ],
                ).afficher()
                pygame.display.update()
                # time.sleep(1.5)

            # print(jeu.dict_obj nvhcfdtst["plaforme"][0].active)
            if clavier.get_pression("echap") == "vien_presser":
                # "echap" = la touche échape
                action = "pause"
                # quit()
            if "quitter" in event and selection_oui_non(
                souris, clavier, "Voulez-vous\nvraiment quitter ?", "entrer", "echap"
            ):
                action = "fin"
        elif action == "pause":
            # print("cat")

            event = actualise_event(clavier, souris)
            if clavier.get_pression("f11") == "vien_presser":
                change_fullscreen()
            menu_pause.clique_bouton(souris)
            screen.fill((0, 0, 0))
            jeu.affiche_obj()
            menu_pause.affiche()
            menu_pause.actualise_bouton(souris)
            pygame.display.update()
            clock.tick(30)

            if clavier.get_pression("echap") == "vien_presser":
                # "echap" = la touche échape
                action = "enjeu"
            # print(menu_pause.etat)
            if "quitter" in event and selection_oui_non(
                souris, clavier, "Voulez-vous\nvraiment quitter ?", "entrer", "echap"
            ):
                action = "fin"
            if menu_pause.etat == "quitter":
                if selection_oui_non(
                    souris,
                    clavier,
                    "Voulez-vous\nvraiment quitter ?",
                    "entrer",
                    "echap",
                ):
                    action = "fin"
                menu_pause.etat = "en cour"
            elif menu_pause.etat == "reprendre":
                action = "enjeu"
            if menu_pause.etat == "option":
                action = "option_demare"
                menu_option.set_contexte({"pause"})
            elif menu_pause.etat == "redémarrer":
                action = "chargement_map"
            elif menu_pause.etat == "level":
                action = "choix_level"
                selection_level.etat = True


main()
