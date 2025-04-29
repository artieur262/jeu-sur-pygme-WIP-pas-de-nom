from py.objet.objetUnicolor import ObjetUnicolor3D

class Playeur(ObjetUnicolor3D):
    """Playeur est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(self, coordonnee: list[int], taille: int, couleur: tuple[int, int, int]):
        """initialise le bouton"""
        self.taille_carrer = taille
        super().__init__(coordonnee, (taille, taille, taille), couleur)
        self.face=2

    def actualiser_taille(self) -> None:
        """actualise la taille de la plateforme"""
        match self.face:
            case 0:
                self.taille = (1, self.taille_carrer, self.taille_carrer)
            case 1:
                self.taille = (self.taille_carrer, 1, self.taille_carrer)
            case 2:
                self.taille = (self.taille_carrer, self.taille_carrer, 1)
        

    def set_taille(self, taille: tuple[int, int]) -> None:
        """set la taille de la plateforme"""
        self.taille_carrer = taille
        self.actualiser_taille()
    
    def set_face(self, face: int) -> None:
        """set la face de la plateforme"""
        self.face = face
        self.actualiser_taille()
    
        
