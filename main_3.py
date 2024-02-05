"""est le main"""

# pylint: disable=no-member
import save
from block.class_obj import genere_obj, vider_affichage
from interface.option import (
    SelectOption,
    active_f11,
    actualise_event,
    pygame,
    screen,
    ObjetGraphique,
    place_texte_in_texture,
    gener_texture,
)

from interface.choix_level import ChoisirLevel
from interface.pause import MenuPause
from interface.menu_pricipale import MenuPrincipale
from game import Game
from class_clavier import Clavier, Souris


def main():
    """est le main"""
    global screen  # pylint: disable=global-statement
    lien_fichier_map = "map/"
    lien_map = "tuto_5.json"  # "tuto_1_troll.json"  # "map_teste.json"  # "tuto_1.json"
    lien_controle = "option/control.json"
    lien_control_default = "option/control_default.json"
    lien_option = "option/option.json"
    lien_option_default = "option/option_default.json"

    controle = save.open_json(lien_controle)
    option = save.open_json(lien_option)

    if option["plein_écran"]:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # rule, map_ = save.open_json(LIEN_FICHIER_MAP + lien_map)
    # controle = save.open_json(lien_controle)
    # map_ = genere_obj(map_)

    clavier = Clavier()
    souris = Souris()
    # jeu = game(map_, rule["face"], rule["valeur_de_fin"], controle, clavier)
    home = MenuPrincipale(souris)
    menu_pause = MenuPause()
    selection_level = ChoisirLevel()
    menu_option = SelectOption(controle, option, souris, clavier, {})
    clock = pygame.time.Clock()
    action = "home"  # "home" # "choix_level"  # "chargement_map"  # "pause" # "option_demare"
    # monospace = pygame.font.SysFont("monospace", 30)
    pygame.display.set_gamma(200, 200, 200)

    # pygame.display.se
    while action != "fin":
        if action == "home":
            home.actualise_bouton()
            home.clique_bouton()
            screen.fill((0, 0, 0))
            home.affiche()
            home.actualise_fenetre()
            pygame.display.update()
            actualise_event(clavier, souris)
            if home.etat == "quitter":
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
            menu_option.set_option(option)
            menu_option.set_control(controle)
            action = "option"
        elif action == "option":
            screen.fill((175, 175, 175))
            actualise_event(clavier, souris)
            active_f11(clavier.get_pression("f11"), option)
            menu_option.clique_bouton()
            menu_option.actualise_bouton()
            menu_option.affiche()
            # print(menu_option.indicateur_face)
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
                menu_option.etat = "en cour"
                if "menu" in menu_option.contexte:
                    action = "menu"
                elif "pause" in menu_option.contexte:
                    action = "pause"
            elif menu_option.etat == "reset":
                if menu_option.page == "graphique":
                    option = save.open_json(lien_option_default)
                    menu_option.set_option(option["indicateur_face"])
                elif menu_option.page == "controle":
                    controle = save.open_json(lien_control_default)
                    menu_option.set_control(controle)
                    menu_option.actualise_control()
                menu_option.etat = "en cour"

        elif action == "choix_level":
            actualise_event(clavier, souris)
            active_f11(clavier.get_pression("f11"), option)
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
                map_, rule["face"], rule["valeur_de_fin"], controle, option, clavier
            )
            action = "enjeu"
        elif action == "enjeu":
            pygame.display.update()
            screen.fill((0, 0, 0))

            actualise_event(clavier, souris)
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
            active_f11(clavier.get_pression("f11"), option)
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
            if clavier.get_pression("\x1b") == "vien_presser":
                # "\x1b" = la touche échape
                action = "pause"
                # quit()
        elif action == "pause":
            # print("cat")

            actualise_event(clavier, souris)
            active_f11(clavier.get_pression("f11"), option)
            menu_pause.clique_bouton(souris)
            screen.fill((0, 0, 0))
            jeu.affiche_obj()
            menu_pause.affiche()
            menu_pause.actualise_bouton(souris)
            pygame.display.update()
            clock.tick(30)

            if clavier.get_pression("\x1b") == "vien_presser":
                # "\x1b" = la touche échape
                action = "enjeu"
            # print(menu_pause.etat)

            if menu_pause.etat == "quitter":
                quit()
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
