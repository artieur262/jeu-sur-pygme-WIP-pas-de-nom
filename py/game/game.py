import pygame

from py.interface.class_clavier import Clavier, Souris
from py.graphique.graphique import screen
from py.graphique.actualisation_pygame import actualise_event, change_fullscreen
from py.graphique.image import Image
from py.block.plateforme import Plateforme
from py.block.playeur import Playeur
from py.block.activateur.activateur import Activateur
from py.objet.objetVisuel import ObjetVisuel3D
from py.objet.zone import Zone3D
from py.logique.blocLogique import Logique

class Map:
    """Map est une classe qui permet de gerer la map
    Args:
        Map (Map): est la map
    """
    def __init__(self, game = "Game"):
        """initialise la map"""
        self.__game = game
        self.__colision:set[Zone3D] = set()
        self.__playeur:Playeur = None
        self.__afficher:set[ObjetVisuel3D] = set()
        self.__graviter:bool = False
        self.__logique:set[Logique] = set()
        self.__signal:set[int] = set()
        self.__activateur:set[Activateur] = set()

    def actualiser_activation(self) -> None:
        """actualise l'activation des blocs logiques"""
        nouveau_signal:set[int] = set()
        for i in self.__logique:
            i.get_activation(self.__signal, nouveau_signal)
        self.__signal = nouveau_signal


    def add_plateforme(self, plateforme: Plateforme) -> None:
        """ajoute une plateforme à la map"""
        self.__colision.add(plateforme)
        self.__afficher.add(plateforme)
    
    def remove_plateforme(self, plateforme: Plateforme) -> None:
        """retire une plateforme de la map"""
        self.__colision.remove(plateforme)
        self.__afficher.remove(plateforme)
    
    def add_colision(self, zone: Zone3D) -> None:
        """ajoute une zone de colision à la map"""
        self.__colision.add(zone)
    
    def remove_colision(self, zone: Zone3D) -> None:
        """retire une zone de colision de la map"""
        self.__colision.remove(zone)
    
    def add_afficher(self, objet: ObjetVisuel3D) -> None:
        """ajoute un objet à afficher à la map"""
        self.__afficher.add(objet)
    
    def remove_afficher(self, objet: ObjetVisuel3D) -> None:
        """retire un objet à afficher de la map"""
        self.__afficher.remove(objet)

    def add_playeur(self, playeur: Playeur) -> None:
        """ajoute un playeur à la map"""
        self.__playeur=playeur
        self.__afficher.add(playeur)
        self.__colision.add(playeur)
    
    def add_logique(self, logique: Logique) -> None:
        """ajoute une logique à la map"""
        self.__logique.add(logique)

    def remove_logique(self, logique: Logique) -> None:
        """retire une logique de la map"""
        self.__logique.remove(logique)

    def affichable(self) -> set[ObjetVisuel3D]:
        """affiche la map"""
        return self.__afficher
    
    def get_game(self) -> "Game":
        """get le jeu"""
        return self.__game

    def get_colision(self) -> set[Zone3D]:
        """get la map"""
        return self.__colision
    
    def get_playeur(self) -> Playeur:
        """get le playeur"""
        return self.__playeur
    
    def get_graviter(self) -> bool:
        """get la graviter"""
        return self.__graviter

    def add_activateur(self, activateur: Activateur) -> None:
        """ajoute un activateur à la map"""
        self.__activateur.add(activateur)
    
    def remove_activateur(self, activateur: Activateur) -> None:
        """retire un activateur de la map"""
        self.__activateur.remove(activateur)
    

class Game:
    """Game est une classe qui permet de gerer le jeu
    Args:
        Game (Game): est le jeu
    """
    def __init__(self, clavier:Clavier, souris:Souris, touche:dict[str, int] ):
        """initialise le jeu"""
        self.map:Map = Map()
        self.clavier:Clavier = clavier
        self.souris:Souris = souris
        self.__running:bool = True
        self.__clock:pygame.time.Clock = pygame.time.Clock()
        self.__fps:int = 60
        self.__touche:dict[str, int] = touche
        self.__plan_actuel:int = 2
        self.hauteur_plan:int = 0
        self.debug:bool = False
    

    def set_plan(self, plan:int) -> None:   
        """set le plan"""
        self.__plan_actuel = plan
        self.map.get_playeur().set_face(plan)

    def get_plan(self) -> int:
        """get le plan"""
        return self.__plan_actuel

    def get_touche(self) -> dict[str, int]:
        """get les touches"""
        return self.__touche

    def deplacer_dans_plan(self,direction:tuple[int,int], plan:int) -> None:
        """deplace le playeur selons les touches du clavier"""
        playeur:Playeur = self.map.get_playeur()
        if isinstance(plan, str):
            plan = Zone3D.LIST_FACE.index(plan)
        if plan == 0:
            playeur.deplacer((0,direction[0], direction[1]), self.map.get_colision())
        elif plan == 1:
            playeur.deplacer((direction[0], 0, direction[1]), self.map.get_colision())
        elif plan == 2:
            playeur.deplacer((direction[0], direction[1], 0), self.map.get_colision())


    def deplacer(self) -> None:
        """deplace le playeur selons les touches du clavier"""
        plan = self.__plan_actuel
        cla=self.clavier
        if not self.map.get_graviter():
            if cla.get_pression(self.__touche["haut"]) == "presser":
                self.deplacer_dans_plan((0, -1), plan)
            if cla.get_pression(self.__touche["bas"]) == "presser":
                self.deplacer_dans_plan((0, 1), plan)
        if cla.get_pression(self.__touche["gauche"]) == "presser":
            self.deplacer_dans_plan((-1, 0), plan)
        if cla.get_pression(self.__touche["droite"]) == "presser":
            self.deplacer_dans_plan((1, 0), plan)


    def afficher(self) -> None:
        """affiche le jeu"""
        screen.fill((0, 0, 0))
        for i in self.map.affichable():
            i.afficher_plan(self.hauteur_plan, self.__plan_actuel)
        pygame.display.flip()      
                        


    def debug_mode(self) -> None:
        """mode debug"""
        if self.debug:
            cla = self.clavier
            if cla.get_pression(pygame.K_1) == "presser":
                self.set_plan(0)
            if cla.get_pression(pygame.K_2) == "presser":
                self.set_plan(1)
            if cla.get_pression(pygame.K_3) == "presser":
                self.set_plan(2)

    def run(self) -> None:
        """lance le jeu"""
        while self.__running:
            event = actualise_event(self.clavier, self.souris)
            if "quitter" in event:
                self.__running = False
            if self.clavier.get_pression(pygame.K_F11) in event:
                change_fullscreen()
            if self.clavier.get_pression(self.__touche["debug"]) == "vien_presser":
                self.debug=True
            self.debug_mode()
            self.deplacer()
            self.afficher()
            self.__clock.tick(self.__fps)
    




            

